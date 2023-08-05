"""file/image gallery view

:organization: Logilab
:copyright: 2006-2009 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from logilab.mtconverter import xml_escape
from logilab.common.decorators import monkeypatch

from cubicweb import typed_eid
from cubicweb.view import EntityView
from cubicweb.selectors import implements
from cubicweb.web.views.basecontrollers import JSonController, xhtmlize

class GalleryView(EntityView):
    __regid__ = 'gallery'
    __select__ = implements('Image', 'File')

    def call(self):
        self._cw.add_js(('cubes.file.js', 'cubicweb.ajax.js'))
        self._cw.add_css('cubes.file.css')
        eid = typed_eid(self._cw.form.get('selected',self.cw_rset[0][0]))
        self.currently_displayed = eid
        for i in xrange(self.cw_rset.rowcount):
            self.cell_call(row=i, col=0)
        rset = self._cw.execute('Any X where X eid %(x)s', {'x': eid}, 'x')
        self.w(u'<div id="imageholder">')
        self.wview('primary', rset, row=0, col=0, initargs={'is_primary':False})
        self.w(u'</div>')
        self.w(u'<div class="imagegallery">')
        self.w(u'</div>')

    def cell_call(self, row, col):
         entity = self.cw_rset.complete_entity(row, col)
         if entity.__regid__ == 'Image':
             icon = xml_escape(entity.download_url()+'&small=true')
         else:
             icon = self._cw.external_resource('FILE_ICON')
         title = xml_escape(entity.dc_title())
         if entity.eid == self.currently_displayed:
             self.w(u'<a href="javascript:displayImg(%(eid)s)" title="%(title)s"><img id="img%(eid)s" '
                    u'class="selectedimg" alt="%(title)s" src="%(icon)s"/></a>'
               % {'eid':entity.eid, 'title':title,'icon':icon})
         else:
             self.w(u'<a href="javascript:displayImg(%(eid)s)" title="%(title)s"><img id="img%(eid)s" '
                    'alt="%(title)s" src="%(icon)s"/></a>'
               % {'eid':entity.eid, 'title':title,'icon':icon})


@monkeypatch(JSonController)
@xhtmlize
def js_get_image(self, eid):
    return self.view('primary', self._cw.eid_rset(eid), row=0, col=0, initargs={'is_primary': False})


class AlbumView(EntityView):
    __regid__ = 'album'
    __select__ = implements('Image')

    def call(self, nbcol=5):
        self._cw.add_css('cubes.file.css')
        lines = [[]]
        for idx in xrange(self.cw_rset.rowcount):
            if len(lines[-1]) == nbcol:
                lines.append([])
            lines[-1].append(self._make_cell(idx, 0))
        while len(lines[-1]) != nbcol:
            lines[-1].append(u'&#160;')
        self.w(u'<table class="album">')
        for line in lines:
            self.w(u'<tr>')
            self.w(u''.join(u'<td>%s</td>' % cell for cell in line))
            self.w(u'</tr>')
        self.w(u'</table>')

    def _make_cell(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        icon = xml_escape(entity.download_url()+'&small=true&noshadow=1')
        title = xml_escape(entity.dc_title())
        return (u'<a href="%(url)s" title="%(title)s"><img alt="%(title)s" src="%(icon)s"/></a>'
                % {'url':xml_escape(entity.absolute_url()), 'title':title,'icon':icon})

    def cell_call(self, row, col):
        self.w(self._make_cell(row, col))

class ImageAdaptedView(AlbumView):
    __regid__ = 'sameetypelist'
    __select__ = implements('Image')
