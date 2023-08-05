'''
.. module:: file
    :synopsis: Loader subclasses which handle loading data from files.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import struqtural.utilities as util
import struqtural.loaders.loader as loader
import struqtural.processes.files as files
import struqtural.processes.language as lang


#==============================================================================
#                                  Classes
#==============================================================================


class DelimitedFileLoader(loader.CollectionLoader):
    '''
    Instantiates a new table in a database using information from a delimited
    file.
    '''

    def __init__(self, input_file, dialect=None, delimiter=None, *args,
                 **kwargs):
        '''
        :param input_file: The name of the file to parse, or an open buffer.
        
        :param name: The name of the table to create.
        
        :param dialect: The csv dialect of the file. 
        
        :param delimiter: The column delimiter character.
        
        .. note::
            if a dialect is specified, the delimiter parameter is ignored.
        '''
        try:
            with open(input_file, 'r+b') as in_:
                lines = [line for line in in_]
        except TypeError:
            # We probably got passed an open buffer
            lines = [line for line in input_file]
        data = files.parse_csv(lines, dialect, delimiter)
        super(DelimitedFileLoader, self).__init__(data, *args, **kwargs)
        

class XmlMultiLoader(loader.MultiLoader):
    '''
    Load an XML document.  generates a list of structures.
    
    .. attribute: properties
    
        ..
        
        |    A mapping from XML tag name to ObjectLoader instance.
    '''
    
    @util.mutable_mappings("primary_keys")  
    def __init__(self, input_file, connector=None, primary_keys=None,
                 table_prefix=None):
        formatter = files.SchemaFormatter(primary_keys=primary_keys)
        (tags, relationships) = files.parse_xml(input_file, formatter)
        if not connector:
            connector = loader.get_default_connector()
        def get_properties(tag):
            data = [dict(i) for i in tags[tag]]
            instance_name = lang.make_class_name(tag)
            primary_key = formatter.primary_key(tag)._fields
            if table_prefix:
                table_name = "_".join((table_prefix, instance_name))
            else:
                table_name = lang.plural(instance_name)
            return loader.CollectionLoader(data, primary_key, instance_name,
                                           connector, table_name)
        self.properties = dict((t, get_properties(t)) for t in tags)
        super(XmlMultiLoader, self).__init__(relationships)
        
