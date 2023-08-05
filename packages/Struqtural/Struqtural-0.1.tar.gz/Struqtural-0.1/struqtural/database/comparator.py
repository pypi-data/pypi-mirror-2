'''
.. module:: comparator
    :synopsis: Custom comparators for instance attributes.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import sqlalchemy.orm as orm


#==============================================================================
#                                 Functions
#==============================================================================


def attach_comparator(parent_class, comparator_class, attribute_name):
    '''
    Attach a custom :class:`sqlalchemy.orm.interfaces.PropComparator` for
    *attribute_name* to *parent_class*
    
    :param parent_class: The mapped class for which the custom comparator
        should be installed.
    
    :param comparator_class: The custom comparator to install in
        *parent_class*.
    
    :param attribute_name: The name of the attribute on *parent_class* for
        which the comparator should be installed.
    '''
    mapper = orm.class_mapper(parent_class)
    attributes = {"parent":parent_class}
    comparitor_name = comparator_class.__name__
    Comparator = type(comparitor_name, (comparator_class,), attributes)
    attribute = getattr(parent_class, attribute_name)
    comparator_hook = orm.comparable_property(Comparator, attribute)
    mapper.add_property(attribute_name, comparator_hook)


#==============================================================================
#                                  Classes
#==============================================================================


class InstancePropertyComparator(orm.PropComparator):
    '''
    Rewrite of the Comparator included in the sqlalchemy vertical attribute
    example.  Additional comparison options have been provided, and reliance
    on case statements has been removed.  As a result, comparisons are much
    more efficient, however the ability to compare values of different types
    is no longer present.
    
    .. attribute:: parent
        
        ..
        
        |    The class with which this comparator is associated.  This is used
        |    to map the compared value's type to its respective database
        |    column.
    '''

    parent = None

    def __eq__(self, other):
        return getattr(self.parent, type(other).__name__) == other

    def __ne__(self, other):
        return getattr(self.parent, type(other).__name__) != other

    def __lt__(self, other):
        return getattr(self.parent, type(other).__name__) < other

    def __le__(self, other):
        return getattr(self.parent, type(other).__name__) <= other

    def __gt__(self, other):
        return getattr(self.parent, type(other).__name__) > other

    def __ge__(self, other):
        return getattr(self.parent, type(other).__name__) >= other
