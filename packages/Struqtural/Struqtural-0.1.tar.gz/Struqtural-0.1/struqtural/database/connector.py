'''
.. module:: connector
    :synopsis: Easy to use database connection manager.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>

.. data:: CONFIG_FILE

    ..
    
    |    The configuration file for system wide defaults.
    
.. data:: USER_CONFIG

    ..
    
    |    The configuration file for user specific configuration data.
'''


import os.path
import ConfigParser as cfg
import sqlalchemy as sa
import sqlalchemy.orm as orm
import struqtural.utilities as util


ENGINE = "engine"
CURRENT_ENGINE = "current engine"
PARAMETER_LISTS = "parameter lists"
PARAMETER_VALUES = "parameter values"
CONFIG_FILE = '../resources/sql_server.cfg'
USER_CONFIG = "~/.struqtural/sql_server.cfg"


#==============================================================================
#                                  Classes
#==============================================================================


class DatabaseConnector(object):
    '''
    A database connection management object.  Can maintain a configuration file
    for database connection information.  Configuration information is loaded
    in the following order:
    
    + Global configuration directives, loaded from the sql_server.cfg file 
        found in the resources directory of the struqtural source tree.
        
    + User configuration directives, loaded from the directory specified by
        USER_CONFIG if it exists.  These values overwrite global configuration
        directives.
        
    + Application configuration directives, loaded from the *config_file*
        referenced in the __init__ method.
    
    .. attribute:: config_file
    
        ..
        
        |    The default location to save connection parameters.
    
    .. attribute:: engine
        
        ..
        
        |    The database engine to use.
    
    .. attribute:: parameter_values
        
        ..
        
        |    The parameter values required to create a connection to the
        |    database. These typically include port, database name, username
        |    and password.
    
    .. attribute:: session
        
        ..
        
        |    the currently active Session instance.
        
    .. attribute:: metadata
        
        ..
        
        |    The SQL Alchemy MetaData object that will maintain schema
        |    information for all Session instances from this
        |    DatabaseConnector.
    '''

    #==========================================================================
    #                                Magic Methods
    #==========================================================================

    def __init__(self, config_file=None, autoconnect=True, metadata=None):
        '''
        :param config_file: The name of a file from which connection
            parameters should be loaded.  If specified, this will also set the
            *config_file* attribute of the DatabaseConnector instance.  If not
            specified, the *config_file* attribute of the DatabaseConnector
            instance will be set to the current user configuration location.
            
        :param autoconnect: If this evaluates to True, a connection will be
            established immediately upon instantiation.
            
        :param metadata: An existing :class:`sqlalchemy.schema.MetaData` object
            that should be used for connections from this connector. If
            *metadata* is already bound, that binding will be re-used when
            creating the local Session class.
        '''
        self._engine = None
        self._engine_configuration = {}
        self._parameter_values = {}
        system_config = self.load_configuration(CONFIG_FILE)
        # Next read configuration values from the caller's home directory if
        # any are present.
        user_config_file = os.path.expanduser(USER_CONFIG)
        if os.path.exists(user_config_file):
            user_config = self.load_configuration(user_config_file)
        else:
            user_config = None
        # If a specific configuration file was specified, load it now.
        if config_file and os.path.exists(config_file):
            self._config = self.load_configuration(config_file)
        else:
            self._config = user_config or system_config
        self.config_file = config_file or user_config_file
        self.metadata = metadata
        self.session = None
        self._Session = None
        if autoconnect:
            self.connect()

    def __repr__(self):
        return "DatabaseConnector(config_file={0})".format(self.config_file)

    #==========================================================================
    #                              Standard Methods
    #==========================================================================

    def _getengine(self):
        '''
        The engine portion of the URL used when establishing database
        connections.
        '''
        return self._engine

    def _setengine(self, new_engine):
        self._engine = new_engine
        self._config.set(CURRENT_ENGINE, new_engine)
        self._engine_configuration = {}
        if self._config.has_section(self._engine):
            engine_configuration = self._config.items(self._engine)
            self._engine_configuration.update(engine_configuration)

    def _delengine(self):
        if self._config.has_section(ENGINE):
            self._config.remove_section(ENGINE)
        self._engine = None

    def _getparameter_values(self):
        '''
        Values for engine URL parameters.
        '''
        return self._parameter_values

    def _setparameter_values(self, pvalues):
        self._parameter_values = {}
        self._parameter_values.update(pvalues)
        # Clear the previous parameter values
        if self._config.has_section(PARAMETER_VALUES):
            self._config.remove_section(PARAMETER_VALUES)
        self._config.add_section(PARAMETER_VALUES)
        for (key, value) in pvalues:
            self._config.set(PARAMETER_VALUES, key, value)

    def _delparameter_values(self):
        if self._config.has_section(PARAMETER_VALUES):
            self._config.remove_section(PARAMETER_VALUES)
        self.parameter_values = {}

    def _getengine_configuration(self):
        '''
        Engine specific URL parameter names.
        '''
        return self._engine_configuration

    def _setengine_configuration(self, evalues):
        self._engine_configuration = {}
        self._engine_configuration.update(evalues)
        if self._config.has_section(self._engine):
            self._config.remove_section(self._engine)
        self._config.add_section(self._engine)
        for (key, value) in evalues:
            self._config.set(self._engine, key, value)

    def _delengine_configuration(self):
        if self._config.has_section(self._engine):
            self._config.remove_section(self._engine)
        self._engine_configuration = {}

    engine = property(_getengine, _setengine, _delengine)
    parameter_values = property(_getparameter_values,
                                _setparameter_values,
                                _delparameter_values)
    engine_configuration = property(_getengine_configuration,
                                    _setengine_configuration,
                                    _delengine_configuration)

    @util.mutable_mappings("engine_args", "session_args")
    def connect(self, url=None, new_session=False, metadata=None,
                engine_args=None, session_args=None):
        '''
        Connects to the database.
        
        :param url: A connection URL to use in lieu of this DatabaseConnector's
            current configuration.
        
        :param new_session: If this evaluates to True, indicates a new session
            should be created, even if one already exists.
        
        :param metadata: An existing :class:`sqlalchemy.schema.MetaData` object
            that should be used for this connection and all future connections.
            If *metadata* is already bound, that binding will be re-used when
            creating the local :class:`sqlalchemy.orm.session.Session`.
        
        :param engine_args: Allows you to specify additional keyword arguments
            which should be passed when instantiating the
            :class:`sqlalchemy.engine.base.Engine`.
        
        :param session_args: Allows you to specify additional keyword
            arguments which should be passed when creating the
            :class:`sqlalchemy.orm.session.Session`.
        
        :returns: a :class:`sqlalchemy.orm.session.Session` instance.
        
        .. note::
            if the connection parameters for an external database are not
            specified, a memory-resident SQLite database is returned.
        '''
        if metadata is not None:
            self.metadata = metadata
        elif self.metadata is None:
            self.metadata = sa.MetaData()
        if not self._Session and not self.metadata.bind:
            parameters = {}
            parameters.update(self.engine_configuration)
            parameters.update(engine_args)
            if not url:
                if not self.engine:
                    url = "sqlite:///:memory:"
                else:
                    url = self._config.get(PARAMETER_LISTS, self.engine)
                    url = url.format(**self.parameter_values)                
            engine = sa.create_engine(url, **parameters)
            self._Session = orm.sessionmaker(bind=engine, **session_args)
            self.session = self._Session()
            self.metadata.bind = self.session.connection()
        elif not self._Session and self.metadata.bind:
            self._Session = orm.sessionmaker(bind=self.metadata.bind,
                                             **session_args)
            self.session = self._Session()
        else:
            con = self.session.connection()
            if new_session or not con or con.closed or con.invalidated:
                self._Session.configure(**session_args)
                self.session = self._Session()
                self.metadata = self.metadata or sa.MetaData()
                self.metadata.bind = self.session.connection()
        return self.session

    def load_configuration(self, config_file):
        '''
        Loads configuration information for this DatabaseConnector from a
        specified file.
        
        :param config_file: The file from which to load configuration
            information.
        
        :returns: The configuration parser which was loaded.
        '''
        config = cfg.SafeConfigParser()
        config.read(config_file)
        if config.has_section(PARAMETER_VALUES):
            self._parameter_values.update(config.items(PARAMETER_VALUES))
        if config.has_section(CURRENT_ENGINE):
            if config.has_option(CURRENT_ENGINE, ENGINE):
                self._engine = config.get(CURRENT_ENGINE, ENGINE)
        if self._engine and config.has_section(self._engine):
            self._engine_configuration.update(config.items(self._engine))
        return config

    def save_configuration(self, config_file=None):
        '''
        Saves the DatabaseConnector's current configuration to a file.
        
        :param config_file: The location where the configuration will be saved.
            If this is not specified, the configuration information will be
            saved in the location specified by this DatabaseConnector's
            *config_file* attribute.
        '''
        if not config_file:
            config_file = self.config_file
        self._config.write(config_file)
