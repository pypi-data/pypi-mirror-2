#!/usr/bin/env python
################################################################################
#
#   core_protein_features.py
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
for downloading protein features from an ensembl data base and caching for local fast
access

"""
import re, os
from dump_object import dump_object
from marshalable_object import marshalable_object
from random_access_file_by_sections import fill_directory_of_sections, write_directory_of_sections, read_directory_of_sections
from collections import defaultdict
import marshal, time, struct
from general import (check_cache_file_version,
                        _prepare_cache_file,
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


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#   classes


#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
t_protein_feature =marshalable_object("t_protein_feature",
                                      " feature_type"        +
                                      " feature_description" +
                                      " display_label"       +
                                      " interpro_ac")

t_protein_feature_match =marshalable_object("t_protein_feature_match",
                                              " seq_beg"    +
                                              " seq_end"    +
                                              " score"      +
                                              " evalue"     +
                                              " perc_ident" +
                                              " hit_beg"    +
                                              " hit_end"    +
                                              " hit_name")

#_________________________________________________________________________________________

#   link_protein_feature_matches_to_prot_id

#_________________________________________________________________________________________
def link_protein_feature_matches_to_prot_id (matches_by_type):
    """
    Allow quick lookup of which proteins have a particular hit
    """
    hit_name_to_prot_id  = defaultdict(set)

    for feature_type in matches_by_type:
        for prot_id, features in matches_by_type[feature_type]:
            for feature in features:
                hit_name_to_prot_id[feature.hit_name].add(prot_id)

    return hit_name_to_prot_id


#_________________________________________________________________________________________

#   _retrieve_mysql_data

#_________________________________________________________________________________________
def _retrieve_mysql_data (mysql_dbh, species, db_name, logger):
    """
    Retrieve protein features e.g. domain hits from an Ensembl mysql database for
        a particular species and database version
    """


    start_time = time.time()


    cursor = mysql_dbh.cursor()
    cursor.execute("use %s" % db_name)

    #
    #   get protein features
    #
    protein_features     = dict()
    db_str = """SELECT
                    interpro.id,
                    xref.display_label,
                    xref.description,
                    interpro.interpro_ac
                FROM
                    xref JOIN
                    interpro on xref.dbprimary_acc = interpro.interpro_ac JOIN
                    external_db ON external_db.external_db_id = xref.external_db_id
            """

    logger.debug("  Retrieving interpro data from Ensembl database for %s..." % species)
    cursor.execute(db_str)
    results = cursor.fetchall()
    for (   hit_name,
            display_label,
            feature_description,
            interpro_ac) in results:

        #   Unknown type
        protein_features[hit_name] = t_protein_feature("Unknown", feature_description, display_label, interpro_ac)



    #
    #   get matches
    #
    matches_by_type     = defaultdict(lambda: defaultdict(list))
    db_str = """SELECT
                        an.logic_name,

                        tsi.stable_id,

                        pf.hit_name,
                        pf.seq_start,
                        pf.seq_end,
                        pf.hit_start,
                        pf.hit_end,
                        pf.score,
                        pf.evalue,
                        pf.perc_ident
                    FROM
                        protein_feature pf JOIN
                        translation_stable_id tsi using (translation_id) JOIN
                        analysis an using (analysis_id)

            """

    logger.debug("  Retrieving protein_features match data from Ensembl database for %s..." % species)
    cursor = mysql_dbh.cursor()
    cursor.execute(db_str)
    cnt_all_matches = 0

    #   Some protein_features are never: only save referenced protein_features
    referenced_protein_features = dict()


    for (

            feature_type,
            prot_id,
            hit_name,
            seq_beg, seq_end,
            hit_beg, hit_end,
            score, evalue, perc_ident) in cursor:

        cnt_all_matches += 1

        if cnt_all_matches % 500000 == 0:
            logger.debug("  %10d.." % cnt_all_matches)


        #
        #   save hittype detail
        #
        if hit_name in protein_features:
            protein_features[hit_name].feature_type = feature_type
            referenced_protein_features[hit_name] = protein_features[hit_name]

        #
        #   save hit loci
        #
        matches_by_type[feature_type][prot_id].append(t_protein_feature_match(
                                                                        seq_beg,
                                                                        seq_end,
                                                                        score,
                                                                        evalue,
                                                                        perc_ident,
                                                                        hit_beg,
                                                                        hit_end,
                                                                        hit_name))

    end_time = time.time()
    logger.info("  Retrieved %d features from Ensembl database for %s in %ds"
                            % (cnt_all_matches, species, end_time - start_time))
    #   Some protein_features are never: only save referenced protein_features
    protein_features = referenced_protein_features
    return protein_features, matches_by_type







#_____________________________________________________________________________________
#
#   _load_feature_types_from_cache
#_____________________________________________________________________________________
def _load_feature_types_from_cache (cache_file_name, logger):
    """
    Load features from cache file
    """
    try:
        if not os.path.exists(cache_file_name):
            return None

        logger.debug("  Loading feature types from cache")
        data_file = open(cache_file_name, 'rb')

        #
        #   Is file version correct
        #
        latest_version, errmsg = check_cache_file_version (data_file, _FILE_VERSION_MAJ)
        if not latest_version:
            logger.warning(errmsg)
            return None

        #
        #   Ignore feature type data
        #
        cnt_protein_features = marshal.load(data_file)
        for i in range(cnt_protein_features):
            name = marshal.load(data_file)
            t_protein_feature.load(data_file)

        #
        #   Retrieve features by type
        #
        file_pos_by_section = read_directory_of_sections (data_file)
        return sorted(file_pos_by_section.keys(), key = str.lower)


    except:
        raise
        return None

#_____________________________________________________________________________________
#
#   _load_features_from_cache
#_____________________________________________________________________________________
def _load_features_from_cache (cache_file_name, logger, filter_feature_types = None):
    """
    Load features from cache file
    """
    start_time = time.time()
    try:
        if not os.path.exists(cache_file_name):
            logger.warning("The cache file %s does not exist" % cache_file_name)
            return None, None

        logger.debug("  Loading features from cache")
        logger.info("  Loading cache file = %s" % cache_file_name)
        data_file = open(cache_file_name, 'rb')

        #
        #   Is file version correct
        #
        latest_version, errmsg = check_cache_file_version (data_file, _FILE_VERSION_MAJ)
        if not latest_version:
            logger.warning(errmsg)
            return None, None

        #
        #   Retrieve feature type data
        #
        protein_features = dict()
        cnt_protein_features = marshal.load(data_file)
        for i in range(cnt_protein_features):
            name = marshal.load(data_file)
            protein_features[name] = t_protein_feature.load(data_file)

        #
        #   Retrieve features by type
        #
        file_pos_by_section = read_directory_of_sections (data_file)

        #
        #   Read all features if none specified
        #
        if filter_feature_types == None:
            filter_feature_types = file_pos_by_section.keys()


        matches_by_type     = defaultdict(lambda: defaultdict(list))
        cnt_all_matches     = 0

        #
        #   have case-independent matches
        #
        filter_feature_types_lc = map(str.lower, filter_feature_types)
        feature_type_lc_to_orig = dict(zip(map(str.lower, file_pos_by_section.keys()),
                                    file_pos_by_section.keys()))

        for feature_type_lc in filter_feature_types_lc:
            if feature_type_lc not in feature_type_lc_to_orig:
                continue
            feature_type = feature_type_lc_to_orig[feature_type_lc]

            data_file.seek(file_pos_by_section[feature_type], os.SEEK_SET)

            #
            #   read feature
            #
            #
            cnt_prot_ids = marshal.load(data_file)
            for i in xrange(cnt_prot_ids):
                prot_id      = marshal.load(data_file)
                cnt_matches = marshal.load(data_file)
                for i in range(cnt_matches):
                    matches_by_type[feature_type][prot_id].append(t_protein_feature_match.load(data_file))

            cnt_all_matches += cnt_matches

        #
        #   log what features have been read?
        #
        end_time = time.time()
        logger.info("  Loaded %d features in %ds" % (cnt_all_matches,  end_time - start_time))

        return protein_features, matches_by_type
    except:
        raise
        return None, None

#_____________________________________________________________________________________
#
#   _save_to_cache
#_____________________________________________________________________________________

def _save_to_cache (protein_features, matches_by_type, cache_file_name, logger):
    """
    Save features to cache file
    """

    data_file = _prepare_cache_file (cache_file_name, logger, _FILE_VERSION_MAJ, "protein features")
    start_time = time.time()

    #
    #   Save feature type first
    #
    marshal.dump(len(protein_features.keys()), data_file)
    for name, data in protein_features.items():
        marshal.dump(name, data_file)
        data.dump(data_file)



    #
    #   save "directory" recording where features of each type are in the files so we
    #       can jump directly to that type
    section_name_directory_entry_pos = write_directory_of_sections(data_file, matches_by_type.keys())

    #
    #   save actual data for each feature_type in a separate section
    #
    file_pos_by_section = {}
    for feature_type in matches_by_type.keys():

        # remember where this section begins
        file_pos_by_section[feature_type] = data_file.tell()

        #
        #   dump features for each prot_id
        #
        marshal.dump(len(matches_by_type[feature_type]), data_file)
        for prot_id, features in matches_by_type[feature_type].iteritems():
            marshal.dump(prot_id, data_file)
            marshal.dump(len(features), data_file)
            for feature in features:
                feature.dump(data_file)


    #
    #   go back and write section starts in the directory
    #
    fill_directory_of_sections(data_file, section_name_directory_entry_pos, file_pos_by_section)


    end_time = time.time()
    logger.info("  Cached in %ds" % (end_time - start_time))





#_____________________________________________________________________________________
#
#   get_core_protein_features
#_____________________________________________________________________________________
def get_core_protein_features(index_file_name, species, logger, ensembl_version = None, filter_feature_types = None):
    """
    Get protein features of a specified species and version
    """

    #
    #   look up cache file name from index
    #
    (   cache_file_name,
        ensembl_version,
        db_version_str) = lookup_core_cache_file_name(index_file_name, species, logger, ensembl_version)

    if cache_file_name == None:
        return None, None, None, None, None,

    logger.info("%s: Loading protein features from version %d (%s)" % (species,
                                                                        ensembl_version,
                                                                        db_version_str))
    protein_features, matches_by_type = _load_features_from_cache (cache_file_name, logger, filter_feature_types)

    return protein_features, matches_by_type, ensembl_version, db_version_str, cache_file_name


#_____________________________________________________________________________________
#
#   get_core_protein_feature_types
#_____________________________________________________________________________________
def get_core_protein_feature_types(index_file_name, species, logger, ensembl_version = None):
    """
    Get protein features of a specified species and version
    """

    #
    #   look up cache file name from index
    #
    (   cache_file_name,
        ensembl_version,
        db_version_str) = lookup_core_cache_file_name(index_file_name, species, logger, ensembl_version)

    if cache_file_name == None:
        return None, None, None

    logger.info("%s: Loading protein feature types from version %d (%s)" % (species,
                                                                        ensembl_version,
                                                                        db_version_str))
    logger.debug("11")
    protein_feature_types = _load_feature_types_from_cache (cache_file_name, logger)

    return protein_feature_types, ensembl_version, db_version_str




#_____________________________________________________________________________________
#
#   _write_to_cache
#_____________________________________________________________________________________
def _write_to_cache(mysql_dbh, species, db_name, cache_file_name, logger):
    """
    Download data from database and write to cache file
    """

    # download from database and write to cache file
    protein_features, matches_by_type = _retrieve_mysql_data (mysql_dbh, species, db_name, logger)
    _save_to_cache (protein_features, matches_by_type, cache_file_name, logger)

    log_core_protein_features (logger, protein_features, matches_by_type)


#_____________________________________________________________________________________
#
#   cache_core_protein_features
#_____________________________________________________________________________________
def cache_core_protein_features(mysql_dbh, index_file_name, cache_file_directory, logger, desired_species = None, ensembl_versions = None, discard_cache = False):
    """
    cache all specified species and versions from an Ensembl database
    ensembl_version can be None (==latest version), a number, or a list of numbers
    desired_species can be None (==all species), a string, or a list of strings
    """

    cache_specified_core_data(mysql_dbh, index_file_name, cache_file_directory, logger,
                                  _FILE_VERSION_MAJ, "{db_name}.protein_features.cache", _write_to_cache,
                                  desired_species, ensembl_versions, discard_cache)


#_____________________________________________________________________________________
#
#   log_core_protein_features
#_____________________________________________________________________________________
def log_core_protein_features (logger, protein_features, matches_by_type):
    """
    Log some summary statistics about the different sort of protein features and their matches
    """
    if protein_features:
        # summarise by feature_type
        cnt_features_by_types = defaultdict(int)
        for feature in protein_features.itervalues():
            cnt_features_by_types[feature.feature_type] += 1

        logger.log(MESSAGE, "  Types of protein features with InterPro information:")
        for feature_type, cnt in sorted(cnt_features_by_types.items(), key= lambda a: a[0].lower()):
            logger.log(MESSAGE, "    Feature type %-13s contained %7d different features" %
                            (feature_type, cnt))

    #
    # Count the different types of genes
    #
    if matches_by_type:
        logger.log(MESSAGE, "  Proteins with matches:")
        for feature_type in sorted(matches_by_type.keys(), key= str.lower):
            cnt_prot_ids = len(matches_by_type[feature_type].keys())
            cnt_features = sum(len(features) for features in matches_by_type[feature_type].itervalues())

            logger.log(MESSAGE, "    Feature type %-13s was found in %6d proteins with %7d matches" %
                            (feature_type, cnt_prot_ids, cnt_features))


