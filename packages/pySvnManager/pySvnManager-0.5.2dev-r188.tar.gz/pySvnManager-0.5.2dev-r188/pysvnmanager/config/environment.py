"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

import pysvnmanager.lib.app_globals as app_globals
import pysvnmanager.lib.helpers
from pysvnmanager.config.routing import make_map
from pysvnmanager.model import init_model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()
    
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='pysvnmanager', paths=paths)

    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = pysvnmanager.lib.helpers
    
    # Setup cache object as early as possible
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])

    # Setup the SQLAlchemy database engine
    if 'sqlalchemy.url' in config:
        engine = engine_from_config(config, 'sqlalchemy.')
    else:
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///%(here)s/db/fallback.db' % config)

    init_model(engine)

    # Create database if not exists.
    if ( engine.url.drivername in ['sqlite'] and
         not os.path.exists( engine.url.database ) ):

        if not os.path.exists( os.path.dirname( engine.url.database ) ):
            os.makedirs( os.path.dirname( engine.url.database ) )

        # initialized database here.
        from pysvnmanager.model.meta import Session, metadata, Base
        Base.metadata.create_all(bind=Session.bind)

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    
    # By default, the tmpl_context (a.k.a 'c'), is no longer a AttribSafeContextObj.
    # This means accessing attributes that don't exist will raise an AttributeError.
    # To use the attribute-safe tmpl_context, add this line to the config/environment.py:
    config['pylons.strict_tmpl_context'] = False

    return config
