'''
.. module:: structure
    :synopsis: Core structure classes providing functionality to other
        structures.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import struqtural.basetypes as basetypes
import struqtural.utilities as util

REPR_TEMPLATE = "{0}(name='{1}', element_primary_key={2})"

class Structure(basetypes.AbstractStructure):
    '''
    A data structure mapped to one (or more) database tables.  Provides
    convenience methods for many sqlalchemy functions.  Structure also
    defines a mapping from local to loader resident attributes.
    '''

    default_loader = None

    @util.iterables("mixins")
    def __init__(self, loader=None, *args, **kwargs):
        self.order_key = None
        loader = loader or self.default_loader
        mixins = kwargs.pop("mixins", [])
        if isinstance(loader, basetypes.AbstractLoader):
            # We've been passed a pre-instantiated loader, just drop it in.
            self.properties = loader
        else:
            self.properties = loader(*args, **kwargs)
        for mixin in mixins:
            mixin._install(self)

    def __len__(self):
        return self.query(self.Instance).count()

    def __iter__(self):
        query = self.query(self.Instance)
        if isinstance(self.order_key, basestring):
            query = query.order_by(getattr(self.Instance, self.order_key))
        return iter(query)

    def __getitem__(self, item):
        '''
        A robust implementation of the __getitem__ notation on session queries.
        
        :param item: The slice or item to get
        :returns: The selected instances
        
        .. note::
            There is no straightforward way to support slices with a value
            other than 1 or -1 using SQL.  If a slice with a different value
            is requested, the range from start to stop is queried and a
            step-only slice is taken.
        '''
        items = self.query(self.Instance)
        if not isinstance(item, slice):
            results = items[item]
        else:
            start = item.start or 0
            step = item.step or 1
            stop = item.stop
            # The extra code here is to support negative slices and steps
            if start >= 0 and (not stop or stop > start) and step >= 1:
                # This is the typical use case, sqlalchemy supports it so I'll
                # just pass it along...
                results = items[item]
            elif not ((start > stop) ^ (step >= 1)):
                # This is a wrap case, Python doesn't support it so I won't
                results = []
            else:
                length = len(self)
                if not stop:
                    if step >= 0:
                        stop = length
                    else:
                        stop = 0
                elif stop < 0:
                    stop = length - abs(stop)
                if start < 0:
                    start = length - abs(start)
                if step < 0:
                    items = items.desc(*self.primary_keys)
                    step = abs(step)
                    (start, stop) = (stop, start)
                limit = abs(stop - start)
                items = items.offset(start).limit(limit)
                results = list(items)[::step]      
        return results

    def __repr__(self):
        class_name = self.__class__.__name__
        return REPR_TEMPLATE.format(class_name, self.name, self._primary_keys)

    def _get_name(self):
        '''
        The structure name.  Analogous to the database table name if the
        structure is represented by a single table, or the join condition
        if the structure is the result of a join over multiple tables.
        '''
        return self.table.name

    def _get_connector(self):
        '''
        The :class:`struqtural.database.connector.DatabaseConnector` for this
        structure.
        '''
        return self.properties.connector

    def _set_connector(self, connector):
        '''setter method for connector property redirection.'''
        self.properties.connector = connector

    def _get_table(self):
        '''
        The :class:`sqlalchemy.schema.Table` representing this structure in
        the database.
        '''
        return self.properties.table

    def _get_primary_key(self):
        '''
        The primary key columns for the table representing this structure
        in the database.
        '''
        return [c.name for c in self.table.primary_key]

    def _get_instance(self):
        '''
        The class of instance contained by this structure.
        '''
        return self.properties.Instance

    def _set_instance(self, instance):
        '''setter method for Instance property redirection.'''
        self.properties.Instance = instance

    def _get_columns(self):
        '''
        The columns of the table representing this structure in the database.
        '''
        return self.table.columns

    columns = property(_get_columns)
    connector = property(_get_connector, _set_connector)
    name = property(_get_name)
    primary_keys = property(_get_primary_key)
    table = property(_get_table)
    Instance = property(_get_instance, _set_instance)

    @util.iterables("instances")
    def add(self, instances, flush=False):
        '''
        Given an iterable of instances, add those instances to the database.
        Optionally, flush the session afterwards.
        '''
        self.connector.session.add_all(instances)
        if flush:
            self.connector.session.flush()

    @util.iterables("instances")
    def delete(self, instances, flush=False):
        '''
        given an iterable of instances, delete those instances from the
        database.  Optionally, flush the session afterwards.
        '''
        for instance in instances:
            self.connector.session.delete(instance)
        if flush:
            self.connector.session.flush()

    def filter(self, *filters):
        '''
        Convenience method to set multiple filters with a single call.  Any
        filter expression supported by sqlalchemy may be used here.
        
        :param filters: The filters to apply to the data set.
        
        :returns: The filtered query expression.
        '''
        query_instances = []
        filters_ = []
        for filter_ in filters:
            if type(filter_) == type:
                query_instances.append(filter_)
            else:
                filters_.append(filter_)
        if not query_instances:
            query_instances.append(self.Instance)
        return self.query(*query_instances).filter(*filters_)

    def values(self, *attributes):
        '''
        Returns the values of the specified columns.
        
        :param attributes: The column names to select from the database.
        '''
        val = lambda a: getattr(self.Instance, a) if isinstance(a, str) else a
        attributes_ = [val(a) for a in attributes]
        return self.query(self.Instance).values(*attributes_)

    def query(self, *args):
        '''
        Query the database for one or more instances.  If no instances are
        supplied, the default instance is assumed.
        '''
        if not args:
            args = [self.Instance]
        return self.properties.Query(*args, session=self.connector.session)


class MultiStructure(object):
    '''
    A structure containing more than one set of related records.
    '''
    
    default_loader = None
    
    def __init__(self, loader=None, *args, **kwargs):
        loader = loader or self.default_loader
        mixins = kwargs.pop("mixins", [])
        self.properties = {}
        if isinstance(loader, basetypes.AbstractLoader):
            # We've been passed a pre-instantiated loader, just drop it in.
            properties = loader.properties
        else:
            properties = loader(*args, **kwargs).properties
        for (key, loader) in properties.items():
            self.properties[key] = Structure(loader)
        for mixin in mixins:
            mixin._install(self)
            
