'''
.. module:: graph
    :synopsis: Nested set, multiply-nested set and standard association list
        representations of trees, directed acyclic graphs and standard graph
        structures.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import networkx as nx
import struqtural.loaders.graph as graph
import struqtural.utilities as util
import struqtural.processes.language as lang

from struqtural.structures.structure import Structure


#==============================================================================
#                                 Constants
#==============================================================================


NODE = "Node"
EDGE = "Edge"
DEFAULT_NAME = "graph"


#==============================================================================
#                                  Classes
#==============================================================================


class NodeSet(Structure):
    '''
    A graph substructure containing node information.
    '''
    
    default_loader = graph.NodeLoader
 
    def __init__(self, nodes, name, *args, **kwargs):
        '''
        '''
        node_class = type(nodes[0][0])
        if util.is_instrumented(node_class):
            properties = graph.InstanceNodeLoader(node_class, *args, **kwargs)
        else:
            loader = kwargs.pop("loader", self.default_loader)
            kwargs["table_name"] = "_".join((name, lang.plural(NODE)))
            properties = loader(nodes, *args, **kwargs)
        super(NodeSet, self).__init__(properties)


class EdgeSet(Structure):
    '''
    A graph substructure containing edge information.
    '''

    default_loader = graph.EdgeLoader
    
    def __init__(self, edges, node_structure, name, *args, **kwargs):
        loader = kwargs.pop("loader", self.default_loader)
        kwargs["table_name"] = "_".join((name, lang.plural(EDGE)))
        properties = loader(edges, node_structure, *args, **kwargs)
        super(EdgeSet, self).__init__(properties)


def matches(columns1, columns2, criteria=None):
    '''
    Generates a query criteria specifying that every column in *columns1*
    matches the corresponding column in *columns2*.  If *criteria* is
    specified, adds these criterion to it generatively.
    '''
    columns = zip(columns1, columns2)
    for (column1, column2) in columns:
        if criteria is None:
            criteria = column1 == column2
        else:
            criteria &= column1 == column2
    return criteria


class Graph(object):
    '''
    A standard graph.  Can represent a directed or undirected graph.
    '''

    @util.mutable_mappings("node_args", "edge_args")
    def __init__(self, graph_, node_args=None, edge_args=None):
        self.name = graph_.name or DEFAULT_NAME
        self.Nodes = NodeSet(graph_.nodes(data=True), self.name, **node_args)
        self.Edges = EdgeSet(graph_.edges(data=True), self.Nodes, self.name,
                             **edge_args)
    
    def _get_node(self):
        '''
        The :class:`NodeSet` substructure of this Graph.
        '''
        return self.Nodes.Instance
    
    def _set_node(self, node):
        self.Nodes.Instance = node
    
    def _get_edge(self):
        '''
        The :class:`EdgeSet` substructure of this graph.
        '''
        return self.Edges.Instance
    
    def _set_edge(self, edge):
        self.Edges.Instance = edge
    
    Node = property(_get_node, _set_node)
    
    Edge = property(_get_edge, _set_edge)
    
    def query(self, *args):
        '''
        Identical to the query method on
        :class:`struqtural.structures.structure.Structure`, with node as the
        default query instance.
        '''
        return self.Nodes.query(*args)
    
    # This is slightly hackish.  A single query should suffice to find the set
    # of all siblings of a node, however my skill with sqlalchemy is not yet
    # sufficient to produce such a beast.
    def siblings(self, node):
        '''
        Given a node, identify all other nodes in the graph which share at
        least one parent in common.
        '''
        end = self.Edges.properties.END
        start = self.Edges.properties.START
        # First, get all the edges pointing to node.
        node_keys = self.Nodes.primary_keys
        node_columns = [getattr(self.Node, c) for c in node_keys]
        node_values = lambda n: [getattr(n, c) for c in node_keys]
        edge_end = ["_".join((end, k)) for k in node_keys]
        edge_start = ["_".join((start, k)) for k in node_keys]
        end_columns = [getattr(self.Edge, c) for c in edge_end]
        start_columns = [getattr(self.Edge, c) for c in edge_start]
        is_end_node = matches(end_columns, node_columns)
        is_start_node = matches(start_columns, node_columns)
        points_to_node = matches(end_columns, node_values(node))
        query = self.query().filter(is_start_node)
        query = query.filter(points_to_node)
        nodes = query.all()
        if nodes:
            criteria = None
            for node_ in nodes:
                if criteria is None:
                    criteria = matches(start_columns, node_values(node_))
                else:
                    criteria |= matches(start_columns, node_values(node_))
            query = self.query().filter(criteria).filter(is_end_node)
            for (column, value) in zip(node_columns, node_values(node)):
                query = query.filter(value != column)
        return query
        # Next, get all the nodes with an edge pointing to node
        

class DirectedAcyclicGraph(Graph):
    '''
    In a directed acyclic graph, a node may have any number of parents or
    children, however there must be no way to traverse the graph such that it
    is possible to go from a child of a node back to the node.
    '''
    
    default_loader = graph.DirectedAcyclicGraphLoader

    @util.mutable_mappings("nesting_args")
    def __init__(self, graph_, *args, **kwargs):
        nesting_loader = kwargs.pop("nesting_loader", self.default_loader)
        nesting_args = kwargs.pop("nesting_args")
        super(DirectedAcyclicGraph, self).__init__(graph_, *args, **kwargs)
        # It is a little bit wacky that we're taking a graph then rebuilding it
        # almost right away, this is due to minor legacy issues with the
        # nesting loader that will be fixed at some point.
        new_graph = nx.DiGraph()
        new_graph.add_edges_from((e.start, e.end) for e in self.Edges.query())
        # Go ahead and mutate Nodes so things which rely on it can use nesting
        # information. 
        self.Nodes.properties = nesting_loader(new_graph, self.Nodes.connector,
                                               **nesting_args)

    def __iter__(self):
        return iter(self._grouped_query())

    def __len__(self):
        # Use the base node here to get the correct count
        return self.query(self.Nodes.properties.BaseInstance).count()

    def _alternates(self, node):
        '''
        Return all representations of a node in the graph.
        '''
        alts = self.query(self.Node)
        for attribute in self.Nodes.primary_keys:
            attr = lambda x: getattr(x, attribute)
            alts = alts.filter(attr(self.Node) == attr(node))
        return alts

    def _grouped_query(self, query=None):
        '''
        Groups instances in a query by their primary key.
        '''
        if not query:
            query = self.query(self.Node)
        for  attribute in self.Nodes.primary_keys:
            query = query.group_by(getattr(self.Node, attribute))
        return query

    def _excluded_grouped_query(self, node, query=None):
        '''Exclude a node from the query results.'''
        for attribute in self.Nodes.primary_keys:
            a = lambda x: getattr(x, attribute)
            query = query.filter(a(self.Node) != a(node))
            query = query.group_by(a(self.Node))
        return query

    def parents(self, node):
        '''
        Return all nodes that are on the path from any root node to this node.
        '''
        query = self.query(self.Node)
        criteria = None
        for alt in self._alternates(node):
            and_ = self.Node.pre < alt.pre
            and_ &= self.Node.post > alt.post
            if criteria is None:
                criteria = and_
            else:
                criteria |= and_
        query = query.filter(criteria)
        return self._excluded_grouped_query(node, query)

    def children(self, node):
        '''
        Return all nodes that have this node in any of their parent sets.
        '''
        query = self.query(self.Node)
        criteria = None
        for alt in self._alternates(node):
            and_ = self.Node.pre.between(alt.pre, alt.post)
            if criteria is None:
                criteria = and_
            else:
                criteria |= and_
        query = query.filter(criteria)
        return self._excluded_grouped_query(node, query)


class Tree(DirectedAcyclicGraph):
    '''
    A tree is a form of graph where each node has 0 or more child nodes and at
    most 1 parent node.  This implementation of a tree is based on the Joe
    Celko nested sets model.  for more information, see
    http://intelligent-enterprise.informationweek.com/001020/celko.jhtml.
    '''

    default_loader = graph.TreeLoader
        
    def parents(self, node):
        '''
        Return all nodes that are on the path from the root of the tree to this
        node.
        '''
        query = self.query(self.Node)
        query = query.filter(self.Node.pre < node.pre)
        query = query.filter(self.Node.post > node.post)
        for attribute in self.Nodes.primary_keys:
            attr = lambda x: getattr(x, attribute)
            query = query.filter(attr(self.Node) != attr(node))
        return query

    def children(self, node):
        '''
        Return all nodes that have this node in their parent set.
        '''
        query = self.query(self.Node)
        query = query.filter(self.Node.pre > node.pre)
        query = query.filter(self.Node.post < node.post)
        for attribute in self.Nodes.primary_keys:
            attr = lambda x: getattr(x, attribute)
            query = query.filter(attr(self.Node) != attr(node))
        return query

