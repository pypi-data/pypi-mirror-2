"""Various blog boxes: archive, per author, etc...

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from logilab.mtconverter import xml_escape

from cubicweb.selectors import one_line_rset, implements
from cubicweb.web.htmlwidgets import BoxLink, BoxWidget
from cubicweb.web.views import boxes

class BlogArchivesBox(boxes.BoxTemplate):
    """blog side box displaying a Blog Archive"""
    __regid__ = 'blog_archives_box'
    title = _('boxes_blog_archives_box')
    order = 35

    def call(self, **kwargs):
        """display blogs archive"""
        # XXX turn into a selector
        count_blogentry = self._cw.execute('Any COUNT(B) WHERE B is BlogEntry')
        if count_blogentry[0][0] > 0:
            box = BoxWidget(self._cw._(self.title), id=self.__regid__, islist=False)
            box.append(boxes.BoxHtml(self._cw.view('blog_archive', None, maxentries=12)))
            box.render(self.w)


class BlogsByAuthorBox(boxes.BoxTemplate):
    __regid__ = 'blog_summary_box'
    title = _('boxes_blog_summary_box')
    order = 36

    def call(self, view=None, **kwargs):
        box = BoxWidget(self._cw._(self.title), self.__regid__, islist=True)
        rql = 'Any U, COUNT(B) GROUPBY U WHERE U is CWUser, ' \
              'B is BlogEntry, B created_by U'
        rset = self._cw.execute(rql)
        for user in rset:
            euser = self._cw.entity_from_eid(user[0])
            box.append(BoxLink(self._cw.build_url('blogentry/%s' % euser.login),
                                              u'%s [%s]' % (euser.name(),
                                                            user[1])))
        box.render(self.w)


class LatestBlogsBox(boxes.BoxTemplate):
    """display a box with latest blogs and rss"""
    __regid__ = 'latest_blogs_box'
    title = _('latest_blogs_box')
    visible = True # enabled by default
    order = 34
    display_see_more_link = True

    def latest_blogs_rset(self):
        return self._cw.execute(
            'Any X,T,CD ORDERBY CD DESC LIMIT 5 WHERE X is BlogEntry, '
            'X title T, X creation_date CD')

    def call(self, **kwargs):
        # XXX turn into a selector
        rset = self.latest_blogs_rset()
        if not rset:
            return
        box = BoxWidget(self._cw._(self.title), self.__regid__, islist=True)
        # TODO - get the date between brakets after link
        # empty string for title argument to deactivate auto-title
        for i in xrange(rset.rowcount):
            entity = rset.get_entity(i, 0)
            box.append(BoxLink(entity.absolute_url(), xml_escape(entity.dc_title())))
        rqlst = rset.syntax_tree()
        rqlst.set_limit(None)
        rql = rqlst.as_string(kwargs=rset.args)
        if self.display_see_more_link:
            url = self._cw.build_url('view', rql=rql, page_size=10)
            box.append(BoxLink(url,  u'[%s]' % self._cw._(u'see more')))
        rss_icon = self._cw.external_resource('RSS_LOGO_16')
        # FIXME - could use rss_url defined as a property if available
        rss_label = u'%s <img src="%s" alt="%s"/>' % (
            self._cw._(u'subscribe'), rss_icon, self._cw._('rss icon'))
        rss_url = self._cw.build_url('view', vid='rss', rql=rql)
        box.append(BoxLink(rss_url, rss_label))
        box.render(self.w)


class LatestBlogsBlogBox(LatestBlogsBox):
    """display a box with latest blogs and rss, filtered for a particular blog
    """
    __select__ = LatestBlogsBox.__select__ & one_line_rset() & implements('Blog')
    title = _('latest_blogs_blog_box')
    display_see_more_link = False

    def latest_blogs_rset(self):
        blog = self.cw_rset.get_entity(self.cw_row or 0, self.cw_col or 0)
        return self._cw.execute(
            'Any X,T,CD ORDERBY CD DESC LIMIT 5 WHERE X is BlogEntry, '
            'X title T, X creation_date CD, X entry_of B, B eid %(b)s',
            {'b': blog.eid})
