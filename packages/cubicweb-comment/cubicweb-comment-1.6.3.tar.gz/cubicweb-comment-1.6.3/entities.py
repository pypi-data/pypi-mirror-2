"""entity classes for Comment entities

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

from logilab.common.textutils import normalize_text

from cubicweb.view import EntityView
from cubicweb.interfaces import ITree
from cubicweb.mixins import TreeMixIn
from cubicweb.selectors import implements
from cubicweb.entities import AnyEntity, fetch_config


def subcomments_count(commentable):
    return sum([len(commentable.reverse_comments)]
               + [subcomments_count(c) for c in commentable.reverse_comments])

class Comment(TreeMixIn, AnyEntity):
    """customized class for Comment entities"""
    __regid__ = 'Comment'
    tree_attribute = 'comments'
    __implements__ = AnyEntity.__implements__ + (ITree,)
    fetch_attrs, fetch_order = fetch_config(('creation_date',),
                                             'creation_date', order='ASC')

    def dc_title(self):
        return u'#%s' % self.eid

    def dc_description(self, format='text/plain'):
        return self.printable_value('content', format=format)

    def after_deletion_path(self):
        """return (path, parameters) which should be used as redirect
        information when this entity is being deleted
        """
        return self.root().rest_path(), {}

    subcomments_count = subcomments_count


# some views potentially needed on web *and* server side (for notification)
# so put them here

class CommentFullTextView(EntityView):
    __regid__ = 'fulltext'
    __select__ = implements('Comment')

    def cell_call(self, row, col, indentlevel=0, withauthor=True):
        e = self.cw_rset.get_entity(row,col)
        if indentlevel:
            indentstr = '>'*indentlevel + ' '
        else:
            indentstr = ''
        if withauthor:
            _ = self._cw._
            author = e.created_by and e.created_by[0].login or _("Unknown author")
            head = u'%s%s - %s :' % (indentstr,
                                     _('On %s') %  self._cw.format_date(e.creation_date, time=True),
                                     _('%s wrote') % author)
            lines = [head]
        else:
            lines = []
        content = e.printable_value('content', format='text/plain')
        lines.append(normalize_text(content, 80, indentstr,
                                    rest=e.content_format=='text/rest'))
        lines.append(indentstr[:-2])
        self.w(u'\n'.join(lines))


class CommentFullThreadText(CommentFullTextView):
    """display a comment and its parents"""
    __regid__ = 'fullthreadtext'

    def cell_call(self, row, col):
        e = self.cw_rset.get_entity(row,col)
        strings = []
        cpath = e.path()[1:]
        indentlevel = len(cpath) - 1
        for i, ceid in enumerate(cpath):
            comment = self._cw.execute('Any C,T,D WHERE C creation_date D, C content T, C eid %(x)s',
                                       {'x': ceid}, 'x', build_descr=True).get_entity(0, 0)
            strings.append(comment.view('fulltext', indentlevel=indentlevel-i,
                                        withauthor=i!=indentlevel).strip() + '\n')
        strings.append(u'\n%s: %s' % (self._cw._('i18n_by_author_field'),
                                      e.dc_creator() or _('unknown author')))
        strings.append(u'url: %s' % e.root().absolute_url())
        self.w(u'\n'.join(strings))


class CommentFullThreadDescText(CommentFullTextView):
    """same as fullthreadtext, but going from top level object to leaf comments
    """
    __regid__ = 'fullthreadtext_descending'

    def cell_call(self, row, col, indentlevel=0):
        e = self.cw_rset.get_entity(row,col)
        self.w(e.view('fulltext', indentlevel=indentlevel).strip() + '\n')
        subcommentsrset = e.related('comments', 'object')
        if subcommentsrset:
            self.wview('fulltext', subcommentsrset, indentlevel=indentlevel+1)
