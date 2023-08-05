"""Specific views and actions for application using the Comment entity type

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from itertools import count

from logilab.mtconverter import xml_escape
from logilab.common.decorators import monkeypatch

from simplejson import dumps

from cubicweb.selectors import (implements, has_permission, authenticated_user,
                                score_entity, relation_possible, one_line_rset)
from cubicweb.view import EntityView
from cubicweb.uilib import rql_for_eid, cut, safe_cut
from cubicweb.mixins import TreeViewMixIn
from cubicweb.web import stdmsgs, uicfg, component, form, formwidgets as fw
from cubicweb.web.action import LinkToEntityAction, Action
from cubicweb.web.views import primary, baseviews, xmlrss, basecontrollers

_afs = uicfg.autoform_section
_afs.tag_subject_of(('*', 'comments', '*'), formtype='main', section='hidden')
_afs.tag_object_of(('*', 'comments', '*'), formtype='main', section='hidden')

_abaa = uicfg.actionbox_appearsin_addmenu
_abaa.tag_subject_of(('*', 'comments', '*'),  False)
_abaa.tag_object_of(('*', 'comments', '*'), False)

_pvs = uicfg.primaryview_section
_pvs.tag_subject_of(('*', 'comments', '*'),  'hidden')
_pvs.tag_object_of(('*', 'comments', '*'), 'hidden')


# comment views ###############################################################

class CommentPrimaryView(primary.PrimaryView):
    __select__ = implements('Comment')

    def cell_call(self, row, col):
        self._cw.add_css('cubes.comment.css')
        entity = self.cw_rset.complete_entity(row, col)
        # display text, author and creation date
        self.w(u'<div class="comment">')
        self.w(u'<div class="commentInfo">')
        # do not try to display creator when you're not allowed to see CWUsers
        if entity.creator:
            authorlink = entity.creator.view('oneline')
            self.w(u'%s %s\n' % (self._cw._('written by'), authorlink))
        self.w(self._cw.format_date(entity.creation_date))
        # commented object
        if entity.comments:
            self.w(u",  %s " % self._cw._('comments'))
            entity.comments[0].view('oneline', w=self.w)
            self.w(u"\n")
        # don't include responses in this view, since the comment section
        # component will display them
        self.w(u'</div>\n')
        self.w(u'<div class="commentBody">%s</div>\n'
               % entity.printable_value('content'))
        # XXX attribute generated_by added by email component
        if hasattr(self, 'generated_by') and self.generated_by:
            gen = self.generated_by[0]
            link = '<a href="%s">%s</a>' % (gen.absolute_url(),
                                            gen.dc_type().lower())
            txt = self._cw._('this comment has been generated from this %s') % link
            self.w(u'<div class="commentBottom">%s</div>\n' % txt)
        self.w(u'</div>\n')


class CommentRootView(EntityView):
    __regid__ = 'commentroot'
    __select__ = implements('Comment')

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        root = entity.root()
        self.w(u'<a href="%s">%s %s</a> ' % (
            xml_escape(root.absolute_url()),
            xml_escape(root.dc_type()),
            xml_escape(cut(root.dc_title(), 40))))


class CommentSummary(EntityView):
    __regid__ = 'commentsummary'
    __select__ = implements('Comment')

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        maxsize = self._cw.property_value('navigation.short-line-size')
        content = entity.printable_value('content', format='text/plain')
        self.w(xml_escape(cut(content, maxsize)))


class CommentOneLineView(baseviews.OneLineView):
    __select__ = implements('Comment')

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'[%s] ' % entity.view('commentroot'))
        self.w(u'<a href="%s"><i>%s</i></a>\n' % (
            xml_escape(entity.absolute_url()),
            entity.view('commentsummary')))


class CommentTreeItemView(baseviews.ListItemView):
    __regid__ = 'treeitem'
    __select__ = implements('Comment')

    def cell_call(self, row, col, **kwargs):
        self._cw.add_js('cubicweb.ajax.js')
        self._cw.add_css('cubes.comment.css')
        entity = self.cw_rset.get_entity(row, col)
        actions = self._cw.vreg['actions']
        # DOM id of the whole comment's content
        cdivid = 'comment%sDiv' % entity.eid
        self.w(u'<div id="%s">' % cdivid)
        self.w(u'<div class="commentInfo">')
        self.w(self._cw.format_date(entity.creation_date))
        self.w(u' %s' % self._cw.format_time(entity.creation_date))
        if entity.creator:
            authorlink = entity.creator.view('oneline')
            self.w(u', %s <span class="author">%s</span> \n'
                   % (self._cw._('written by'), authorlink,))
        replyaction = actions.select_or_none('reply_comment', self._cw,
                                       rset=self.cw_rset, row=row)
        if replyaction is not None:
            url = self._cw.build_ajax_replace_url(
                'comment%sHolder' % entity.eid, rql_for_eid(entity.eid),
                'addcommentform')
            self.w(u' | <span class="replyto"><a href="%s">%s</a></span>'
                   % (xml_escape(url), self._cw._(replyaction.title)))
        editaction = actions.select_or_none('edit_comment', self._cw,
                                            rset=self.cw_rset, row=row)
        if editaction is not None:
            # split(':', 1)[1] to remove javascript:
            formjs = self._cw.build_ajax_replace_url(
                cdivid, rql_for_eid(entity.eid),
                'editcommentform', 'append').split(':', 1)[1]
            url = "javascript: jQuery('#%s div').hide(); %s" % (cdivid, formjs)
            self.w(u' | <span class="replyto"><a href="%s">%s</a></span>'
                   % (xml_escape(url), self._cw._(editaction.title)))

        deleteaction = actions.select_or_none('delete_comment', self._cw,
                                             rset=self.cw_rset, row=row)
        if deleteaction is not None:
            url = self._cw.build_ajax_replace_url(
                'comment%s' % entity.eid, rql_for_eid(entity.eid),
                'deleteconf', __redirectpath=entity.root().rest_path())

            self.w(u' | <span class="replyto"><a href="%s">%s</a></span>'
                   % (xml_escape(url), self._cw._(deleteaction.title)))
        self.w(u'</div>\n') # close comment's info div
        self.w(u'<div class="commentBody">%s</div>\n'
               % entity.printable_value('content'))
        # holder for reply form
        self.w(u'<div id="comment%sHolder" class="replyComment"></div>' % entity.eid)
        self.w(u'</div>\n') # close comment's content div


class CommentThreadView(TreeViewMixIn, baseviews.ListView):
    """a recursive tree view"""
    __select__ = implements('Comment')
    title = _('thread view')

    def open_item(self, entity):
        self.w(u'<li id="comment%s" class="comment">\n' % entity.eid)


class RssItemCommentView(xmlrss.RSSItemView):
    __select__ = implements('Comment')

    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        self.w(u'<item>\n')
        self.w(u'<guid isPermaLink="true">%s</guid>\n'
               % xml_escape(entity.absolute_url()))
        self.render_title_link(entity)
        description = entity.dc_description(format='text/html') + \
                      self._cw._(u'about') + \
                      u' <a href=%s>%s</a>' % (entity.root().absolute_url(),
                                               entity.root().dc_title())
        self._marker('description', description)
        self._marker('dc:date', entity.dc_date(self.date_format))
        self.render_entity_creator(entity)
        self.w(u'</item>\n')
        self.wview('rssitem', entity.related('comments', 'object'), 'null')


# comment forms ################################################################

class InlineEditCommentForm(form.FormViewMixIn, EntityView):
    __regid__ = 'editcommentform'
    __select__ = implements('Comment')

    jsfunc = "processComment(%s, '%s', false)"
    jsonmeth = 'edit_comment'

    def cell_call(self, row, col):
        self.comment_form(self.cw_rset.get_entity(row, col))

    def propose_to_login(self):
        self.w(u'<div class="warning">%s ' % self._cw._('You are not authenticated.'))
        if 'registration' in self._cw.vreg.config.cubes():
            self.w(u'<a href="%s">%s</a> or ' % (self._cw.build_url('register'),
                                                 self._cw._(u'register')))
        self.w(u'<a onclick="showLoginBox()">%s</a>' % self._cw._(u'login'))
        self.w(u'</div>')

    def comment_form(self, commented, newcomment=None):
        self._cw.add_js('cubes.comment.js')
        if newcomment is None:
            newcomment = commented
        if self._cw.cnx.anonymous_connection:
            self.propose_to_login()
        # hack to avoid tabindex conflicts caused by Ajax requests
        self._cw.next_tabindex = count(20).next
        jseid = dumps(commented.eid)
        cancel_action = self.jsfunc % (jseid, '')
        buttons = [fw.Button(onclick=self.jsfunc % (jseid, self.jsonmeth)),
                   fw.Button(stdmsgs.BUTTON_CANCEL,
                             onclick=cancel_action)]
        form = self._cw.vreg['forms'].select('edition', self._cw,
                                             entity=newcomment,
                                             form_buttons=buttons)
        self.w(u'<div id="comment%sSlot">%s</div>' % (
            commented.eid, form.render(main_form_title=u'',
                                       display_label=False,
                                       display_relations_form=False)))


class InlineAddCommentForm(InlineEditCommentForm):
    __regid__ = 'addcommentform'
    __select__ = relation_possible('comments', 'object', 'Comment', 'add')

    jsfunc = "processComment(%s, '%s', true)"
    jsonmeth = 'add_comment'

    def cell_call(self, row, col):
        commented = self.cw_rset.get_entity(row, col)
        newcomment = self._cw.vreg['etypes'].etype_class('Comment')(self._cw)
        newcomment.eid = self._cw.varmaker.next()
        self.comment_form(commented, newcomment)


# contextual components ########################################################

class CommentSectionVComponent(component.EntityVComponent):
    """a component to display a <div> html section including comments
    related to an object
    """
    __regid__ = 'commentsection'
    __select__ = (component.EntityVComponent.__select__
                  & relation_possible('comments', 'object', 'Comment'))

    context = 'navcontentbottom'

    def cell_call(self, row, col, view=None):
        req = self._cw
        req.add_js( ('cubicweb.ajax.js', 'cubes.comment.js') )
        eid = self.cw_rset[row][col]
        self.w(u'<div id="%s" class="%s" cubicweb:rooteid="%s">' % (
            self.div_id(), self.div_class(), eid))
        rql = u'Any C,CD,CC,CCF,U,UL,US,UF ORDERBY CD WHERE C is Comment, '\
              'C comments X, C creation_date CD, C content CC, C content_format CCF, ' \
              'C created_by U?, U login UL, U firstname UF, U surname US, X eid %(x)s'
        rset = req.execute(rql, {'x': eid}, 'x')
        if rset.rowcount:
            self.w(u'<h4>%s</h4>' % (req._('Comment_plural')))
        if rset.rowcount:
            self.w(u'<ul class="comment">')
            for i in xrange(rset.rowcount):
                self.wview('tree', rset, row=i)
            self.w(u'</ul>')
        self.w(u'</div>')
        addcomment = self._cw.vreg['actions'].select_or_none('reply_comment', req,
                                                        rset=self.cw_rset,
                                                        row=row, col=col)
        if addcomment is not None:
            self.w(u'<div id="comment%sHolder"></div>' % eid)
            url = req.build_ajax_replace_url(
                'comment%sHolder' % eid, rql_for_eid(eid), 'addcommentform')
            self.w(u' (<a href="%s">%s</a>)' % (url, req._(addcomment.title)))
            # XXX still necessary?
            #if req.use_fckeditor() and req.property_value('ui.default-text-format') == 'text/html':
            #    req.fckeditor_config()


class UserLatestCommentsSection(component.EntityVComponent):
    """a section to display latest comments by a user"""
    __select__ = component.EntityVComponent.__select__ & implements('CWUser')
    __regid__ = 'latestcomments'

    def cell_call(self, row, col, view=None):
        user = self.cw_rset.get_entity(row, col)
        maxrelated = self._cw.property_value('navigation.related-limit') + 1
        rset = self._cw.execute(
            'Any C,CD,C,CCF ORDERBY CD DESC LIMIT %s WHERE C is Comment, '
            'C creation_date CD, C content CC, C content_format CCF, '
            'C created_by U, U eid %%(u)s' % maxrelated,
            {'u': user.eid})
        if rset:
            self.w(u'<div class="section">')
            self.w(u'<h4>%s</h4>\n' % self._cw._('Latest comments').capitalize())
            self.wview('table', rset,
                       displaycols=range(3), # XXX may be removed with cw >= 3.8
                       headers=[_('about'), _('on date'),
                                _('comment content')],
                       cellvids={0: 'commentroot',
                                 2: 'commentsummary',
                                 })
            self.w(u'</div>')


# actions ######################################################################

class ReplyCommentAction(LinkToEntityAction):
    __regid__ = 'reply_comment'
    __select__ = LinkToEntityAction.__select__ & implements('Comment')

    rtype = 'comments'
    role = 'object'
    target_etype = 'Comment'

    title = _('reply to this comment')
    category = 'hidden'
    order = 111

    def url(self):
        comment = self.cw_rset.get_entity(self.cw_row or 0, self.cw_col or 0)
        linkto = '%s:%s:subject' % (self.rtype, comment.eid)
        return self._cw.build_url(vid='creation', etype=self.target_etype,
                                  __linkto=linkto,
                                  __redirectpath=comment.root().rest_path(),
                                  __redirectvid=self._cw.form.get('vid', ''))


class AddCommentAction(LinkToEntityAction):
    """add comment is like reply for everything but Comment"""
    __regid__ = 'reply_comment'
    __select__ = LinkToEntityAction.__select__ & ~implements('Comment')

    rtype = 'comments'
    role = 'object'
    target_etype = 'Comment'

    title = _('add comment')
    category = 'hidden'
    order = 111


class EditCommentAction(Action):
    __regid__ = 'edit_comment'
    __select__ = one_line_rset() & implements('Comment') & has_permission('update')

    title = _('edit comment')
    category = 'hidden'
    order = 110

    def url(self):
        return self._cw.build_url(rql=self.cw_rset.printable_rql(), vid='edition')

class DeleteCommentAction(Action):
    __regid__ = 'delete_comment'
    __select__ = implements('Comment') & authenticated_user() & \
                 score_entity(lambda x: not x.reverse_comments and x.has_perm('delete'))

    title = _('delete comment')
    category = 'hidden'
    order = 110

    def url(self):
        return self._cw.build_url(rql=self.cw_rset.printable_rql(), vid='deleteconf')


# JSONController extensions through monkey-patching ############################

@monkeypatch(basecontrollers.JSonController)
@basecontrollers.jsonize
def js_add_comment(self, commented, text, format):
    return self._cw.execute('INSERT Comment C: C comments X, C content %(text)s, '
                            'C content_format %(format)s  WHERE X eid %(x)s',
                            {'format' : format, 'text' : text, 'x' : commented}, 'x')[0][0]

@monkeypatch(basecontrollers.JSonController)
@basecontrollers.jsonize
def js_edit_comment(self, comment, text, format):
    self._cw.execute('SET C content %(text)s, C content_format %(format)s '
                     'WHERE C eid %(x)s',
                     {'format' : format, 'text' : text, 'x' : comment}, 'x')
