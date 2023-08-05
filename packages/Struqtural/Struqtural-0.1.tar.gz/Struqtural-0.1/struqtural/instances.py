'''
.. module:: instances
    :synopsis: Instance types and supporting functions.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import struqtural.utilities as util


#==============================================================================
#                                 Functions
#==============================================================================


@util.mutable_sets("excluded")
@util.iterables("attributes", "bases")
def unique_attributes(attributes=None, bases=None, excluded=None):
    '''
    Generates a set of unique attribute names, given a supplied list of
    attributes, a list of bases, and a list of excluded attributes.
    '''
    base_attributes = []
    observed = set()
    def get_iterable_unique(attributes_):
        for attribute in attributes_:
            if attribute not in observed and attribute not in excluded:
                observed.add(attribute)
                base_attributes.append(attribute)
    for base in bases:
        get_iterable_unique(getattr(base, "__attributes__", []))
    get_iterable_unique(attributes)
    return {"__attributes__":base_attributes}


@util.mutable_sequences("bases")
def create(attributes=None, bases=None, name=None, excluded=None):
    '''
    An Instance factory.
    
    :param attributes: An iterable of strings containing the names of all
        attributes possessed by this instance class.
    
    :param bases: The bases this instance class should inherit from.
    
    :param name: The name of the Instance being created.
    
    :param excluded: Attributes from parent Instances which should be excluded
        in the created Instance.
    
    :returns: An Instance class.
    '''
    class_attributes = unique_attributes(attributes, bases, excluded)
    if not class_attributes:
        raise ValueError("no attributes specified")
    # Everything appears to be in order, generate the instance
    if not name:
        if bases:
            name = bases[0].__name__
        else:
            name = "Instance"
    if any(issubclass(b, Instance) for b in bases):
        base_types = tuple(bases)
    else:
        base_types = tuple(bases + [Instance])
    return type(name, base_types, class_attributes)


#==============================================================================
#                                  Classes
#==============================================================================


class Instance(object):
    '''
    This is capable of flexibly representing almost anything.  As long as the
    value of __attributes__ is maintained, a great of functionality is provided
    "for free".
    
    .. attribute:: __attributes__
        
        ..
        
        |    a list of attribute names possessed by the class.  Used for a
        |    variety of things including checking equality, and creating string
        |    representations.
    '''

    # This should be here.  This is used to make the attributes of the Instance
    # easy to access at run-time.
    __attributes__ = tuple()

    #==========================================================================
    #                                Magic Methods
    #==========================================================================

    def __init__(self, *args, **kwargs):
        '''
        Positional arguments are matched with elements of __attributes__ by
        index. keyword arguments are applied directly, though they have
        no effect unless they correspond to names specified in __attributes__.
        '''
        super(Instance, self).__init__()
        for (index, arg) in enumerate(args):
            setattr(self, self.__attributes__[index], arg)
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        template = "{0}={1}"
        def value(x):
            attribute_value = getattr(self, x)
            if isinstance(attribute_value, basestring):
                attribute_value = '"{0}"'.format(attribute_value)
            return template.format(x, attribute_value)
        values = ", ".join(value(a) for a in self.__attributes__)
        return "{0}({1})".format(type(self).__name__, values)

    def __eq__(self, other):
        if not other:
            return False
        iseq = lambda x: getattr(self, x) == getattr(other, x)
        try:
            return all(iseq(a) for a in self.__attributes__)
        except AttributeError:
            return False
