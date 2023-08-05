'''
.. module:: utilities
    :synopsis: Miscellaneous utility functions related to SQL Alchemy.

.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>

.. data:: TYPE_MAPPINGS

    ..
    
    |    Mapping from Python object types to SQL Alchemy types.
    
.. data:: TYPE_ARGUMENTS

    ..
    
    |    Arguments that should be used when SQL Alchemy types are
    |    instantiated.
'''

import re
import collections
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.sql as sql
import struqtural.utilities as util
import struqtural.processes.typeinference as infer

from operator import itemgetter
from itertools import chain, product


#==============================================================================
#                                 Constants
#==============================================================================


MAX_STRING_LENGTH = 64
ID = "id"
ID_SEQUENCE = "id_sequence"
STRING = "S{0}"
UNICODE = "U{0}"
DOUBLE = "f8"
BOOLEAN = "b"
LONG = "i4"
PRE = "pre"
POST = "post"
KEY = "key"
DEFAULT_STRING_LENGTH = 16
PROPERTIES = "properties"
REMOVED_CHARACTERS = r"[^-.\w\s]"
REPLACED_CHARACTERS = r"[-.\s]+"


#==============================================================================
#                                 Attributes
#==============================================================================


TYPE_MAPPINGS = {'int':sa.Integer, 'float':sa.Float, 'bool':sa.Boolean,
                 'datetime':sa.DateTime, 'date':sa.Date, 'time': sa.Time,
                 'Decimal':sa.Numeric, 'unicode':sa.Unicode, 'str':sa.String}
TYPE_ARGUMENTS = {sa.String:{"length":MAX_STRING_LENGTH},
                  sa.Unicode:{"length":MAX_STRING_LENGTH}}

removed_expr = re.compile(REMOVED_CHARACTERS)
replaced_expr = re.compile(REPLACED_CHARACTERS)

#==============================================================================
#                                 Functions
#==============================================================================


def sql_format(names):
    '''
    Convert one or more strings specified by *names* to values allowed for
    SQL objects such as tables and columns.  This means only alphanumeric
    characters, underscores and whitespace, with no leading or trailing
    whitespace characters.  The replacement of internal whitespace with
    underscores is performed to avoid having difficult to access instance
    properties.
    
    :param names: The string(s) to convert
    
    :returns: the formatted string
    '''
    format_ = lambda n: replaced_expr.sub("_", removed_expr.sub("", n).strip())
    format_all = lambda names_: [format_(n) for n in names_]
    if isinstance(names, basestring):
        results = format_(names)
    elif isinstance(names, collections.Sequence):
        results = format_all(names)
    else:
        raise ValueError("names is not string type or sequence")
    return results


def metadata_from_connector(connector):
    '''
    Returns metadata given a connector object.  If the object happens to be the
    :class:`sqlalchemy.schema.MetaData` instance, that can be returned as is.
    If the connector is not specified, return a new
    :class:`sqlalchemy.schema.MetaData` instance.
    '''
    if connector:
        if isinstance(connector, sa.MetaData):
            metadata = connector
        else:
            metadata = connector.metadata
    else:
        metadata = sa.MetaData()
    return metadata


# @deprecated: No longer has much utility.
@util.mutable_sequences("data")
def generate_column_types(data):
    '''
    Infer the best SQL ALchemy data types of a table on a per column basis.
    
    :param data: the the lists for which SQL Alchemy types should be
        determined.
    
    :returns: the list column types, from :mod:`sqlalchemy.types`
    '''
    types = infer.map_data_types(data, TYPE_MAPPINGS, sa.PickleType,
                                 sa.String(MAX_STRING_LENGTH), sa.PickleType)
    return types


@util.defaults("factory")
@util.mutable_mappings("mapper_args", "factory_args")
def instance_from_table(table, factory=None, mapper_args=None,
                        factory_args=None):
    '''
    Generate an instance class given a :class:`sqlalchemy.schema.Table`
    '''
    column_names = [c.name for c in table.columns]
    Instance = factory(column_names, **factory_args)
    map_(Instance, table, **mapper_args)
    return Instance


def introspect_table(table_name, metadata, **kwargs):
    '''
    Generates a mapped Instance via introspection.  All kwargs are passed
    unmodified to the :class:`sqlalchemy.schema.Table`.
    
    :param table_name: The database table to introspect.
    
    :param metadata: The DatabaseConnector to use.  
    
    :returns: The mapped class.
    '''
    metadata = metadata_from_connector(metadata)
    return sa.Table(table_name, metadata, autoload=True, **kwargs)


@util.sequences("entries")
def insert(table, entries):
    '''
    Insert *entries* into *table* using executemany.
    '''
    if not entries:
        return
    if hasattr(type(entries[0]), "_fields"):
        # namedtuple...
        entries = [e._asdict() for e in entries]
    table.metadata.bind.execute(table.insert(), entries)


def map_(instance, table, **kwargs):
    '''
    Exists to avoid SQL Alchemy imports popping up all over the code base.
    '''
    orm.mapper(instance, table, **kwargs)


def get_table(instance):
    '''
    Takes an Instance, returns its mapped table.
    '''
    return orm.class_mapper(instance).local_table


def get_columns(instance):
    '''
    Takes an instance, return the columns of its mapped table.
    '''
    return get_table(instance).columns


def get_column_names(instance):
    '''
    Takes an instance, return the names of the columns in its mapped table.
    '''
    return list(c.name for c in get_columns(instance))


def primary_key_columns(instance):
    '''
    Takes an instance, return the primary key columns of its mapped table.
    '''
    return list(get_table(instance).primary_key)


def primary_key_names(instance):
    '''
    Takes an instance, return the names of the primary key columns in its
    mapped table.
    '''
    return list(c.name for c in primary_key_columns(instance))


def get_metadata(instance):
    '''
    Convenience method, takes an instance, return the metadata where the
    instance's table is defined.
    '''
    return get_table(instance).metadata


def get_common_keys(one, two):
    '''
    Get all common column keys between two tables.
    '''
    return set(get_column_names(one)).intersection(get_column_names(two))


def configure_alchemy_type(type_, type_mappings=None, type_arguments=None):
    '''
    Returns an SQL Alchemy instance corresponding to a specified type.  If a
    SQL Alchemy type is specified, returns an instance of that type.
    
    :param type_: The type for which the corresponding SQL Alchemy type should
        be returned.
        
    :param type_mappings: A dictionary mapping Python type names to SQL Alchemy
        types.
        
    :param type_arguments: A dictionary mapping SQL Alchemy types to default
        arguments.
        
    :returns: An instance of the SQL Alchemy type with specified arguments.
    '''
    if not type_mappings:
        type_mappings = TYPE_MAPPINGS
    if not type_arguments:
        type_arguments = TYPE_ARGUMENTS 
    if not issubclass(type_, sa.types.AbstractType):
        type_name = type_.__name__
        type_ = TYPE_MAPPINGS.get(type_name, sa.String)
    return type_(**type_arguments.get(type_, {}))


@util.mutable_mappings("table_args")
@util.mutable_sequences("primary_keys")
def infer_schema(data, name=None, primary_keys=None, metadata=None,
                 types=None, missing_value='', table_args=None):
    '''
    This takes a sequence of sequences as input and produces a database table.
    
    :param data: The data objects to use as the base for the new database
        table.  An iterable containing namedtuples or any class fulfilling
        the Mapping abstract base class requirements will work.
        
    :param name: The name of the table that should be created in the
        database. If none is specified, generate a unique table name based
        on the checksum of the data.
    
    :param primary_keys: The names of the columns that should be used as
        the primary key in the generated database table.
    
    :param metadata: The SQL Alchemy metadata or
        :class:`struqtural.database.metadata.DatabaseConnector` to use.
    
    :param types: The SQL Alchemy data types of the columns.  This may be
        either a sequence of the same length as the sequences in *data* or a
        mapping from names specified by columns to types.  If these are not
        SQL Alchemy types, then the corresponding type is determined
        automatically.
    
    :param missing_value: If type inference must be done from strings, the
        value that is equivalent to None.
    
    :param table_args:  Allows you to specify additional keyword arguments
        which should be passed when instantiating the
        :class:`sqlalchemy.schema.Table`.
    '''
    if isinstance(data, collections.Sequence):
        names = util.all_keys(data)
        if all(isinstance(d, collections.Mapping) for d in data):
            # Dictionaries coming in is fine, they need to be converted to
            # named tuples though.
            item = collections.namedtuple("Item", names)
            data = [item(**d) for d in data]
        else:
            item = type(data[0])
        if not types:
            all_elements = chain.from_iterable(data)
            if all(isinstance(e, basestring) for e in all_elements):
                py_types = infer.infer_table_types(data)
                data = infer.strings_to_types(data, py_types, missing_value)
            types = generate_column_types(data)
        elif isinstance(types, collections.Mapping):
            types = item._make(types.get(n) for n in names)    
        else:
            # Types should be some kind of sequence.
            if len(types) != len(names):
                raise ValueError("inconsistent table specification: specified"
                                 "{0} columns and {1} data types"
                                 .format(len(names), len(types)))
            if not hasattr(types, "_fields"):
                # Types needs to be converted to a namedtuple.
                types = item._make(types)
    else:
        # Data had better be the namedtuple class or we're in trouble.
        item = data
        data = None # We don't actually have any data...
        names = item._fields 
        if not types:
            types = item._make(None for c in names) 
    types = item._make(configure_alchemy_type(t) for t in types)
    column_generator = (sa.Column(n, t) for (n, t) in zip(names, types))
    if not name:
        name = infer.unique_name(data)
    columns = configure_primary_keys(column_generator, primary_keys)
    return create_table(name, metadata, data, *columns, **table_args)


@util.mutable_sequences("columns", "primary_keys")
def configure_primary_keys(columns, primary_keys=None):
    '''
    Configures the primary key for a set of columns.  If no primary key is
    specified, one will be created.  If no primary key is desired, a value of
    False may be passed for *primary_keys*.
    
    :param columns: The SQL Alchemy columns which should have their primary
        key configured.
    
    :param primary_keys: The names of the columns which should be used in the
        primary key.  If none are specified and an integer column is defined
        with the name 'id', that column will be promoted to primary
        key status.  If no such column exists, a new integer primary key
        column will be inserted into the table with the name 'id'.  A value
        of False may be passed if no primary key is desired.
    '''
    if all(primary_keys) and not any(c.primary_key for c in columns):
        if primary_keys and all(isinstance(k, basestring) for k in
                                primary_keys):
            # Specific keys were named, so use those.
            primary_keys = sql_format(primary_keys)
            for column in columns:
                if column.name in primary_keys:
                    column.primary_key = True
                    column.nullable = False
        else:
            # We got some non-null value but not a set of usable keys.
            for column in columns:
                # Let's see if we can locate something that LOOKS like a
                # primary key...
                if (column.name == ID and
                    util.descendant(column.type, sa.Integer)):
                    column.primary_key = True
                    column.nullable = False 
                    break
            else:
                # Still no primary key?  Let's create a new column for one.
                sequence = sa.Sequence("generated_id_sequence")
                id_ = sa.Column("id", sa.Integer(), sequence, primary_key=True)
                columns.append(id_)
    return columns


def create_table(name, metadata, data=None, *columns, **kwargs):
    '''
    Utility method for creating SQL Alchemy tables.  Can extract metadata from
    a :class:`struqtural.database.connector.DatabaseConnector` instance and
    will automatically create the table in the database if the specified
    metadata is bound.  Can also automatically populate the table with data.
    Columns and kwargs are passed to the SQL Alchemy table unmodified. 
    
    :param name: The name of the database table to create.
    
    :param metadata: A SQL Alchemy metadata object, or a Struqtural
        DatabaseConnector instance.
    
    :param data: Data to be automatically inserted into the table after it is
        instantiated.
    '''
    metadata = metadata_from_connector(metadata)
    table = sa.Table(name, metadata, *columns, **kwargs)
    if metadata.bind:
        table.create()
        insert(table, data)
    return table


@util.mutable_mappings("functions")
@util.iterables("pivot_columns", "non_pivot_columns", "group_by")
def pivot(selectable, pivot_on, pivot_columns, non_pivot_columns=None,
          group_by=None, default_function=None, functions=None):
    '''
    Produces a pivot table from a given select statement.  A pivot table
    is generated when one or more columns in a source table are converted to
    rows in a new table. Data is aggregated in pivot tables based on unique
    values of the converted columns. 
    
    Very loosely based on:
        www.machine-envy.com/blog/2009/10/30/pivot-tables-with-sqlalchemy/
    
    :param selectable: The selectable object that should be used as input.
    
    :param pivot_on: The columns to convert into rows.
    
    :param pivot_columns: The columns which should be included in aggregate
        form in the pivot table.
    
    :param non_pivot_columns: The columns which should be included without
        aggregation.
    
    :param group_by: The columns which contain values that should be used
        to merge duplicate rows.
    
    :param default_function:  The default row aggregation function.
    
    :param functions: A dictionary of column names to specific aggregation
        functions.
    '''
    default_function = default_function or sql.func.sum
    pivot_on = selectable.columns[pivot_on]
    def new_column(value, column):
        case_statement = sql.case([(pivot_on == value, column)])
        label = "_".join((value, column.name))
        pivot_func = functions.get(column.name, default_function)
        return pivot_func(case_statement).label(label)
    pivot_columns = [selectable.columns[n] for n in pivot_columns]
    non_pivot_columns = [selectable.columns[n] for n in non_pivot_columns]
    group_by = [selectable.columns[n] for n in group_by]
    # find all possible values of the pivot
    selection = sql.select([pivot_on], from_obj=selectable).distinct()
    value = itemgetter(0)
    pivot_values = [value(item) for item in selection.execute()]
    # build the new pivot columns
    pivot_axis = product(pivot_values, pivot_columns)
    new_columns = [new_column(v, c) for (v, c) in pivot_axis]
    all_columns = non_pivot_columns + new_columns
    return sql.select(all_columns, from_obj=selectable, group_by=group_by)


@util.defaults("factory")
@util.sequences("joins")
@util.mutable_mappings("constraint_args", "mapper_args")
def join_sequence(left, joins, isouter=True, factory=None,
                  constraint_args=None, mapper_args=None):
    '''
    This performs successive left joins of *left* against the instances
    specified in *joins*, building a compound table.
    
    :param left: The instance to treat as the base for all joins
    
    :param joins: Either a single tuple or an sequence of tuples, with the form
        (Instance, {left_key:right_key}).
    
    :param isouter: Should the an outer join be performed?  If this is True,
        only instances of instance2 that have keys values referenced in
        instances1 will be included.
    
    :param factory:  Allows you to specify an alternate Instance creating
        factory, if you need special Instance creation behavior which
        can't be achieved by passing the default factory a class template.
    
    :param mapper_args:  Allows you to specify additional keyword arguments
        which should be passed when creating the object-relational mapping.
    
    :param constraint_args:  Allows you to specify additional keyword arguments
        which should be passed when creating foreign key constraint between
        tables.
    '''
    left_table = get_table(left)
    merged_table = None
    if len(joins) == 2 and util.is_instrumented(joins[0]):
        # Since a single join is such a common use case, deal with it.
        joins = [joins]
    for (right, keys) in joins:
        right_table = get_table(right)
        getcols = lambda x, y: (left_table.columns[x], right_table.columns[y])
        columns = [getcols(l, r) for (l, r) in keys.items()]
        (left_columns, right_columns) = zip(*columns)
        constraint = sa.ForeignKeyConstraint(right_columns, left_columns,
                                             **constraint_args)
        right_table.append_constraint(constraint)
        if merged_table is None:
            merged_table = orm.join(left_table, right_table, isouter=isouter)
        else:
            merged_table = orm.join(merged_table, right_table, isouter=isouter)
        mapper_properties = dict((l.name, (l, r)) for (l, r) in columns)
        excluded = [v for (k, v) in keys.items() if k != v]
        left = factory(bases=(left, right), excluded=excluded)
        orm.mapper(left, merged_table, properties=mapper_properties,
                   **mapper_args)
    return left


def record_tuple(column):
    '''
    Generates a record tuple from a sqlalchemy column, suitable to use for
    constructing a record array in numpy.
    
    :param column: The data type to use as a base for the numpy record tuple.
    
    :returns: A record tuple consisting of a parameter name and its associated
        numpy data type code.
    '''
    name = column.name
    type_ = column.type
    if util.descendant(type_, sa.String):
        return (name, STRING.format(type_.length or MAX_STRING_LENGTH))
    elif util.descendant(type_, sa.Float):
        return (name, DOUBLE)
    elif util.descendant(type_, sa.Boolean):
        return (name, BOOLEAN)
    elif util.descendant(type_, sa.Integer):
        return (name, LONG)
    else:
        raise ValueError("unsupported primitive type") 


#==============================================================================
#                                  Classes
#==============================================================================


class ArraySetCreator(object):
    '''
    Handles the nuances of creating the backing table for an array set, mapping
    it and creating a relationship between the instance and its associated
    property.
    '''

    @util.mutable_mappings("relationship_args", "mapper_args")
    def __new__(cls, instance, property_, relationship, table_name=None,
                mapper_args=None, backref_args=None, relationship_args=None):
        table = cls.create_table(instance, property_, table_name)
        cls.add_primary_key(table)
        foreign_keys = cls.to_keys(instance)
        primary_keys = primary_key_names(instance)
        table.create()
        map_(property_, table, **mapper_args)
        relationship(instance, property_, None, primary_keys, foreign_keys,
                     PROPERTIES, backref_args=backref_args,
                     **relationship_args)
    
    @staticmethod
    def to_keys(instance):
        '''
        This generates a table for and maps the specified Property, then creates
        a relationship between that property and the specified Instance.
        
        :param Instance: The Instance that the property should be related to.
        
        :param Property: The Property that should be persisted.
        
        :param relationship_type: The type of relationship to use between the
            Instance and Property.
        
        :param table_name: The name to give the table generated for Property.
        
        :param relationship_args: Allows you to specify additional keyword
            arguments which should be passed to the sqlalchemy relationship
            function.
        '''
        instance_name = instance.__name__.lower()
        property_name = lambda c: "_".join((instance_name, c.name))
        return [property_name(c) for c in primary_key_columns(instance)]

    @classmethod
    def create_table(cls, instance, property_, table_name=None):
        '''
        Generates the sqlalchemy table to support a Property that will be
        mapped to the given Instance.
        
        :param Instance: The Instance the Property will be attached to.
        
        :param property_types: The types of values this property can represent.
        
        :param table_name: The name to give the generated table.
        '''
        property_types = {}
        for type_ in property_.types:
            property_types[type_] = TYPE_MAPPINGS[type_]
        name = instance.__name__.lower()
        columns = [cls.column(name, c) for c in primary_key_columns(instance)]
        if not property_types:
            columns.append(sa.Column("str", sa.String(MAX_STRING_LENGTH)))
        if len(property_types) > 1:
            column_type = sa.String(max(len(k) for k in TYPE_MAPPINGS))
            columns.append(sa.Column("type", column_type))
        for (name_, type_) in property_types.items():
            columns.append(sa.Column(name_, type_))
        table_name = table_name or "_".join((name, PROPERTIES))
        metadata = get_metadata(instance)
        return sa.Table(table_name, metadata, *columns)

    @staticmethod
    def column(instance_name, column):
        name = "_".join((instance_name, column.name))
        return sa.Column(name, column.type)

    @staticmethod
    def add_primary_key(table):
        if not table.primary_key:
            sequence = sa.Sequence(table.name + "_sequence")
            id_ = sa.Column("id", sa.Integer(), sequence, primary_key=True)
            table.append_column(id_)


class DictionarySetCreator(ArraySetCreator):
    '''
    Handles the nuances of creating the backing table for an array set, mapping
    it and creating a relationship between the instance and its associated
    property.
    
    .. attribute:: key_type

        ..
        
        |    The data type of the key column in the properties table.
    '''
    
    key_type = sa.String(MAX_STRING_LENGTH)
    
    @util.mutable_mappings("backref_args")
    def __new__(cls, *args, **kwargs):
        attribute_map = orm.collections.attribute_mapped_collection
        key = kwargs.pop("key", KEY)
        backref_args = kwargs["backref_args"]
        backref_args["collection_class"] = attribute_map(key)
        super(DictionarySetCreator, cls).__new__(cls, *args, **kwargs)
    
    @staticmethod
    def column(instance_name, column):
        name = "_".join((instance_name, column.name))
        return sa.Column(name, column.type, primary_key=True)

    @classmethod
    def add_primary_key(cls, table):
        table.append_column(sa.Column("key", cls.key_type, primary_key=True))
    