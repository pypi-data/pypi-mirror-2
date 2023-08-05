'''
.. module:: numeric
    :synopsis: Mixins to provide NumPy related functionality to structures.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import numpy as np
import struqtural.database as db
import struqtural.mixins.mixin as mixin


class NumericMixin(mixin.Mixin):
    
    def as_numpy_array(self, select=None):
        '''
        Provides a numpy array representation of the data in the table.
        
        
        :param select: A specific select statement limiting the scope of the
            resulting array.
        
        :returns: A compact local array of instances
        
        :rtype: numpy record array
        '''
        if select is not None:
            if hasattr(select, "statement"):
                select = select.statement
            columns = getattr(select, "columns")
        else:
            columns = self.columns
        template = [db.record_tuple(c) for c in columns]
        instances = [tuple(row) for row in select.all()]
        return np.array(instances, dtype=template)

