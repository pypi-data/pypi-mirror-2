import os, sys
import martian
import webob
import webob.exc
import webob.dec
from hurry import resource
from hurry.resource.wsgi import Middleware
from serf.hash import resource_hash

_default_library = 'index'
_default_resource = 'index.html'

class HurryResourcePlugin(object):
    def get_library_url(self, library):
        return path(library.name)

def configure():
    global _extension_to_content_type
    global _handlers
    _extension_to_content_type = {}
    _handlers = {}
    from serf import core, conf
    reg = martian.GrokkerRegistry()
    reg.grok('core', core)
    reg.grok('conf', conf)

    resource.register_plugin(HurryResourcePlugin())

    # load up all libraries registered through entry points
    library_names = []
    for library in resource.libraries():
        library_names.append(library.name)
        _handlers[library.name] = LibraryHandler(library)
    
    print "serf - publishing:", ", ".join(sorted(library_names))

    return reg

@webob.dec.wsgify
def core_app(request):
    needed = resource.NeededInclusions()
    request.environ['hurry.resource.needed'] = needed
    
    steps = request.path.split('/')
    steps = [step for step in steps if step != '']
    steps.reverse()
    if not steps:
        default_library_hash = get_library_hash(_default_library)
        if default_library_hash is None:
            raise webob.exc.HTTPNotFound()
        default_location = (
            request.application_url +
            '/' + _default_library +
            '/' + default_library_hash +
            '/' + _default_resource)
        raise webob.exc.HTTPFound(location=default_location)
    library = steps.pop()
    handler = _handlers.get(library)
    if handler is None:
        raise webob.exc.HTTPNotFound()
    library_hash = resource_hash(handler.library.path)
    if not steps:
        location = (
            request.application_url +
            '/' + library + 
            '/' + library_hash +
            '/' + _default_resource)
        raise webob.exc.HTTPFound(location=location)
    hash_step = steps.pop()

    if library_hash != hash_step:
        raise webob.exc.HTTPNotFound()
    return handler(request, steps)    

app = Middleware(core_app)

class UnknownLibrary(ValueError):
    pass

def get_library_hash(library):
    library_path = get_library_path(library)
    if library_path is None:
        return None
    return resource_hash(library_path)

def path(library, subpath=None):
    library_path = get_library_path(library)
    if library_path is None:
        raise UnknownLibrary()
    hash = resource_hash(library_path)
    result = '/' + library + '/' + hash
    if subpath is not None:
        result += '/' + subpath
    return result

_extension_to_content_type = {}

class Extension(object):
    def __init__(self, name, content_type):
        self.name = name
        self.content_type = content_type
        self.__grok_module__ = martian.util.caller_module()
              
class ExtensionGrokker(martian.InstanceGrokker):
    martian.component(Extension)

    def execute(self, extension, **kw):
                
        name = extension.name 
        if not name.startswith('.'):
            name = '.' + name
        _extension_to_content_type[name] = extension.content_type
        return True

_handlers = {}

class LibraryHandler(object):
    def __init__(self, library):
        self.library = library
        self.dependencies = {}

    def __call__(self, request, steps):
        # XXX should check for illegal paths
        local_path = '/'.join(reversed(steps))
        path = os.path.join(self.library.path, local_path)
        try:
            f = open(path, 'rb')
            data = f.read()
            f.close()
        except IOError:
            return webob.exc.HTTPNotFound()
        response = webob.Response()
        rest, ext = os.path.splitext(path)
        response.content_type = _extension_to_content_type.get(
            ext, 'text/plain')
        response.body = data

        # add any needed inclusions
        inclusions = self.dependencies.get(local_path)

        if inclusions is not None:
            needed = request.environ['hurry.resource.needed']
            for inclusion in inclusions:
                needed.need(inclusion)
        return response

# only reason to superclass this is to let it be grokkable properly
class Library(resource.Library):
    def __init__(self, *args, **kw):
        super(Library, self).__init__(*args, **kw)
        self.__grok_module__ = martian.util.caller_module()
        # XXX argh, subclassing breaks automagic setting of 'path',
        # recreate it
        self.path = os.path.join(caller_dir(), self.rootpath)

# total hack to be able to get the dir the resources will be in
def caller_dir():
    return os.path.dirname(sys._getframe(2).f_globals['__file__'])

class LibraryGrokker(martian.InstanceGrokker):
    martian.component(Library)
    martian.priority(10) # must run before dependency grokker
    
    def execute(self, library, **kw):
        _handlers[library.name] = LibraryHandler(library)
        return True

def get_library_path(name):
    try:
        return _handlers[name].library.path
    except KeyError:
        return None

class Dependency(object):
    def __init__(self, library, resourcepath, needs):
        self.library = library
        self.resourcepath = resourcepath
        self.needs = needs
        self.__grok_module__ = martian.util.caller_module()

class DependencyGrokker(martian.InstanceGrokker):
    martian.component(Dependency)

    def execute(self, dependency, **kw):
        _handlers[dependency.library.name].dependencies[
            dependency.resourcepath] = dependency.needs
        return True
