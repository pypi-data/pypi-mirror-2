'''
.. module:: eav
    :synopsis: Entity-Attribute-Value store loaders.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import struqtural.database as db
import struqtural.utilities as util
import struqtural.loaders.loader as loader


PROPERTIES = "properties"


#==============================================================================
#                                  Classes
#==============================================================================


class EntityAttributeValueSetLoader(loader.CollectionLoader):
    '''
    The base class for loaders implementing entity-attribute-value stores.
    
    This class provides basic initialization logic for the
    :class:`ArraySetLoader` and :class:`DictionarySetLoader` classes.
    
    .. attribute:: default_comparator
    
        ..
        
        |    The :class:`sqlalchemy.orm.Comparator` to implement on the
        |    property class if none is specified during initialization.
        
    .. attribute:: default_query
        
        ..
        
        |    The default :class:`sqlalchemy.orm.query.Query` subclass to use.

    .. attribute:: default_relationship
        
        ..
        
        |    The default :func:`struqtural.database.relationship.relationship`
        |    type to use.
        
    .. attribute:: creator
        
        ..
        
        |    The creator class to use when generating the table, nesting
        |    instance and relationship.
    '''
    
    default_comparator = db.InstancePropertyComparator
    default_query = db.EntityAttributeValueQuery
    creator = None
    
    @util.mutable_mappings("relationship_args")
    def __init__(self, data=None, primary_keys=None, instance_name=None,
                 connector=None, table_name=None, column_types=None,
                 property_=None, **kwargs):
        '''
        '''
        relationship = kwargs.pop("relationship", db.relationship)
        comparator = kwargs.pop("comparator", self.default_comparator)
        property_table = kwargs.pop("property_table", None)
        relationship_args = kwargs.pop("relationship_args")
        parent_init = super(EntityAttributeValueSetLoader, self).__init__
        parent_init(data, primary_keys, instance_name, connector, table_name,
                    column_types, **kwargs)
        self.creator(self.Instance, property_, relationship, property_table,
                     **relationship_args)
        db.attach_comparator(property_, comparator, "value")
        self.Instance._property_type = property_
        self.Instance._property_mapping = PROPERTIES

    
class DictionarySetLoader(EntityAttributeValueSetLoader):
    '''
    Loader specialized to load DictionarySets.
    '''
    
    default_query = db.DictionaryQuery
    creator = db.DictionarySetCreator
    
    def __init__(self, *args, **kwargs):
        key_type = kwargs.pop("key_type", None)
        if key_type:
            attrs = {"key_type":db.type_mappings[key_type.__name__]}
            self.creator = type(self.creator.__name__, (self.creator,), attrs)
        super(DictionarySetLoader, self).__init__(*args, **kwargs)


class ArraySetLoader(EntityAttributeValueSetLoader):
    '''
    Loader specialized to load ArraySets
    '''
    
    default_query = db.ArrayQuery
    creator = db.ArraySetCreator