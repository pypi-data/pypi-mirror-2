'''
.. module:: graph
    :synopsis: Utility functions used for preprocessing graphs.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import struqtural.utilities as util

from itertools import product
from collections import deque
from operator import itemgetter


#==============================================================================
#                                 Constants
#==============================================================================


START = "start"
END = "end"
ID = "id"
START_PREFIX = START + "_"
END_PREFIX = END + "_"



#==============================================================================
#                                 Functions
#==============================================================================


def get_node_properties(nodes):
    '''
    Returns a list of node properties dictionaries with related node
    identifiers included.  These dictionaries provide sufficient information
    to generate the requisite database tables.
    
    :param nodes:  The nodes to process, as returned by a by a call to the
        nodes method of a networkx Graph or DiGraph with the data argument set
        to True.  This is equivalent to an iterable of (node, property_dict)
        tuples.
        
    :returns: A closure over all node properties observed in the graph.
    '''
    def node_properties(node):
        properties = node[1]
        properties[ID] = node[0]
        return properties
    return [node_properties(n) for n in nodes]


@util.mutable_sequences("node_keys")
def get_edge_properties(edges, node_keys=ID):
    '''
    Returns a list of edge properties dictionaries with related node
    identifiers included.  These dictionaries provide sufficient information
    to generate the requisite database tables.
    
    :param edges:  The edges to process, as returned by a by a call to the
        edges method of a networkx Graph or DiGraph with the data argument set
        to True.  This is equivalent to an iterable of (start_node, end_node,
        property_dict) tuples.
    
    :param node_keys: The attributes of the start and end nodes which should be
        used to uniquely identify them in the corresponding edge dictionary.
        
    :returns: A closure over all edge properties observed in the graph.
    '''
    def edge_properties(edge):
        properties = edge[2]
        prefixes = (START_PREFIX, END_PREFIX)
        id_properties = product(node_keys, range(2))
        for (k, i) in id_properties:
            properties[prefixes[i] + k] = getattr(edge[i], k, edge[i])
        return properties
    return [edge_properties(e) for e in edges]


def find_roots(graph):
    '''
    Identify all roots, where a root is a node that has no edges that point to
    it.
    
    :param graph: A networkx DiGraph.
    '''
    instances = set(graph.nodes())
    if not instances:
        raise ValueError("graph contains no edges")
    for edge in graph.edges():
        if edge[1] in instances:
            # Remove all nodes that are the child of another node.
            instances.remove(edge[1])
    return instances


def generate_edge_order(graph, roots=None, sort=False):
    '''
    Determine the proper ordering of edges in the graph.  The proper ordering
    is defined as the order in which rows should be created for nodes in the
    nesting table.
    
    :param graph: A networkx DiGraph.
    
    :param roots: the roots of *graph*, if known.
    
    :param sort: should the nodes at each level of the tree be traversed in
        sorted order?
        
    :returns: The set of edges in modified preorder.
    '''
    roots = [(None, r) for r in (roots or find_roots(graph))]
    if sort:
        roots = sorted(roots, key=itemgetter(1), reverse=True)
    edge_queue = deque(roots)
    order = []
    while edge_queue:
        edge = edge_queue.pop()
        node = edge[1]
        neighbors = ((node, n) for n in graph.edge[node])
        if sort:
            neighbors = sorted(neighbors, key=itemgetter(1), reverse=True)
        edge_queue.extend(neighbors)
        order.append(edge)
    return order