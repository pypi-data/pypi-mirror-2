'''
.. module:: loader
    :synopsis: Core Loader classes providing functionality to other loaders.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import collections
import struqtural.basetypes as basetypes
import struqtural.database as db
import struqtural.utilities as util
import struqtural.processes.language as lang
import struqtural.processes.introspection as introspect

from itertools import chain


def get_default_connector(metadata=None):
    '''
    :returns: A new
        :class:`struqtural.database.connector.DatabaseConnector` using
        system and user default settings.
    '''
    return db.DatabaseConnector(metadata=metadata)


#==============================================================================
#                                  Classes
#==============================================================================


class Loader(object):
    '''
    Provides basic initialization and representation functionality and default
    attribute values. 
    
    .. attribute:: default_query
    
        ..
    
        |    The Query class to provide to referencing structures
        |    if none is specified at initialization time.
        
    .. attribute:: default_connector
    
        ..
    
        |    The DatabaseConnector to use if
        |    none is specified at initialization time.
        
    .. attribute:: attributes
    
        ..
 
        |    The names of the attributes which should be displayed when the
        |    class's __repr__ method is called.
    '''
    
    attributes = ("Instance", "Query", "table", "connector")
    default_query = db.Query

    def __init__(self, connector=None, query=None, connector_metadata=None):
        '''
        :param connector: The
            :class:`struqtural.database.connector.DatabaseConnector` to use.
        
        :param query: The :class:`sqlalchemy.orm.Query` to provide to
            referencing structures
            
        :param connector_metadata: The :class:`sqlalchemy.schema.MetaData` that
            should be bound to the
            :class:`struqtural.database.connector.DatabaseConnector` for this
            loader.
        
        :param instance_name: instance name
        '''
        self.connector = connector or get_default_connector(connector_metadata)
        self.connector.connect(metadata=connector_metadata)
        self.Query = query or self.default_query
    
    def __repr__(self):
        template = "{0}={1}"
        value = lambda x: template.format(x, getattr(self, x))
        values = ", ".join(value(a) for a in self.attributes)
        return "{0}({1})".format(type(self).__name__, values)
   
    @util.mutable_sequences("data")
    def process_data(self, data=None):
        '''
        Convert the data passed to the loader to a format suitable for
        consumption.
        '''
        if not data:
            data = collections.namedtuple("Item", "")
        elif all(isinstance(d, collections.Mapping) for d in data):
            data = util.dicts_to_namedtuples(data)
        elif all(isinstance(d, basestring) for d in data):
            data = collections.namedtuple("Item", data)
        elif all(isinstance(d, collections.Sequence) for d in data):
            if not hasattr(data, "_fields"):
                if len(data) == 2 and len(data[0]) == len(data[1][0]):
                    columns = data[0]
                    data = data[1]
                else:
                    columns =  ["v{0}".format(i + 1) for i in range(len(data))]
                item = collections.namedtuple("Item", columns)
                data = [item(*d) for d in data]
        else:
            raise ValueError("unsupported data type.")
        return data


class MultiLoader(object):
    '''
    This handles creating relationships between Instance classes based on
    previously constructed relationship arguments.
    '''
    
    def __init__(self, relationships):
        '''
        :param relationships: A dictionary keyed by a tuple of parent and
            child names, with a list of arguments for that relationship as
            values.
        '''
        for ((parent_key, child_key), args) in relationships.items():
            parent = self.properties[parent_key].Instance
            child = self.properties[child_key].Instance
            if "intermediate_table" in args: 
                data = args["intermediate_table"]
                name = "_".join((parent.__name__, child.__name__,
                                 "association"))
                connector = self.properties[parent_key].connector
                if isinstance(data, collections.Sequence):
                    table = db.infer_schema(data, name, False, connector)
                else:
                    table = data
                args["intermediate_table"] = table
            db.relationship(parent, child, **args)


class CollectionLoader(Loader):
    '''
    This loader should be used when you are trying to instantiate a database
    table from data objects.
    
    .. attribute:: Instance
    
        ..
        
        |    The instance class
    
    .. attribute:: connector
    
        ..
    
        |    The associated connector
        
    .. attribute:: table
        
        ..
        
        |    The associated table.
        
    .. attribute:: default_instance_name
        
        ..
        
        |    The default instance name to use.
    '''

    default_instance_name = None

    @util.defaults("factory")
    def __init__(self, data=None, primary_keys=None, instance_name=None,
                 connector=None, table_name=None, column_types=None,
                 factory=None, query=None, table_args=None):
        '''
        :param data: The data objects to use as the base for the new database
            table.  Any iterable containing objects that fulfill the Sequence
            or Mapping abstract base class requirements will work.  If the
            objects in data are sequences, *columns* must also be specified or
            generic names will be created.
        
        :param columns: If the objects in *data* are sequences, this is used to
            generate column names for the database table.  Names from *columns*
            are assigned to elements of *data* based on index value.  If
            *columns* contains fewer elements than *data*, additional generic
            names will be created.  All additional elements in *columns*
            which are not in *data* are ignored. If *data* contains mappings,
            the created table will have columns generated by the closure of
            all keys found and *columns*.
        
        :param primary_keys: The names of the columns that should be used as
            the primary key in the generated database table.  If primary_keys
            is not specified, an integer id sequence will be created.
        
        :param instance_name: The name of the instance class to create.
        
        :param connector: The
            :class:`struqtural.database.connector.DatabaseConnector` to use.
        
        :param table_name: The name of the table to create in the database.
            If *table_name* is not specified, the lower case plural form of
            *instance_name* is used.
        
        :param column_types: The sqlalchemy data types of the columns.  If
            these are not sqlalchemy types, then a corresponding sqlalchemy
            type is determined automatically.
        
        :param factory:  Allows you to specify an alternate Instance class
            factory. 
        
        :param query: The :class:`sqlalchemy.orm.Query` to provide to
            referencing structures.
        
        :param table_args:  Allows you to specify additional keyword arguments
            which should be passed when instantiating the
            :class:`sqlalchemy.schema.Table`.
        
        :param mapper_args:  Allows you to specify additional keyword arguments
            which should be passed when initializing the
            :class:`sqlalchemy.orm.mapper.Mapper`.
        '''
        super(CollectionLoader, self).__init__(connector, query)
        instance_name = instance_name or self.default_instance_name
        if instance_name and not table_name:
            table_name = lang.plural(instance_name)
        data = self.process_data(data)
        self.table = db.infer_schema(data, table_name, primary_keys,
                                     self.connector, column_types,
                                     table_args=table_args)
        factory_args = {"name":instance_name}
        self.Instance = db.instance_from_table(self.table, factory,
                                               factory_args=factory_args)


class ObjectLoader(Loader):
    '''
    Persists objects with simple attributes.  All collections and objects
    without a standard database mapping are pickled.
    
    .. note::
        This creates persistent copies of the objects, but does not directly
        instrument them.  If you want any changes you make to the objects to
        be persisted, you must query the database for their persisted
        representations.
    '''
    
    @util.defaults("factory")
    @util.sequences("instances")  
    def __init__(self, instances, primary_keys=None, connector=None,
                 table_prefix=None, column_types=None, query=None,
                 factory=None, table_args=None):
        '''
        :param instances: The instance objects to be used as the base for the
            new mapped instances.
            
        :param primary_keys: The primary keys for the new mapped instances.
        
        :param connector: The
            :class:`struqtural.database.connector.DatabaseConnector` to use.
        
        :param table_prefix: The prefix to apply to the instance class name
            for the generated table.
            
        :param column_types: The sqlalchemy data types of the columns.  If
            these are not sqlalchemy types, then a corresponding sqlalchemy
            type is determined automatically.
        
        :param query: The :class:`sqlalchemy.orm.Query` to provide to
            referencing structures.
        
        :param factory:  Allows you to specify an alternate Instance class
            factory. 
        
        :param table_args:  Allows you to specify additional keyword arguments
            which should be passed when instantiating the
            :class:`sqlalchemy.schema.Table`.
        '''
        super(ObjectLoader, self).__init__(connector, query)
        instance_class = type(instances[0])
        instance_name = lang.plural(instance_class.__name__.lower())
        if table_prefix:
            table_name = "_".join((table_prefix, instance_name))
        else:
            table_name = instance_name
        instance_name = instance_name or self.default_instance_name
        data = introspect.instances_to_dicts(instances)
        data = self.process_data(data)
        self.table = db.infer_schema(data, table_name, primary_keys,
                                     self.connector, column_types,
                                     table_args=table_args)
        factory_args = {"bases":instance_class,
                        "name":instance_class.__name__}
        self.Instance = db.instance_from_table(self.table, factory,
                                               factory_args=factory_args)


class DatabaseLoader(Loader):
    '''
    This loader should be used when you are trying to generate instances from a
    pre-existing database table.
    
    .. attribute:: Instance
    
        ..
        
        |    The instance class
    
    .. attribute:: connector
        
        ..
        
        |    The associated connector
        
    .. attribute:: table
        
        ..
        
        |    The associated table.
        
    .. attribute:: default_instance_name
        
        ..
        
        |    The default instance name to use.
    '''

    default_instance_name = None

    @util.defaults("factory")
    @util.mutable_mappings("table_args")
    def __init__(self, table_name, connector=None, instance_name=None,
                 factory=None, query=None, mapper_args=None, table_args=None):
        '''
        :param instance_name: The name of the instance class to create.
        
        :param connector: The :class:
            `struqtural.database.connector.DatabaseConnector` to use.
        
        :param table_name: The name of the table to create in the database.
            If *table_name* is not specified, the lower case plural form of
            *instance_name* is used.
        
        :param column_types: The sqlalchemy data types of the columns.  If
            these are not sqlalchemy types, then a corresponding sqlalchemy
            type is determined automatically. If the length of *column_types*
            is less than the length of columns, it will be ignored and
            automatic type inference will be performed.
        
        :param factory:  Allows you to specify an alternate Instance class
            factory. 
        
        :param query: The :class:`sqlalchemy.orm.Query` to provide to
            referencing structures.
        
        :param table_args:  Allows you to specify additional keyword arguments
            which should be passed when instantiating the
            :class:`sqlalchemy.schema.Table`.
        
        :param mapper_args:  Allows you to specify additional keyword arguments
            which should be passed when initializing the
            :class:`sqlalchemy.orm.mapper.Mapper`.
        '''
        super(DatabaseLoader, self).__init__(connector, query)
        self.table = db.introspect_table(table_name, self.connector,
                                         **table_args)
        factory_args = {"name":instance_name or self.default_instance_name}
        self.Instance = db.instance_from_table(self.table, factory,
                                               mapper_args, factory_args)


class DatabaseMultiLoader(MultiLoader):
    '''
    Loads a table and all tables associated via foreign key relationships,
    then configures relationships between them.
    
    .. attribute: properties
        
        ..
        
        |    A mapping from database table name to ObjectLoader instance.
    '''
    
    @util.mutable_mappings("instance_names", "factories", "queries",
                           "backreferences")
    def __init__(self, table_name, connector=None, instance_names=None,
                 factories=None, queries=None, backref_by_default=False,
                 backreferences=None, mapper_args=None, table_args=None):
        def _get_arguments(table):
            instance_name = instance_names.get(table)
            factory = factories.get(table)
            query = queries.get(table)
            return (instance_name, factory, query, mapper_args, table_args)
        connector = connector or get_default_connector()
        connector.metadata.reflect()
        backref = collections.defaultdict(lambda: backref_by_default)
        backref.update(backreferences)
        self.properties = {}
        relationships = {}
        table_queue = collections.deque()
        all_tables = connector.metadata.sorted_tables
        foreign_key_iterable = (t.foreign_keys for t in all_tables)
        foreign_keys = list(chain.from_iterable(foreign_key_iterable))
        old_table_queue_length = 0
        table_queue.append(connector.metadata.tables[table_name])
        while (len(table_queue) != old_table_queue_length):
            old_table_queue_length = len(table_queue)
            for foreign_key in foreign_keys:
                column_in_queue = foreign_key.column.table in table_queue
                parent_in_queue = foreign_key.parent.table in table_queue
                if column_in_queue and not parent_in_queue:
                    table_queue.append(foreign_key.parent.table)
                elif parent_in_queue and not column_in_queue:
                    table_queue.append(foreign_key.column.table)
        while table_queue:
            table = table_queue.pop()
            foreign_columns = [c for c in table.columns if c.foreign_keys]
            if len(foreign_columns) == len(table.columns):
                foreign_keys = set(chain.from_iterable(c.foreign_keys for c in
                                                       foreign_columns))
                table_set = set(k.column.table for k in foreign_keys)
                referenced_columns = dict((k.parent, k.column) for k in
                                          foreign_keys)
                if len(table_set) == 2:
                    # This is an intermediate table, and does not require any
                    # kind of special treatment to provide many to many
                    # functionality.  To and from are effectively meaningless
                    # as well.
                    (intermediate_to, primary) = referenced_columns.popitem()
                    to = primary.table
                    (intermediate_from, foreign) = referenced_columns.popitem()
                    from_ = foreign.table
                    relationship = {"primary":primary,
                                    "foreign":foreign,
                                    "intermediate_to":intermediate_to,
                                    "intermediate_from":intermediate_from,
                                    "intermediate_table":table}
                    relationships[(to.name, from_.name)] = relationship
                    continue
            for foreign_key in table.foreign_keys:
                from_ = table
                to = foreign_key.column.table
                primary = foreign_key.column
                foreign = foreign_key.parent        
                relationship = {"primary":primary,
                                "foreign":foreign}
                if backref[to]:
                    relationship["backref"] = True
                relationships[(to.name, from_.name)] = relationship
            args = _get_arguments(table.name)
            properties = DatabaseLoader(table.name, connector, *args)
            self.properties[table.name] = properties
        super(DatabaseMultiLoader, self).__init__(relationships)
            

class InstanceLoader(Loader):
    '''
    Creates a new loader based on an existing, mapped instance class.
    '''
    
    def __init__(self, instance_, connector=None, query=None):
        '''
        '''
        metadata = db.get_metadata(instance_)
        super(InstanceLoader, self).__init__(connector, query, metadata)
        self.table = db.get_table(instance_)
        self.Instance = instance_


class JoinLoader(Loader):
    '''
    Creates a new loader based on a set of instances and join conditions.
    '''
    
    @util.defaults("factory")
    def __init__(self, left, *joined, **kwargs):
        '''
        :param left: The left-most table in the series of join conditions.
        
        :param joined: 2 element tuples where the first element is the
            table to join and the second element is either a list if the
            columns to join along share the same name, or a dictionary
            mapping from the name of column in the left table to the name of
            the column in the table being joined.
        
        :param kwargs: Additional keyword arguments which should be passed to
            :func:`struqtural.database.utilities.join_sequence`.
        
        '''
        query = kwargs.pop("query", None)
        joined = list(joined)
        bases = (basetypes.AbstractInstance,
                 basetypes.AbstractLoader,
                 basetypes.AbstractStructure)
        if not util.descendant(left, basetypes.AbstractInstance):
            self.connector = left.connector
            # Since join_sequence uses instances.
            left = left.Instance
        else:
            self.connector = get_default_connector()
            self.connector.connect(metadata=db.get_metadata(left))
        for (index, join) in enumerate(joined):
            if not util.descendant(join, bases):
                # We got a tuple with a join condition, just make sure it is an
                # Instance...
                if not util.descendant(join[0], basetypes.AbstractInstance):
                    joined[index] = (join[0].Instance, join[1])
            else:
                if not util.descendant(join, basetypes.AbstractInstance):
                    join_instance = join.Instance
                # Since we didn't get a join condition, let's try to identify
                # columns common to both left and join_instance.
                common_keys = db.get_common_keys(left, join_instance)
                join_condition = dict((k, k) for k in common_keys)
                joined[index] = (join_instance, join_condition)  
        self.Instance = db.join_sequence(left, joined, **kwargs)
        self.table = db.get_table(self.Instance)
        self.Query = query or self.default_query
