'''
.. module:: introspection
    :synopsis: Utility functions used for performing introspection on Python
        objects.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import types
import collections
import struqtural.utilities as util


# Thanks Carl!
def class_(class_):
    '''
    Determines if a given class is a native Python object.
    
    :param class_: The class which should be inspected.
    
    :returns: True if the class is a native Python object, False otherwise.
    '''
    if isinstance(class_, types.ClassType):
        return True
    return bool(isinstance(class_, type) and class_.__flags__ & 512)


def function(instance, attribute_name):
    '''
    Determines if the attribute with *attribute_name* on an object is a
    function.
    '''
    attribute = getattr(instance, attribute_name)
    return isinstance(attribute, types.FunctionType)


def private(attribute_name):
    '''
    Determines if the attribute specified by *attribute_name* is should be
    considered private.
    '''
    return attribute_name.startswith("__")


def property_(instance, attribute_name):
    '''
    Determines if a given attribute with *attribute_name* is a property on
    *instance*'s class.
    '''
    class_attribute = getattr(type(instance), attribute_name, None)
    return isinstance(class_attribute, property)


def collection(instance, attribute_name):
    '''
    Determines if a given attribute with *attribute_name* on an object is
    a collection.
    '''
    attribute = getattr(instance, attribute_name)
    return isinstance(attribute, (collections.Container, collections.Iterable,
                                  collections.Sized))


def base_validator(instance, attribute):
    '''
    Determines if attributes on an instance should be considered for
    persistence when transforming a class.
    '''
    return (not function(instance, attribute) and not private(attribute) and
            not property_(instance, attribute))
      
         
@util.mutable_sets("ignore")
def get_attributes(instance, valid=base_validator, ignore=None):
    '''
    Returns the attributes of *instance*.  If *instance* is a struqtural
    instance subclass, returns the set of attributes specified by
    __attributes__.
    
    :param instance: The type instance to search for attributes.
    
    :param valid: The validation function to use when identifying attributes
        on *instance*.
    
    :param ignore: Attributes which should be ignored outright.
    
    :returns: A sequence containing all the attributes of *instance* that
        match the criterion specified.
    '''
    validate = lambda i: [a for a in vars(i) if valid(i, a) and a not in ignore]
    attributes = lambda i: getattr(i, "__attributes__", validate(i))
    return attributes(instance)


def instance_to_dict(instance, attributes):
    '''
    Converts a type instance to its dictionary representation over the set of
    *attributes*
    '''
    return dict((a, getattr(instance, a, None)) for a in attributes)


@util.mutable_sequences("instances")
def instances_to_dicts(instances, basetype=None):
    '''
    Identifies an attribute closure for instances, then generates a list of
    dictionary instance representations, given the identified attribute
    closure. 
    
    :param instances: The sequence of type instances to be converted.
    
    :param basetype: The base type of the instances being converted, if they
        are not all of the same type.
    
    :returns: A list of dictionaries with attribute mappings identical to
        those found on instances.
    '''
    all_attributes = set()
    properties = set()
    # In case we get handed a generator...
    basetype = basetype or type(instances[0])
    uniform_type = lambda x: all(isinstance(i, basetype) for i in x)
    if not class_(basetype) or not uniform_type(instances):
        raise ValueError("invalid instances supplied.")
    for instance in instances:
        all_attributes.update(get_attributes(instance, ignore=properties))
    to_dict = lambda i: instance_to_dict(i, list(all_attributes))
    return [to_dict(i) for i in instances]
