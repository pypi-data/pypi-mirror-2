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
                    lookup_core_cache_file_name
                        )
from marshalable_object import marshalable_object, load_dict_of_object_lists, dump_dict_of_object_lists, load_dict_of_objects, dump_dict_of_objects
from collections import namedtuple
import sqlite3
import tempfile

import compara_orthology
from compara_orthology import *

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
    setup_std_logging(logger, "me.log", True)


    from general import *
    mysql_dbh = connect_ensembl_mysql()

    cursor = mysql_dbh.cursor()
    cursor.execute("use ensembl_compara_58")
    taxon_id_to_name_and_assembly       = compara_orthology._retrieve_species_name_and_assembly (cursor, logger)    



    converting_species = "Anolis carolinensis", "Ailuropoda melanoleuca", "Branchiostoma floridae", "Canis familiaris", "Danio rerio", "Equus caballus", "Gasterosteus aculeatus", "Gallus gallus", "Homo sapiens", "Monodelphis domestica", "Mus musculus", "Macaca mulatta", "Nematostella vectensis", "Ornithorhynchus anatinus", "Oryzias latipes", "Petromyzon marinus", "Rattus norvegicus", "Strongylocentrotus purpuratus", "Taeniopygia guttata", "Tetraodon nigroviridis", "Xenopus tropicalis"


    taxon_ids = []
    taxon_id_to_species_name = dict()
    for s in  converting_species:
        for t in taxon_id_to_name_and_assembly.values():
            if s == t.scientific_name:
                taxon_ids.append(t.taxon_id)
                taxon_id_to_species_name[t.taxon_id] = s.replace(' ', '_')
                break
        else:
            logger.warning("No orthology_data for species %s" % s)

    taxon_id_pairs = []
    species_name_pairs = []
    for t in taxon_ids:
        for tt in taxon_ids:
            if t < tt:
                taxon_id_pairs.append((t, tt))
                species_name_pairs.append((taxon_id_to_species_name[t], taxon_id_to_species_name[tt]))



    for taxon_id_pair, species_name_pair in zip(taxon_id_pairs, species_name_pairs):
        (ortholog_sets,
        ortholog_set_pairwise_scores,
        ortholog_set_pairwise_alignment,
        ensembl_version, cache_file_name) = compara_orthology.get_compara_orthology_for_taxon_ids("me.index", logger, taxon_id_pair, None, data_to_load = "ortholog_sets")
        compara_orthology.log_compara_orthology (logger, taxon_id_pair, species_name_pair, ortholog_sets, ortholog_set_pairwise_scores, ortholog_set_pairwise_alignment)

        #
        #   empty set
        #
        if not len(ortholog_sets):
            continue

        orthologs_file = open("try/%s_%s.orthologs" % species_name_pair, "w")

        #
        #   Count genes for each ortholog set and place in category
        #
        for ortholog_set in ortholog_sets.itervalues():
            gene_cnts = [len(ortholog_set.gene_ids[t]) for t in taxon_id_pair]
            if gene_cnts != [1, 1]:
                continue
            orthologs_file.write("%s\t%s\n" %
                                 (ortholog_set.gene_ids[taxon_id_pair[0]][0],
                                 ortholog_set.gene_ids[taxon_id_pair[1]][0]))







