#!/usr/bin/env python
################################################################################
#
#   compara_species_pairs.py
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
import re, os
from dump_object import dump_object

from random_access_file_by_sections import fill_directory_of_sections, write_directory_of_sections, read_directory_of_sections
from collections import defaultdict, namedtuple
import marshal, cPickle, time, struct
from general import (check_cache_file_version,
                        _prepare_cache_file,
                    cache_specified_compara_data,
                        lookup_compara_cache_file_name,
                    cache_specified_core_data,
                    lookup_core_cache_file_name
                        )



#
#   Magic numbers
#
_FILE_VERSION_MAJ = 3
#
#   for logging: halfway between DEBUG and INFO
#
MESSAGE = 15

t_species_data = namedtuple("t_species_data", "taxon_id, scientific_name, assembly")

#_________________________________________________________________________________________

#   _retrieve_mysql_data

#_________________________________________________________________________________________
def _retrieve_mysql_data (mysql_dbh, db_name, logger):
    """
    Retrieve species pair data
    """


    start_time = time.time()


    cursor = mysql_dbh.cursor()
    cursor.execute("use %s" % db_name)

    #
    #   species_pairs data
    #
    taxon_ids_to_ortholog_species_pair    = dict()
    taxon_id_to_species_data              = dict()


    #
    #   method_link
    #
    db_str = """
                  SELECT
                          method_link_species_set_id,
                          mlss.name,
                          taxon_id,
                          gdb.name AS species_name,
                          assembly,
                          type = 'ENSEMBL_ORTHOLOGUES'
                      FROM
                          method_link_species_set mlss NATURAL JOIN
                          method_link JOIN
                          species_set USING (species_set_id) JOIN
                          genome_db gdb USING (genome_db_id)
                      WHERE
                          type = 'ENSEMBL_ORTHOLOGUES'
                        """

    logger.debug("  Retrieving species_pairs from Ensembl compara...")
    cursor.execute(db_str)

    #
    #   save method_link_ids to link up species pairs in the next step
    #
    method_link_id_to_species_pair = defaultdict(set)
    method_link_id_to_name         = dict()
    for (   method_link_id,
            method_link_name,
            taxon_id,
            scientific_name,
            assembly,
            ortholog_not_paralog) in cursor:
        taxon_id_to_species_data[taxon_id] = t_species_data(taxon_id, scientific_name, assembly)
        method_link_id_to_species_pair[method_link_id].add(taxon_id)
        method_link_id_to_name[method_link_id]         = method_link_name, ortholog_not_paralog


    #
    #   make sure each method_link_id has 2 species
    #
    taxon_id_to_within_species_homology = dict()
    taxon_id_to_between_species_homology = dict()
    cnt_items = 0
    for method_link_id, all_species in method_link_id_to_species_pair.iteritems():
        cnt_items += 1
        method_name, ortholog_not_paralog = method_link_id_to_name[method_link_id]

        #
        #   keep "in-paralogues" i.e. pair-wise comparisons within ortholog_sets from the same species
        #
        if len(all_species) == 1:
            assert(not ortholog_not_paralog)
            taxon_id_to_within_species_homology[all_species.pop()] = (method_link_id, method_name)
        #
        #   more than 2 species == error
        #
        elif len(all_species) != 2:
            raise Exception("%d (should be 2) species [%s] found for method_link_id = %d " %
                                (len(all_species), ",".join(map(str, all_species)), method_link_id))

        #
        #   not interested in "out-paralogues" i.e. between species paralogues
        #
        if not ortholog_not_paralog:
            continue

        taxon_id_to_between_species_homology[tuple(all_species)] = (method_link_id, method_name)

    for sp_pair in taxon_id_to_between_species_homology.iterkeys():
        (species1, species2) = sp_pair
        between = taxon_id_to_between_species_homology[species1, species2]
        same1   = taxon_id_to_within_species_homology[species1]
        same2   = taxon_id_to_within_species_homology[species2]
        taxon_ids_to_ortholog_species_pair[species1, species2] = [between, same1, same2]
        taxon_ids_to_ortholog_species_pair[species2, species1] = [between, same2, same1]


    end_time = time.time()

    return taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair


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

        taxon_id_to_species_data                = cPickle.load(data_file)
        taxon_ids_to_ortholog_species_pair   = cPickle.load(data_file)
        return taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair

    except:
        raise
        return None, None

#_____________________________________________________________________________________
#
#   _save_to_cache
#_____________________________________________________________________________________
def _save_to_cache (taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair, cache_file_name, logger):
    """
    Save data to cache file
    """

    data_file = _prepare_cache_file (cache_file_name, logger, _FILE_VERSION_MAJ, "species pair")

    cPickle.dump(taxon_id_to_species_data, data_file)
    cPickle.dump(taxon_ids_to_ortholog_species_pair, data_file)




#_____________________________________________________________________________________
#
#   get_compara_species_pairs
#_____________________________________________________________________________________
def get_compara_species_pairs(index_file_name, logger, ensembl_version = None, data_to_load = None):
    """
    Get protein tree data for a specified version
    data_to_load can be one or more of ["node", "node_to_parent", "alignment"]
    """

    #
    #   look up cache file name from index
    #
    (   cache_file_name,
        ensembl_version) = lookup_compara_cache_file_name(index_file_name, logger, ensembl_version, "species_pairs")

    if cache_file_name == None:
        return (None, ) * 4

    logger.info("Loading species pairs for Compara v.%d" % (ensembl_version))

    taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair = _load_from_cache (cache_file_name, logger, data_to_load)

    return taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair, ensembl_version, cache_file_name


#_____________________________________________________________________________________
#
#   _write_to_cache
#_____________________________________________________________________________________
def _write_to_cache (mysql_dbh, db_name, cache_file_name, logger):
    """
    Download data from database and write to cache file
    """
    taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair = _retrieve_mysql_data (mysql_dbh, db_name, logger)
    _save_to_cache (taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair, cache_file_name, logger)

    log_compara_species_pairs (logger, taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair)


#_____________________________________________________________________________________
#
#   cache_compara_species_pairs
#_____________________________________________________________________________________
def cache_compara_species_pairs(mysql_dbh, index_file_name, cache_file_directory, logger, ensembl_versions = None, discard_cache = False):
    """
    cache all specified versions from an Ensembl database
    ensembl_version can be None (==latest version), a number, or a list of numbers
    """
    cache_specified_compara_data(mysql_dbh, index_file_name, cache_file_directory, logger, _FILE_VERSION_MAJ,
                                     "{db_name}.{data_name}.cache", ['species_pairs'], _write_to_cache,
                                     ensembl_versions, discard_cache)


#_____________________________________________________________________________________
#
#   log_compara_species_pairs
#_____________________________________________________________________________________
def log_compara_species_pairs (logger, taxon_id_to_species_data, taxon_ids_to_ortholog_species_pair):
    """
    Log some summary statistics about the different sort of protein tree data
    """

    logger.log(MESSAGE, "  Summary for species / species_pair data from Ensembl Compara:")
    num_of_species          = len(taxon_id_to_species_data)
    num_of_pairs            = len(taxon_ids_to_ortholog_species_pair) / 2
    expected_num_of_pairs   = num_of_species * (num_of_species - 1) / 2

    logger.log(MESSAGE, "  %5d species" % num_of_species)
    if num_of_pairs == expected_num_of_pairs:
        logger.log(MESSAGE, "  %5d species pairs as expected" % num_of_pairs)
    else:
        logger.warning("  %5d species pairs (%7d expected)" % (num_of_pairs, expected_num_of_pairs))
    for taxon_id, species_data in sorted(taxon_id_to_species_data.iteritems(), key = lambda x: x[1].scientific_name):
        logger.log(MESSAGE, "  %40s, taxon_id = %-10d assembly = %s" % (species_data.scientific_name, taxon_id, species_data.assembly))

    #
    # #   print out one pair
    #
    # taxon_id1, taxon_id2  = taxon_ids_to_ortholog_species_pair.keys()[0]
    #
    # #   first the two species
    #
    # logger.debug(str(taxon_id_to_species_data[taxon_id1]))
    # logger.debug(str(taxon_id_to_species_data[taxon_id2]))
    #
    # #   Then the pair both in species order and in reverse
    #
    # logger.debug(str(taxon_ids_to_ortholog_species_pair[taxon_id1, taxon_id2]))
    # logger.debug(str(taxon_ids_to_ortholog_species_pair[taxon_id2, taxon_id1]))

