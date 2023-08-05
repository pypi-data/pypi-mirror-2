#!/usr/bin/env python
################################################################################
#
#   compara_ncbi_taxa.py
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
for downloading ncbi taxa from an ensembl data base and caching for local fast
access

"""
import re, os
from dump_object import dump_object

from random_access_file_by_sections import fill_directory_of_sections, write_directory_of_sections, read_directory_of_sections
from collections import defaultdict
import marshal, time, struct
from general import check_cache_file_version, cache_is_valid, read_compara_index_file, lookup_compara_cache_file_name, _prepare_cache_file,  cache_specified_compara_data, cache_specified_core_data


#
#   Magic numbers
#
_FILE_VERSION_MAJ = 3
#
#   for logging: halfway between DEBUG and INFO
#
MESSAGE = 15



#_________________________________________________________________________________________

#   _retrieve_mysql_data

#_________________________________________________________________________________________
def _retrieve_mysql_data (mysql_dbh, db_name, logger):
    """
    Retrieve taxa_names from a particular compara database version
    """


    start_time = time.time()


    cursor = mysql_dbh.cursor()
    cursor.execute("use %s" % db_name)

    #
    #   get taxon names
    #
    taxon_id_to_name            = dict()
    taxon_id_to_name["common name"] = dict()
    taxon_id_to_name["scientific name"] = dict()

    for name_type in "common name", "scientific name":
        db_str = """    SELECT
                                name,
                                taxon_id
                            FROM
                                ncbi_taxa_name
                            WHERE
                                name_class = '%s'
                """ % name_type

        logger.debug("  Retrieving %ss from %s..." % (name_type, db_name))
        cursor.execute(db_str)
        results = cursor.fetchall()

        for (   taxon_name,
                taxon_id) in results:

            #   Unknown type
            taxon_id_to_name[name_type][taxon_id] = taxon_name



    #
    #   Get phylogeny
    #
    matches_by_type     = defaultdict(lambda: defaultdict(list))
    db_str = """SELECT
                        taxon_id,
                        parent_id
                    FROM
                        ncbi_taxa_node
            """

    logger.debug("  Retrieving taxonomical phylogeny from %s..." % db_name)
    cursor = mysql_dbh.cursor()
    cursor.execute(db_str)
    cnt_all_matches = 0

    taxon_id_to_parent = dict()

    for (
            taxon_id,
            parent_id) in cursor:
        cnt_all_matches += 1
        taxon_id_to_parent[taxon_id] = parent_id


    end_time = time.time()
    logger.info("  Retrieved %d taxa from Ensembl database in %ds"
                            % (cnt_all_matches, end_time - start_time))
    return (taxon_id_to_name["scientific name"],
            taxon_id_to_name["common name"],
            taxon_id_to_parent)






#_____________________________________________________________________________________
#
#   _load_from_cache
#_____________________________________________________________________________________
def _load_from_cache (cache_file_name, logger):
    """
    Load from cache file
    """
    try:
        if not os.path.exists(cache_file_name):
            return None, None, None

        logger.debug("  Loading taxa data from cache")
        data_file = open(cache_file_name, 'rb')

        #
        #   Is file version correct
        #
        latest_version, errmsg = check_cache_file_version (data_file, _FILE_VERSION_MAJ)
        if not latest_version:
            logger.warning(errmsg)
            return None, None, None

        #
        #   taxon data
        #
        taxon_id_to_scientific_name = marshal.load(data_file)
        taxon_id_to_common_name     = marshal.load(data_file)
        taxon_id_to_parent          = marshal.load(data_file)
        return (taxon_id_to_scientific_name,
                taxon_id_to_common_name    ,
                taxon_id_to_parent         )



    except:
        raise
        return None, None, None


#_____________________________________________________________________________________
#
#   _save_to_cache
#_____________________________________________________________________________________
def _save_to_cache (   taxon_id_to_scientific_name,
                                taxon_id_to_common_name    ,
                                taxon_id_to_parent         ,
                                cache_file_name, logger):
    """
    Save to cache file
    """
    data_file = _prepare_cache_file (cache_file_name, logger, _FILE_VERSION_MAJ, "ncbi taxa")
    start_time = time.time()

    #
    #   taxon data
    #
    marshal.dump(taxon_id_to_scientific_name , data_file)
    marshal.dump(taxon_id_to_common_name     , data_file)
    marshal.dump(taxon_id_to_parent          , data_file)

    end_time = time.time()
    logger.info("  Cached in %ds" % (end_time - start_time))






#_____________________________________________________________________________________
#
#   get_compara_ncbi_taxa
#_____________________________________________________________________________________
def get_compara_ncbi_taxa(index_file_name, logger, ensembl_version = None):
    """
    Get taxa data
    """

    #
    #   look up cache file name from index
    #
    try:
        (   cache_file_name,
            ensembl_version) = lookup_compara_cache_file_name(index_file_name, logger, ensembl_version, 'ncbi_taxa')
    except IOError, e:
        raise Exception("Could not open index file %s\n\t%s" %
                        (index_file_name, str(e)))


    if cache_file_name == None:
        return (None, ) * 5

    logger.info("Loading ncbi taxa from compara v. %d" % (ensembl_version))

    (taxon_id_to_scientific_name,
     taxon_id_to_common_name    ,
     taxon_id_to_parent         ) = _load_from_cache (cache_file_name, logger)

    return (taxon_id_to_scientific_name,
            taxon_id_to_common_name    ,
            taxon_id_to_parent         ,
            ensembl_version            ,
            cache_file_name            )

#_____________________________________________________________________________________
#
#   _write_to_cache
#_____________________________________________________________________________________
def _write_to_cache (mysql_dbh, data_name, db_name, cache_file_name, logger):
    """
    Download data from database and write to cache file
    """
    (taxon_id_to_scientific_name,
     taxon_id_to_common_name    ,
     taxon_id_to_parent         ) = _retrieve_mysql_data (mysql_dbh, db_name, logger)
    _save_to_cache (taxon_id_to_scientific_name,
                            taxon_id_to_common_name    ,
                            taxon_id_to_parent         ,
                            cache_file_name, logger)

    logger.log(MESSAGE, "  %7d taxa downloaded" % len(taxon_id_to_parent))
    logger.log(MESSAGE, "  %7d taxa scientific names downloaded" % len(taxon_id_to_scientific_name))
    logger.log(MESSAGE, "  %7d taxa common names downloaded" % len(taxon_id_to_common_name))

#_____________________________________________________________________________________
#
#   cache_compara_ncbi_taxa
#_____________________________________________________________________________________
def cache_compara_ncbi_taxa(mysql_dbh, index_file_name, cache_file_directory, logger, ensembl_versions = None, discard_cache = False):
    """
    cache all specified versions from an Ensembl database
    ensembl_version can be None (==latest version), a number, or a list of numbers
    """
    cache_specified_compara_data(mysql_dbh, index_file_name, cache_file_directory, logger, _FILE_VERSION_MAJ,
                                     "{db_name}.{data_name}.cache", ['ncbi_taxa'], _write_to_cache,
                                     ensembl_versions, discard_cache)


