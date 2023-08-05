#!/usr/bin/env python
################################################################################
#
#   compara_protein_tree.py
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
for downloading protein tree data from an ensembl compara data base and caching for local fast
access

"""
import re, os
from dump_object import dump_object

from random_access_file_by_sections import fill_directory_of_sections, write_directory_of_sections, read_directory_of_sections
from collections import defaultdict
import marshal, time, struct
from general import (check_cache_file_version,
                        _prepare_cache_file,
                    cache_specified_compara_data,
                        lookup_compara_cache_file_name,
                    cache_specified_core_data,
                    lookup_core_cache_file_name
                        )
from marshalable_object import marshalable_object, load_dict_of_object_lists, dump_dict_of_object_lists, load_dict_of_objects, dump_dict_of_objects

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
t_prot_tree_alignment =marshalable_object("t_prot_tree_alignment",
                                          " cigar_line" +
                                          " beg"        +
                                          " end")
t_prot_tree_node      =marshalable_object("t_prot_tree_node",
                                          " prot_id"     +
                                          " root_id"     +
                                          " taxon_id")


#_________________________________________________________________________________________

#   _retrieve_mysql_data

#_________________________________________________________________________________________
def _retrieve_mysql_data (mysql_dbh, db_name, logger):
    """
    Retrieve protein tree data
    """


    start_time = time.time()


    cursor = mysql_dbh.cursor()
    cursor.execute("use %s" % db_name)

    #
    #   tree data
    #
    prot_node_id_to_alignments  = dict()
    prot_node_id_to_nodes       = dict()
    prot_node_id_to_parent      = dict()


    #
    #   member
    #
    db_str = """    SELECT
                            member_id,
                            stable_id,
                            taxon_id
                        FROM
                            member
                        WHERE
                            source_name = 'ENSEMBLPEP'
                        """

    logger.debug("  Retrieving protein id and taxon id from Ensembl compara...")
    cursor.execute(db_str)
    member_id_to_prot_id_taxon_id = dict()

    cnt_items = 0
    for (   member_id,
            prot_id,
            taxon_id) in cursor:

        # show progress for long downloads
        cnt_items += 1
        if cnt_items % 500000 == 0:
            logger.debug("  %10d.." % cnt_items)

        member_id_to_prot_id_taxon_id[member_id] = prot_id, taxon_id
    logger.debug("  %10d member_ids downloaded" % cnt_items)

    #
    #   protein_tree_member
    #
    db_str = """    SELECT
                            node_id,
                            root_id,
                            member_id,
                            cigar_line,
                            cigar_start,
                            cigar_end
                        FROM
                            protein_tree_member
                            """
    logger.debug("  Retrieving alignments and protein tree members from Ensembl compara...")
    cursor.execute(db_str)
    cnt_items = 0
    for (   node_id,
            root_id,
            member_id,
            cigar_line,
            beg,
            end) in cursor:
        # show progress for long downloads
        cnt_items += 1
        if cnt_items % 500000 == 0:
            logger.debug("  %10d.." % cnt_items)

        prot_id, taxon_id = member_id_to_prot_id_taxon_id[member_id]
        prot_node_id_to_alignments[node_id]  = t_prot_tree_alignment(cigar_line, beg, end)
        prot_node_id_to_nodes[node_id] = t_prot_tree_node(prot_id, root_id, taxon_id)
    logger.debug("  %10d protein tree members downloaded" % cnt_items)

    #
    #   protein_tree_node
    #
    db_str = """    SELECT
                            node_id,
                            parent_id,
                            distance_to_parent
                        FROM
                            protein_tree_node
            """

    logger.debug("  Retrieving phylogeny for proteins from Ensembl compara...")
    cursor.execute(db_str)
    cnt_items = 0
    for (   node_id,
            parent_node_id,
            distance_to_parent) in cursor:

        # show progress for long downloads
        cnt_items += 1
        if cnt_items % 500000 == 0:
            logger.debug("  %10d.." % cnt_items)

        #   Unknown type
        prot_node_id_to_parent[node_id] = [parent_node_id, distance_to_parent]

    logger.debug("  %10d protein tree nodes downloaded" % cnt_items)

    end_time = time.time()

    logger.info("  Retrieved %d protein tree nodes and %d relationships from Ensembl database in %ds"
                            % (len(prot_node_id_to_nodes), len(prot_node_id_to_parent),
                                    end_time - start_time))
    return prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent



#_____________________________________________________________________________________
#
#   _load_from_cache
#_____________________________________________________________________________________
def _load_from_cache (cache_file_name, logger, data_to_load = None):
    """
    Load tree data from cache file
        data_to_load is a list or set of the following values
                "alignment", "node", "node_to_parent" which determines what data to load
                usually just node or node_to_parent is useful.
    """
    start_time = time.time()
    try:
        if not os.path.exists(cache_file_name):
            return None, None, None

        logger.debug("  Loading protein tree from cache")
        logger.info("  Loading cache file = %s" % cache_file_name)
        data_file = open(cache_file_name, 'rb')

        #
        #   Is file version correct
        #
        latest_version, errmsg = check_cache_file_version (data_file, _FILE_VERSION_MAJ)
        if not latest_version:
            logger.warning(errmsg)
            return None, None, None
        #
        #   Retrieve protein tree data in sections
        #
        file_pos_by_section = read_directory_of_sections (data_file)

        #
        #   Read all data if none specified
        #
        if data_to_load == None:
            data_to_load = file_pos_by_section.keys()

        load_method = dict()
        load_method["alignment"]       = load_dict_of_objects, t_prot_tree_alignment
        load_method["node"]            = load_dict_of_objects, t_prot_tree_node
        load_method["node_to_parent"]  = (lambda d, ignore: marshal.load(d)), dict

        data = dict()
        for section in file_pos_by_section:

            #
            #   initialise to empty data
            #
            data[section] = dict()

            if section not in data_to_load:
                continue

            #
            #   read data
            #
            data_file.seek(file_pos_by_section[section], os.SEEK_SET)
            load_func, object_type = load_method[section]

            data[section] = load_func(data_file, object_type)



        #   log what data have been read?
        #
        end_time = time.time()
        logger.info("  Loaded tree data in %ds" % (end_time - start_time))

        # prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent
        return [data[k] for k in sorted(data.keys())]
    except:
        raise
        return None, None, None

#_____________________________________________________________________________________
#
#   _save_to_cache
#_____________________________________________________________________________________
def _save_to_cache (prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent, cache_file_name, logger):
    """
    Save data to cache file
    """
    data_file = _prepare_cache_file (cache_file_name, logger, _FILE_VERSION_MAJ, "protein tree")
    start_time = time.time()


    data = dict()
    data["alignment"]       = prot_node_id_to_alignments, dump_dict_of_objects
    data["node"]            = prot_node_id_to_nodes, dump_dict_of_objects
    data["node_to_parent"]  = prot_node_id_to_parent, marshal.dump




    #
    #   save "directory" recording where data are in the files so we
    #       can jump directly to that type
    section_name_directory_entry_pos = write_directory_of_sections(data_file, data.keys())

    #
    #   save actual data
    #
    file_pos_by_section = {}
    for section in sorted(data.keys()):

        # remember where this section begins
        file_pos_by_section[section] = data_file.tell()
        d, dump_func = data[section]
        dump_func(d, data_file)

    #
    #   go back and write section starts in the directory
    #
    fill_directory_of_sections(data_file, section_name_directory_entry_pos, file_pos_by_section)


    end_time = time.time()
    logger.info("  Cached in %ds" % (end_time - start_time))




#_____________________________________________________________________________________
#
#   get_compara_protein_trees
#_____________________________________________________________________________________
def get_compara_protein_trees(index_file_name, logger, ensembl_version = None, data_to_load = None):
    """
    Get protein tree data for a specified version
    data_to_load can be one or more of ["node", "node_to_parent", "alignment"]
    """

    #
    #   look up cache file name from index
    #
    (   cache_file_name,
        ensembl_version) = lookup_compara_cache_file_name(index_file_name, logger, ensembl_version, 'protein_tree')

    if cache_file_name == None:
        return None, None, None, None, None,

    logger.info("Loading protein tree data for version %d" % (ensembl_version))

    prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent = _load_from_cache (cache_file_name, logger, data_to_load)

    return prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent, ensembl_version, cache_file_name


#_____________________________________________________________________________________
#
#   _write_to_cache
#_____________________________________________________________________________________
def _write_to_cache (mysql_dbh, data_name, db_name, cache_file_name, logger):
    """
    Download data from database and write to cache file
    """
    # download from database and write to cache file
    prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent = _retrieve_mysql_data (mysql_dbh, db_name, logger)
    _save_to_cache (prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent, cache_file_name, logger)

    log_compara_protein_trees (logger, prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent)

#_____________________________________________________________________________________
#
#   cache_compara_protein_trees
#_____________________________________________________________________________________
def cache_compara_protein_trees(mysql_dbh, index_file_name, cache_file_directory, logger, ensembl_versions = None, discard_cache = False):
    """
    cache all specified versions from an Ensembl database
    ensembl_version can be None (==latest version), a number, or a list of numbers
    """
    cache_specified_compara_data(mysql_dbh, index_file_name, cache_file_directory, logger, _FILE_VERSION_MAJ,
                                     "{db_name}.{data_name}.cache", ['protein_tree'], _write_to_cache,
                                     ensembl_versions, discard_cache)

#_____________________________________________________________________________________
#
#   log_compara_protein_trees
#_____________________________________________________________________________________
def log_compara_protein_trees (logger, prot_node_id_to_alignments, prot_node_id_to_nodes, prot_node_id_to_parent):
    """
    Log some summary statistics about the different sort of protein tree data
    """

    logger.log(MESSAGE, "  Summary for protein tree data:")
    logger.log(MESSAGE, "  %10d alignments for creating the protein tree" %
               len(prot_node_id_to_alignments))
    logger.log(MESSAGE, "  %10d relationships between trees" %
               len(prot_node_id_to_parent))

    cnts = defaultdict(lambda:[0,0,0])
    taxon_ids = set()
    for n in prot_node_id_to_nodes.itervalues():
        taxon_ids.add(n.taxon_id)
        cnts[n.root_id][0] += 1
        # mouse
        if n.taxon_id == 10090:
            cnts[n.root_id][1] += 1
        elif n.taxon_id == 9606:
            cnts[n.root_id][2] += 1

    logger.debug("  %10d species" % len(taxon_ids))



    #
    #   tree sizes for all species / just human / just mouse
    #
    all_cnts = sorted([all for (all, mus, homo) in cnts.itervalues() ], reverse= True)
    mus_cnts = sorted([mus for (all, mus, homo) in cnts.itervalues() if mus ], reverse= True)
    homo_cnts = sorted([homo for (all, mus, homo) in cnts.itervalues() if homo ], reverse= True)
    logger.log(MESSAGE, "  %10d protein trees" % len(all_cnts))
    logger.log(MESSAGE, "             median size = %d" % all_cnts[int(len(all_cnts) / 2)])
    logger.log(MESSAGE, "             top 10 = %s" % ", ".join(map(str, all_cnts[0:10])))
    if len(homo_cnts):
        logger.log(MESSAGE, "  %10d protein trees with human proteins" % len(homo_cnts))
        logger.log(MESSAGE, "             median size = %d" % homo_cnts[int(len(homo_cnts) / 2)])
        logger.log(MESSAGE, "             top 10 = %s" % ", ".join(map(str, homo_cnts[0:10])))
    if len(mus_cnts):
        logger.log(MESSAGE, "  %10d protein trees with mouse proteins" % len(mus_cnts))
        logger.log(MESSAGE, "             median size = %d" % mus_cnts[int(len(mus_cnts) / 2)])
        logger.log(MESSAGE, "             top 10 = %s" % ", ".join(map(str, mus_cnts[0:10])))

