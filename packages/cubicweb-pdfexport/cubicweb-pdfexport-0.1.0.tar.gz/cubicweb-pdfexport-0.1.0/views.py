"""cubicweb-pdfexport views/forms/actions/components for web ui

:organization: LOGILAB S.A. (Paris, FRANCE)
:copyright: 2010 LOGILAB S.A. (Paris, FRANCE)
:contact: http://www.logilab.fr -- mailto:contact@logilab.fr
:license: GNU Lesser General Public License, v2.1 - http://www.gnu.org/licenses
"""

from xml.etree.cElementTree import ElementTree
from subprocess import Popen as sub
from StringIO import StringIO
from tempfile import NamedTemporaryFile

from logilab.mtconverter import xml_escape

from cubicweb.web import component
from cubicweb.web.views.basetemplates import TheMainTemplate

from cubes.pdfexport.xhtml2fo import ReportTransformer


class PdfViewComponent(component.EntityVComponent):
    __regid__ = 'pdfview'

    context = 'ctxtoolbar'

    def cell_call(self, row, col, view):
        entity = self.cw_rset.get_entity(row, col)
        url = entity.absolute_url(vid=view.__regid__, __template='pdf-main-template')
        iconurl = self._cw.build_url('data/pdf_icon.gif')
        label = self._cw._('Download page as pdf')
        self.w(u'<a href="%s" title="%s" class="toolbarButton"><img src="%s" alt="%s"/></a>' %
               (xml_escape(url), label, xml_escape(iconurl), label))

class PdfMainTemplate(TheMainTemplate):
    __regid__ = 'pdf-main-template'

    def call(self, view):
        """build the standard view, then when it's all done, convert xhtml to pdf
        """
        super(PdfMainTemplate, self).call(view)
        section = self._cw.form.pop('section', 'contentmain')
        pdf = self.to_pdf(self._stream, section)
        self._cw.set_content_type('application/pdf', filename='report.pdf')
        self.binary = True
        self.w = None
        self.set_stream()
        # pylint needs help
        self.w(pdf)

    def to_pdf(self, stream, section):
        # XXX see ticket/345282
        stream = stream.getvalue().replace('&nbsp;', '&#160;').encode('utf-8')
        xmltree = ElementTree()
        xmltree.parse(StringIO(stream))
        foptree = ReportTransformer(section).transform(xmltree)
        foptmp = NamedTemporaryFile()
        pdftmp = NamedTemporaryFile()
        foptree.write(foptmp)
        foptmp.flush()
        fopproc = sub(['/usr/bin/fop', foptmp.name, pdftmp.name])
        fopproc.wait()
        pdftmp.seek(0)
        return pdftmp.read()
