#!/usr/bin/env python
################################################################################
#
#   compara_orthology.py
#
#
#   Copyright (c) 11/3/2010 Leo Goodstadt
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#################################################################################
"""
for downloading homology data from an ensembl compara data base and caching for local fast
access

"""
import re, os,sys, cPickle
from dump_object import dump_object

from random_access_file_by_sections import fill_directory_of_sections, write_directory_of_sections, read_directory_of_sections
from collections import defaultdict, namedtuple
import marshal, time, struct
from general import (check_cache_file_version,
                        _prepare_cache_file,
                    cache_specified_compara_data,
                        lookup_compara_cache_file_name,
                    cache_specified_core_data,
                    lookup_core_cache_file_name,
                    _specify_ensembl_versions,
                    connect_ensembl_mysql,
                    get_compara_databases,
                    cache_is_valid,
                    get_missing_cache_file_names

                        )
from marshalable_object import marshalable_object, load_dict_of_object_lists, dump_dict_of_object_lists, load_dict_of_objects, dump_dict_of_objects
from collections import namedtuple
import sqlite3
import tempfile

#
#   Magic numbers
#
_FILE_VERSION_MAJ = 3
#
#   for logging: halfway between DEBUG and INFO
#
MESSAGE = 15




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   classes


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
t_ortholog_set =marshalable_object("t_ortholog_set",
                                   " ancestor_node_id" +    # LCA of all orthologs on protein tree
                                   " tree_node_id"     +    # root_id on protein tree
                                   " orthology_type"   +    # "ortholog_one2one", "apparent_ortholog_one2one",
                                                            # "ortholog_one2many", "ortholog_many2many", "possible_ortholog"
                                                            # "within_species_paralog",
                                                            # NOT "other_paralog", "putative_gene_split", "contiguous_gene_split",
                                   " gene_ids"         +    #[taxon_id] = [gene_id1,...]
                                   " prot_ids"         +    #[taxon_id] = [prot_id1,...]
                                   " ds")


t_ortholog_set_pairwise_scores =marshalable_object("t_ortholog_set_pairwise_scores",
                                   " gene_ids"
                                   " dn" +
                                   " ds" +
                                   " n" +
                                   " s" )
t_ortholog_set_pairwise_alignment =marshalable_object("t_ortholog_set_pairwise_alignment",
                                   " gene_ids"
                                   " perc_cov1"   +
                                   " perc_id1"    +
                                   " perc_pos1"   +
                                   " perc_cov2"   +
                                   " perc_id2"    +
                                   " perc_pos2")
t_species_data = namedtuple("t_species_data", "taxon_id, scientific_name, assembly")




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Helper functions for ortholog_sets

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   get_gene_ids_to_ortholog_sets

#_________________________________________________________________________________________
def get_gene_ids_to_ortholog_sets ():
    """
    Transform ortholog sets indexed by ancestor_id to gene_id
    """
    gene_ids_to_ortholog_sets = dict()
    for ortholog_set in ortholog_sets.itervalues():
        for per_species_genes_ids in ortholog_sets.gene_ids.values():
            for gene_id in per_species_genes_ids:
                gene_ids_to_ortholog_sets[gene_id] = ortholog_set

    return gene_ids_to_ortholog_sets

#_________________________________________________________________________________________

#   get_gene_ids_to_ortholog_sets

#_________________________________________________________________________________________
def get_gene_ids_to_ortholog_sets (ortholog_sets):
    """
    Transform ortholog sets indexed by ancestor_id to gene_id
    """
    if not len(ortholog_sets):
        return {}

    gene_ids_to_ortholog_sets = dict()
    for ortholog_set in ortholog_sets.itervalues():
        for per_species_genes_ids in ortholog_sets.gene_ids.values():
            for gene_id in per_species_genes_ids:
                gene_ids_to_ortholog_sets[gene_id] = ortholog_set

    return gene_ids_to_ortholog_sets

#_________________________________________________________________________________________

#   get_ortholog_sets_by_category

#_________________________________________________________________________________________
def get_ortholog_sets_by_category(ortholog_sets):
    """
    Divide up ortholog sets by category, e.g. 1:1 etc.
    """
    #
    #   set up default ortholog sets by the four categories
    #
    category_names = {(False, False): "1:1",
                      (False, True) : "1:m",
                      (True,  False): "m:1",
                      (True,  True) : "m:m"}

    ortholog_sets_by_category = dict()
    for category_name in category_names.values():
        ortholog_sets_by_category[category_name] = dict()

    #
    #   empty set
    #
    if not len(ortholog_sets):
        return ortholog_sets_by_category

    #
    #   Get taxon ids off first ortholog set
    #
    for ortholog_set in ortholog_sets.itervalues():
        taxon_ids = sorted(ortholog_set.gene_ids.keys())
        break
    if len(taxon_ids) != 2:
        raise Exception ("taxon_ids = %s " % str(taxon_ids))


    #
    #   Count genes for each ortholog set and place in category
    #
    for ancestor_node_id, ortholog_set in ortholog_sets.iteritems():
        gene_cnts = [len(ortholog_set.gene_ids[t]) for t in taxon_ids]
        # 1:1 / 1:m etc.
        category = (gene_cnts[0] > 1, gene_cnts[1] > 1)
        category_name = category_names[category]

        # put in correct set
        ortholog_sets_by_category[category_name][ancestor_node_id] = ortholog_set

    return ortholog_sets_by_category




#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Make local sqlite copy of MySQL Ensembl data

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


#_________________________________________________________________________________________

#   _sqlite_file_is_valid

#_________________________________________________________________________________________
def _sqlite_file_is_valid(cache_file_name, logger):
    "For sqlite"

    #
    #   sqlite
    #
    if not os.path.exists(cache_file_name):
        return False

    try:
        sqlite_conn = sqlite3.connect(cache_file_name)
        c = sqlite_conn.cursor()
        for table_name in "homology", "homology_member", "ortholog_types":
            c.execute("pragma table_info('%s')" % table_name)
            table_ok = False
            for row in c:
                table_ok = True
            if not table_ok:
                break
        else:
            return True
    except:
        pass

    logger.debug("%s is faulty and will be deleted" % cache_file_name)
    raise Exception("here")
    #
    #   ignore all exceptions
    #
    try:
        sqlite_conn.close()
    except:
        pass
    try:
        os.unlink(cache_file_name)
    except:
        pass

    return False


#_________________________________________________________________________________________

#   _retrieve_member_ids

#_________________________________________________________________________________________
def _retrieve_member_ids (cursor, logger, from_ensembl = True):
    """
    Retrieve member_ids to prot_id and gene_id
    """
    #
    #   member_id data
    #
    member_id_to_real_id = dict()


    #
    #   member_id to protein / gene_ids
    #
    db_str = """
                SELECT
                        member_id,
                        stable_id,
                        taxon_id
                    FROM
                        member
               """
    if from_ensembl:
        db_str += """
                    WHERE
                        source_name IN
                           ('ENSEMBLGENE',
                            'ENSEMBLPEP')
               """

               #and member_id in
               # (1521969, 1521971, 1522002, 1522004, 1589442, 1589443, 1589524, 1589526, 1781684, 1781686, 1839706, 1839711, 1839747, 1839752, 1839777, 1839783, 22348, 22350, 22412, 22414, 22418, 22419, 304624, 304626, 343501, 343502, 412892, 412893, 475248, 475250, 475272, 475273, 98888, 98891)

    logger.debug("  Retrieving gene and protein identifiers...")
    start_time = time.time()
    cursor.execute(db_str)

    cnt_items = 0
    for (   member_id, real_id, taxon_id) in cursor:
        cnt_items += 1
        if cnt_items % 500000 == 0:
            logger.debug(str(cnt_items))
        member_id_to_real_id[member_id] = real_id, taxon_id

    end_time = time.time()
    logger.log(MESSAGE, "  %10d identifiers downloaded in %ds" % (len(member_id_to_real_id), end_time - start_time))
    return member_id_to_real_id




#_________________________________________________________________________________________

#   _save_member_ids_to_sqlite_db

#_________________________________________________________________________________________
def _save_member_ids_to_sqlite_db (sqlite_conn, member_id_to_real_id, logger):
    """
    cache member_ids to sqlite
    """

    #
    #   cache to sqlite
    #
    sqlite_cur = sqlite_conn.cursor()
    sqlite_cur.execute('''CREATE TABLE member
                            (
                                member_id                   INTEGER,
                                stable_id                   TEXT,
                                taxon_id                    INTEGER
                            )''')

    for member_id, (real_id, taxon_id) in member_id_to_real_id.iteritems():
        # Save row of data
        #   ignore source_name by specifying all as ENSEMBLGENE
        sqlite_cur.execute("""INSERT INTO member VALUES (?, ?, ?)""",
                            (member_id, real_id, taxon_id))

    sqlite_conn.commit()


#_________________________________________________________________________________________

#   _save_homology_member_table_to_local_sqlite

#_________________________________________________________________________________________
def _save_homology_member_table_to_local_sqlite (cursor, sqlite_conn, homology_id_to_method_link_species_set_id, logger):
    """
    Save homology_member table to local sqlite database
    We add the method_link_species_set_id column which means we can read all the data
        in order of species pairs
    """

    #
    #   cache to sqlite
    #
    sqlite_cur = sqlite_conn.cursor()
    sqlite_cur.execute('''CREATE TABLE homology_member
                            (
                            homology_id                 integer                 ,
                            member_id                   integer                 ,
                            peptide_member_id           integer                 ,
                            perc_cov                    real                    ,
                            perc_id                     real                    ,
                            perc_pos                    real                    ,
                            method_link_species_set_id  integer
                            )''')

    #
    #   estimate count
    #
    cursor.execute("SELECT count(*) FROM homology_member")
    total_cnt = 0
    for data in cursor:
        total_cnt = data[0]
    if not total_cnt:
        raise Exception("Couldn't estimate number of rows in homology_member")



    #
    #   member_id to protein / gene_ids
    #
    db_str = """
                SELECT
                        homology_id,
                        member_id,
                        peptide_member_id,
                        perc_cov,
                        perc_id,
                        perc_pos
                    FROM
                        homology_member
               """

    logger.debug("  Retrieving per homolog data from Ensembl compara...")
    start_time = time.time()
    cursor.execute(db_str)

    cnt_items = 0
    for data in cursor:
        cnt_items += 1
        if cnt_items % 500000 == 0:
            #
            #   Save (commit) the changes every 500000
            #
            time_taken = time.time() - start_time
            estimated_time = time_taken / cnt_items * total_cnt
            logger.debug("  %9d out of %d: %5ds out of %5ds" %
                            (cnt_items, total_cnt, time_taken, estimated_time))
            sqlite_conn.commit()

        if data[0] not in homology_id_to_method_link_species_set_id:
            continue

        method_link_species_set_id = homology_id_to_method_link_species_set_id[data[0]]

        # Save row of data
        sqlite_cur.execute("""INSERT INTO homology_member VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                                data + (method_link_species_set_id,))

    end_time = time.time()
    logger.log(MESSAGE, "  %10d homologs downloaded in %ds" %
                    (cnt_items, end_time - start_time))

    sqlite_cur.execute("CREATE INDEX i_homology_member ON homology_member(method_link_species_set_id);")
    sqlite_conn.commit()

    logger.log(MESSAGE, "  Indexed in %ds" % (time.time() - end_time))


#_________________________________________________________________________________________

#   _save_homology_table_to_local_sqlite

#_________________________________________________________________________________________
def _save_homology_table_to_local_sqlite (cursor, sqlite_conn, ortholog_species_pair_ids, logger):
    """
    Retrieve data from homology table
    """
    homology_id_to_method_link_species_set_id = dict()

    #
    #   cache to sqlite
    #
    sqlite_cur = sqlite_conn.cursor()
    sqlite_cur.execute('''CREATE TABLE homology
                            (
                                method_link_species_set_id  INTEGER,
                                homology_id                 INTEGER,
                                ortholog_type_id            INTEGER,
                                dn                          REAL,
                                ds                          REAL,
                                n                           REAL,
                                s                           REAL,
                                ancestor_node_id            INTEGER,
                                tree_node_id                INTEGER
                            )''')

    #
    #   estimate count
    #
    db_str = """
                SELECT count(*) FROM homology
                    WHERE method_link_species_set_id IN (%s)
               """ % ",".join(map(str, ortholog_species_pair_ids))
    cursor.execute(db_str)
    total_cnt = 0
    for data in cursor:
        total_cnt = data[0]
    if not total_cnt:
        raise Exception("Couldn't estimate number of rows in homology")


    #
    #   member_id to protein / gene_ids
    #
    db_str = """
                SELECT
                        method_link_species_set_id,
                        homology_id,
                        description,
                        dn,
                        ds,
                        n,
                        s,
                        ancestor_node_id,
                        tree_node_id
                    FROM
                        homology
                    WHERE method_link_species_set_id IN
                    (%s)
                    ORDER BY method_link_species_set_id
               """ % ",".join(map(str, ortholog_species_pair_ids))

    logger.debug("  Retrieving homolog pair data from Ensembl compara...")
    start_time = time.time()
    cursor.execute(db_str)

    str_to_index = dict()

    cnt_items = 0
    set_of_method_link_species_set_ids = set()
    for data in cursor:
        cnt_items += 1
        if cnt_items % 500000 == 0:
            time_taken = time.time() - start_time
            estimated_time = time_taken / cnt_items * total_cnt
            logger.debug("  %9d out of %d: %5ds out of %5ds" %
                            (cnt_items, total_cnt, time_taken, estimated_time))
            sqlite_conn.commit()

        homology_id_to_method_link_species_set_id[data[1]] = data[0]

        set_of_method_link_species_set_ids.add(data[0])

        # convert description into description_id
        data = list(data)
        description = data[2]
        if description not in str_to_index:
            str_to_index[description] = len(str_to_index)
        data[2] = str_to_index[description]


        # Save row of data
        sqlite_cur.execute("""INSERT INTO homology VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

    end_time = time.time()
    logger.log(MESSAGE, "  %10d homolog pairs for %d species pairs downloaded in %ds" %
                        (   cnt_items,
                            len(set_of_method_link_species_set_ids),
                            end_time - start_time))

    sqlite_cur.execute("CREATE INDEX i_homology ON homology(method_link_species_set_id);")
    logger.log(MESSAGE, "  Indexed in %ds" % (time.time() - end_time))

    sqlite_cur.execute('''CREATE TABLE ortholog_types
                            (
                                ortholog_type_id            INTEGER,
                                ortholog_type               TEXT
                            )''')

    # Save ortholog types
    for ortholog_type, ortholog_type_id in str_to_index.iteritems():
        sqlite_cur.execute("""INSERT INTO ortholog_types VALUES (?, ?)""",
                                        (ortholog_type_id, ortholog_type))

    sqlite_conn.commit()

    return homology_id_to_method_link_species_set_id



#_________________________________________________________________________________________

#   _copy_from_mysql_to_sqlite

#_________________________________________________________________________________________
def _copy_from_mysql_to_sqlite (cursor, cache_file_name, ortholog_species_pair_ids, logger):
    """
    cache tables locally using sqlite because this gives us a lot more control
    over the database => optimise for speed
    """
    #if _sqlite_file_is_valid(cache_file_name, logger):
    #    return
    sqlite_conn = sqlite3.connect(cache_file_name)

    # homology
    homology_id_to_method_link_species_set_id = _save_homology_table_to_local_sqlite (cursor, sqlite_conn, ortholog_species_pair_ids, logger)
    # homology_member with added "method_link_species_set_id" column
    _save_homology_member_table_to_local_sqlite(cursor, sqlite_conn, homology_id_to_method_link_species_set_id, logger)
    # member
    member_id_to_real_id                = _retrieve_member_ids(cursor, logger)
    _save_member_ids_to_sqlite_db (sqlite_conn, member_id_to_real_id, logger)



#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Read data back from sqlite

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
#_________________________________________________________________________________________

#   _sqlite_read_ortholog_type_ids

#_________________________________________________________________________________________
def _sqlite_read_ortholog_type_ids(sqlite_conn, logger):
    """
    retrieve data from sqlite ortholog_types table for this method link id
    """
    #
    #   cache to sqlite
    #
    logger.debug("  Retrieving ortholog types data from sqllite database...")
    start_time = time.time()
    sqlite_cur = sqlite_conn.cursor()

    #
    #   get data
    #

    ortholog_type_id_to_ortholog_type = dict()


    sqlite_cur.execute("""
                       SELECT
                               ortholog_type_id,
                               ortholog_type
                            FROM
                                ortholog_types;""")
    for ortholog_type_id, ortholog_type in sqlite_cur:
        ortholog_type_id_to_ortholog_type[ortholog_type_id] = ortholog_type

    return ortholog_type_id_to_ortholog_type


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Cache species list

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________

#   _retrieve_mysql_list_of_species_pairs

#_________________________________________________________________________________________
def _retrieve_mysql_list_of_species_pairs (cursor, logger):
    """
    Retrieve species_pair_ids from compara:
        This is just short hand for the Ensembl method_link_species_set_id
        First step in caching
    """
    #
    #   species_pairs data
    #
    taxon_ids_to_species_pair_id    = dict()


    #
    #   method_link
    #
    db_str = """  SELECT
                          method_link_species_set_id,
                          mlss.name,
                          taxon_id
                      FROM
                          method_link_species_set mlss NATURAL JOIN
                          method_link JOIN
                          species_set USING (species_set_id) JOIN
                          genome_db gdb USING (genome_db_id)
                      WHERE
                          type = 'ENSEMBL_ORTHOLOGUES'"""

    logger.debug("  Retrieving species_pairs from Ensembl compara...")
    cursor.execute(db_str)

    #
    #   save method_link_ids to link up species pairs in the next step
    #
    method_link_id_to_species_pair = defaultdict(set)
    method_link_species_set_id_to_is_ortholog = dict()
    for (   method_link_id,
            method_link_name,
            taxon_id) in cursor:
        method_link_id_to_species_pair[method_link_id].add(taxon_id)


    #
    #   make sure each method_link_id has 2 species
    #
    taxon_id_to_within_species_homology = dict()
    cnt_items = 0
    for method_link_id, all_taxon_ids in method_link_id_to_species_pair.iteritems():
        cnt_items += 1

        #   more or fewer than 2 species == error
        #
        if len(all_taxon_ids) != 2:
            raise Exception("%d (should be 2) species [%s] found for method_link_id = %d " %
                                (len(all_taxon_ids), ",".join(map(str, all_taxon_ids)), method_link_id))

        #
        # only store as sorted taxon_ids
        #
        all_taxon_ids = tuple(sorted(all_taxon_ids))
        taxon_ids_to_species_pair_id[all_taxon_ids] = method_link_id

    return taxon_ids_to_species_pair_id




#_________________________________________________________________________________________

#   _retrieve_mysql_species_name_and_assembly

#_________________________________________________________________________________________
def _retrieve_mysql_species_name_and_assembly (cursor, logger):

    """
    Retrieve scientific name and assembly name for each taxon_id
        2nd step in caching
    """
    taxon_id_to_name_and_assembly              = dict()
    db_str = """  SELECT
                          taxon_id,
                          name,
                          assembly
                      FROM
                          genome_db gdb"""

    logger.debug("  Retrieving species names from Ensembl compara...")
    cursor.execute(db_str)

    for (taxon_id, scientific_name, assembly) in cursor:
        taxon_id_to_name_and_assembly[taxon_id] = t_species_data(taxon_id, scientific_name, assembly)

    return taxon_id_to_name_and_assembly

#_________________________________________________________________________________________

#   _save_species_pairs_to_cache

#_________________________________________________________________________________________
def _save_species_pairs_to_cache (cache_file_name, taxon_id_to_name_and_assembly, taxon_ids_to_species_pair_id):
    """
    Write data for species pairs to cache file
    """
    data_file = _prepare_cache_file (cache_file_name, logger, _FILE_VERSION_MAJ, "species_pair")


    section_data_names = [  "taxon_id_to_name_and_assembly",
                            "taxon_ids_to_species_pair_id" ]
    section_name_directory_entry_pos = write_directory_of_sections(data_file, section_data_names)

    #
    #   save actual data
    #
    file_pos_by_section = {}

    file_pos_by_section["taxon_id_to_name_and_assembly"] = data_file.tell()
    cPickle.dump(taxon_id_to_name_and_assembly, data_file)

    file_pos_by_section["taxon_ids_to_species_pair_id"] = data_file.tell()
    cPickle.dump(taxon_ids_to_species_pair_id, data_file)

    #
    #   go back and write section starts in the directory
    #
    fill_directory_of_sections(data_file, section_name_directory_entry_pos, file_pos_by_section)





#_____________________________________________________________________________________
#
#   _cache_list_of_species_from_msql
#_____________________________________________________________________________________
def _cache_list_of_species_from_msql(cursor, index_file, compara_db_per_version, cache_file_directory, logger,
                                        ensembl_version, discard_cache, valid_taxon_id_pairs, valid_taxon_ids):
    """
    Retrieves list of species pairs from Ensembl and caches them

    Returns a list of species name pairs with which to name our caches, and their corresponding
        id from Ensembl (i.e. method_link_species_set_id)
    """

    #
    #   list of taxon_id_pairs. Each pair is sorted
    #
    taxon_ids_to_species_pair_id  = _retrieve_mysql_list_of_species_pairs (cursor, logger)

    #
    #   scientific name from taxon_id
    #           (assembly data comes for free!)
    #
    taxon_id_to_name_and_assembly = _retrieve_mysql_species_name_and_assembly (cursor, logger)

    #
    #   cache if nothing on disk
    #
    db_name = compara_db_per_version[ensembl_version]
    data_name = "species_pairs"
    cache_file_part = "{db_name}.orthology.{data_name}.cache".format(db_name = db_name, data_name = data_name.replace(' ', '_'))
    cache_file_name = os.path.join(cache_file_directory, cache_file_part)

    if not cache_is_valid(cache_file_name, logger, _FILE_VERSION_MAJ) or discard_cache:
        _save_species_pairs_to_cache (cache_file_name, taxon_id_to_name_and_assembly, taxon_ids_to_species_pair_id)

    index_file.write("%d\t%s\t%s\n" % (ensembl_version, data_name, cache_file_name))

    #
    #   convert between species scientific names and taxon_ids
    #
    all_species_pair_ids = set()
    data_name_to_species_pair_id = dict()

    #
    #   Link This is a list of desired all taxon_id pairs / species_pair_id (method_link_species_set_id)
    #           and the corresponding pretty scientific name used to name cache files
    #
    for taxon_ids, species_pair_id in taxon_ids_to_species_pair_id.iteritems():
        data_name = "%s_%s" % tuple(taxon_id_to_name_and_assembly[t].scientific_name for t in taxon_ids)
        all_species_pair_ids.add(species_pair_id)
        if taxon_ids in valid_taxon_id_pairs or set(taxon_ids) & set(valid_taxon_ids):
            data_name_to_species_pair_id[data_name] = species_pair_id

    return all_species_pair_ids, data_name_to_species_pair_id

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   Cacheing functions

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#_________________________________________________________________________________________

#   _process_homology_table_row

#_________________________________________________________________________________________
def _process_homology_table_row (   data, ortholog_type_id_to_ortholog_type,
                                    homolog_id_to_data, member_id_to_real_id,
                                    ortholog_sets,
                                    ortholog_set_pairwise_scores,
                                    ortholog_set_pairwise_alignment):
    """
    helper function to save each row of from the homology table
    """
    (method_link_id, homology_id, ortholog_type_id,
     dn, ds, n, s,
     ancestor_node_id, tree_node_id) = data

    orthology_type  = ortholog_type_id_to_ortholog_type[ortholog_type_id]



    #
    #   Make sure both homology_members for this homology_id are present
    #
    for i in 0, 1:
        if (homology_id, i) not in homolog_id_to_data:
            logger.warning("Missing %d rows from homology_member for homolog_id = %d" %
                                (2 - i, homology_id))
            #raise Exception("Missing row from homology_member")
            return

    #
    #   get ids for both genes and save only for gene_id1 < gene_id2
    #
    ids_and_alignments = []
    cnt_non_protein_coding_genes = 0
    for i in 0, 1:
        (gene_member_id, prot_member_id,
         perc_cov, perc_id, perc_pos) = homolog_id_to_data[homology_id, i]
        # give up if gene_id or prot_id not found
        if prot_member_id not in member_id_to_real_id:
            cnt_non_protein_coding_genes += 1
            continue
        gene_id, taxon_id = member_id_to_real_id[gene_member_id]
        prot_id, taxon_id = member_id_to_real_id[prot_member_id]
        ids_and_alignments.append([gene_id, prot_id, taxon_id, perc_cov, perc_id, perc_pos])


    # if orthologs not peptides, continue
    if len(ids_and_alignments) != 2:
        return cnt_non_protein_coding_genes

    ((gene_id1, prot_id1, pair_taxon_id1, perc_cov1, perc_id1, perc_pos1),
     (gene_id2, prot_id2, pair_taxon_id2, perc_cov2, perc_id2, perc_pos2)) = sorted(ids_and_alignments)



    #-----------------------------------
    #   t_ortholog_set
    #-----------------------------------
    if ancestor_node_id not in ortholog_sets:
        #
        #   new ortholog_set
        #
        ortholog_sets[ancestor_node_id] = t_ortholog_set(ancestor_node_id,
                                                         tree_node_id,
                                                         orthology_type,
                                                         {pair_taxon_id1: set([(gene_id1, prot_id1)]),
                                                          pair_taxon_id2: set([(gene_id2, prot_id2)])},
                                                         {pair_taxon_id1: None,
                                                          pair_taxon_id2: None},
                                                         [ds])
    else:
        #
        #   add to preexisting ortholog_set
        #
        ortholog_set = ortholog_sets[ancestor_node_id]
        assert(ortholog_set.ancestor_node_id == ancestor_node_id)
        assert(ortholog_set.tree_node_id     == tree_node_id)
        assert(ortholog_set.orthology_type   == orthology_type)
        ortholog_set.gene_ids[pair_taxon_id1].add((gene_id1,prot_id1))
        ortholog_set.gene_ids[pair_taxon_id2].add((gene_id2,prot_id2))
        ortholog_set.ds.append(ds)

    #-----------------------------------
    #   t_ortholog_set_pairwise_scores
    #-----------------------------------
    ortholog_set_pairwise_scores[ancestor_node_id].append(
            t_ortholog_set_pairwise_scores((gene_id1,gene_id2), dn, ds, n, s))

    #-----------------------------------
    #   ortholog_set_pairwise_alignment
    #-----------------------------------
    ortholog_set_pairwise_alignment[ancestor_node_id].append(
            t_ortholog_set_pairwise_alignment((gene_id1,gene_id2),
                                            perc_cov1, perc_id1, perc_pos1,
                                            perc_cov2, perc_id2, perc_pos2))

    return 0

#_____________________________________________________________________________________
#
#   _process_homology_member_table_row
#_____________________________________________________________________________________
def _process_homology_member_table_row (data, homolog_id_to_data):
    """
    Helper function
    Save one row from the homology_member table
    """
    homology_id = data[1]
    if (homology_id, 0) not in homolog_id_to_data:
        homolog_id_to_data[homology_id, 0] = data[2:]
    else:
        homolog_id_to_data[homology_id, 1] = data[2:]

#

#_____________________________________________________________________________________
#
#   _save_to_cache
#_____________________________________________________________________________________
def _save_to_cache (cache_file_name, data_name, ortholog_sets, ortholog_set_pairwise_scores, ortholog_set_pairwise_alignment):
    """
    Write data for a single species pair to a single file
    """
    data_file = _prepare_cache_file (cache_file_name, logger, _FILE_VERSION_MAJ, data_name)


    #
    #   convert from set to tuple to save room
    #
    for ortholog_set in ortholog_sets.itervalues():
        for taxon_id in ortholog_set.gene_ids.keys():
            ortholog_set.gene_ids[taxon_id] = tuple(sorted(ortholog_set.gene_ids[taxon_id]))
            ortholog_set.prot_ids[taxon_id] = tuple(p for (g,p) in ortholog_set.gene_ids[taxon_id])
            ortholog_set.gene_ids[taxon_id] = tuple(g for (g,p) in ortholog_set.gene_ids[taxon_id])

    section_data_names = [  "pairwise_alignments"          ,
                            "pairwise_scores"              ,
                            "ortholog_sets"                ]
    section_name_directory_entry_pos = write_directory_of_sections(data_file, section_data_names)

    #
    #   save actual data
    #
    file_pos_by_section = {}

    section_name = "ortholog_sets"
    file_pos_by_section[section_name] = data_file.tell()
    dump_dict_of_objects(ortholog_sets, data_file)

    section_name = "pairwise_scores"
    file_pos_by_section[section_name] = data_file.tell()
    dump_dict_of_object_lists(ortholog_set_pairwise_scores, data_file)

    section_name = "pairwise_alignments"
    file_pos_by_section[section_name] = data_file.tell()
    dump_dict_of_object_lists(ortholog_set_pairwise_alignment, data_file)

    #
    #   go back and write section starts in the directory
    #
    fill_directory_of_sections(data_file, section_name_directory_entry_pos, file_pos_by_section)


#_____________________________________________________________________________________
#
#   _save_orthology_for_species_pair_to_cache
#_____________________________________________________________________________________
def _save_orthology_for_species_pair_to_cache(sqlite_cache_file_name, species_pair_id_to_data_name_cache_file_name, ensembl_version, index_file, logger):

    sqlite_conn = sqlite3.connect(sqlite_cache_file_name)

    ortholog_type_id_to_ortholog_type = _sqlite_read_ortholog_type_ids(sqlite_conn, logger)
    sqlite_cur = sqlite_conn.cursor()
    member_id_to_real_id   = _retrieve_member_ids(sqlite_cur, logger, False)

    sqlite_cur.execute('PRAGMA cache_size = 200000')
    sqlite_cur.execute('DROP TABLE IF EXISTS method_link_ids;')
    sqlite_cur.execute('CREATE TEMP TABLE method_link_ids (method_link_species_set_id INTEGER);')
    for mi in species_pair_id_to_data_name_cache_file_name.keys():
        sqlite_cur.execute("""INSERT INTO method_link_ids VALUES (?)""", (mi,))
    sqlite_cur.execute("CREATE index i_method_link_ds on method_link_ids(method_link_species_set_id);")

    #
    #   Have two parallel cursors for looping over homology and homology_member tables
    #       in order of method_link_species_set_id
    #
    homology_cur = sqlite_conn.cursor()
    homology_cur.execute("""  SELECT
                                    method_link_species_set_id,
                                    homology_id, ortholog_type_id, dn, ds, n, s,
                                    ancestor_node_id, tree_node_id
                                FROM
                                    homology NATURAL JOIN
                                    method_link_ids
                                ORDER BY method_link_species_set_id""")

    homology_member_cur = sqlite_conn.cursor()
    homology_member_cur.execute(""" SELECT
                                    method_link_species_set_id,
                                    homology_id, member_id,
                                    peptide_member_id,
                                    perc_cov, perc_id, perc_pos
                                FROM
                                    homology_member NATURAL JOIN
                                    method_link_ids
                                ORDER BY method_link_species_set_id""")



    start = time.time()
    cnt_species_pairs           = 0
    cnt_total_species_pairs     = len(species_pair_id_to_data_name_cache_file_name)

    # bookmarking looping over all method_link_species_set_id
    homology_cur_ended        = False
    homology_member_cur_ended = False
    curr_method_link_species_set_id = None

    # this is the first row of the NEXT method_link_species_set_id
    homology_row = None
    homology_member_row = None

    logger.info("Process homology and homology_member tables")

    #
    #   Outer loops once for each species pair
    #
    #       Ends when both homology and homology_member cursors have finished
    #       (homology_cur_ended / homology_member_cur_ended = True)
    #
    while 1:

        #
        #   holds homology_member data
        #
        homolog_id_to_data = dict()

        # Process row from previous iteration which we downloaded before noticing the
        #   species were different
        if homology_member_row:
            _process_homology_member_table_row (homology_member_row, homolog_id_to_data)

        #
        #   iterate through homology_members which share the same species_pair method_link_id
        #
        for data in homology_member_cur:
            #if data[0] not in species_pair_id_to_data_name_cache_file_name:
            #    continue
            #
            # If new species pair (differnt curr_method_link_species_set_id)
            #   Break and save row to be processed as part of the next round
            #
            if not curr_method_link_species_set_id:
                curr_method_link_species_set_id = data[0]
            elif curr_method_link_species_set_id <> data[0]:
                homology_member_row = data
                break

            #
            #   save data by homolog_id
            #
            _process_homology_member_table_row (data, homolog_id_to_data)

        # All has ended for the homology_member table...
        else:
            homology_member_cur_ended = True

        # holds orthology data
        ortholog_sets = dict()
        ortholog_set_pairwise_scores    = defaultdict(list)
        ortholog_set_pairwise_alignment = defaultdict(list)
        cnt_non_protein_coding_genes = 0

        # Process row from previous iteration which we downloaded before noticing the
        #   species were different
        if homology_row:
            cnt_non_protein_coding_genes += \
                _process_homology_table_row (homology_row, ortholog_type_id_to_ortholog_type,
                                            homolog_id_to_data, member_id_to_real_id,
                                            ortholog_sets,
                                            ortholog_set_pairwise_scores,
                                            ortholog_set_pairwise_alignment)

        for data in homology_cur:
            #if data[0] not in species_pair_id_to_data_name_cache_file_name:
            #    continue

            #
            # If new species pair (differnt curr_method_link_species_set_id)
            #   Break and save row to be processed as part of the next round
            #
            if curr_method_link_species_set_id <> data[0]:
                homology_row = data
                break

            cnt_non_protein_coding_genes += \
                _process_homology_table_row (data, ortholog_type_id_to_ortholog_type,
                                            homolog_id_to_data, member_id_to_real_id,
                                            ortholog_sets,
                                            ortholog_set_pairwise_scores,
                                            ortholog_set_pairwise_alignment)
        else:
            homology_cur_ended = True

        if cnt_non_protein_coding_genes:
            logger.warning("      %d non protein coding genes ignored." % cnt_non_protein_coding_genes)

        data_name, cache_file_name = species_pair_id_to_data_name_cache_file_name[curr_method_link_species_set_id]
        _save_to_cache (cache_file_name, data_name, ortholog_sets, ortholog_set_pairwise_scores, ortholog_set_pairwise_alignment)
        index_file.write("%d\t%s\t%s\n" % (ensembl_version, data_name, cache_file_name))

        if homology_cur_ended and homology_member_cur_ended:
            break
        cnt_species_pairs +=1
        total_time = time.time() - start
        projected_total_time = total_time / cnt_species_pairs * cnt_total_species_pairs
        logger.debug("%4d species pairs (out of %5d) in %4.1fs (out of %5ds) [%s]" %
                     (  cnt_species_pairs, cnt_total_species_pairs,
                        total_time, projected_total_time, data_name))

        curr_method_link_species_set_id = homology_row[0]
        assert(curr_method_link_species_set_id == homology_member_row[0])

    logger.info("%4d species pairs in %ds" % (cnt_species_pairs, time.time() - start))
    sqlite_cur.execute('DROP TABLE IF EXISTS method_link_ids;')



#_____________________________________________________________________________________
#
#   _cache_compara_orthology_per_version
#_____________________________________________________________________________________
def _cache_compara_orthology_per_version(mysql_dbh, compara_db_per_version, index_file, cache_file_directory, logger,
                                        ensembl_version, discard_cache = False,
                                        valid_taxon_id_pairs = set(), valid_taxon_ids = set()):
    """
    Cache a specified version of Compara from an Ensembl database
    """

    db_name = compara_db_per_version[ensembl_version]

    cursor = mysql_dbh.cursor()
    cursor.execute("use %s" % db_name)

    #
    #   get list of species pairs and their corresponding Ensembl ids
    #
    (all_species_pair_ids,
    data_name_to_species_pair_id) = _cache_list_of_species_from_msql(cursor, index_file, compara_db_per_version,
                                                                    cache_file_directory, logger, ensembl_version,
                                                                    discard_cache, valid_taxon_id_pairs, valid_taxon_ids)

    #
    #   list cache files which have to be redone
    #
    data_names = data_name_to_species_pair_id.keys()

    (missing_cache_file_names,
     uptodate_cache_file_names) = get_missing_cache_file_names (compara_db_per_version, data_names,
                                                                cache_file_directory,
                                                                "{db_name}.orthology.{data_name}.cache",
                                                                _FILE_VERSION_MAJ,
                                                                logger, [ensembl_version],
                                                                discard_cache)

    #
    #   Write up to date cache file names to index
    #
    for db_version, db_name, data_name, cache_file_name in uptodate_cache_file_names:
        logger.log(MESSAGE, "  Compara cache file for %s %s is already up to date." % (db_name, data_name))
        index_file.write("%d\t%s\t%s\n" % (db_version, data_name, cache_file_name))
    index_file.flush()


    #
    #   Link missing file names to species_pair_ids
    #
    species_pair_id_to_data_name_cache_file_name = dict()
    for db_version, db_name, data_name, cache_file_name in missing_cache_file_names:
        if data_name in data_name_to_species_pair_id:
            species_pair_id = data_name_to_species_pair_id[data_name]
            species_pair_id_to_data_name_cache_file_name[species_pair_id] = (data_name, cache_file_name)


    #
    #   all up to date
    #
    if not len(missing_cache_file_names):
        return

    #
    #   sqlite cache file name
    #
    cache_file_part = "{db_name}.orthology.{data_name}.cache".format(db_name = db_name, data_name = "sqlite")
    sqlite_cache_file_name = os.path.join(cache_file_directory, cache_file_part)


    #
    #   Save MySql locally first (as sqlite)
    #
    if not os.path.exists(sqlite_cache_file_name) or not _sqlite_file_is_valid:
        # ignore paralogs
        ortholog_species_pair_ids          = all_species_pair_ids
        _copy_from_mysql_to_sqlite (cursor, sqlite_cache_file_name, ortholog_species_pair_ids, logger)


    #
    #   Save all species pairs
    #
    _save_orthology_for_species_pair_to_cache(sqlite_cache_file_name, species_pair_id_to_data_name_cache_file_name, ensembl_version, index_file, logger)





#_____________________________________________________________________________________
#
#   cache_compara_orthology
#_____________________________________________________________________________________
def cache_compara_orthology(mysql_dbh, index_file_name, cache_file_directory, logger,
                            ensembl_versions = None, discard_cache = False,
                            valid_taxon_id_pairs = set(), valid_taxon_ids = set()):
    """
    Cache all specified versions from an Ensembl database
    ensembl_version can be None (==latest version), a number, or a list of numbers
    """

    #
    #   get list of database names
    #
    compara_db_per_version = get_compara_databases (mysql_dbh)

    ensembl_versions = _specify_ensembl_versions(compara_db_per_version, ensembl_versions)

    #
    #   make index directory if does not exists
    #
    file_dir = os.path.split(os.path.abspath(index_file_name))[0]
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    index_file = open(index_file_name, "w")


    #
    #   cache per ensembl version
    #
    for ensembl_version in ensembl_versions:
        _cache_compara_orthology_per_version(mysql_dbh, compara_db_per_version, index_file, cache_file_directory, logger,
                                            ensembl_version, discard_cache ,
                                            valid_taxon_id_pairs, valid_taxon_ids)

    index_file.close()






































#_________________________________________________________________________________________

#   _save_memory_for_strings

#_________________________________________________________________________________________
_common_strings =dict()
def _save_memory_for_strings (s):
    """save memory by using string reference. Relying on python COW"""
    if s not in _common_strings:
        _common_strings[s] = s
    return _common_strings[s]









#_____________________________________________________________________________________
#
#   _load_from_cache
#_____________________________________________________________________________________
def _load_from_cache (cache_file_name, data_file, file_pos_by_section, logger, data_to_load = ["ortholog_sets"]):
    """
    Load orthology from cache file
        data_to_load is a list or set of the following values
                "ortholog_sets", "pairwise_scores", "pairwise_alignments" which determines what data to load
                usually just "ortholog_sets" is useful.
    """
    #
    #   data to return
    #
    ortholog_sets                   = None
    ortholog_set_pairwise_scores    = None
    ortholog_set_pairwise_alignment = None


    for section_name in data_to_load:
        if section_name not in file_pos_by_section:
            raise Exception("Missing section %s in cache file %s" % (section_name, cache_file_name))

    #
    #   read ortholog_sets
    #
    if "ortholog_sets" in data_to_load:
        data_file.seek(file_pos_by_section["ortholog_sets"], os.SEEK_SET)
        ortholog_sets = load_dict_of_objects(data_file, t_ortholog_set)

    #
    #   read ortholog_sets
    #
    if "pairwise_scores" in data_to_load:
        data_file.seek(file_pos_by_section["pairwise_scores"], os.SEEK_SET)
        ortholog_set_pairwise_scores = load_dict_of_object_lists(data_file, t_ortholog_set_pairwise_scores)
    #
    #   read ortholog_sets
    #
    if "pairwise_alignments" in data_to_load:
        data_file.seek(file_pos_by_section["pairwise_alignments"], os.SEEK_SET)
        ortholog_set_pairwise_alignment = load_dict_of_object_lists(data_file, t_ortholog_set_pairwise_alignment)

    return ortholog_sets, ortholog_set_pairwise_scores, ortholog_set_pairwise_alignment



#_____________________________________________________________________________________
#
#   open_cache_file
#_____________________________________________________________________________________
def open_cache_file(index_file_name, logger, ensembl_version, data_name):
    """
    return cache file given an index file name
    """
    #
    #   look up cache file name from index
    #
    (   cache_file_name,
        ensembl_version) = lookup_compara_cache_file_name(index_file_name, logger, ensembl_version, data_name)

    if cache_file_name == None or not os.path.exists(cache_file_name):
        return (None,) * 4


    logger.info("  Loading cache file = %s" % cache_file_name)
    data_file = open(cache_file_name, 'rb')

    #
    #   Is file version correct
    #
    latest_version, errmsg = check_cache_file_version (data_file, _FILE_VERSION_MAJ)
    if not latest_version:
        logger.warning(errmsg)
        return (None,) * 4

    #
    #   Retrieve protein tree data in sections
    #
    file_pos_by_section = read_directory_of_sections (data_file)

    return data_file, file_pos_by_section, ensembl_version, cache_file_name



















#_____________________________________________________________________________________
#
#   get_compara_orthology_for_species_pair
#_____________________________________________________________________________________
def get_compara_orthology_for_species_pair(index_file_name, logger, species_names, ensembl_version = None, data_to_load = ["ortholog_sets"]):
    """
    Get orthology data for a specified version
    data_to_load can be one or more of ["node", "node_to_parent", "alignment"]
    """

    #
    #   Get cached species pairs
    #
    (taxon_id_to_name_and_assembly,
     taxon_ids_to_species_pair_id,
     ensembl_version,
     cache_file_name) =_get_compara_species_pairs(index_file_name, logger, ensembl_version)

    if not taxon_id_to_name_and_assembly:
        return (None,) * 5

    #
    #   Match to suppled species names
    #

    taxon_id_species = []
    for s in  species_names:
        for t in taxon_id_to_name_and_assembly.values():
            if s == t.scientific_name:
                taxon_id_species.append((t.taxon_id, s))
                break
        else:
            logger.warning("No orthology_data for species %s in Ensembl Compara v. %d" % (s, ensembl_version))

    if len(taxon_id_species) != 2:
        return (None,) * 5

    taxon_id_species.sort()

    species_names = tuple(ts[1] for ts in taxon_id_species)
    logger.info("Loading orthology data for version %d %s-%s" % (ensembl_version, species_names[0], species_names[1]))


    #
    #   Load from cache file
    #
    (   data_file,
        file_pos_by_section,
        ensembl_version,
        cache_file_name     ) = open_cache_file(index_file_name, logger, ensembl_version, "%s_%s" % species_names)
    if not data_file:
        return (None,) * 5
    return _load_from_cache (cache_file_name, data_file, file_pos_by_section, logger, data_to_load) + (ensembl_version, cache_file_name)

#_____________________________________________________________________________________
#
#   get_compara_orthology_for_taxon_ids
#_____________________________________________________________________________________
def get_compara_orthology_for_taxon_ids(index_file_name, logger, taxon_ids, ensembl_version = None, data_to_load = ["ortholog_sets"]):
    """
    Get orthology data for a specified version
    data_to_load can be one or more of ["node", "node_to_parent", "alignment"]
    """

    #
    #   Get cached species pairs
    #
    (taxon_id_to_name_and_assembly,
     taxon_ids_to_species_pair_id,
     ensembl_version,
     cache_file_name) =_get_compara_species_pairs(index_file_name, logger, ensembl_version)

    if not taxon_id_to_name_and_assembly:
        return (None,) * 5

    #
    #   Match to suppled species names
    #

    taxon_id_species = []
    for t in taxon_ids:
        if t not in taxon_id_to_name_and_assembly:
            logger.warning("No orthology_data for taxon_id %d in Ensembl Compara v. %d" % (t, ensembl_version))
            continue
        taxon_id_species.append((t, taxon_id_to_name_and_assembly[t].scientific_name))

    if len(taxon_id_species) != 2:
        return (None,) * 5

    taxon_id_species.sort()

    species_names = tuple(ts[1] for ts in taxon_id_species)
    logger.info("Loading orthology data for version %d %s-%s" % (ensembl_version, species_names[0], species_names[1]))


    #
    #   Load from cache file
    #
    (   data_file,
        file_pos_by_section,
        ensembl_version,
        cache_file_name     ) = open_cache_file(index_file_name, logger, ensembl_version, "%s_%s" % species_names)
    if not data_file:
        return (None,) * 5
    return _load_from_cache (cache_file_name, data_file, file_pos_by_section, logger, data_to_load) + (ensembl_version, cache_file_name)


#_____________________________________________________________________________________
#
#   _get_compara_species_pairs
#_____________________________________________________________________________________
def _get_compara_species_pairs(index_file_name, logger, ensembl_version = None):
    """
    Helper function: data should be taxon_id_to_name_and_assembly or taxon_ids_to_species_pair_id
    """

    (data_file, file_pos_by_section,
     ensembl_version, cache_file_name) = open_cache_file(index_file_name, logger, ensembl_version, "species_pairs")
    if not data_file:
        return (None,) * 4

    data_file.seek(file_pos_by_section["taxon_id_to_name_and_assembly"], os.SEEK_SET)
    taxon_id_to_name_and_assembly = cPickle.load(data_file)
    data_file.seek(file_pos_by_section["taxon_ids_to_species_pair_id"], os.SEEK_SET)
    taxon_ids_to_species_pair_id = cPickle.load(data_file)

    return (taxon_id_to_name_and_assembly, taxon_ids_to_species_pair_id, ensembl_version, cache_file_name)


#_____________________________________________________________________________________
#
#   get_cached_or_remote_compara_species
#_____________________________________________________________________________________
def get_cached_or_remote_compara_species(index_file_name, logger, ensembl_version = None, mysql_dbh = None):
    """
    Helper function: data should be taxon_id_to_name_and_assembly or taxon_ids_to_species_pair_id
    """

    #
    #   Is cached version available
    #
    (   taxon_id_to_name_and_assembly,
        taxon_ids_to_species_pair_id,
        ensembl_version,
        cache_file_name) = _get_compara_species_pairs(index_file_name, logger, ensembl_version)

    if taxon_id_to_name_and_assembly:
        return (taxon_id_to_name_and_assembly, ensembl_version)


    #
    #   use Remote version
    #
    if not mysql_dbh:
        mysql_dbh = connect_ensembl_mysql()
        if not mysql_dbh:
            return (None, None)

    #
    #   Connect to specified version of compara
    #
    compara_db_per_version = get_compara_databases (mysql_dbh)
    ensembl_version = _specify_ensembl_versions(compara_db_per_version, ensembl_version)[0]
    cursor = mysql_dbh.cursor()
    db_name = compara_db_per_version[ensembl_version]
    cursor.execute("use %s" % db_name)

    taxon_id_to_name_and_assembly = _retrieve_mysql_species_name_and_assembly (cursor, logger)

    return (taxon_id_to_name_and_assembly, ensembl_version)




#_____________________________________________________________________________________
#
#   log_compara_orthology
#_____________________________________________________________________________________
def log_compara_orthology (logger, taxon_ids, species_names, ortholog_sets, ortholog_set_pairwise_scores, ortholog_set_pairwise_alignment):
    """
    Log some summary statistics about the orthology
    """
    if ortholog_sets:
        logger.log(MESSAGE, "  %s - %s" % species_names)
        logger.log(MESSAGE, "    %6d ortholog sets" % len(ortholog_sets))
        cnt_ortholog_sets_by_category = defaultdict(int)
        cnt_genes_by_category = defaultdict(lambda:[0,0])
        for ortholog_set in ortholog_sets.itervalues():
            gene_cnts = [len(ortholog_set.gene_ids[t]) for t in taxon_ids]
            # 1:1 / 1:m etc.
            category = (gene_cnts[0] > 1, gene_cnts[1] > 1)
            cnt_ortholog_sets_by_category[category] +=1
            cnt_genes_by_category[category][0] += gene_cnts[0]
            cnt_genes_by_category[category][1] += gene_cnts[1]

        for i in 0,1:
            cnt_genes = 0
            for c in cnt_genes_by_category.values():
                cnt_genes += c[i]
            logger.log(MESSAGE, "    %6d genes for %s" % (cnt_genes, species_names[i]))


        category_names = [((False, False), "1:1"),
                          ((False, True),  "1:m"),
                          ((True,  False), "m:1"),
                          ((True,  True),  "m:m")]
        for category, name in category_names:
            logger.log(MESSAGE, "    %6d %s ortholog sets" % (cnt_ortholog_sets_by_category[category], name))
            logger.log(MESSAGE, "    %6d:%6d genes"  % tuple(cnt_genes_by_category[category]))
    if ortholog_set_pairwise_scores:
        logger.log(MESSAGE, "  %8d dn, ds, n, s"  % (sum(len(v) for v in ortholog_set_pairwise_scores.itervalues())))
    if ortholog_set_pairwise_alignment:
        logger.log(MESSAGE, "  %8d pairwise alignment quality scores"  % (sum(len(v) for v in ortholog_set_pairwise_alignment.itervalues())))

    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888
    #   DEBUG
    #
    #if len(ortholog_sets):
    #    import pprint
    #    pp = pprint.PrettyPrinter(indent=4)
    #    for ancestor_node_id, o_s in ortholog_sets.iteritems():
    #        sys.stderr.write("%d=\n" % ancestor_node_id)
    #        sys.stderr.write("    " + pp.pformat(o_s._as_dict()).replace("\n", "\n    ") + "\n")
    #        if ortholog_set_pairwise_scores:
    #            for i in ortholog_set_pairwise_scores[ancestor_node_id]:
    #                sys.stderr.write("    " + pp.pformat(i._as_dict()).replace("\n", "\n    ") + "\n")
    #        if ortholog_set_pairwise_alignment:
    #            for i in ortholog_set_pairwise_alignment[ancestor_node_id]:
    #                sys.stderr.write("    " + pp.pformat(i._as_dict()).replace("\n", "\n    ") + "\n")
    #   DEBUG
    #
    #8888888888888888888888888888888888888888888888888888888888888888888888888888888888888



if __name__ == '__main__':
    import logging,sys
    import logging.handlers

    MESSAGE = 15
    logging.addLevelName(MESSAGE, "MESSAGE")

    def setup_std_logging (logger, log_file, verbose):
        """
        set up logging using programme options
        """
        class debug_filter(logging.Filter):
            """
            Ignore INFO mesages
            """
            def filter(self, record):
                return logging.INFO != record.levelno

        class NullHandler(logging.Handler):
            """
            for when there is no logging
            """
            def emit(self, record):
                pass

        # We are interesting in all messages
        logger.setLevel(logging.DEBUG)
        has_handler = False

        # log to file if that is specified
        if log_file:
            handler = logging.FileHandler(log_file, delay=False)
            handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)6s - %(message)s"))
            handler.setLevel(MESSAGE)
            logger.addHandler(handler)
            has_handler = True

        # log to stderr if verbose
        if verbose:
            stderrhandler = logging.StreamHandler(sys.stderr)
            stderrhandler.setFormatter(logging.Formatter("    %(message)s"))
            stderrhandler.setLevel(logging.DEBUG)
            if log_file:
                stderrhandler.addFilter(debug_filter())
            logger.addHandler(stderrhandler)
            has_handler = True

        # no logging
        if not has_handler:
            logger.addHandler(NullHandler())


    #
    #   set up log
    #
    logger = logging.getLogger("me")
    setup_std_logging(logger, "/net/cpp-mirror/databases/ensembl_cache/compara_orthology.log", True)

    index_file_name = "/net/cpp-mirror/databases/ensembl_cache/compara_orthology.index"
    cache_directory = "/net/cpp-mirror/databases/ensembl_cache/compara/orthology/"

    converting_species = "Anolis carolinensis", "Ailuropoda melanoleuca", "Branchiostoma floridae", "Canis familiaris", "Danio rerio", "Equus caballus", "Gasterosteus aculeatus", "Gallus gallus", "Homo sapiens", "Monodelphis domestica", "Mus musculus", "Macaca mulatta", "Nematostella vectensis", "Ornithorhynchus anatinus", "Oryzias latipes", "Petromyzon marinus", "Rattus norvegicus", "Strongylocentrotus purpuratus", "Taeniopygia guttata", "Tetraodon nigroviridis", "Xenopus tropicalis"


    #
    #   link taxon ids and species names
    #
    (taxon_id_to_name_and_assembly,
        ensembl_version) = get_cached_or_remote_compara_species(index_file_name, logger, ensembl_version = None)


    logger.debug("Use latest Ensembl version v.%d" % ensembl_version)


    #
    #   get taxon ids for each species name
    #
    taxon_ids = []
    taxon_id_to_species_name = dict()
    for s in  converting_species:
        for t in taxon_id_to_name_and_assembly.values():
            if s == t.scientific_name:
                taxon_ids.append(t.taxon_id)
                taxon_id_to_species_name[t.taxon_id] = s
                break
        else:
            logger.warning("No orthology_data for species %s" % s)

    #
    #   get taxon id / species name pairs
    #
    taxon_id_pairs = []
    species_name_pairs = []
    for t in taxon_ids:
        for tt in taxon_ids:
            if t < tt:
                taxon_id_pairs.append((t, tt))
                species_name_pairs.append((taxon_id_to_species_name[t], taxon_id_to_species_name[tt]))








    #
    #   Cache if necessary
    #
    mysql_dbh = connect_ensembl_mysql()
    cache_compara_orthology(mysql_dbh, index_file_name, cache_directory, logger, None, discard_cache = False, valid_taxon_ids = taxon_ids)

    #
    #   Try and get by species name pair or taxon_id pair
    #
    for taxon_id_pair, species_name_pair in zip(taxon_id_pairs, species_name_pairs):
        # taxon_id pair
        (ortholog_sets,
        ortholog_set_pairwise_scores,
        ortholog_set_pairwise_alignment,
        ensembl_version, cache_file_name) = get_compara_orthology_for_taxon_ids(index_file_name, logger, taxon_id_pair, None, data_to_load = ["ortholog_sets"])
        log_compara_orthology (logger, taxon_id_pair, species_name_pair, ortholog_sets, ortholog_set_pairwise_scores, ortholog_set_pairwise_alignment)

        # species name pair
        (ortholog_sets,
        ortholog_set_pairwise_scores,
        ortholog_set_pairwise_alignment,
        ensembl_version, cache_file_name) = get_compara_orthology_for_species_pair(index_file_name, logger, species_name_pair, None, data_to_load = ["ortholog_sets"])
        log_compara_orthology (logger, taxon_id_pair, species_name_pair, ortholog_sets, ortholog_set_pairwise_scores, ortholog_set_pairwise_alignment)
        break




