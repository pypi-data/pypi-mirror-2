'''
.. module:: units
    :synopsis: Mixin for providing unit-related functionality to structures.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import re
import quantities
import struqtural.utilities as util
import struqtural.database as db
import struqtural.mixins.mixin as mixin


#==============================================================================
#                                 Functions
#==============================================================================


def convert_unit_expression(expr):
    '''
    Performs basic validation on a string unit expression and returns a
    quantities unit expression object.
    
    :param expr: A string representing the units.  See rescale_by_units for
        a thorough explanation of exactly what is acceptable here.
    
    :returns: A quantities unit expression object.
    '''
    # Some basic sanity checking of the units string.  Not the prettiest
    # code in the world but not a critical part of the process either.
    # First verify that no illegal characters are present.
    if re.search(r"[^a-z0-9*/()\s]", expr) is not None:
        raise ValueError, "the unit string contains invalid characters."
    # Then verify that every unit name has a quantities unit, and if so
    # substitute it for evaluation.
    for result in re.findall(r"[a-z]+", expr):
        if hasattr(quantities, result):
            expr = re.sub(result, "quantities." + result, expr)
        else:
            raise AttributeError, "the specified unit type is undefined."
    return eval(expr)


@util.mutable_sequences("instances")
def rescale_by_units(instances, old_units, new_units, property_):
    '''
    Rescales the value of *property_* on *instances* according to the
    conversion ratio from old_units to new_units.  Units can be specified
    using quantities expression objects or intuitive strings, for example::
    
        "meter / second ** 2"
        "mile / hour"
        "kg / m ** 3"
    
    :param instances: The object(s) to be converted
    
    :param old_units: The original units of the instance's property.
    
    :param new_units: The new units for instance's property.
    
    :param property_: The property of instances to convert.
    '''
    if isinstance(old_units, str):
        old_units = convert_unit_expression(old_units)
    if isinstance(new_units, str):
        new_units = convert_unit_expression(new_units)
    scale_value = float(old_units.rescale(new_units))
    for instance in instances:
        rescale(instance, scale_value, property_)


def rescale(instance, scale, property_):
    '''
    Adjust the value of *property_* on *instance* by a factor of *scale*.
    
    :param instance: The object to be rescaled.
    
    :param scale: The ratio by which to rescale the value of instance's
        property.
    
    :param property_: The property of instance to convert.
    '''
    new_value = getattr(instance, property_) * scale
    setattr(instance, property_, new_value)


class ColumnUnitsMixin(mixin.ColumnMetaDataMixin):
    '''
    Provides functionality for setting and adjusting units.
    '''

    column_metadata = db.ColumnUnits

    def set_units(self, name, new_units=None):
        '''
        Sets the units for *name* to *new_units*.  Rescales the values in the
        column if units were previously present. Units can be specified by
        strings or quantities unit objects.
        
        :param name: The name of the column to which the units should be applied
        
        :param new_units: The column's new units        
        '''
        column = self.column_metadata(name)
        old_units = column.units
        if old_units is None:
            column.units = new_units
        else:
            if new_units != None:
                rescale_by_units(self, old_units, new_units, name)
            column.units = new_units

    def get_units(self, name):
        '''
        Retrieve the units for a given column.
        
        :param name: The column for which units should be retrieved.
        
        :returns: The column's units.
        '''
        return self.column_metadata(name).first().units

