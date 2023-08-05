"""Primary views for blogs

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

from logilab.mtconverter import xml_escape

from cubicweb.utils import UStringIO
from cubicweb.selectors import implements
from cubicweb.web import uicfg, component
from cubicweb.web.views import primary, workflow

_pvs = uicfg.primaryview_section
_pvs.tag_attribute(('Blog', 'title'), 'hidden')
_pvs.tag_attribute(('Blog', 'rss_url'), 'hidden')
_pvs.tag_attribute(('BlogEntry', 'title'), 'hidden')
_pvs.tag_object_of(('*', 'entry_of', 'Blog'), 'hidden')
_pvs.tag_subject_of(('BlogEntry', 'entry_of', '*'), 'relations')

_pvdc = uicfg.primaryview_display_ctrl
_pvdc.tag_attribute(('Blog', 'description'), {'showlabel': False})

_abaa = uicfg.actionbox_appearsin_addmenu
_abaa.tag_object_of(('*', 'entry_of', 'Blog'), True)

_afs = uicfg.autoform_section
_afs.tag_subject_of(('BlogEntry', 'entry_of', 'Blog'), 'main', 'attributes')


class BlogPrimaryView(primary.PrimaryView):
    __select__ = implements('Blog')

    def render_entity_relations(self, entity):
        super(BlogPrimaryView, self).render_entity_relations(entity)
        rset = entity.related('entry_of', 'object')
        if rset:
            strio = UStringIO()
            self.paginate(self._cw, w=strio.write, page_size=10, rset=rset)
            self.w(strio.getvalue())
            self.wview('sameetypelist', rset, showtitle=False)
            self.w(strio.getvalue())


class SubscribeToBlogComponent(component.EntityVComponent):
    __regid__ = 'blogsubscribe'
    __select__ = component.EntityVComponent.__select__ & implements('Blog')
    context = 'ctxtoolbar'

    def cell_call(self, row, col, view):
        entity = self.cw_rset.get_entity(row, col)
        self.w('<a href="%s"><img src="%s" alt="%s"/></a>' % (
            xml_escape(entity.rss_feed_url()),
            self._cw.external_resource('RSS_LOGO_16'),
            self._cw._(u'subscribe to this blog')))


class BlogEntryPrimaryView(primary.PrimaryView):
    __select__ = implements('BlogEntry')
    show_attr_label = False

    def render_entity_relations(self, entity):
        rset = entity.related('entry_of', 'subject')
        if rset:
            self.w(self._cw._('blogged in '))
            self.wview('csv', rset, 'null')


# don't show workflow history for blog entry
class BlogEntryWFHistoryVComponent(workflow.WFHistoryVComponent):
    __select__ = workflow.WFHistoryVComponent.__select__ & implements('BlogEntry')

    def cell_call(self, row, col, view=None):
        pass
