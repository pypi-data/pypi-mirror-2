#! /usr/bin/env python

##############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2010 Jeet Sukumaran and Mark T. Holder.
##  All rights reserved.
##
##  See "LICENSE.txt" for terms and conditions of usage.
##
##  If you use this work or any portion thereof in published work,
##  please cite it as:
##
##     Sukumaran, J. and M. T. Holder. 2010. DendroPy: a Python library
##     for phylogenetic computing. Bioinformatics 26: 1569-1571.
##
##############################################################################

"""
Implementation of NEWICK-schema data reader and writer.
"""
from cStringIO import StringIO
import re

from dendropy.utility import containers
from dendropy.utility import textutils
from dendropy.utility import iosys
from dendropy.dataio import nexustokenizer
from dendropy import dataobject

###############################################################################
## lightweight trees from NEWICK sources

def tree_source_iter(stream, **kwargs):
    """
    Iterates over a NEWICK-formatted source of trees given by file-like object
    `stream`

    Note that if `encode_splits` is True, then a `taxon_set` has to be given.
    This is because adding Taxon objects to a taxon set may invalidate split
    bitmasks. Because NEWICK tree taxa are added to a TaxonSet as they are found
    on a tree, there is a strong possibility that all split bitmasks get
    invalidated in the middle of parsing a tree. To avoid this, and, more
    importantly to avoid errors downstream in client code due to this, we
    force specification of a `taxon_set` if `encode_splits` is requested.

    The following optional keyword arguments are also recognized:

        - `taxon_set`: TaxonSet object to use when reading data
        - `as_rooted=True` (or `as_unrooted=False`): interprets trees as rooted
        - `as_unrooted=True` (or `as_rooted=False`): interprets trees as unrooted
        - `default_as_rooted=True` (or `default_as_unrooted=False`): interprets
           all trees as rooted if rooting not given by `[&R]` or `[&U]` comments
        - `default_as_unrooted=True` (or `default_as_rooted=False`): interprets
           all trees as rooted if rooting not given by `[&R]` or `[&U]` comments
        - `edge_len_type`: specifies the type of the edge lengths (int or float)
        - `encode_splits`: specifies whether or not split bitmasks will be
           calculated and attached to the edges.
        - `store_tree_weights`: if True, process the tree weight ("[&W 1/2]")
           comment associated with each tree, if any.
        - `finish_node_func`: is a function that will be applied to each node
           after it has been constructed.

    """
    if "taxon_set" in kwargs:
        taxon_set = kwargs["taxon_set"]
        del(kwargs["taxon_set"])
    else:
        taxon_set = None
    if "encode_splits" in kwargs and taxon_set is None:
        raise Exception('When encoding splits on trees, a pre-populated TaxonSet instance ' \
            + "must be provided using the 'taxon_set' keyword to avoid taxon/split bitmask values "\
            + "changing as new Taxon objects are added to the set.")
    preserve_underscores = kwargs.get('preserve_underscores', False)
    hyphens_as_tokens = kwargs.get('hyphens_as_tokens', nexustokenizer.DEFAULT_HYPHENS_AS_TOKENS)
    newick_stream = nexustokenizer.NexusTokenizer(stream,
                                                  preserve_underscores=preserve_underscores,
                                                  hyphens_as_tokens=hyphens_as_tokens)
    while not newick_stream.eof:
        t = nexustokenizer.tree_from_token_stream(newick_stream, taxon_set=taxon_set, **kwargs)
        if t is not None:
            yield t
        else:
            raise StopIteration()

###############################################################################
## parse_newick_string
#
# def parse_newick_string(tree_statement, taxon_set=None, **kwargs):
#     "Processes a (SINGLE) TREE statement string."
#     stream_handle = StringIO(tree_statement)
#     stream_tokenizer = NexusTokenizer(stream_handle)
#     tree = nexustokenizer.tree_from_token_stream(stream_tokenizer=stream_tokenizer,
#                                      taxon_set=taxon_set,
#                                      **kwargs)
#     return tree


############################################################################
## CLASS: NewickReader

class NewickReader(iosys.DataReader):
    "Implementation of DataReader for NEWICK files and strings."

    def __init__(self, **kwargs):
        """
        __init__ recognizes the following keywords arguments:

            - `dataset`: all data read from the source will be instantiated as
               objects within this `DataSet` object
            - `taxon_set`: TaxonSet object to use when reading data
            - `as_rooted=True` (or `as_unrooted=False`): interprets trees as rooted
            - `as_unrooted=True` (or `as_rooted=False`): interprets trees as unrooted
            - `default_as_rooted=True` (or `default_as_unrooted=False`): interprets
               all trees as rooted if rooting not given by `[&R]` or `[&U]` comments
            - `default_as_unrooted=True` (or `default_as_rooted=False`): interprets
               all trees as rooted if rooting not given by `[&R]` or `[&U]` comments
            - `edge_len_type`: specifies the type of the edge lengths (int or float)
            - `encode_splits`: specifies whether or not split bitmasks will be
               calculated and attached to the edges.
            - `finish_node_func`: is a function that will be applied to each node
               after it has been constructed.
            - `hyphens_as_tokens`: if True, hyphens will be treated as special
               as special punctuation, as required by the NEXUS standard. If
               False, hyphens will not be treated as special punctuation which
               means that they are allowed in unquoted labels, but this
               violates the NEXUS standard, and will break NEXUS parsing (and
               many in-the-wild NEWICK as well). Default value is given by:
               ``dendropy.dataio.nexustokenizer.DEFAULT_HYPHENS_AS_TOKENS``.
            - `store_tree_weights`: if True, process the tree weight ("[&W 1/2]")
               comment associated with each tree, if any.
        """
        iosys.DataReader.__init__(self, **kwargs)
        self.stream_tokenizer = nexustokenizer.NexusTokenizer()
        self.finish_node_func = kwargs.get("finish_node_func", None)
        self.rooting_interpreter = kwargs.get("rooting_interpreter", nexustokenizer.RootingInterpreter(**kwargs))
        self.hyphens_as_tokens = kwargs.get('hyphens_as_tokens', nexustokenizer.DEFAULT_HYPHENS_AS_TOKENS)
        self.encode_splits = kwargs.get('encode_splits', False)
        self.store_tree_weights = kwargs.get('store_tree_weights', False)
        self.preserve_underscores = kwargs.get('preserve_underscores', False)

    def read(self, stream):
        """
        Instantiates and returns a `DataSet` object based on the
        NEWICK-formatted contents read from the file-like object source
        `stream`.
        """
        if self.exclude_trees:
            return self.dataset
        if self.dataset is None:
            self.dataset = dataobject.DataSet()
        taxon_set = self.get_default_taxon_set()
        tree_list = self.dataset.new_tree_list(taxon_set=taxon_set)
        for t in tree_source_iter(stream=stream,
                taxon_set=taxon_set,
                rooting_interpreter=self.rooting_interpreter,
                hyphens_as_tokens=self.hyphens_as_tokens,
                store_tree_weights=self.store_tree_weights,
                encode_splits=self.encode_splits,
                preserve_underscores=self.preserve_underscores):
            tree_list.append(t, reindex_taxa=False)
        return self.dataset

############################################################################
## CLASS: NewickWriter

class NewickWriter(iosys.DataWriter):
    "Implementation of DataWriter for NEWICK files and strings."

    def __init__(self, **kwargs):
        """
        __init__ recognizes the following keywords (in addition to those of `DataWriter.__init__`):

            - `dataset`: data to be written
            - `edge_lengths` : if False, edges will not write edge lengths [True]
            - `internal_labels` : if False, internal labels will not be written [True]
            - `preserve_spaces` : spaces not mapped to underscores in labels [False]
            - `quote_underscores` : labels with underscores are quoted, for "hard" underscores [True]
            - `store_tree_weights` : tree weights are stored
            - `nhx_key_to_func_dict` : a dict of NHX "key" to a function that takes an edge and returns the string that is the value of the NHX key (or None to omit that key for that edge)
        """
        iosys.DataWriter.__init__(self, **kwargs)
        self.edge_lengths = kwargs.get("edge_lengths", True)
        self.is_write_rooting = kwargs.get("write_rooting", True)
        self.internal_labels = kwargs.get("internal_labels", True)
        self.preserve_spaces = kwargs.get("preserve_spaces", False)
        self.quote_underscores = kwargs.get('quote_underscores', True)
        self.store_tree_weights = kwargs.get("store_tree_weights", False)
        self.nhx_key_to_func = kwargs.get("nhx_key_to_func_dict")

    def write(self, stream):
        """
        Writes attached `DataSource` or `TaxonDomain` to a destination given
        by the file-like object `stream`.
        """

        if self.exclude_trees:
            return

        assert self.dataset is not None, \
            "NewickWriter instance is not attached to a DataSet: no source of data"

        for tree_list in self.dataset.tree_lists:
            if self.attached_taxon_set is None or self.attached_taxon_set is tree_list.taxon_set:
                self.write_tree_list(tree_list, stream)

    def write_tree_list(self, tree_list, stream):
        """
        Writes a `TreeList` in NEWICK schema to `stream`.
        """
        if self.exclude_trees:
            return
        for tree in tree_list:
            if tree.rooting_state_is_undefined or not self.is_write_rooting:
                rooting = ""
            elif tree.is_rooted:
                rooting = "[&R] "
            elif not tree.is_rooted:
                rooting = "[&U] "
            else:
                rooting = ""
            if self.store_tree_weights and tree.weight is not None:
                weight = "[&W %s] " % tree.weight
            else:
                weight = ""
            stream.write("%s%s%s;\n" % (rooting, weight, self.compose_node(tree.seed_node)))

    def compose_tree(self, tree):
        "Convienience method.        "
        return self.compose_node(tree.seed_node)

    def choose_display_tag(self, node):
        """
        Based on current settings, the attributes of a node, and
        whether or not the node is a leaf, returns an appropriate tag.
        """
        if hasattr(node, 'taxon') and node.taxon:
            tag = node.taxon.label
        elif hasattr(node, 'label') and node.label:
            tag = node.label
        elif len(node.child_nodes()) == 0:
            # force label if a leaf node
            tag = node.oid
        else:
            tag = ""
        if tag:
            tag = textutils.escape_nexus_token(tag, preserve_spaces=self.preserve_spaces, quote_underscores=self.quote_underscores)
        return tag

    def compose_node(self, node):
        """
        Given a DendroPy Node, this returns the Node as a NEWICK
        statement according to the class-defined formatting rules.
        """
        child_nodes = node.child_nodes()
        if child_nodes:
            subnodes = [self.compose_node(child) for child in child_nodes]
            statement = '(' + ','.join(subnodes) + ')'
            if self.internal_labels:
                statement = statement + self.choose_display_tag(node)
            if node.edge and node.edge.length != None and self.edge_lengths:
                statement =  "%s:%s" % (statement, node.edge.length)
        else:
            statement = self.choose_display_tag(node)
            if node.edge and node.edge.length != None and self.edge_lengths:
                statement =  "%s:%s" % (statement, node.edge.length)
        if self.nhx_key_to_func:
            nhx_to_print = []
            for k, v in self.nhx_key_to_func.items():
                r = v(node.edge)
                if r is not None:
                    nhx_to_print.append("%s=%s" % (k, str(r)))
            if nhx_to_print:
                statement = statement + ('[&&NHX:%s]' % ':'.join(nhx_to_print))
        return statement
