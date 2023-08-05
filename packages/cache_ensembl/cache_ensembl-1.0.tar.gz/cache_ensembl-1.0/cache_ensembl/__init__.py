#!/usr/bin/env python
################################################################################
#
#   __init__.py
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

from general import connect_ensembl_mysql, get_core_databases, get_compara_databases
from cache_ensembl_version import __version__
from compara_protein_tree import (
    t_prot_tree_node,
    t_prot_tree_alignment,
    cache_compara_protein_trees,
    get_compara_protein_trees,
    log_compara_protein_trees
    )
from compara_ncbi_taxa import (
    cache_compara_ncbi_taxa,
    get_compara_ncbi_taxa,
    )

from compara_species_pairs import (
    t_species_data,
    cache_compara_species_pairs,
    get_compara_species_pairs,
    log_compara_species_pairs)

from core_protein_features import (
    t_protein_feature_match,
    t_protein_feature,
    link_protein_feature_matches_to_prot_id,
    cache_core_protein_features,
    get_core_protein_features,
    get_core_protein_feature_types,
    log_core_protein_features,
    )

from compara_orthology import (
    t_ortholog_set,
    t_ortholog_set_pairwise_scores,
    t_ortholog_set_pairwise_alignment,
    t_species_data,
    get_gene_ids_to_ortholog_sets,
    get_gene_ids_to_ortholog_sets,
    get_ortholog_sets_by_category,
    cache_compara_orthology,
    get_cached_or_remote_compara_species,
    get_compara_orthology_for_taxon_ids,
    get_compara_orthology_for_species_pair,
    log_compara_orthology,
)
