'''
.. module:: typeinference
    :synopsis: Utility functions for inferring data types or type mappings.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import cPickle
import cStringIO
import re
import zlib
import datetime
import collections

import struqtural.utilities as util

#==============================================================================
#                                 Constants
#==============================================================================


DATE_SEP = r"\s*([-/., ])\s*"
MONTHS = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7,
          'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
TIME = r"(\d{1,2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?(?:\s*([ap])\.?[m]\.?)?"
BOOLEAN_VALUES = {"t":True, "f":False, "true":True, "false":False, '':None}


#==============================================================================
#                                 Attributes
#==============================================================================


date_expr = re.compile(DATE_SEP)
time_expr = re.compile(TIME, re.I)


#==============================================================================
#                                 Functions
#==============================================================================


def bool_(string):
    '''
    Determines the boolean representation of a given string.
    '''
    string = string.lower()
    if string not in BOOLEAN_VALUES:
        raise ValueError("no valid boolean value for specified string")
    else:
        return BOOLEAN_VALUES[string]


# This has been orphaned here, and will be moving to a new home at some point
# in the not too distant future.
def unique_name(data, prefix="data"):
    '''
    Generates a unique name for *data* based on the checksum of its serialized
    representation.
    
    :param data: The data for which the name is being generated.
    
    :param prefix: The string prefix to the unique numerical portion of the
        name.
    '''
    tmp = cStringIO.StringIO()
    cPickle.dump(data, tmp, protocol=2)
    # Now we need to generate a reasonable name from thin air.  The
    # checksum of the data should help here.
    return "{0}{1}".format(prefix, zlib.adler32(tmp.getvalue()))


def _find_year(year_string):
    '''
    Given a string representation of the year, return the most
    likely 4 digit year it represents. 
    '''
    year_value = int(year_string)
    if year_value <  100:
        if 2000 + year_value > datetime.date.today().year:
            return year_value + 1900
        else:
            return year_value + 2000
    else:
        return year_value


def date_(string, default_to_american=True):
    '''
    This takes the **vast** majority of commonly found string date
    representations and returns a datetime.date instance with the date
    specified in the string.
    
    I didn't know about dateutils when I wrote this, however this function
    will go head to head with pretty much any date parser.
    
    :param string: A string representing a particular date.
    
    :returns: A datetime.date instance with the date specified by *string*. 
    '''
    d = date_expr.split(string)
    if len(d) != 5:
        raise ValueError("invalid number of tokens in date string")
    elif not d[4].isdigit():
        raise ValueError("final token of date string must be numeric")
    elif d[0].isalpha() and d[2].isalpha():
        raise ValueError("only one token may be alphabetic")
    if d[0].isalpha():
        if d[0][:3] not in MONTHS:
            raise ValueError("month does not match known months") 
        elif not d[2].isdigit():
            raise ValueError("token must contain only digits")
        elif not (0 < len(d[2]) < 3):
            raise ValueError("day token must be one or two characters long")
        elif len(d[4]) not in (2, 4):
            raise ValueError("year token must be two or four characters long")
        else:
            # Colloquial date format
            day = int(d[2])
            month = MONTHS[d[0][:3]]
            year = _find_year(d[4])
    elif d[2].isalpha():
        if d[2][:3] not in MONTHS:
            raise ValueError("month does not match known months") 
        elif not d[0].isdigit():
            raise ValueError("token must contain only digits")
        elif not (0 < len(d[0]) < 3):
            raise ValueError("day token must be one or two characters long")
        elif len(d[4]) not in (2, 4):
            raise ValueError("year token must be two or four characters long")
        else:
            # Common business date format
            day = int(d[0])
            month = MONTHS[d[2][:3]]
            year = _find_year(d[4])
    elif d[0].isdigit() and d[2].isdigit():
        if len(d[0]) == 4:
            # ISO date
            day = int(d[4])
            month = int(d[2])
            year = _find_year(d[0])
        else:
            if (d[1] in " \t," and d[3] in " \t," or d[1] != d[3]):
                raise ValueError("match to date format is ambiguous")
            year = _find_year(d[4])
            # We need to figure out if it's M/D or D/M
            v1 = int(d[0])
            v2 = int(d[2])
            if v1 > 12 or (v2 < 13 and not default_to_american):
                # European format
                day = v1
                month = v2
            else:
                # American format
                day = v2
                month = v1
    else:
        raise ValueError("invalid characters in date string")
    # Minefield clear!
    return datetime.date(year, month, day)            
         

def time_(string):
    '''
    This takes the majority of commonly found string time representations and
    returns a datetime.time instance with the time specified in the string.
    
    :param string: A string representing a particular time.
    
    :returns: A datetime.time instance with the time specified by *string*. 
    '''
    t = time_expr.match(string)
    if not t:
        raise ValueError("invalid time string specified")
    hours = int(t.group(1))
    minutes = int(t.group(2))
    if t.group(3):
        seconds = int(t.group(3))
    else:
        seconds = 0
    if t.group(4) and t.group(4) in "pP":
        hours += 12
    return datetime.time(hours, minutes, seconds)


# I'll get around to this guy at some point, however there are so many formats
# a datetime string could be represented in, I need to generate a set of the
# most commonly observed varieties to make it even distantly efficient.
def to_datetime(string):
    '''
    Not yet implemented.
    '''
    raise NotImplementedError


def map_data_types(data, type_mappings=None, polymorphic_type=object,
                   no_type=type(None), default_type=None):
    '''
    Maps from an observed set of input types to a desired set of output types.
        
    :param data: The data to determine a type mapping for.
    
    :param type_mappings: A mapping from one data type to another.
    
    :param polymorphic_type: A special catch all data type for columns which
        contain more than one data type.
    
    :param no_type: If no types are identified for whatever reason (for
        instance if a particular column has all None values), the type that
        should be used for that column
    
    :param default_type: The new data type to use if the column contains only
        one type, for which no mapping is specified.
        
    :returns: A list of new types, corresponding to the mappings for the
        types identified in data, in column order.
    '''
    data_types = []
    columns = range(len(data[0]))
    type_set = lambda c: set(type(r[c]) for r in data if r)
    column_type_sets = [type_set(c) for c in columns]
    for types_ in column_type_sets:
        # First get the type of the column
        if len(types_) > 1:
            # If there's more than one type, we can't store the value using SQL
            # primitives.
            data_types.append(polymorphic_type)
        else:
            if types_:
                column_type = types_.pop()
            else:
                column_type = no_type
            type_name = column_type.__name__
            data_types.append(type_mappings.get(type_name, default_type))
    return data_types


TYPE_INFERENCE_FUNCTIONS = (bool_, int, float, date_, time_)


@util.sequences("type_inference_functions")
def infer_column_type(data, type_inference_functions=None, default=str,
                       missing_value=''):
    '''
    This performs individual column coersion for :func:`infer_table_types`.
    The type precedence order is determined by the *type_inference_functions*
    argument.  New types can be added to the precedence order, the only
    requirement is that the type coercion function raise a ValueError
    if it a given string is not of an acceptable form.
    
    :param data: The sequence of strings to be coerced to a type.
    
    :param type_inference_functions: A sequence of functions to apply in order
        to determine the most specific python type for data.  Any function
        that returns a value or raises a ValueError if the input is not of the
        correct form will work.
        
    :param default: The default type conversion function if no functions in
        *type_inference_function* apply.
        
    :param missing_value: The value that should be skipped when determining
        the correct type inference function.
    '''
    if not type_inference_functions:
        type_inference_functions = TYPE_INFERENCE_FUNCTIONS
    value = lambda x, y: x(y) if y != missing_value else None
    for type_ in type_inference_functions:
        try:
            for d in data:
                value(type_, d)
            else:
                return type_
        except ValueError:
            pass
    else:
        return default


def infer_table_types(data, *args, **kwargs):
    '''
    This deceptively simple looking function takes a tabular collection of
    string tokens and determines the most specific data type every member of
    any given column can be coerced to, then converts the tokens in that
    column to that type.
    '''
    columns = util.all_keys(data)
    column_types = []
    type_tuple = collections.namedtuple("Item", columns)
    for column in columns:
        column_data = [util.get(d, column) for d in data]
        column_types.append(infer_column_type(column_data, *args, **kwargs))
    return type_tuple._make(column_types)
        


@util.sequences("types")
def strings_to_types(data, types, missing_value=''):
    '''
    This performs a straightforward conversion of tabular string data to
    specified python types.
    
    :param data: Any table like data structure with cells comprised of string
        tokens.
    
    :param types: The type coercion functions which should be used for data. 
    
    :param missing_value: The string token value to automatically assign the
        object None and ignore for the purposes of type inference.
        
    :returns: A sequence of namedtuples with values corresponding to the
        converted contents of data.
    '''
    results = [list() for i in range(len(data))]
    columns = util.all_keys(data)
    for column in columns:
        converter = util.get(types, column)
        value = lambda x, y: x(y) if y != missing_value else None
        values = [value(converter, util.get(d, column)) for d in data]
        for (i, result) in enumerate(values):
            results[i].append(result)
    # Now that we've collected all the results
    item = collections.namedtuple("Item", columns)
    return [item._make(r) for r in results]
