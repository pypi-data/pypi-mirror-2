'''
.. module:: eav
    :synopsis: Entity-attribute-value based implementations of standard Python
        collection types.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import struqtural.loaders.eav as eav
import struqtural.utilities as util

from struqtural.structures.structure import Structure


def create_property(property_types=str, with_key=True):
    '''
    Creates a new Property class.
    
    :param property_types: The Python data types to support.  These should be
        the type objects themselves, for instance int, str, bool, etc.  If more
        than one type is specified, the property will have an additional
        attribute 'type' which specifies the data type for this property's
        value.
    
    :param with_key: Should properties have an associated key?  If you are
        creating a dictionary-like structure, this should evaluate to True.
        For array-like structures it should be False.
    
    :returns: A property object with attributes corresponding to the types
        in *property_types*.  If *with_key* was specified the property will
        be a NamedProperty with a 'key' attribute.  If more than one type
        was specified, the property will be a PolymorphicProperty with a
        'type' attribute.
    '''
    types = set()
    for type_ in property_types:
        types.add(type_.__name__)
    if len(types) > 1:
        if with_key:
            base = PolymorphicNamedProperty
        else:
            base = PolymorphicUnnamedProperty
    else:
        if with_key:
            base = NamedProperty
        else:
            base = UnnamedProperty
    Property = type(base.__name__, (base,), {"types":types})
    return Property


class NamedProperty(object):
    '''
    This is a base type for properties with a value which is referenced by a
    key.
    
    .. attribute:: key
    
        ..
        
        |    The reference attribute for this property's *value*.  This may be
        |    of any one Python data type with a corresponding SQL primitive
        |    type which can be part of a primary key.  No instances can have
        |    more than one property with a given key.
        
    .. attribute:: value
        
        ..
        
        |    The *value* contained by this property.
    '''

    def __init__(self, key, value):
        '''
        :param key: The value to use for this property's *key* attribute.
        
        :param value: The value to assign to this property's *value* attribute.
        '''
        self.key = key
        self.value = value

    def __repr__(self):
        return '%s(%r=%r)' % (self.__class__.__name__, self.key, self.value)


class UnnamedProperty(object):
    '''
    This is a base type for properties without a key.  The primary key for
    these types is a sequential integer so duplicate property values are
    possible.

    .. attribute:: value
        
        ..
        
        |    The *value* contained by this property.
    '''

    def __init__(self, value):
        '''
        :param value: The value to assign to this property's *value* attribute.
        '''
        self.value = value

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)


class PolymorphicProperty(object):
    '''
    This is a base type for properties which can take on more than one type of
    value.
    
    .. attribute types::
    
        ..
        
        |    A set containing the names of all the Python types which this
        |    property is capable of storing.  These names correspond to
        |    column names in the property's mapped table with SQL primitive
        |    types which are roughly equivalent to the named type. 
        
    .. attribute type::
        
        ..
        
        |    The name of the type this property is currently storing (and its
        |    corresponding column in the table).
    '''

    types = None

    def _get_value(self):
        '''
        The value of this property.
        '''
        return getattr(self, self.type) if self.type else None

    def _set_value(self, value):
        if value is not None:
            py_type = type(value).__name__
        else:
            py_type = None
        if py_type and py_type not in self.types:
            raise TypeError(py_type)
        for field_type in self.types:
            field_value = None
            if py_type == field_type:
                self.type = py_type
                field_value = value
            if field_type is not None:
                setattr(self, field_type, field_value)

    def _del_value(self):
        self._set_value(None)

    value = property(_get_value, _set_value, _del_value)


class PolymorphicNamedProperty(PolymorphicProperty, NamedProperty):
    '''
    This class provides specialized initialization logic.
    '''
    def __init__(self, key, value=None):
        super(PolymorphicNamedProperty, self).__init__(key, value)
        if value is not None:
            self.type = type(value).__name__
        else:
            self.type = None


class PolymorphicUnnamedProperty(PolymorphicProperty, UnnamedProperty):
    '''
    This class provides specialized initialization logic.
    '''
    def __init__(self, value=None):
        super(PolymorphicUnnamedProperty, self).__init__(value)
        if value is not None:
            self.type = type(value).__name__
        else:
            self.type = None


class EntityAttributeValueMixin(object):
    '''
    This is a base type which provides basic property mapping support.
    
    .. attribute:: _property_type
    
        ..
        
        |    The property class. Valid types include:
        |        :class:`PolymorphicUnnamedProperty`
        |        :class:`PolymorphicNamedProperty`
        |        :class:`UnnamedProperty`
        |        :class:`NamedProperty`
        
    .. attribute:: _property_mapping
        
        ..
        
        |    This is the attribute on the host class which should be used
        |    as a back reference for the properties table relationship.
    
    .. attribute:: _map
        
        ..
        
        |    a convenience data descriptor simplifying the process of getting
        |    and setting of this property's value.
    '''
    
    def _get_property_mapping(self):
        '''
        Provides a convenient point of access for keyed attributes.
        '''
        return getattr(self, self._property_mapping)
    
    def _set_property_mapping(self, value):
        setattr(self, self._property_mapping, value)
    
    _property_type = None
    _property_mapping = None
    _map = property(_get_property_mapping, _set_property_mapping)


class DictionaryMixin(EntityAttributeValueMixin):
    '''
    This mixin allows an instance to effectively mimic a Python dictionary
    using an entity-attribute-value data store.
    '''

    def __iter__(self):
        return self.keys()

    def __getitem__(self, key):
        return self._map[key].value

    def __setitem__(self, key, value):
        property_ = self._map.get(key)
        if property_ is None:
            self._map[key] = self._property_type(key, value)
        else:
            property_.value = value

    def __delitem__(self, key):
        del self._map[key]

    def __contains__(self, key):
        return key in self._map

    def keys(self):
        '''
        Analogous to the Python dictionary method of the same name.
        '''
        return self._map.keys()

    def values(self):
        '''
        Analogous to the Python dictionary method of the same name.
        '''
        return [prop.value for prop in self._map.values()]

    def items(self):
        '''
        Analogous to the Python dictionary method of the same name.
        '''
        return [(key, prop.value) for key, prop in self._map.items()]
    
    def pop(self, key, default=None):
        '''
        Analogous to the Python dictionary method of the same name.
        '''
        if key not in self._map and default is not None:
            return default
        else:
            return self._map.pop(key).value
    
    def get(self, key, default=None):
        '''
        Analogous to the Python dictionary method of the same name.
        '''
        if key not in self._map and default is not None:
            return default
        else:
            return self._map[key].value
        
    # FIXME: write this code.
    def update(self, iterable):
        '''
        Not yet implemented.
        '''
        raise NotImplementedError


class ArrayMixin(EntityAttributeValueMixin):
    '''
    This mixin allows an instance to effectively mimic a Python array using
    an entity-attribute-value data store.
    '''
    
    def __iter__(self):
        return self._map.__iter__()
    
    def __contains__(self, other):
        # Not the best way to do this, come back to me later
        return list(p.value for p in self._map).__contains__(other)
    
    def __len__(self):
        return self._map.__len__()
    
    def __getitem__(self, item):
        return self._map.__getitem__(item).value
    
    def __setitem__(self, item, value):
        property_ = self._map.__getitem__(item)
        property_.value = value
    
    def __delitem__(self, item):
        self._map.__delitem__(item)
    
    def insert(self, index, item):
        '''
        Analogous to the Python list method of the same name.
        '''
        self._map.insert(index, self._property_type(item))
    
    def append(self, item):
        '''
        Analogous to the Python list method of the same name.
        '''
        self._map.append(self._property_type(item))
        
    def extend(self, iterable):
        '''
        Analogous to the Python list method of the same name.
        '''
        self._map.extend(self._property_type(i) for i in iterable)
    
    def index(self, item):
        '''
        Analogous to the Python list method of the same name.
        '''
        return list(p.value for p in self._map).index(item)
    
    def count(self, item):
        '''
        Analogous to the Python list method of the same name.
        '''
        # FIXME: his is not the best way to do this, come back to me later
        return list(p.value for p in self._map).count(item)
    
    def pop(self, item=None):
        '''
        Analogous to the Python list method of the same name.
        '''
        if not item:
            item = len(self) - 1
        return self._map.pop(item).value
    
    def remove(self, item):
        '''
        Analogous to the Python list method of the same name.
        '''
        self.__delitem__(self.index(item))        
    

class EntityAttributeValueSet(Structure):
    '''
    This provides the core initialization logic for the :class:`DictionarySet`
    and :class:`ArraySet` classes.
    
    .. attribute:: default_loader
        
        ..
        
        |    The default loader class to use if none is specified on
        |    initialization.
    
    .. attribute:: set_mixin
        
        ..
        
        |    The mixin that is providing collection behavior for instances in
        |    this structure.
    
    .. attribute:: with_key
        
        ..
        
        |    Determines whether :func:`create_property` generates a
        |    :class:`NamedProperty` or :class:`UnnamedProperty` subclass.
    '''
    
    default_loader = eav.EntityAttributeValueSetLoader
    set_mixin = EntityAttributeValueMixin
    with_key = True

    def __init__(self, data=None, primary_keys=None, instance_name=None,
                 connector=None, table_name=None, column_types=None,
                 property_types=None, **kwargs):
        '''
        :param loader: The loader to use.  Defaults to *default_loader* if not
            specified.
        
        :param property_types: The Python types that the property must be
            capable of representing.
        '''
        loader = util.from_args("loader", kwargs) or self.default_loader
        self.Property = create_property(property_types, self.with_key)
        parent_init = super(EntityAttributeValueSet, self).__init__
        parent_init(loader, data, primary_keys, instance_name, connector,
                    table_name, column_types, self.Property, **kwargs)
        if not issubclass(self.Instance, self.set_mixin):
            self.Instance.__bases__ += (self.set_mixin,)


class DictionarySet(EntityAttributeValueSet):
    '''
    This structure provides a container for instances emulating Python
    dictionaries.
    '''

    default_loader = eav.DictionarySetLoader
    set_mixin = DictionaryMixin
      

class ArraySet(EntityAttributeValueSet):
    '''
    This structure provides a container for instances emulating Python lists.
    '''
    
    default_loader = eav.ArraySetLoader
    set_mixin = ArrayMixin
    with_key = False
