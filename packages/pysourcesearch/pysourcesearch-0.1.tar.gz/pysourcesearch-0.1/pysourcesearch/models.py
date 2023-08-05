from os import path

import re
class_re = re.compile('class\s(?P<class>.*)\(.*\):')
method_re = re.compile('def\s(?P<method>.*)\(.*\):')
# could index parameters...

class File(object):
    
    def __init__(self, path=None):
        self.path = path
        
    @property
    def contents(self):
        if hasattr(self, '_contents'):
            return self._contents
        else:
            fi = open(self.path)
            self._contents = fi.read()
            fi.close()
            
        return self._contents
        
    @property
    def classes(self):
        return class_re.findall(self.contents)
        
    @property
    def methods(self):
        return method_re.findall(self.contents)
        
    @property
    def preview(self):
        return self.contents[:350]
        
    @property
    def filename(self):
        return self.path.split(path.sep)[-1]

def FileFactory(request):
    from catalog import catalogs
    docid = int(request.matchdict['docid'])
    return File(catalogs['Plone'].document_map.get_metadata(docid)['abspath'])

class MyModel(object):
    pass

root = MyModel()

def get_root(request):
    return root
