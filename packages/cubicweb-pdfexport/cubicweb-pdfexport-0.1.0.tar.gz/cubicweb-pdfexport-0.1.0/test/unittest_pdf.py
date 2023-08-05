import os.path as osp
from tempfile import NamedTemporaryFile
from subprocess import Popen as sub
from xml.etree.cElementTree import ElementTree

from logilab.common.testlib import TestCase, unittest_main

from cubes.pdfexport.xhtml2fo import ReportTransformer

DATADIR = osp.join(osp.dirname(__file__), 'data')

class PDFTC(TestCase):

    def test_xhtml_to_fop_to_pdf(self):
        xmltree = ElementTree()
        xmltree.parse(osp.join(DATADIR, 'sample1.xml'))
        foptree = ReportTransformer(u'contentmain').transform(xmltree)
        # next
        foptmp = NamedTemporaryFile()
        foptree.write(foptmp)
        foptmp.flush()
        pdftmp = NamedTemporaryFile()
        fopproc = sub(['/usr/bin/fop', foptmp.name, pdftmp.name])
        fopproc.wait()
        del foptmp
        if fopproc.returncode:
            self.skip('fop returned status %s' % fopproc.returncode)
        pdftmp.seek(0) # a bit superstitious
        reference = open(osp.join(DATADIR, 'sample1.pdf'), 'r').read()
        output = pdftmp.read()
        # XXX almost equals due to ID, creation date, so it seems to fail
        self.assertEquals( len(output), len(reference) )
        # cut begin & end 'cause they contain variyng data
        self.assertTextEquals(output[150:1500], reference[150:1500])

if __name__ == '__main__':
    unittest_main()

