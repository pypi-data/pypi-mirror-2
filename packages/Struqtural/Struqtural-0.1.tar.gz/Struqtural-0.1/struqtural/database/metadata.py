'''
.. module:: metadata
    :synopsis: Column metadata classes, which allow structures to provide
        additional persistable functionality on a column by column basis.
        These column metadata classes are applied to structures via mixins.

.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import sqlalchemy as sa
import sqlalchemy.orm as orm
import struqtural.utilities as util

from sqlalchemy.exc import InvalidRequestError


METADATA = "column_metadata"


@util.mutable_mappings("table_args")
def column_metadata(table, connector, base_meta, table_args=None):
    '''
    Creates a meta data table from a ColumnMetaData object and associates it
    with the given table.
    
    :param table: The table with which this column metadata should be
        associated.
    
    :param connector: The
        :class:`struqtural.database.connector.DatabaseConnector` to use.
    
    :param meta_class: The :class:`ColumnMetaData` subclass to use as a base.
    
    :returns: The created :class:`ColumnMetaData` subclass associated with the
        metadata table.
    '''
    name = "_".join((table.name, METADATA))
    meta_class = type(base_meta.__name__, (base_meta,), {})
    try:
        type_table = sa.Table(name, connector.metadata, autoload=True,
                              **table_args)
    except InvalidRequestError:
        type_table = meta_class.to_table(name, connector, **table_args)
        type_table.create()
    finally:
        orm.mapper(meta_class, type_table)
        connector.session.add_all(meta_class(c.name) for c in table.columns)
        connector.session.flush()
    return meta_class


#==============================================================================
#                                  Classes
#==============================================================================


class ColumnMetaData(object):
    '''
    Base type for ColumnMetaData classes.
    
    .. attribute:: name
        
        ..
        
        |    The name of the column in the associated table.
    '''

    _properties = [sa.Column("name", sa.String(), primary_key=True)]

    def __init__(self, name):
        '''
        :param name: The name of the column in the associated table.
        '''
        self.name = name

    def __repr__(self):
        template = "{0}={1}"
        value = lambda x: template.format(x, getattr(self, x))
        values = ", ".join(value(c.name) for c in self._properties)
        return "{0}({1})".format(type(self).__name__, values)

    def __eq__(self, other):
        if other:
            columns = lambda x: [c.name for c in getattr(x, "_properties")]
            return columns(self) == columns(other)
        else:
            return False

    @classmethod
    def to_table(cls, name, connection, **kwargs):
        '''
        Generate a :class:`sqlalchemy.schema.Table` definition from the column
        properties specified in this ColumnMetaData class.
        
        :param name: The name to assign to the generated table.
        
        :param connection: A
            :class:`struqtural.database.connector.DatabaseConnector` or
            :class:`sqlalchemy.schema.MetaData` instance.
        
        :returns: A :class:`sqlalchemy.schema.Table` representing the
            attributes of this ColumnMetaData.
        
        .. note::
            Any additional keyword arguments provided to :func:`to_table` are
            passed directly to the :class:`sqlalchemy.schema.Table`
            constructor.
        '''
        columns = [c.copy() for c in cls._properties]
        if isinstance(connection, sa.MetaData):
            # Allow a little shortcut, since we just want the metadata
            metadata = connection
        else:
            metadata = connection.metadata
        return sa.Table(name, metadata, *columns, **kwargs)


class ColumnUnits(ColumnMetaData):
    '''
    This ColumnMetaData class provides support for units, and the associated
    ColumnUnitsMixin provides methods for structures to get and set units, with
    automatic value rescaling as needed.  The unit types are persisted as
    Python pickle objects.
    
    .. attribute:: units
        
        ..
        
        |    The quantities units associated with this column.
    '''

    _properties = [sa.Column("name", sa.String(), primary_key=True),
                   sa.Column("units", sa.PickleType)]

    def __init__(self, name, units=None):
        '''
        :param name: The name of the associated column.
        
        :param units: The units associated with the column.  This can be either
            quantities unit objects or a string using quantities compatible
            names, for example 'meter / second ** 2' or 'mile / hour'.
        '''
        super(ColumnUnits, self).__init__(name)
        self.units = units


