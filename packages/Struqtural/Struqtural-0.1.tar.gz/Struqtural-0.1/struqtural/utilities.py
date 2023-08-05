'''
.. module:: utilities
    :synopsis: A big grab basket of miscellaneous functions designed to
        simplify the rest of the code base.  Of particular note are the
        type-coercing functions and their associated decorators, which are
        used liberally in the code base.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import decorator
import inspect
import collections
import copy
from itertools import chain


def iter_(variable):
    '''
    Provides an iterator for objects with or without an __iter__ function.
    Strings are treated as atomic units, rather than arrays of characters,
    thus if a single string were passed to this function, the iterator would
    be one element long, returning the original string the first time the
    next method was called.
    '''
    try:
        if variable is None:
            variable = tuple()
        if not isinstance(variable, basestring):
            return iter(variable)
    except TypeError:
        pass
    return iter((variable,))


def len_(variable):
    '''
    Provides a length for objects with or without a __len__ function.  Strings
    are treated as atomic units, rather than arrays of characters, thus if a
    single string were passed to this function, the return value would be 1. 
    '''
    try:
        if not isinstance(variable, basestring):
            return len(variable)
    except TypeError:
        pass
    return 1



def make_hashable(variable):
    '''
    Checks to see if variable is an unhashable type, and if so, converts it to
    its nearest hashable representation.  For sets, this mean conversion to a
    frozenset, for lists it means conversion to a tuple and for dictionaries it
    means conversion to a tuple of (key, value) tuples.
    
    :param variable: The original variable.
    
    :returns: The hashable form of *variable*
    '''
    if isinstance(variable, set):
        return frozenset(variable)
    elif isinstance(variable, list):
        return tuple(variable)
    elif isinstance(variable, dict):
        return tuple(variable.iteritems())
    else:
        return variable


def as_sequence(variable):
    '''
    Takes almost anything and returns a tuple.  If a tuple is passed, it is
    returned unchanged.  Otherwise, the variable is converted to a tuple
    using fairly intuitive logic.  If a variable is supplied that evaluates
    to False in a boolean context, an empty tuple is returned. Non-iterable
    variables are handled smoothly.
    
    :param variable: The original variable.
    
    :returns: The closest possible sequence representation of *variable*.
    '''
    is_sequence = isinstance(variable, collections.Sequence)
    is_string = isinstance(variable, basestring)
    if is_sequence and not is_string:
        return variable
    if variable is None:
        return tuple()
    return tuple(iter_(variable))


def as_immutable_sequence(variable):
    '''
    Takes almost anything and returns a tuple.  If a tuple is passed, it is
    returned unchanged.  Otherwise, the variable is converted to a tuple
    using fairly intuitive logic.  If a variable is supplied that evaluates
    to False in a boolean context, an empty tuple is returned. Non-iterable
    variables are handled smoothly.
    
    :param variable: The original variable.
    
    :returns: The closest possible immutable sequence representation of
        *variable*.
    '''
    variable = as_sequence(variable)
    if not isinstance(variable, collections.MutableSequence):
        return variable
    return tuple(variable)


def as_mutable_sequence(variable):
    '''
    Takes almost anything and returns a list.  If a list is passed, it is
    returned unchanged.  Otherwise, the variable is converted to a list
    using fairly intuitive logic.  If a variable is supplied that evaluates
    to False in a boolean context, an empty list is returned. Non-iterable
    variables are handled smoothly.
    
    :param variable: The original variable.
    
    :returns: The closest possible mutable sequence representation of
        *variable*.
    '''
    if isinstance(variable, collections.MutableSequence):
        return variable
    if variable is None:
        return []
    return list(iter_(variable))


def as_set(variable):
    '''
    Takes almost anything and returns a set.  If some variant of a set is
    passed, it is returned unchanged.  Otherwise, the variable is converted
    to a set using fairly intuitive logic.  If a variable is supplied that
    evaluates to False in a boolean context, an empty frozenset is returned.
    Common unhashable types like lists, dictionaries and sets in variable are
    converted to hashable equivalents. Non-iterable variables are handled
    smoothly. 
    
    :param variable: The original variable.
     
    :returns: The closest possible set representation of *variable*.
    '''
    
    is_mutable_set = isinstance(variable, collections.MutableSet)
    is_set = isinstance(variable, collections.Set)
    if is_set and not is_mutable_set:
        return variable
    if variable is None:
        return frozenset()
    try:
        result = frozenset(iter_(variable)) 
    except TypeError:
        # If we need this, it's probably because we're being passed an
        # unhashable type.  Try to convert all of its sub-elements to tuples.
        result = frozenset(tuple(v) for v in iter_(variable))
    return result


def as_mutable_set(variable):
    '''
    Takes almost anything and returns a set.  If some variant of a set is
    passed, it is returned unchanged.  Otherwise, the variable is converted
    to a set using fairly intuitive logic.  If a variable is supplied that
    evaluates to False in a boolean context, an empty set is returned. Common
    unhashable types like lists, dictionaries and sets in variable are
    converted to hashable equivalents. Non-iterable variables are handled
    smoothly. 
    
    :param variable: The original variable.
    
    :returns: The closest possible set representation of *variable*.
    '''
    if isinstance(variable, collections.MutableSet):
        return variable
    if variable is None:
        return set()
    try:
        result = set(iter_(variable)) 
    except TypeError:
        # If we need this, it's probably because we're being passed an
        # unhashable type.  Try to convert all of its sub-elements to tuples.
        result = set(tuple(v) for v in iter_(variable))
    return result
        

def as_mutable_mapping(variable, default_value=None):
    '''
    Takes almost anything and returns a dictionary which is as close of an
    approximation to the original as possible.  If a dictionary or iterable of
    length 2 tuples is supplied, the dictionary returned is precisely what you
    would expect.  If an iterable of objects with no or variable length is
    supplied, a dictionary is created with keys from the iterable, all set to
    the value *default*.  If a variable is supplied that evaluates to False in
    a boolean context, an empty dictionary is returned.  Common unhashable
    types like lists, dictionaries and sets in variable are converted to
    hashable equivalents.  Non-iterable variables are handled smoothly. 
    
    :param variable: The original variable.
    
    :param default_input: An alternate variable to use, in the event that
        *variable* is not specified for whatever reason.
    
    :param default: The default value applied to keys when no value is
        specified.
    
    :returns: The closest possible dictionary representation of *variable*.
    '''
    if isinstance(variable, collections.MutableMapping):
        return variable
    if variable is None:
        variable = dict()
    pairing = lambda x: len(x) == 2 and not isinstance(x, basestring)
    if all(pairing(v) for v in iter_(variable)):
        # We were passed an iterable of key/value pairs in tuples, avoid
        # failure due to unhashable types as keys.
        item = lambda i: (make_hashable(i[0]), i[1])
    else:
        # Who knows what we were passed... Just make it a dict
        item = lambda i: (make_hashable(i), default_value) 
    return dict(item(i) for i in iter_(variable))


def expander(callable_, collection):
    '''
    Takes a callable object and calls it repeatedly with arguments generated
    by performing expansion on elements from the iterable collection.  This is
    similar to the starmap function, although expander supports both
    positional and keyword argument expansion.
    
    :param callable_: The callable object which should receive arguments from
        items in the collection.
    
    :param collection: an iterable providing iterables of positional or keyword
        arguments.
    '''
    for item in collection:
        if isinstance(item, dict):
            yield callable_(**item)
        else:
            yield callable_(*item)


def descendant(class_or_instance, class_):
    '''
    This function takes a class or instance and determines if it is either a
    subclass or instance of *class_*. This is useful if you allow either a class
    or an instance to serve as a template for a function.
    
    :param class_or_instance: The class or instance to check against *class_*
    
    :param class\_: The class being checked for an inheritance relationship.
    
    :returns: Boolean True if *class_or_instance* is in some way a descendant
        of *class_*, False otherwise.
    '''
    if type(class_or_instance) == type:
        return issubclass(class_or_instance, class_)
    else:
        return isinstance(class_or_instance, class_)



def wrap(f, wrapping_function, *args):
    '''
    Wraps a function *f* in *wrapping_function*.
    '''
    argspec = inspect.getargspec(f)
    without_defaults = len(argspec.args) - len(argspec.defaults or [])
    f._args = {}
    f._varkw = []
    f._arg_defaults = (None,) * without_defaults + (argspec.defaults or tuple())
    for arg in args:
        if arg in argspec.args:
            f._args[arg] = argspec.args.index(arg)
        else:
            if argspec.keywords:
                f._varkw.append(arg)  
    return decorator.decorator(wrapping_function, f)


def return_as_output(output_f):
    '''
    Returns a function that wraps another function, mutating arguments
    specified by \*args and \*\*kwargs by passing them through *output_f*.
    '''
    def func(f, *args, **kwargs):
        new_args = list(args)
        for (dict_name, index) in f._args.items():
            if len(args) > index:
                new_args[index] = output_f(args[index])
            else:
                d = f._arg_defaults[index]
                kwargs[dict_name] = output_f(kwargs.pop(dict_name, d))
        for dict_name in f._varkw:
            kwargs[dict_name] = output_f(kwargs.pop(dict_name, None))
        try:
            return f(*new_args, **kwargs)
        except Exception:
            # Help keep our stack traces clean!
            raise
    return func


def return_as_defaults(f, *args, **kwargs):
    '''
    Returns a function that wraps another function, mutating arguments
    specified by \*args and \*\*kwargs by replacing them with the defaults
    for that argument if their value evaluates to None.
    '''
    new_args = list(args)
    for (default_name, index) in f._args.items():
        if len(args) > index:
            if args[index] is None:
                new_args[index] = get_default(default_name, f.__name__)
        else:
            default = get_default(default_name, f.__name__)
            kwargs[default_name] = kwargs.pop(default_name, default)
    for default_name in f._varkw:
        default = getattr(defaults_, default_name, None)
        kwargs[default_name] = kwargs.pop(default_name, default)
    return f(*new_args, **kwargs)


def defaults(*args):
    '''
    Decorator replacing arguments specified in *args* with defaults if they
    evaluate to None.
    '''
    return lambda f: wrap(f, return_as_defaults, *args)


default_defaultdict = lambda: collections.defaultdict(lambda: None)
defaults_ = collections.defaultdict(default_defaultdict)


def get_default(arg, f=None):
    '''
    Attempts to get the default argument value for a function, falling back to
    the global default argument value if no function is specified or no
    function default exists for the argument.
    
    :param arg: The argument name to get the default for.
    
    :param f: The function name to get this default for.
    '''
    arg_default = defaults_[arg]
    return copy.copy(arg_default[f] or arg_default[None])


def set_default(default_, arg, f=None):
    '''
    Sets the default argument value.
    
    :param arg: the argument name this default should be applied to.
    
    :param f: The function this default should be applied to.
    '''
    defaults_[arg][f] = default_


def mutable_sequences(*args):
    '''
    Decorator that guarantees that the named arguments will be mutable
    sequences.
    '''
    as_lists = return_as_output(as_mutable_sequence)
    return lambda f: wrap(f, as_lists, *args)


def sequences(*args):
    '''
    Decorator that guarantees that the named arguments will be sequences.
    '''
    as_tuples = return_as_output(as_sequence)
    return lambda f: wrap(f, as_tuples, *args)


def mutable_mappings(*args):
    '''
    Decorator that guarantees that the named arguments will be mutable
    mappings.
    '''
    as_dicts = return_as_output(as_mutable_mapping)
    return lambda f: wrap(f, as_dicts, *args)


def mutable_sets(*args):
    '''
    Decorator that guarantees that the named arguments will be mutable sets.
    '''
    as_sets = return_as_output(as_mutable_set)
    return lambda f: wrap(f, as_sets, *args)


def iterables(*args):
    '''
    Decorator that guarantees that the named arguments will be iterable.
    '''
    as_iterables = return_as_output(iter_)
    return lambda f: wrap(f, as_iterables, *args)


def all_keys(dicts):
    '''
    Return a list containing all keys observed in *dicts*.
    
    :param dicts: An iterable of mappings.
    '''
    seen = set()
    results = []
    for result in chain.from_iterable(keys(d) for d in dicts):
        if result not in seen:
            results.append(result)
            seen.add(result)
    return results


def keys(thing):
    '''
    Return a set of keys for *thing*.  Allows dictionaries and namedtuples to
    be used interchangeably with less hassle. 
    '''
    if isinstance(thing, collections.Mapping):
        return thing.keys()
    else:
        # To ease working with defaultdicts
        return thing._fields


def get(thing, key):
    '''
    Returns an attribute or mapped value of *thing* represented by *key*.
    Allows dictionaries and namedtuples to be used interchangeably with less
    hassle.
    '''
    if isinstance(thing, collections.Mapping):
        return thing.get(key)
    else:
        return getattr(thing, key)


# @deprecated: will be replaced by dicts_to_namedtuples eventually.
def dicts_to_lists(dicts, key_order):
    '''
    Converts *dicts* to a tabular list representation with key values for
    entries occuring in *key_order*.
    
    :param dicts: An iterable of mappings.
    
    :param key_order: A sequence of key_names specifying the order dictionary
        key values should appear in the generated sequences.
        
    :returns: List of lists corresponding to *dicts*, with each list
        having values corresponding to values from entries in *dicts*,
        occurring in key order.
    '''
    values = lambda r: [r.get(p) for p in key_order]
    return [values(d) for d in dicts]


def dicts_to_namedtuples(dicts):
    '''
    Converts *dicts* to a named tuple representation.
    
    :param dicts: An iterable of mappings.
        
    :returns: Sequence of namedtuples with values corresponding to *dicts*.
    '''
    keys = all_keys(dicts)
    item = collections.namedtuple("Item", keys)
    values = lambda d: [d.get(k) for k in keys]
    return [item(*values(d)) for d in dicts]


# @deprecated: only used in one place and not terribly useful 
def from_args(name, kwargs, args=None): 
    value = kwargs.pop(name, None)
    if not value:
        if args:
            value = args.pop(0)
    return value


def split_dict(dict_, set_):
    '''
    Partitions a dictionary into two disjoint sub-dictionaries.
    
    :param dict_: The original dictionary.
    
    :param set_: A set of keys used to form the disjoint dictionary.
    '''
    new_dict = {}
    old_dict = {}
    for (key, value) in dict_.items():
        if key in set_:
            new_dict[key] = value
        else:
            old_dict[key] = value
    return (old_dict, new_dict)


def get_args(f):
    '''Return the arg names of a function.'''
    return set(inspect.getargspec(f).args)


# I dislike this, and it will probably go away in favor of something more
# elegant, as soon as I figure out what that is.
def is_instrumented(class_):
    '''Hack to determine if a class has been instrumented by Sql Alchemy.'''
    return hasattr(class_, "_sa_class_manager")
