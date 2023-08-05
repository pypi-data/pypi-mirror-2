import webob
import martian
import unittest
from hurry import resource
import re

import serf
import serf.tests

# XXX urgh, we have to use 'reg._grokker' to grok individual components
# reg.grok works most of the time but still gets confused as it's actually
# expecting to grok a module, not a component.
# now in real-world usage we'll be using the module grokker but it's
# still ugly.

class SerfTestCase(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_publish_library_resource(self):
        reg = serf.configure()

        library = serf.Library('library', 'testdata1')
        reg._grokker.grok('library', library)
        request = webob.Request.blank(serf.path('library', 'test.html'))
        response = request.get_response(serf.app)
        self.assertEquals('''\
<html>
<head>
</head>
<body>
<p>Hello world</p>
</body>
</html>
''', response.body)

    def test_publish_library_redirect(self):
        reg = serf.configure()

        library = serf.Library('library', 'testdata1')
        reg._grokker.grok('library', library)

        request = webob.Request.blank('/library')
        response = request.get_response(serf.app)

        self.assertEquals('302 Found', response.status)

        request = webob.Request.blank(response.location)
        response = request.get_response(serf.app)

        self.assertEquals('''\
<html>
<head>
</head>
<body>
<p>index.html</p>
</body>
</html>
''', response.body)


    def test_publish_root(self):
        reg = serf.configure()

        library = serf.Library('index', 'testdata1')
        reg._grokker.grok('library', library)

        request = webob.Request.blank('/')
        response = request.get_response(serf.app)

        self.assertEquals('302 Found', response.status)

        request = webob.Request.blank(response.location)
        response = request.get_response(serf.app)

        self.assertEquals('''\
<html>
<head>
</head>
<body>
<p>index.html</p>
</body>
</html>
''', response.body)

    def test_publish_library_notfound(self):
        reg = serf.configure()

        library = serf.Library('library', 'testdata1')
        reg._grokker.grok('library', library)

        request = webob.Request.blank('/unknownlibrary')
        response = request.get_response(serf.app)

        self.assertEquals('404 Not Found', response.status)

    def test_publish_wrong_hash(self):
        reg = serf.configure()

        library =  serf.Library('library', 'testdata1')
        reg._grokker.grok('library', library)

        request = webob.Request.blank('/library/unknownhash')
        response = request.get_response(serf.app)

        self.assertEquals('404 Not Found', response.status)

    def test_publish_resource_notfound(self):
        reg = serf.configure()

        library = serf.Library('library', 'testdata1')
        reg._grokker.grok('library', library)

        request = webob.Request.blank(serf.path('library', 'unknown.htm'))
        response = request.get_response(serf.app)

        self.assertEquals('404 Not Found', response.status)

    def test_standard_content_types(self):
        reg = serf.configure()
        library = serf.Library('library', 'testdata1')
        reg._grokker.grok('library', library)        
        
        request = webob.Request.blank(serf.path('library', 'test.html'))
        response = request.get_response(serf.app)
        self.assertEquals('text/html', response.content_type)
        request = webob.Request.blank(serf.path('library', 'test.json'))
        response = request.get_response(serf.app)
        self.assertEquals('application/json', response.content_type)
        request = webob.Request.blank(serf.path('library', 'test.css'))
        response = request.get_response(serf.app)
        self.assertEquals('text/css', response.content_type)
        request = webob.Request.blank(serf.path('library', 'test.js'))
        response = request.get_response(serf.app)
        self.assertEquals('text/javascript', response.content_type)
        # unknown content types are text/plain
        request = webob.Request.blank(serf.path('library', 'test.foo'))
        response = request.get_response(serf.app)
        self.assertEquals('text/plain', response.content_type)

    def test_extra_content_type(self):
        reg = serf.configure()

        foo_ext = serf.Extension('foo', 'application/foo')
    
        reg._grokker.grok('library', foo_ext)

        library = serf.Library('library', 'testdata1')
        reg._grokker.grok('library', library)

        request = webob.Request.blank(serf.path('library', 'test.foo'))
        response = request.get_response(serf.app)
        self.assertEquals('application/foo', response.content_type)

    def test_hurry_resource(self):
        reg = serf.configure()

        library = serf.Library('library', 'testdata1')
        test_inclusion = resource.ResourceInclusion(library, 'test.js')

        dep = serf.Dependency(library, 'needs.html', [test_inclusion])
    
        reg._grokker.grok('library', library)
        reg._grokker.grok('dep', dep)
        
        request = webob.Request.blank(serf.path('library', 'needs.html'))
        response = request.get_response(serf.app)
        self.assertEquals('''\
<html>
<head>
    <script type="text/javascript" src="/library/.../test.js"></script>

</head>
<body>
<p>I have needs!</p>
</body>
</html>
''', re.sub('/[^/]*/test.js', '/.../test.js', response.body))

        
def testsuite():
    suite = unittest.TestSuite()
    suite.addTests([
            unittest.makeSuite(SerfTestCase),
            ])
    return suite

