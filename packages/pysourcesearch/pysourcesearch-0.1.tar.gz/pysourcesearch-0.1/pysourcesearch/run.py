from os import path
from repoze.bfg.configuration import Configurator
from models import get_root
from catalog import setup_catalogs

SETTINGS = {}
import re

def format_list(string):
    return [s.strip() for s in string.strip().splitlines() if s.strip() not in ('')]

def app(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    global SETTINGS
    SETTINGS = settings
    
    SETTINGS['package_groups'] = format_list(settings['package_groups'])
    SETTINGS['package_descriptions'] = format_list(settings.get('package_descriptions', ''))
    SETTINGS['catalogs_location'] = settings['catalogs_location']
    
    zcml_file = settings.get('configure_zcml', 'configure.zcml')
    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()
    config.load_zcml(zcml_file)
    config.end()
    
    skipped_paths = format_list(settings.get('skipped_paths', ''))
    skipped_paths = skipped_paths and re.compile('(%s)' % '|'.join(skipped_paths))
    
    reindex = settings.get('reindex', 'True').lower() == 'true' and True or False
    
    setup_catalogs(
        SETTINGS['catalogs_location'], 
        SETTINGS['package_groups'], 
        reindex=reindex, 
        skipped_paths=skipped_paths
    )
    
    return config.make_wsgi_app()
