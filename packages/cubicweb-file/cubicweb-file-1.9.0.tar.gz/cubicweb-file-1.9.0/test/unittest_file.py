from cubicweb.devtools.testlib import CubicWebTC

from cubicweb import ValidationError, NoSelectableObject, Binary
from cubicweb.interfaces import IDownloadable


class FileTC(CubicWebTC):

    def setup_database(self):
        self.fobj = self.request().create_entity('File', data_name=u"foo.pdf",
                                                 data=Binary("xxx"),
                                                 data_format=self.mime_type)

    icon = 'text.ico'
    mime_type = u"text/plain"

    def test_idownloadable(self):
        idownloadable = self.fobj.cw_adapt_to('IDownloadable')
        self.assertEquals(idownloadable.download_data(), 'xxx')
        self.assertEquals(idownloadable.download_url(),
                          u'http://testing.fr/cubicweb/%s/%s?vid=download' % (
            self.fobj.__regid__.lower(), self.fobj.eid))
        self.assertEquals(idownloadable.download_content_type(), self.mime_type)

    def test_base(self):
        self.assertEquals(self.fobj.size(), 3)
        self.assertEquals(self.fobj.icon_url(),
                          'http://testing.fr/cubicweb/data/icons/'+self.icon)

    def test_views(self):
        self.vreg['views'].select('download', self.fobj._cw, rset=self.fobj.cw_rset)
        self.fobj.view('gallery')
        self.assertRaises(NoSelectableObject, self.fobj.view, 'image')
        self.assertRaises(NoSelectableObject, self.fobj.view, 'album')


class ImageTC(FileTC):
    icon = 'image_png.ico'
    mime_type = u"image/png"

    def setup_database(self):
        self.fobj = self.request().create_entity('File', data_name=u"foo.png", data=Binary("xxx"),
                                    data_format=self.mime_type)

    def test_views(self):
        self.vreg['views'].select('download', self.fobj._cw, rset=self.fobj.cw_rset)
        self.fobj.view('gallery')
        self.fobj.view('image')
        self.fobj.view('album')
        # XXX test thumbnail generation

if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
