#!/usr/bin/env python
################################################################################
#
#   general.py
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

import re, os, struct
from collections import defaultdict
import logging
import logging.handlers

MESSAGE = 15
logging.addLevelName(MESSAGE, "MESSAGE")
#_________________________________________________________________________________________
#
#   connect_ensembl_core_mysql
#
#_________________________________________________________________________________________
def connect_ensembl_mysql (**connection_settings):
    """
    Get connection to Ensembl database
    """
    import MySQLdb
    import MySQLdb.cursors
    default_connection_settings = {'host'       : 'ensembldb.ensembl.org',
                                   'user'       : "anonymous",
                                   'port'       : 5306,
                                   'cursorclass': MySQLdb.cursors.SSCursor}
    default_connection_settings.update(connection_settings)


    return MySQLdb.connect(**default_connection_settings)


#_________________________________________________________________________________________
#
#   get_core_databases
#
#_________________________________________________________________________________________
#   Regular expression to parse species and version numbers from core database name
core_databases_regex = re.compile(r"(.+)_core_(\d+)(.+)")

def get_core_databases (db):
    """
    Get database names per Ensembl version per species scientific name

    Returns a dictionary
    """
    c=db.cursor()
    c.execute("""SHOW DATABASES;""")
    databases = c.fetchall()

    core_db_per_version = defaultdict(dict)
    for db_name, in  databases:
        m = core_databases_regex.search(db_name)
        if not m:
            continue
        species, db_version_str, db_version_extra = m.groups()
        #
        #   integer overall version
        db_version = int(db_version_str)

        #
        #   species
        #
        species = species.capitalize()

        db_version_str += db_version_extra

        core_db_per_version[db_version][species] = [db_name, db_version_str]


    return core_db_per_version


#
#_________________________________________________________________________________________
#
#   get_compara_databases
#
#_________________________________________________________________________________________
#   Regular expression to parse version numbers from compara database name
compara_databases_regex = re.compile(r"ensembl_compara_(\d+)")

def get_compara_databases (dbh):
    """
    Get database names per Ensembl version

    Returns a dictionary
    """
    c=dbh.cursor()
    c.execute("""SHOW DATABASES;""")
    databases = c.fetchall()

    compara_db_per_version = defaultdict(dict)
    for db_name, in  databases:
        m = compara_databases_regex.search(db_name)
        if not m:
            continue
        db_version = int(m.group(1))

        compara_db_per_version[db_version] = db_name


    return compara_db_per_version


#
#   Magic numbers
#
_FILE_MAGIC_NUM = 1234


#
def _prepare_cache_file (cache_file_name, logger, file_version_num, cache_file_data_name):
    """
    open cache file for saving data to
    """
    #
    #   make directory if does not exists
    #
    file_dir = os.path.split(os.path.abspath(cache_file_name))[0]
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    logger.info("  Saving %s data to %s" % (cache_file_data_name, os.path.basename(cache_file_name)))
    data_file = open(cache_file_name, 'wb', 5)

    #
    #   Write sentinel version number
    #
    data_file.write(struct.pack("q", file_version_num))
    data_file.write(struct.pack("q", _FILE_MAGIC_NUM))

    return data_file


#_____________________________________________________________________________________
#
#   check_cache_file_version
#____________________________________________________________________________________
def check_cache_file_version (data_file, correct_file_version_num):
    """
    Is sentinel version number correct?
    """
    try:
        file_version_num  = struct.unpack("q", data_file.read(8))[0]
        file_magic_num    = struct.unpack("q", data_file.read(8))[0]
        if file_version_num != correct_file_version_num or file_magic_num != _FILE_MAGIC_NUM:
            versions = (file_version_num, file_magic_num, correct_file_version_num, _FILE_MAGIC_NUM)
            return (False, "  Cache file wrong version = %d.%d (should be %d.%d)" % versions)
        return True, None
    except:
        return False, "  Cache file is invalid"


#_____________________________________________________________________________________
#
#   cache_is_valid
#_____________________________________________________________________________________
def cache_is_valid(cache_file_name, logger, file_version_num):
    """
    Check if cache file is valid
    """
    if not os.path.exists(cache_file_name):
        return False

    data_file = open(cache_file_name, 'rb')

    #
    #   Is file version correct
    #
    latest_version, errmsg = check_cache_file_version (data_file, file_version_num)
    if not latest_version:
        logger.warning(errmsg)
        return False

    return True



#_________________________________________________________________________________________
#
#   read_core_index_file
#_________________________________________________________________________________________
def read_core_index_file (index_file_name):
    """
    Reads the index file for caching core database data

    :param index_file_name: Path to the index file
    :type index_file_name: string
    :rtype List of [<db_version> <species> <db_version_str> <cache_file_name>]

    """
    try:
        index_file = open(index_file_name)
    except IOError, (errno, strerror):
        if errno == 2 and "No such file or directory" in strerror:
            raise Exception ("Please save some Ensembl core data before trying to read from the cache!")
        raise

    db_names_per_version_per_species = defaultdict(dict)
    for line in index_file:
        if not len(line) or line[0] == '#':
            continue
        #
        #   fields = <db_version> <species> <db_version_str> <cache_file_name>
        #
        fields = line.rstrip().split("\t")
        if len(fields) != 4:
            continue
        db_version = int(fields[0])
        species, db_version_str, cache_file_name = fields[1:]
        db_names_per_version_per_species[db_version][species] = [db_version_str, cache_file_name]
    return db_names_per_version_per_species


#_________________________________________________________________________________________
#
#   read_compara_index_file
#_________________________________________________________________________________________
def read_compara_index_file (index_file_name):
    """
    Reads the index file for caching compara database data

    :param index_file_name: Path to the index file
    :type index_file_name: string
    :rtype List of [<db_version><data_type><cache_file_name>]

    """
    try:
        index_file = open(index_file_name)
    except IOError, (errno, strerror):
        if errno == 2 and "No such file or directory" in strerror:
            raise Exception ("%s does not exist. " % index_file_name +
                             "Please save some Ensembl compara data before trying to read from the cache!")
        raise

    db_names_per_version = defaultdict(dict)
    for line in index_file:
        if not len(line) or line[0] == '#':
            continue
        #
        #   fields = <db_version> <cache_file_name>
        #
        fields = line.rstrip().split("\t")
        if len(fields) <> 3:
            continue
        db_version = int(fields[0])
        data_type       = fields[1]
        cache_file_name = fields[2]
        db_names_per_version[db_version][data_type] = cache_file_name
    return db_names_per_version


#_____________________________________________________________________________________
#
#   lookup_compara_cache_file_name
#_____________________________________________________________________________________
def lookup_compara_cache_file_name (index_file_name, logger, ensembl_version = None, data_type = None):
    """
    Get cache file name corresponding to a version saved in index

    Returns the cache file name as well as the ensembl version actually used
    """

    db_names_per_version = read_compara_index_file (index_file_name)

    #
    #   Empty index file?
    #
    if len(db_names_per_version) == 0:
        logger.warning("Empty index file %s: No Compara data cached" % index_file_name)
        return None, None


    #
    #   Default to latest version
    #
    if ensembl_version == None:
        ensembl_version = max(db_names_per_version.keys())

    if not ensembl_version in db_names_per_version.keys():
        logger.warning("Ensembl version %s taxa have not been cached." %
                        ensembl_version)
        return None, None

    if data_type not in db_names_per_version[ensembl_version]:
        logger.warning("Data from ensembl compara (%s) v.%s." % (data_type,ensembl_version))
        return None, None



    cache_file_name = db_names_per_version[ensembl_version][data_type]

    return cache_file_name, ensembl_version



#
#_____________________________________________________________________________________
#
#   lookup_core_cache_file_name
#_____________________________________________________________________________________
def lookup_core_cache_file_name (index_file_name, species, logger, ensembl_version = None):
    """
    Get cache file name corresponding to a specified species and version saved in index

    Returns the cache file name as well as the ensembl version / version string actually used
    """

    db_names_per_version_per_species = read_core_index_file (index_file_name)

    #
    #   Empty index file?
    #
    if len(db_names_per_version_per_species) == 0:
        logger.warning("Empty index file %s: No protein features cached" % index_file_name)
        return None, None, None


    #
    #   Default to latest version
    #
    if ensembl_version == None:
        ensembl_version = max(db_names_per_version_per_species.keys())

    if not ensembl_version in db_names_per_version_per_species.keys():
        logger.warning("Ensembl version %s of the protein features has not been cached." %
                        ensembl_version)
        return None, None, None


    if species not in db_names_per_version_per_species[ensembl_version].keys():
        logger.warning(("Ensembl version %s of the protein features "+
                     "has not been cached for this species (%s).")
                        % (ensembl_version, species))
        return None, None, None


    db_version_str, cache_file_name = db_names_per_version_per_species[ensembl_version][species]

    return cache_file_name, ensembl_version, db_version_str



#_____________________________________________________________________________________
#
#   cache_specified_core_data
#_____________________________________________________________________________________
def cache_specified_core_data(mysql_dbh, index_file_name, cache_file_directory, logger,
                              file_version_num, cache_file_name_pattern, cache_write_func,
                              desired_species = None, ensembl_versions = None, discard_cache = False):
    """
    cache all specified species and versions from an Ensembl database
    ensembl_version can be None (==latest version), a number, or a list of numbers
    desired_species can be None (==all species), a string, or a list of strings
    """

    #
    #   get list of database names
    #
    core_db_per_version = get_core_databases (mysql_dbh)

    #
    #   Which version? defaults to latest
    #
    ensembl_versions = _specify_ensembl_versions(core_db_per_version, ensembl_versions)

    #
    #   Which species? defaults to all
    #
    if desired_species == None:
        pass
    elif isinstance(desired_species, basestring):
        desired_species = [desired_species]
    elif isinstance(desired_species, list):
        pass
    else:
        raise Exception("desired_species [%s] should be None or a string, or a list of strings" % desired_species)

    #
    #   make directory if does not exists
    #
    file_dir = os.path.split(index_file_name)[0]
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


    index_file = open(index_file_name, "w")

    for db_version in sorted(ensembl_versions):
        if not db_version in core_db_per_version:
            logger.warning("No ensembl core v.%d database was not found at the server." % db_version)
            continue

        if desired_species == None:
            species_to_cache = sorted(core_db_per_version[db_version].keys())
        else:
            species_to_cache = desired_species

        for species, (db_name, db_version_str) in core_db_per_version[db_version].items():
            if not species in species_to_cache:
                logger.warning("The v.%d core database for %s was not found at the server." %
                               (db_version, species))
                continue

            cache_file_name = os.path.join(cache_file_directory,
                                           cache_file_name_pattern.format(db_name   = db_name))

            #
            #   only re-cache if necessary
            #
            if discard_cache or not cache_is_valid(cache_file_name, logger, file_version_num):


                cache_write_func(mysql_dbh, species, db_name, cache_file_name, logger)
            else:
                logger.log(MESSAGE, "  Core cache file for %s v.%d is already up to date." %
                                            (species, db_version))

            # write to index file

            index_file.write("\t".join([str(db_version), species, db_version_str, cache_file_name])+ "\n")
            index_file.flush()
    index_file.close()


#_____________________________________________________________________________________
#
#   _specify_ensembl_versions
#_____________________________________________________________________________________
def _specify_ensembl_versions(ensembl_db_per_version, ensembl_versions):
    """
    Helper function to return latest or specified ensembl version
    """
    if ensembl_versions == None:
        ensembl_versions = [max(ensembl_db_per_version.keys())]
    elif isinstance(ensembl_versions, basestring):
        ensembl_versions = [int(ensembl_versions)]
    elif isinstance(ensembl_versions, int):
        ensembl_versions = [ensembl_versions]
    elif isinstance(ensembl_versions, list):
        ensembl_versions = [int(d) for d in ensembl_versions]
    else:
        raise Exception("ensembl_versions [%s] should be an integer or a list of integers" % ensembl_versions)

    #
    # Check Ensembl compara versions are correct
    #
    for ev in ensembl_versions:
        if not ev in ensembl_db_per_version:
            raise Exception("Ensembl Database does not contain data for v.%d" % ev)
    return ensembl_versions

#_____________________________________________________________________________________
#
#   get_missing_cache_file_names
#
#_____________________________________________________________________________________
def get_missing_cache_file_names (ensembl_db_per_version, data_names,
                                  cache_file_directory, cache_file_name_pattern, file_version_num,
                                  logger, ensembl_versions = None,
                                  discard_cache = False, check_cache_valid_func = None):
    """
    Returns a list of missing cache files
    """
    missing_cache_file_names = []
    uptodate_cache_file_names = []


    for db_version in sorted(ensembl_db_per_version.keys()):
        if not db_version in ensembl_versions:
            continue

        db_name = ensembl_db_per_version[db_version]

        for data_name in data_names:

            cache_file_name = os.path.join(cache_file_directory,
                                           cache_file_name_pattern.format(db_name   = db_name,
                                                                          data_name = data_name))
            #
            #   only re-cache if necessary
            #
            if not discard_cache:

                #
                #   use custom func to check validity
                #
                #       needs to be passed as :
                #           check_cache_valid_func = {'data1':check_func1, 'data2':check_func2}
                #
                if (check_cache_valid_func and data_name in check_cache_valid_func):

                    if check_cache_valid_func[data_name](cache_file_name, logger):
                        uptodate_cache_file_names.append((db_version, db_name, data_name, cache_file_name))
                        continue
                elif cache_is_valid(cache_file_name, logger, file_version_num):
                    uptodate_cache_file_names.append((db_version, db_name, data_name, cache_file_name))
                    continue
            missing_cache_file_names.append((db_version, db_name, data_name, cache_file_name))

    return missing_cache_file_names, uptodate_cache_file_names

#_____________________________________________________________________________________
#
#   cache_specified_compara_data
#_____________________________________________________________________________________
def cache_specified_compara_data(mysql_dbh, index_file_name, cache_file_directory, logger,
                                 file_version_num,
                                 cache_file_name_pattern, data_names, cache_write_func,
                                 ensembl_versions = None, discard_cache = False,
                                 check_cache_valid_func = None,
                                 **extra_param):
    """
    cache all specified versions from an Ensembl database
    ensembl_version can be None (==latest version), a number, or a list of numbers
    """

    #
    #   get list of database names
    #
    compara_db_per_version = get_compara_databases (mysql_dbh)

    ensembl_versions = _specify_ensembl_versions(compara_db_per_version, ensembl_versions)

    missing_cache_file_names, uptodate_cache_file_names = \
            get_missing_cache_file_names (compara_db_per_version, data_names,
                                          cache_file_directory, cache_file_name_pattern, file_version_num,
                                          logger, ensembl_versions,
                                          discard_cache, check_cache_valid_func)

    #
    #   make index directory if does not exists
    #
    file_dir = os.path.split(os.path.abspath(index_file_name))[0]
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    index_file = open(index_file_name, "w")


    for db_version, db_name, data_name, cache_file_name in uptodate_cache_file_names:
        logger.log(MESSAGE, "  Compara cache file for %s %s is already up to date." %
                                                        (db_name, data_name))
        # write to index file
        index_file.write("%d\t%s\t%s\n" % (db_version, data_name, cache_file_name))
    index_file.flush()


    # download from database and write to cache file
    for db_version, db_name, data_name, cache_file_name in missing_cache_file_names:
        cache_write_func(mysql_dbh, data_name, db_name, cache_file_name, logger,
                         **extra_param)


        # write to index file
        index_file.write("%d\t%s\t%s\n" % (db_version, data_name, cache_file_name))
        index_file.flush()


    index_file.close()





