
from pysmvt import db, settings, modimport
from pysmvt.utils import tb_depth_in
from sqlalchemy import engine_from_config, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

try:
    import elixir
except ImportError:
    pass

class SQLAlchemyContainer(object):
    
    def __init__(self):
        self.engine = engine_from_config(dict(settings.db), prefix='')
        self.meta = MetaData()
        self.Session = scoped_session(sessionmaker(bind=self.engine))
    
    def get_session(self):
        return self.Session()
        
class SQLAlchemyApp(object):
    """
        Creates an Sqlalchemy Engine and Metadata for the application
        
        Sets up thread-local sessions and cleans them up per request
    """
    def __init__(self, application):
        self.application = application
        self.container = SQLAlchemyContainer()
        db._push_object(self.container)
        db.sess = self.container.Session
        self.loadmodels()
    
    def start_request(self):
        pass
    
    def __call__(self, environ, start_response):
        if environ.has_key('pysapp.callable_dispatch'):
            self.callable_dispatch(environ['pysapp.callable_dispatch'])
            return
        if environ.has_key('paste.registry'):
            environ['paste.registry'].register(db, self.container)
        self.start_request()
        environ['sqlalchemy.sess'] = db.sess
        try:
            return self.application(environ, start_response)
        finally:
            del environ['sqlalchemy.sess']
            self.end_request()
    
    def console_dispatch(self, callable, environ=None):
        self.start_request()
        try:
            self.application.console_dispatch(callable, environ)
        finally:
            self.end_request()
    
    def callable_dispatch(self, callable, environ=None):
        self.console_dispatch(callable, environ)
        
    def end_request(self):
        db.Session.remove()
    
    def loadmodels(self):
        for module in settings.modules.keys():
            try:
                modimport('%s.model.orm' % module)
            except ImportError:
                # check the exception depth to make sure the import
                # error we caught was just .model or .model.orm missing
                _, _, tb = sys.exc_info()
                # 3 = .model wasn't found
                #print traceback_depth(tb)
                if traceback_depth(tb) in (3,):
                    pass
                else:
                    raise

class ElixirApp(SQLAlchemyApp):
    """
    loading models for elixir is a little complicated because Elixir
    entities can inherit from other entities in other Application
    Module's models.  At the same time, all Entities have to be
    setup using setup_all() before the sqlalchemy metadata is correct,
    which is required in order to manually add indexes, etc. after
    an Elixir entity sets up the metadata.  The solution is to split
    the model into `orm` code and `metadata` code and calling
    setup_all() between loading the two.
    """

    def loadmodels(self):
         # load all the ORM objects
        self.loadorm()
    
        # now setup ORM metadata
        elixir.setup_all()
    
        # now load metadata
        self.loadmetadata()
    
    def loadorm(self):
        for module in settings.modules.keys():
            try:
                modimport('%s.model.orm' % module)
            except ImportError:
                # 3 = .model wasn't found, which is ok.  Any other depth
                # means a different import error, and we want to raise that
                if not tb_depth_in(3):
                    raise
    
    def loadmetadata(self):
        for module in settings.modules.keys():
            try:
                modimport('%s.model.metadata' % module)
            except ImportError:
                # 3 = .model wasn't found, which is ok.  Any other depth
                # means a different import error, and we want to raise that
                if not tb_depth_in(3):
                    raise