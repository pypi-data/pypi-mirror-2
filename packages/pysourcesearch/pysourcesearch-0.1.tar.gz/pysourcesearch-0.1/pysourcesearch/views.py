from catalog import get_metadata_factory, get_object_factory, get_catalog, factories
from repoze.catalog.catalog import ConnectionManager
from models import File, class_re, method_re

from pygments import highlight as pyg_highlight
from pygments.lexers import guess_lexer_for_filename, PythonLexer, HtmlLexer, XmlLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
import webob
from webob.exc import HTTPFound
from urllib import urlencode
from settings import packages

formatter = HtmlFormatter(style='colorful')

def highlight(obj):
    try:
        lexer = guess_lexer_for_filename(obj.filename, obj.contents)
    except ClassNotFound:
        ext = obj.filename.split('.')[-1]
        if ext in ('pt', 'cpt'):
            lexer = HtmlLexer()
        elif ext in ('cpy', 'py_tmpl'):
            lexer = PythonLexer()
        elif ext in ('zcml'):
            lexer = XmlLexer()

    return pyg_highlight(obj.contents, lexer, formatter)
    
class Paging(object):
    
    def __init__(self, request, numres):
        self.request = request
        self.numres = numres
        
    @property
    def page(self):
        return int(self.request.params.get('page', '1'))
        
    @property
    def pagesize(self):
        return int(self.request.params.get('pagesize', '10'))
        
    @property
    def pages(self):
        pages = []
        for num in range(0, (self.numres/self.pagesize)+1):
            pages.append(num+1)
        return pages
        
    @property
    def start(self):
        return (self.page-1) * self.pagesize
        
    @property
    def end(self):
        return ((self.page-1) * self.pagesize) + self.pagesize

def combined_list(one, two):
    """
    This can't be the best way!!! 
    XXX UGLY
    wish we could still use generators--weird
    the type of lists returned from catalog
    """
    res = []
    for item in one:
        res.append(item)
    for item in two:
        res.append(item)
    
    return res

def get_package(request):
    return request.params.get('package', packages.keys()[0])

def search(request):
    """
    try to query in this order::
    1. method(only if starts with "def")
    2. class(only if starts with "class")
    3. filename(if there is a '.' in the query)
    4. contents
    
    I know--many queries in one call possibly, but I think
    it's really the best way.
    """
    query = request.params.get('q', '').strip()
    selected_package = get_package(request)
    encoded = urlencode({'q' : query, 'package' : selected_package})
    man, cat = get_catalog(selected_package)
    numdocs = 0
    results = []

    if query:
        if query.startswith('def '): # method
            numdocs, results = cat.search(methods=query.strip('def').strip())
        elif query.startswith('class '): # query
            numdocs, results = cat.search(classes=query.strip('class').strip())
        elif '.' in query[-4:]: # has file extension
            numdocs, results = cat.search(filename=query, sort_index="filename")
            
        if numdocs != 1:
            n, r = cat.search(contents=query, sort_index="contents")
            numdocs += n
            results = combined_list(results, r)
            
    if numdocs == 1:
        # go straight to doc--I'm feeling lucky
        docid = [r for r in results][0]
        return HTTPFound(location=request.application_url + '/view/' + str(docid) + '?' + encoded)
            
    return {
        'numdocs' : numdocs, 
        'results' : results, 
        'get_metadata' : get_metadata_factory(cat), 
        'request' : request,
        'query' : encoded,
        'searched' : query and True or False,
        'paging' : Paging(request, numdocs),
        'packages' : packages.keys(),
        'selected_package' : selected_package
    }
    
def view_document(request):
    docid = int(request.matchdict['docid'])
    man, cat = get_catalog(req=request)
    metadata = cat.document_map.get_metadata(docid)
    obj = File(metadata['abspath'])
    man.close()
    return {
        'docid' : docid, 
        'context' : obj, 
        'metadata' : metadata, 
        'highlight' : highlight,
        'packages' : packages.keys(),
        'selected_package' : get_package(request)
    }
    

def pygments_colorful(request):
    response = webob.Response()
    response.write(formatter.get_style_defs('.highlight'))
    response.content_type = 'text/css'
        
    return response