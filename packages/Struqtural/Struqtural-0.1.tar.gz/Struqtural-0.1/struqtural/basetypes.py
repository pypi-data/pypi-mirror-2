'''
.. module:: basetypes
    :synopsis: This module provides abstract base classes for core struqtural
        objects.

.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

from collections import Iterable, Sequence


def verify_functionality(names, other):
    if all(hasattr(other, name) for name in names):
        return True
    return False


#==============================================================================
#                                  Classes
#==============================================================================


class InstanceMeta(type):
    '''
    Meta class for AbstractInstance.  Provides instance and subclass check
    functionality.
    '''

    @classmethod
    def __instancecheck__(cls, other):
        attributes = getattr(type(other), "__attributes__", None)
        if isinstance(attributes, Sequence):
            return True
        else:
            return False
        
    @classmethod
    def __subclasscheck__(cls, other):
        attributes = getattr(other, "__attributes__", None)
        if isinstance(attributes, Sequence):
            return True
        else:
            return False


class LoaderMeta(type):
    '''
    Meta class for AbstractLoader.  Provides instance and subclass check
    functionality.
    '''
    
    names = ("table", "connector", "Instance")

    @classmethod
    def __instancecheck__(cls, other):
        result = False
        try:
            if (verify_functionality(cls.names, other) and
                callable(getattr(getattr(other, "connector"), "connect")) and
                hasattr(getattr(other, "connector"), "session")):
                result = True
        finally:
            return result


class StructureMeta(type):
    '''
    Meta class for AbstractStructure.  Provides instance and subclass check
    functionality.
    '''
    names = ("primary_key", "columns", "__getitem__", "__iter__", "__len__")
    
    @classmethod
    def __instancecheck__(cls, other):
        result = False
        try:
            if (isinstance(AbstractLoader, other) and
                verify_functionality(cls.names, other) and
                isinstance(getattr(other, "primary_key"), Iterable) and 
                isinstance(getattr(other, "columns"), Iterable)):
                result = True
        finally:
            return result


class AbstractInstance(object):
    '''
    Abstract base class for instances.  Only used for instance checks.
    '''
    
    __metaclass__ = InstanceMeta


class AbstractLoader(object):
    '''
    Abstract base class for loaders.  Only used for instance checks.
    '''
    __metaclass__ = LoaderMeta

        
class AbstractStructure(object):
    '''
    Abstract base class for structures.  Only used for instance checks.
    '''
    __metaclass__ = StructureMeta