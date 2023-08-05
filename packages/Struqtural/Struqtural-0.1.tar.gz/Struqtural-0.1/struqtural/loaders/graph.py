'''
.. module:: graph
    :synopsis: Loader subclasses which handle loading data from graphs.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import struqtural.utilities as util
import struqtural.processes.language as lang
import struqtural.processes.graph as graph
import struqtural.loaders.loader as loader
import struqtural.database as db

from itertools import count


TREE = "tree"
DAG = "directed_acyclic_graph"


#==============================================================================
#                                  Classes
#==============================================================================


class GraphMixin(object):
    '''
    Doesn't currently do a whole lot.  Will do more in the future when
    GraphQuery and other niceties have been properly implemented.
    '''
    
    default_query = db.GraphQuery


class NestingMixin(object):
    '''
    This represents a constituent in a directed graphical data structure
    (either a nested or partially ordered set).  Although normal Instances
    are capable of representing such structures through an adjacency list
    model, NestedInstances provide join-free parent, child and sibling
    queries.
    
    .. attribute:: parent
        
        ..
        
        |    This node's parent in the data structure.
    
    .. attribute:: pre
        
        ..
        
        |    The start of this node's descendant space.
    
    .. attribute:: post
        
        ..
        
        |    The end of this node's descendant space.
    '''

    def __init__(self, instance, parent=None):
        super(NestingMixin, self).__init__()
#        self._parent = None
        self.pre = None
        self.post = None
        # Note that the nesting mixin is intended to be applied to instances.
        for attribute in self.__attributes__:
            attribute_value = getattr(instance, attribute)
            setattr(self, attribute, attribute_value)
        self.parent = parent


class NestingMixinWithID(NestingMixin):
    '''
    This Instance is used with databases that do not support auto-incrementing
    integer columns as part of a compound primary key.
    '''

    _id_generator = count(1).next
    id_name = None

    def __init__(self, instance, parent=None):
        setattr(self, self.id_name, self._id_generator())
        super(NestingMixinWithID, self).__init__(instance, parent)


class InstanceNodeLoader(GraphMixin, loader.InstanceLoader):
    '''
    Nothing special here other than the combination of base classes.
    '''


class NodeLoader(GraphMixin, loader.CollectionLoader):
    '''
    Determines a closure on the set of properties for a group of nodes and
    creates a set of mappings to accommodate it.
    '''

    instance_name = "Node"
    _primary_keys = "id"
    
    def __init__(self, nodes, **kwargs):
        data = graph.get_node_properties(nodes)
        super(NodeLoader, self).__init__(data, self._primary_keys,
                                         self.instance_name, **kwargs)


class EdgeLoader(GraphMixin, loader.CollectionLoader):
    '''
    Determines a closure on the set of properties for a group of edges and
    creates a set of mappings to accommodate it, then proceeds to build
    relationships between the loaded edges and the nodes they reference.
    '''
    
    instance_name = "Edge"
    START = "start"
    END = "end"
    
    def __init__(self, edges, node_structure, **kwargs):
        # Pull what we need out of the NodeSet to tie them together
        Node = node_structure.Instance
        to_keys = node_structure.primary_keys
        relationship_args = kwargs.pop("relationship_args", {})
        get_id = lambda x: ["_".join((x, k)) for k in to_keys]
        sid = get_id(self.START)
        eid = get_id(self.END)
        connector = node_structure.connector
        data = graph.get_edge_properties(edges, to_keys)
        super(EdgeLoader, self).__init__(data, sid + eid,
                                         self.instance_name, connector,
                                         **kwargs)
        db.relationship(Node, self.Instance, graph.START, to_keys, sid,
                        **relationship_args) 
        db.relationship(Node, self.Instance, graph.END, to_keys, eid,
                        **relationship_args)


class TreeCreator(object):
    '''
    Used to generate and map NestedInstances.
    
    .. attribute:: extension
        
        ..
        
        |    The mapper extension used by this creator.
    '''

    NAME_PRE = "tree"
    PARENT_PRE = "parent"
    extension = db.TreeExtension
    nesting_mixin = NestingMixin

    def __new__(cls, *args, **kwargs):
        return cls.create(*args, **kwargs)

    @classmethod
    @util.defaults("factory")
    @util.mutable_mappings("mapper_args")
    def create(cls, ordered_edges, connector, join_columns=None, name=None,
               factory=None, mapper_args=None):
        '''
        Creates a partial ordering table from the information contained in
        *ordered_edges*, produces a join condition between that table and the
        table mapped to the Instance in ordered_edges and maps it to a
        NestedInstance.
        
        :param ordered_edges: an iterable of (Instance, Instance) tuples,
            representing directed edges from start node to end node in a tree.
            Root nodes are presented in the form (None, Instance).
        
        :param connector: The DatabaseConnector to use.
        
        :param join_columns: The columns to use for the primary join condition
            of the relationship between Instance and NestedInstance.
        
        :param name: The name to give the created nesting table.
        
        :param table_args:  Allows you to specify additional keyword arguments
            which should be passed when instantiating the sqlalchemy table.
        
        :param mapper_args:  Allows you to specify additional keyword arguments
            which should be passed when creating the object-relational mapping.
        '''
        class_ = type(ordered_edges[0][1])
        table = db.get_table(class_)
        name = name or "_".join((cls.NAME_PRE, table.name))
        join_columns = cls.generate_join_columns(table, join_columns)
        join_column_names = [c.name for c in join_columns]
        nesting_table = cls.nesting_table(name, table.metadata, join_columns)
        NestedInstance = factory(join_column_names, cls.nesting_mixin)
        mapper_args["batch"] = False
        mapper_args["extension"] = cls.create_extension(join_column_names)
        db.map_(NestedInstance, nesting_table, **mapper_args)
        nesting_table.create()
        available_parents = {}
        nested = []
        for (p, i) in ordered_edges:
            if p in available_parents:
                p = available_parents[p]
            instance_ = NestedInstance(i, p)
            available_parents[i] = instance_
            nested.append(instance_)
        connector.session.add_all(nested)
        join_condition = dict((c.name, c.name) for c in join_columns)
        return db.join_sequence(class_, (NestedInstance, join_condition),
                                mapper_args)

    @classmethod
    def create_extension(cls, columns):
        '''
        Creates the nesting table's mapper extension.
        '''
        return cls.extension(columns)

    @staticmethod
    def generate_join_columns(table, columns=None):
        '''
        Generates the sqlalchemy columns that will be used in the join
        condition between the nesting table and the instance table.
        '''
        if not columns:
            columns = table.primary_key
        try:
            return [c.copy() for c in columns]
        except TypeError:
            return [columns.copy()]
        
    @staticmethod
    def nesting_table(*args, **kwargs):
        '''
        Creates the nesting table.
        '''
        return db.tree_table(*args, **kwargs) 


class DirectedAcyclicGraphCreator(TreeCreator):
    '''
    Used to generate and map NestedInstances
    '''

    NAME_PRE = "directed_acyclic"
    extension = db.DirectedAcyclicGraphExtension

    @classmethod
    def create(cls, ordered_edges, connector, *args, **kwargs):
        '''
        Creates a partial ordering table from the information contained in
        *ordered_edges*, produces a join condition between that table and the
        table mapped to the Instance in ordered_edges and maps it to a
        NestedInstance.
        
        :param ordered_edges: an iterable of (Instance, Instance) tuples,
            representing directed edges from start node to end node in a tree.
            Root nodes are presented in the form (None, Instance).
        
        :param connector: The DatabaseConnector to use.
        
        :param join_columns: The columns to use for the primary join condition
            of the relationship between Instance and NestedInstance.
        
        :param name: The name to give the created nesting table.
        
        :param table_args:  Allows you to specify additional keyword arguments
            which should be passed when instantiating the sqlalchemy table.
        
        :param mapper_args:  Allows you to specify additional keyword arguments
            which should be passed when creating the object-relational mapping.
        '''
        if not connector.engine or connector.engine == 'sqlite':
            # Slightly ugly hack here to work around SQLite's decision not to
            # support auto-incrementing column values in compound primary keys.
            cls.nesting_mixin = NestingMixinWithID
            cls.nesting_mixin.id_name = "_".join((cls.NAME_PRE, "id"))
        parent = super(DirectedAcyclicGraphCreator, cls)
        return parent.create(ordered_edges, connector, *args, **kwargs)

    @classmethod
    def create_extension(cls, columns):
        '''
        Creates the nesting table's mapper extension.
        '''
        return cls.extension(columns + ["_".join((cls.NAME_PRE, "id"))])
    
    @classmethod
    def nesting_table(cls, *args, **kwargs):
        '''
        Creates the nesting table.
        '''
        return db.dag_table(cls.NAME_PRE, *args, **kwargs) 


class DirectedAcyclicGraphLoader(GraphMixin, loader.Loader):
    '''
    Generates a directed acyclic graph table structure based on a modification
    of the nested set pattern. A directed acyclic graph differs from a tree in
    that one node may have multiple parents.  The directed acyclic graph model
    allows for join free queries for all a node's parents or children.  Note
    that this model effectively enumerates all possible paths through the input
    graph, thus if it is very densely connected, the table will explode in size
    if many nodes have more than one parent.
    '''

    _creator = DirectedAcyclicGraphCreator
    _type = DAG
    
    @util.mutable_mappings("mapper_args")
    def __init__(self, graph_, connector=None, join_columns=None, name=None,
                 root=None, query=None, mapper_args=None):
        '''
        :param graph: A networkx DiGraph object with Instance nodes.
        
        :param connector: The DatabaseConnector to use.
        
        :param join_columns: The columns that should be used in the join
            condition between the nesting table and the Instance's table.
        
        :param name: The name of the nesting table.
        
        :param root: The root node of the graph.  This can usually be
            identified if it is not specified.
        
        :param query:  Allows you to specify a custom sqlalchemy query
            subclass with additional functionality.
        
        :param table_args:  Allows you to specify additional keyword arguments
            which should be passed when instantiating the sqlalchemy table.
        
        :param mapper_args:  Allows you to specify additional keyword arguments
            which should be passed when creating the object-relational mapping.
        '''
        super(DirectedAcyclicGraphLoader, self).__init__(connector, query)
        self.BaseInstance = type(graph_.nodes()[0])
        self.table = db.get_table(self.BaseInstance)
        if not name:
            instance_name = lang.plural(self.BaseInstance.__name__).lower()
            name = "_".join((self._type, instance_name))
        self.name = name
        edges = graph.generate_edge_order(graph_, root, sort=True)
        self.Instance = self._creator(edges, connector, join_columns, name,
                                      **mapper_args)


class TreeLoader(DirectedAcyclicGraphLoader):
    '''
    Generates a hierarchical table structure based on the nested set pattern.
    Based on heavily re-worked code from the sqlalchemy nested set example.
    The NestedSet model allows for join free queries for a node's parents or
    children.
    '''
    
    _creator = TreeCreator
    _type = TREE