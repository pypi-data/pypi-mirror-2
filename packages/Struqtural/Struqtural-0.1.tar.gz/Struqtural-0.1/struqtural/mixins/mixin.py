'''
.. module:: mixin
    :synopsis: Base mixins providing core functionality for other mixins.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import struqtural.database as db

class Mixin(object):
    '''
    This base class provides simple installation and uninstallation
    functionality.
    '''
    
    @classmethod
    def _install(cls, target):
        '''
        Installs the mixin on an instance's class.
        
        :param target: The instance whose class should be modified.
        '''
        type_ = type(target)
        bases = type_.__bases__
        new_bases = tuple(m for m in cls.__bases__ if m not in bases)
        type_.__bases__ = new_bases + bases
        type_._old_bases = bases

    @classmethod
    def _uninstall(cls, target):
        '''
        Uninstalls the mixin from an instance's class.
        
        :param target: The instance whose class should be restored.
        '''
        type_ = type(target)
        old_bases = getattr(type_, "_old_bases", None)
        if old_bases:
            type_.__bases__ = type_._old_bases
            del type_._old_bases


class ColumnMetaDataMixin(Mixin):
    '''
    This mixin provides additional functionality for loading and unloading
    column metadata related mixins.
    
    .. attribute:: column_metadata
        
        ..
        
        |    The class which should be used to generate persistent column
        |    metadata. related to the target's table in the database.
    '''
    
    column_metadata = db.ColumnMetaData
    
    @classmethod
    def _install(cls, target):
        super(ColumnMetaDataMixin, cls)._install(target)
        connector = target.connector
        target.ColumnMetaData = db.column_metadata(target.table, connector,
                                                   cls.column_metadata,
                                                   cls.table_args)
    @classmethod
    def _uninstall(cls, target):
        db.get_table(target.ColumnMetaData).drop()
        del target.ColumnMetaData
        super(ColumnMetaDataMixin, cls)._uninstall(target)

    def column_metadata(self, *columns):
        return self.query(self.ColumnMetaData.name.in_(columns))