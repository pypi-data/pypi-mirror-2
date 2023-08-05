"""Secondary views for blogs

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

from calendar import monthrange
from datetime import datetime

from logilab.mtconverter import xml_escape

from cubicweb.schema import display_name
from cubicweb.view import EntityView, StartupView
from cubicweb.selectors import paginated_rset, sorted_rset, implements
from cubicweb.web.views import baseviews, calendar, navigation

class BlogEntryArchiveView(StartupView):
    """control the view of a blog archive"""
    __regid__ = 'blog_archive'
    countrql = 'Any COUNT(B) WHERE B is BlogEntry, B creation_date >=  %(firstday)s, B creation_date <= %(lastday)s'

    def represent(self, items, year, month):
        """represent a single month entry"""
        firstday = datetime(year, month, 1)
        lastday = datetime(year, month, monthrange(year, month)[1])
        rql = ('Any B, BD ORDERBY BD DESC '
               'WHERE B is BlogEntry, B creation_date BD, '
               'B creation_date >=  "%s", B creation_date <= "%s"' %
                (firstday.strftime('%Y-%m-%d'), lastday.strftime('%Y-%m-%d')))
        args = {'firstday':firstday, 'lastday':lastday}
        nmb_entries = self._cw.execute(self.countrql, args)[0][0]
        label = u'%s %s [%s]' % (self._cw._(calendar.MONTHNAMES[month-1]), year,
                                 nmb_entries)
        vtitle = '%s %s' % (display_name(self._cw, 'BlogEntry', 'plural'), label)
        url = xml_escape(self._cw.build_url('view', rql=rql, month=month,
                                            year=year, vtitle=vtitle))
        link = u'<a href="%s" title="">%s</a>' % (url, label)
        items.append( u'<li class="">%s</li>\n' % link )

    def call(self, maxentries=None, **kwargs):
        """display a list of entities by calling their <item_vid> view
        """
        rset = self._cw.execute('Any CD ORDERBY CD DESC WHERE B is BlogEntry, '
                                'B creation_date CD')
        blogmonths = []
        items = []
        for (blogdate,) in rset:
            year, month = blogdate.year, blogdate.month
            if (year, month) not in blogmonths:
                blogmonths.append( (year, month) )
        if maxentries is None:
            displayed_months = blogmonths
            needmore = False
        else:
            needmore = len(blogmonths) > maxentries
            displayed_months = blogmonths[:maxentries]
        for year, month in displayed_months:
            self.represent(items, year, month)
        if needmore:
            url = self._cw.build_url('view', vid='blog_archive')
            link = u'<a href="%s" title="">[%s]</a>' % (
                url, self._cw._('see more archives'))
            items.append( u'<li class="">%s</li>\n' % link )
        self.w(u'<div class="boxFrame">')
        if items:
            self.w(u'<div class="boxContent">\n')
            self.w(u'<ul class="boxListing">')
            self.w(''.join(items))
            self.w(u'</ul>\n</div>\n')
        self.w(u'</div>')


class BlogEntrySameETypeListView(baseviews.SameETypeListView):
    __select__ = baseviews.SameETypeListView.__select__ & implements('BlogEntry')
    countrql = ('Any COUNT(B) WHERE B is BlogEntry, '
                'B creation_date >= %(firstday)s, B creation_date <= %(lastday)s')
    item_vid = 'blog'

    def call(self, **kwargs):
        self._cw.add_css('cubes.blog.css')
        super(BlogEntrySameETypeListView, self).call(**kwargs)
        if 'year' in self._cw.form and 'month' in self._cw.form:
            self.render_next_previous(int(self._cw.form['year']), int(self._cw.form['month']))

    def render_next_previous(self, year, month):
        if month == 12:
            nextmonth = 1
            year = year + 1
        else:
            nextmonth = month + 1
        if month == 1:
            previousmonth = 12
            year = year - 1
        else:
            previousmonth = month -1
        self.w(u'<div class="prevnext">')
        self.w(u'<span class="previousmonth">%s</span>' \
               % self.render_link(year, previousmonth,
                                  xml_escape(u'<< ' + self._cw._(u'previous month'))))
        self.w(u'<span class="nextmonth">%s</span>' \
               % self.render_link(year, nextmonth,
                                  xml_escape(self._cw._(u'next month') + u' >>')))
        self.w(u'</div>')

    def render_link(self, year, month, atitle):
        firstday = datetime(year, month, 1)
        lastday = datetime(year, month, monthrange(year, month)[1])
        args = {'firstday': firstday, 'lastday': lastday}
        nmb_entries = self._cw.execute(self.countrql, args)[0][0]
        if not nmb_entries:
            return
        rql = ('Any B, BD ORDERBY BD DESC '
               'WHERE B is BlogEntry, B creation_date BD, '
               'B creation_date >= "%s", B creation_date <= "%s"' %
                (firstday.strftime('%Y-%m-%d'), lastday.strftime('%Y-%m-%d')))
        label = u'%s %s [%s]' % (self._cw._(calendar.MONTHNAMES[month-1]), year,
                                 nmb_entries)
        vtitle = '%s %s' % (display_name(self._cw, 'BlogEntry', 'plural'), label)
        url = self._cw.build_url('view', rql=rql, vtitle=vtitle,
                                 month=month, year=year)
        return u'<a href="%s">%s</a>' % (xml_escape(url), atitle)


class BlogEntryBlogView(EntityView):
    __regid__ = 'blog'
    __select__ = implements('BlogEntry')

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        w = self.w
        _ = self._cw._
        w(u'<div class="post">')
        w(u'<h1>%s</h1>' % entity.view('incontext'))
        w(u'<div class="creation_date">%s</div>' %
          self._cw.format_date(entity.creation_date))
        creator = entity.creator
        if creator:
            vtitle = _('blog entries created by %s') % creator.name()
            rql = 'Any X ORDERBY D DESC WHERE X is BlogEntry, X created_by Y, '\
                  'Y eid %s, X creation_date D' % creator.eid
            url = self._cw.build_url('view', rql=rql, vtitle=vtitle, page_size=10)
            w(u'<span class="author">%s <a title="%s" href="%s">%s</a></span>' % (
                _('by'), xml_escape(vtitle), xml_escape(url), creator.name()))
        w(u'<div class="entry">')
        body = entity.printable_value('content')
        w(body)
        w(u'</div>')
        w(u'<br class="clear"/>')
        w(u'<div class="postmetadata">%s</div>' % entity.view('post-reldata'))
        w(u'</div>')


class BlogEntryPostMetaData(EntityView):
    __regid__ = 'post-reldata'
    __select__ = implements('BlogEntry')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        _ = lambda ertype, form='': display_name(self._cw, ertype, form)
        reldata = []
        w = reldata.append
        schema = self._cw.vreg.schema
        if 'comments' in schema and \
               'BlogEntry' in schema.rschema('comments').objects():
            from cubes.comment.entities import subcomments_count
            count = subcomments_count(entity)
            if count:
                url = xml_escape(entity.absolute_url())
                if count > 1:
                    label = _('Comment', 'plural')
                else:
                    label = _('Comment')
                w(u'<a href="%s">%s %s</a>' % (url, count, label))
            else:
                w(u'%s %s' % (count, _('Comment')))
        if 'tags' in schema and 'BlogEntry' in schema.rschema('tags').objects():
            tag_rset = entity.related('tags', 'object')
            if tag_rset:
                w(u'%s %s' % (_('tags', 'object'), self._cw.view('csv', tag_rset)))
        rset = entity.related('entry_of', 'subject')
        if rset:
            w(u'%s %s' % (self._cw._('blogged in '),
                          self._cw.view('csv', rset, 'null')))
        self.w(u' | '.join(reldata))


class BlogNavigation(navigation.PageNavigation):
    __select__ = paginated_rset() & sorted_rset() & implements('BlogEntry')

    def index_display(self, start, stop):
        return u'%s' % (int(start / self.page_size)+1)
