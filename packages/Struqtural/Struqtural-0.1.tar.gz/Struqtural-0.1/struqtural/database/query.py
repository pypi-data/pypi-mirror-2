'''
.. module:: query
    :synopsis: Customized SQL Alchemy Query subclasses providing additional
        functionality.

.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import sqlalchemy as sa
import sqlalchemy.orm as orm
import struqtural.utilities as util

from itertools import product


#==============================================================================
#                                  Classes
#==============================================================================


class Query(orm.Query):
    '''
    Parent query type, providing some additional utility methods over the
    base :class:`sqlalchemy.orm.query.Query` class.
    
    .. attribute:: queried_on
        The instance types or attributes targeted in this query.
    '''
    
    def __init__(self, entities, session=None):
        # This is here since sqlalchemy's _entities aren't the entities passed.
        self.queried_on = util.as_sequence(entities)
        super(Query, self).__init__(entities, session)
    
    def _attribute_columns(self, columns):
        '''
        Given a list of string column names, this will pull out all matching
        entity attributes.
        '''
        tables = [orm.class_mapper(e).local_table for e in self.queried_on]
        possible = product(tables, columns)
        return [t.columns[c] for (t, c) in possible if c in t.columns]
    
    def asc(self, *columns):
        '''
        Return Instances ordered according to ascending values of the specified
        columns.
        '''
        order = (c.asc() for c in self._attribute_columns(columns))
        return self.order_by(*order)
    
    def desc(self, *columns):
        '''
        Return Instances ordered according to descending values of the
        specified columns.
        '''
        order = (c.desc() for c in self._attribute_columns(columns))
        return self.order_by(*order)

    def filter(self, *filters):
        '''
        Convenience method to set multiple filters with a single call.  Any
        filter expression supported by sqlalchemy may be used here.
        
        :param filters: The filters to apply to the data set.
        
        :returns: The filtered query expression.
        '''
        for filter_ in filters:
            self = super(Query, self).filter(filter_)
        return self


class GraphQuery(Query):
    '''
    Knows about the relationship between nodes and edges.  Not currently
    implemented.
    '''

    
class DirectedAcyclicGraphQuery(GraphQuery):
    '''
    Not currently implemented.
    '''
    

class TreeQuery(GraphQuery):
    '''
    Not currently implemented.
    '''


class EntityAttributeValueQuery(Query):
    '''
    Specialized Query class to simplify working with instances based on
    key/value pairs.
    '''
    
    def __init__(self, entities, session=None):
        # Let's just take note of what we're querying on for later...
        _property = lambda e: (e, getattr(e, "_property_type", None))
        self._properties = dict(_property(e) for e in util.iter_(entities))
        super(EntityAttributeValueQuery, self).__init__(entities, session)
    
    def _comparison(self, comparison_function):
        '''
        Comparison on the properties of an instance or directly on the
        instance, depending on the _properties for this query.
        '''
        criterion = None
        for (entity, property_) in self._properties.items():
            if property_:
                and_ = comparison_function(property_)
                match = entity.properties.any(and_)
            else:
                match = comparison_function(entity)
            if criterion is None:
                criterion = match
            else:
                criterion |= match
        return self.filter(criterion)
    
    def _entity_comparison(self, comparison_function):
        '''
        Comparison directly on an instance.
        '''
        criterion = None
        for (entity, property_) in self._properties.items():
            if property_:
                match = comparison_function(entity)
                if criterion is None:
                    criterion = match
                else:
                    criterion |= match             
        return self.filter(criterion)

    def has_value(self, value):
        '''
        Filters instances that do not have an associated property with value
        *key*.
        
        :param key: The property key to use as a presence constraint.
        '''
        _value = lambda p: p._property_type.value
        comparison = lambda p: p.properties.any(_value(p) == value)
        return self._entity_comparison(comparison)
    
    def not_has_value(self, value):
        '''
        Filters instances that have an associated property with value *value*.
        
        :param value: The property value to use as an absence constraint.
        '''
        _value = lambda p: p._property_type.value
        comparison = lambda p: ~p.properties.any(_value(p) == value)
        return self._entity_comparison(comparison)

    
class DictionaryQuery(EntityAttributeValueQuery):
    '''
    Provides simplified queries on dictionary-like instance attributes.
    '''
    
    def __contains__(self, key):
        '''
        Not currently functional.
        '''
        return key if self.has_key(key).count() else False
            
    def gt(self, key, value):
        '''
        Filters instances that do not have an associated property with key
        *key* and a value greater than *value*.
        
        :param key: The property key to use for comparison.
        
        :param value: The cutoff for the associated value, above which entities
            with this property should not be filtered. 
        '''
        comparison = lambda p: sa.and_(p.key == key, p.value > value)
        return self._comparison(comparison)

    def ge(self, key, value):
        '''
        Filters instances that do not have an associated property with key
        *key* and a value greater than or equal to *value*.
        
        :param key: The property key to use for comparison.
        
        :param value: The cutoff for the associated value, at or above which
            entities with this property should not be filtered.
        '''
        comparison = lambda p: sa.and_(p.key == key, p.value >= value)
        return self._comparison(comparison)

    def lt(self, key, value):
        '''
        Filters instances that do not have an associated property with key
        *key* and a value less than *value*.
        
        :param key: The property key to use for comparison.
        
        :param value: The cutoff for the associated value, below which
            entities with this property should not be filtered.
        '''
        comparison = lambda p: sa.and_(p.key == key, p.value < value)
        return self._comparison(comparison)

    def le(self, key, value):
        '''
        Filters instances that do not have an associated property with key
        *key* and a value less than or equal to *value*.
        
        :param key: The property key to use for comparison.
        
        :param value: The cutoff for the associated value, at or below which
            entities with this property should not be filtered.
        '''
        comparison = lambda p: sa.and_(p.key == key, p.value <= value)
        return self._comparison(comparison)

    def eq(self, key, value):
        '''
        Filters instances that do not have an associated property with key
        *key* and a value equal to *value*.
        
        :param key: The property key to use for comparison.
        
        :param value: The equality constraint for the property's associated
            value.
        '''
        comparison = lambda p: sa.and_(p.key == key, p.value == value)
        return self._comparison(comparison)

    def ne(self, key, value):
        '''
        Filters instances that do not have an associated property with key
        *key* and a value not equal to *value*.
        
        :param key: The property key to use for comparison.
        
        :param value: The inequality constraint for the property's associated
            value.
        '''
        comparison = lambda p: sa.and_(p.key == key, p.value != value)
        return self._comparison(comparison)

    def has_key(self, key):
        '''
        Filters instances that do not have an associated property with key
        *key*.
        
        :param key: The property key to use as a presence constraint.
        '''
        _key = lambda p: p._property_type.key
        comparison = lambda p: p.properties.any(_key(p) == key)
        return self._entity_comparison(comparison)
    
    def not_has_key(self, key):
        '''
        Filters instances that have an associated property with key *key*.
        
        :param key: The property key to use as an absence constraint.
        '''
        _key = lambda p: p._property_type.key
        comparison = lambda p: ~p.properties.any(_key(p) == key)
        return self._entity_comparison(comparison)


class ArrayQuery(EntityAttributeValueQuery):
    '''
    Not currently implemented.
    '''
