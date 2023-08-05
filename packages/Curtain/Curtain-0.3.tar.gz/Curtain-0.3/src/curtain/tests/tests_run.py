from __future__ import with_statement

import unittest, functools, xml.sax, xml.sax.handler, cStringIO as stringio, tempfile
import difflib, os.path as op
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n import interpolate
from zope.interface import implements
import zope.component as component

import curtain, curtain.bfg
from curtain import ns

class _hashdict(dict):
    def __hash__(self):
        if not hasattr(self, '_hash'):
            setattr(self, '_hash', hash(self.items()))
        return self._hash

def _implements_attributes(x):
    # very partial
    return hasattr(x, 'items') and hasattr(x, 'getType')

class _Attributes(object):
    def __init__(self, attributes):
        self.__dct = dict(attributes)
    def __str__(self):
        return str(self.__dct)
    def __repr__(self):
        return repr(self.__dct)
    def __hash__(self):
        return hash(tuple(self.__dct.items()))
    def __eq__(self, other):
        return (isinstance(other, _Attributes) and
            self.__dct == other.__dct)

def _hasher(el):
    if _implements_attributes(el):
        return _Attributes(el)
    elif isinstance(el, dict):
        kwargs = _hashdict(
            (_hasher(k), _hasher(v))
            for k, v
            in el.items()
        )
    elif isinstance(el, (list, tuple)):
        return tuple([_hasher(x) for x in el])
    else:
        return el

class LoggerLine(object):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = _hasher(args)
        self.kwargs = _hasher(kwargs)
    def __str__(self):
        return '~ %s - %r - %r ~' % (self.name, self.args, self.kwargs)
    def __repr__(self):
        return '_LoggerLine(%r, %r, %r)' % (self.name, self.args, self.kwargs)
    def __eq__(self, other):
        return (self.name == other.name and
            self.args == other.args and
            self.kwargs == other.kwargs)
    def __hash__(self):
        return hash(self.name) + hash(self.args) + hash(self.kwargs)

def _logger_decorator(meth):
    @functools.wraps(meth)
    def decorated(self, *args, **kwargs):
        self.log.append(LoggerLine(meth.__name__, *args, **kwargs))
    return decorated

class LoggerContentHandler(xml.sax.handler.ContentHandler):
    def __init__(self, *args, **kwargs):
        xml.sax.handler.ContentHandler.__init__(self, *args, **kwargs)
        self.log = []
    @_logger_decorator
    def startDocument(self):
        pass
    @_logger_decorator
    def endDocument(self):
        pass
    @_logger_decorator
    def startElementNS(self, name, qname, attrs):
        pass
    @_logger_decorator
    def endElementNS(self, name, qname):
        pass
    @_logger_decorator
    def characters(self, content):
        pass
    @_logger_decorator
    def ignorableWhitespace(self, whitespace):
        pass
    @_logger_decorator
    def processingInstruction(self, target, data):
        pass
    @_logger_decorator
    def skippedEntity(self, name):
        pass
    @_logger_decorator
    def startPrefixMapping(self, prefix, uri):
        pass
    @_logger_decorator
    def endPrefixMapping(self, prefix):
        pass

class Tests(unittest.TestCase):
    def _compare(self, testname, testnum, log = True):
        # load the data of the test
        d = op.dirname(__file__)
        with open(op.join(d, testname + '.ct')) as f:
            source = f.read() % {'ns': ns}
        with open(op.join(d, '%s_%d.env' % (testname, testnum))) as f:
            env = eval(f.read())
        with open(op.join(d, '%s_%d.xml' % (testname, testnum))) as f:
            result = f.read()
        # execute the template
        lch1 = LoggerContentHandler()
        ct = curtain.Template(str_source = source.strip())
        self._location = curtain.Location()
        try:
            ct(lch1, env, location = self._location)
            # execute the expat parser
            lch2 = LoggerContentHandler()
            parser = xml.sax.make_parser()
            parser.setContentHandler(lch2)
            parser.setFeature(xml.sax.handler.feature_namespaces, 1)
            parser.parse(stringio.StringIO(result))
            # they should give the same result
            if lch1.log != lch2.log:
                s = difflib.SequenceMatcher(None, lch1.log, lch2.log)
                for tag, i1, i2, j1, j2 in s.get_opcodes():
                    if tag == 'delete' or tag == 'insert':
                        tag = 'replace'
                    if tag == 'equal':
                        for n in range(i2-i1):
                            print ' ', lch1.log[i1+n]
                    elif tag == 'replace':
                        for n in range(i2-i1):
                            print '<', lch1.log[i1+n]
                        for n in range(j2-j1):
                            print '>', lch2.log[j1+n]
                    else:
                        raise ValueError('tag = %r unknown' % tag)
                print '-' * 79
            self.assert_(lch1.log == lch2.log)
        except:
            if log:
                print '-' * 79
                print ct.source
                print '-' * 79
                for k, v in env.items():
                    if isinstance(v, curtain.Template):
                        print '-' * 79
                        print k
                        print '-' * 79
                        print v.source
                        print '-' * 79
            raise
    def testIdentity(self):
        self._compare('identity', 1)
    def testAttr(self):
        self._compare('attr', 1)
    def testCondition(self):
        self._compare('condition', 1)
        self._compare('condition', 2)
    def testLoop(self):
        self._compare('loop', 1)
        self._compare('content', 1)
    def testSkip(self):
        self._compare('skip', 1)
        self._compare('skip', 2)
    def testC(self):
        self._compare('c', 1)
    def testDefn(self):
        self._compare('defn', 1)
        self._compare('nested_defn', 1)
    def testMacro(self):
        self._compare('macro', 1)
    def testI18n(self):
        self._compare('i18n', 1)
    def testErrorPosition(self):
        self.assertRaises(ZeroDivisionError, lambda: self._compare('error', 1, log=False))
        self.assertEquals(self._location.current, (3, 4))
    def testAutoReload(self):
        # 'str' sources cannot use auto_reload
        self.assertRaises(Exception, lambda: curtain.Template(str_source = 'hello', auto_reload=True))
        # try autoreload
        f = tempfile.NamedTemporaryFile()
        sources = []
        for content in ['<?xml version="1.0"?><hello/>', '<?xml version="1.0"?><another><tag/></another>']:
            f.write(content)
            f.flush()
            f.seek(0)
            t = curtain.Template(file_source = f.name, auto_reload = True)
            sources.append(t.source)
            l1 = LoggerContentHandler()
            t(l1, {})
            parser = xml.sax.make_parser()
            l2 = LoggerContentHandler()
            parser.setContentHandler(l2)
            parser.setFeature(xml.sax.handler.feature_namespaces, 1)
            parser.parse(stringio.StringIO(content))
            self.assertEquals(l1.log, l2.log)
        self.assert_(isinstance(sources[0], str))
        self.assert_(isinstance(sources[1], str))
        self.assertNotEqual(sources[0], sources[1])
    def testBfg(self):
        f = tempfile.NamedTemporaryFile()
        content = '<?xml version="1.0"?><hello xmlns:c="%(ns)s" c:cont="hello"></hello>' % {'ns': ns}
        dct = {'hello': 'hello', 'context': None}
        result = '<?xml version="1.0"?><hello>hello</hello>'
        f.write(content)
        f.flush()

        parser = xml.sax.make_parser()
        l1 = LoggerContentHandler()
        parser.setContentHandler(l1)
        parser.setFeature(xml.sax.handler.feature_namespaces, 1)
        parser.parse(stringio.StringIO(result))

        r = curtain.bfg.CurtainRenderer(f.name)
        tmplresult = r({}, dct)
        parser = xml.sax.make_parser()
        l2 = LoggerContentHandler()
        parser.setContentHandler(l2)
        parser.setFeature(xml.sax.handler.feature_namespaces, 1)
        parser.parse(stringio.StringIO(result))

        self.assertEquals(l1.log, l2.log)

        r = curtain.bfg.CurtainRenderer('curtain.tests:hello.ct')
        tmpl2result = r({}, dct)
        parser = xml.sax.make_parser()
        l2 = LoggerContentHandler()
        parser.setContentHandler(l2)
        parser.setFeature(xml.sax.handler.feature_namespaces, 1)
        parser.parse(stringio.StringIO(result))

        self.assertEquals(l1.log, l2.log)

        r = curtain.bfg.CurtainRenderer('curtain.tests:hello_wrong.ct')
        try:
            tmpl2result = r({}, dct)
        except curtain.bfg.TemplateError, te:
            self.assertEquals(te.filename, 'curtain.tests:hello_wrong.ct')
            self.assertEquals(te.line, 3)
            self.assertEquals(te.column, 4)
            self.assert_(isinstance(te.inner_exception, ZeroDivisionError),
                "inner exception %r should be a ZeroDivisionError" % (te.inner_exception,))
        else:
            self.assert_(False, "should raise a TemplateError")

class FakeTranslationDomain(object):
    implements(ITranslationDomain)
    def __init__(self, domain):
        self.domain = domain
    def translate(self, msgid, mapping=None, context=None, target_language=None, default=None):
        return interpolate(u'[%s]%s_%r' % (self.domain, msgid, target_language), mapping)
component.provideUtility(FakeTranslationDomain(u'test'), name=u'test')

test_suite = unittest.TestLoader().loadTestsFromTestCase(Tests)

if __name__ == '__main__':
    unittest.main()
