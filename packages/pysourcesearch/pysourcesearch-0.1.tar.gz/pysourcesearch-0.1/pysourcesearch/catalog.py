from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager

from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.document import DocumentMap
from repoze.catalog.indexes.keyword import CatalogKeywordIndex

from repoze.bfg.log import make_stream_logger
log_file = open('pysourcesearch.log', 'a')
logger = make_stream_logger('pysourcesearch', log_file)

from models import File
from os import path
import os
import re

factories = {}
managers = {}
file_types = re.compile('^.*\.(py|txt|js|pt|cpy|cpt|css|rst|zcml|py_tmpl|ini|ini_tmpl|txt_tmpl|cfg|cfg_tmpl)$')

def relative_path(obj, path):
    return obj.path[len(path):].lstrip('/')

count = 0
def setup_catalogs(catalogs_location, package_groups, reindex=False, skipped_paths=None):
    for package_group in package_groups:
        global count
        count = 0
        name, package_group = package_group.split(':')
        logger.info('indexing the package %s at %s' % (name, package_group))
        filename = '%s.db' % name
        location = path.join(catalogs_location, filename)
        factory = FileStorageCatalogFactory(location, name)
        manager = ConnectionManager()
        catalog = factory(manager)

        if 'contents' not in catalog:
            catalog['contents'] = CatalogTextIndex('contents')
        if 'classes' not in catalog:
            catalog['classes'] = CatalogKeywordIndex('classes')
        if 'methods' not in catalog:
            catalog['methods'] = CatalogKeywordIndex('methods')
        if 'filename' not in catalog:
            catalog['filename'] = CatalogFieldIndex('filename')
        
        if not hasattr(catalog, 'document_map') or reindex:
            catalog.document_map = DocumentMap()
        
        if reindex:
            catalog.clear()
        
        def search_files(base):
            for file in os.listdir(base):
                abspath = path.join(base, file)
                if skipped_paths.match(file):
                    continue
                elif path.isfile(abspath):
                    if file_types.match(file):
                        docid = catalog.document_map.docid_for_address(abspath)
                        if not docid or reindex:
                            docid = catalog.document_map.add(abspath)
                            file_obj = File(abspath)
                            catalog.index_doc(docid, file_obj)
                            catalog.document_map.add_metadata(docid, {
                                'preview' : file_obj.preview,
                                'abspath' : abspath,
                                'relative_path' : relative_path(file_obj, package_group)
                            })
                            global count
                            count += 1
                            if count % 300 == 0:
                                logger.info('indexed %i items' % count)
                else:
                    search_files(abspath)
    
        search_files(package_group)
        manager.commit()
        manager.close()
    
        managers[name] = manager
        factories[name] = factory        
        
def get_object_factory(cat):
    
    def get_object(id):
        return File(cat.document_map.address_for_docid(id))
        
    return get_object
    
def get_metadata_factory(cat):
    def get_metadata(docid):
        return cat.document_map.get_metadata(int(docid))
        
    return get_metadata
    
def get_catalog(name=None, req=None):
    if (not name or not factories.has_key(name)) and req:
        name = req.params.get('package', factories.keys()[0])
        
    manager = managers[name]
    if not manager.conn.opened:
        manager.conn.open()
    return manager, factories[name](manager)
    
    