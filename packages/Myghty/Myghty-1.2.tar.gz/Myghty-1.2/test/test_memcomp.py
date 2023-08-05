import sys, unittest
import myghty.exception
import testbase

class MemCompTester(testbase.ComponentTester):
    def failUnlessOutputEqual(self, component_src, output, msg=None):
        comp = self.makeMemoryComponent(component_src)
        self.runComponent(comp)
        self.failUnlessEqual(self.output, output, msg=msg)
        
class UnicodeMemoryComponentTests(MemCompTester):
    """Tests of in-memory components whose source is a unicode string
    """

    config = { 'encoding_errors': 'htmlentityreplace' }
    
    def testSimple(self):
        self.failUnlessOutputEqual(u"Howdy!", "Howdy!")
        
    def testUnicodeText(self):
        self.failUnlessOutputEqual(u"\xa4", '&curren;');

    def testUnicodeWrite(self):
        self.failUnlessOutputEqual("% m.write(u'\xa4')".decode('iso-8859-15'),
                                   '&euro;')
        
class DisabledUnicodeMemoryComponentTests(MemCompTester):
    """Tests of unicode in-memory components with disable_unicode=True
    """

    config = { 'disable_unicode': True }

    def testSimple(self):
        self.failUnlessOutputEqual(u"Howdy!", "Howdy!")
        
    def testUnicodeText(self):
        # raw text get encoded to utf-8, and output as such
        self.failUnlessOutputEqual(u"\u00a4", "\xc2\xa4")

    def testUnicodeWrite(self):
        # m.write()ing a unicode is an error under disable_unicode
        comp = self.makeMemoryComponent("% m.write(u'\xa4')".decode('iso-8859-15'))
        self.failUnlessRaisesWrappedError(UnicodeEncodeError, self.runComponent, comp)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
    unittest.main(testRunner=runner)
                
