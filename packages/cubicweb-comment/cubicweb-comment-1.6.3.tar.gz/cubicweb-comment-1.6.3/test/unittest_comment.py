import re

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.web.views import actions

from cubes.comment import views

class CommentTC(CubicWebTC):
    """Comment"""

    def setup_database(self):
        req = self.request()
        self.b = req.create_entity('BlogEntry', title=u"yo", content=u"qu\'il est beau")

    def test_schema(self):
        self.assertEquals(self.schema['comments'].rdef('Comment', 'BlogEntry').composite,
                          'object')

    def test_possible_views(self):
        # comment primary view priority
        req = self.request()
        rset = req.create_entity('Comment', content=u"bouh!", comments=self.b).as_rset()
        self.assertIsInstance(self.vreg['views'].select('primary', req, rset=rset),
                             views.CommentPrimaryView)
        self.assertIsInstance(self.vreg['views'].select('tree', req, rset=rset),
                             views.CommentThreadView)

    def test_possible_actions(self):
        req = self.request()
        req.create_entity('Comment', content=u"bouh!", comments=self.b)
        self.create_user('user') # will commit
        rset = req.execute('Any X WHERE X is BlogEntry')
        actions = self.pactions(req, rset)
        self.failUnless(('reply_comment', views.AddCommentAction) in actions)
        self.failIf(('edit_comment', views.EditCommentAction) in actions)
        rset = req.execute('Any X WHERE X is Comment')
        actions = self.pactions(req, rset)
        self.failUnless(('reply_comment', views.ReplyCommentAction) in actions)
        self.failUnless(('edit_comment', views.EditCommentAction) in actions)
        cnx = self.login('user')
        req = self.request()
        rset = req.execute('Any X WHERE X is Comment')
        actions = self.pactions(req, rset)
        self.failUnless(('reply_comment', views.ReplyCommentAction) in actions)
        self.failIf(('edit_comment', views.EditCommentAction) in actions)
        rset = self.execute('INSERT Comment X: X content "ho bah non!", X comments B WHERE B is Comment')
        cnx.commit()
        actions = self.pactions(req, rset)
        self.failUnless(('reply_comment', views.ReplyCommentAction) in actions)
        self.failUnless(('edit_comment', views.EditCommentAction) in actions)
        cnx.rollback()
        cnx = self.login('anon')
        req = self.request()
        rset = req.execute('Any X WHERE X is Comment')
        self.failUnlessEqual(self.pactions(req, rset), [])
        cnx.rollback()

    def test_nonregr_possible_actions(self):
        req = self.request()
        req.create_entity('Comment', content=u"bouh!", comments=self.b)
        req.create_entity('Comment', content=u"Yooo!", comments=self.b)
        # now two comments are commenting the blog
        rset = self.b.related('comments', 'object')
        self.assertEquals(len(rset), 2)
        self.failUnless(self.vreg['actions'].select('reply_comment', req, rset=rset, row=0))
        self.failUnless(self.vreg['actions'].select('reply_comment', req, rset=rset, row=1))

    def test_add_related_actions(self):
        req = self.request()
        req.create_entity('Comment', content=u"bouh!", comments=self.b)
        self.create_user('user') # will comit
        rset = req.execute('Any X WHERE X is Comment')
        self.failUnlessEqual(self.pactions_by_cats(req, rset), [])
        cnx = self.login('user')
        rset = req.execute('Any X WHERE X is Comment')
        self.failUnlessEqual(self.pactions_by_cats(req, rset), [])
        cnx.rollback()
        cnx = self.login('anon')
        rset = req.execute('Any X WHERE X is Comment')
        self.failUnlessEqual(self.pactions_by_cats(req, rset), [])
        cnx.rollback()

    def test_path(self):
        req = self.request()
        c1 = req.create_entity('Comment', content=u"oijzr", comments=self.b)
        c11 = req.create_entity('Comment', content=u"duh?", comments=c1)
        self.assertEquals(c1.path(), [self.b.eid, c1.eid])
        self.assertEquals(c1.root().eid, self.b.eid)
        self.assertEquals(c11.path(), [self.b.eid, c1.eid, c11.eid])
        self.assertEquals(c11.root().eid, self.b.eid)

    def test_comments_ascending_order(self):
        req = self.request()
        c1 = req.create_entity('Comment', content=u"one", comments=self.b)
        c11 = req.create_entity('Comment', content=u"one-one", comments=c1)
        c12 = req.create_entity('Comment', content=u"one-two", comments=c1)
        c2 = req.create_entity('Comment', content=u"two", comments=self.b)
        self.assertEquals([c.eid for c in self.b.reverse_comments],
                          [c1.eid, c2.eid])
        self.assertEquals([c.eid for c in c1.children()],
                          [c11.eid, c12.eid])

    def test_subcomments_count(self):
        req = self.request()
        c1 = req.create_entity('Comment', content=u"one", comments=self.b)
        c11 = req.create_entity('Comment', content=u"one-one", comments=c1)
        c12 = req.create_entity('Comment', content=u"one-two", comments=c1)
        c21 = req.create_entity('Comment', content=u"two-one", comments=c12)
        self.assertEquals(c1.subcomments_count(), 3)

    def test_fullthreadtext_views(self):
        req = self.request()
        c = req.create_entity('Comment', content=u"bouh!", comments=self.b)
        c2 = req.create_entity('Comment', content=u"""
some long <b>HTML</b> text which <em>should not</em> fit on 80 characters, so i'll add some extra xxxxxxx.
Yeah !""", content_format=u"text/html", comments=c)
        self.commit() # needed to set author
        content = c2.view('fullthreadtext')
        # remove date
        content = re.sub('..../../.. ..:..', '', content)
        self.assertTextEquals(content,
                          """\
> On  - admin wrote :
> bouh!

some long **HTML** text which _should not_ fit on 80 characters, so i'll add
some extra xxxxxxx. Yeah !


i18n_by_author_field: admin
url: http://testing.fr/cubicweb/blogentry/%s""" % self.b.eid)
        # fullthreadtext_descending view
        self.assertTextEquals(re.sub('..../../.. ..:..', '', c.view('fullthreadtext_descending')),
                              '''On  - admin wrote :
bouh!
> On  - admin wrote :
> some long **HTML** text which _should not_ fit on 80 characters, so i\'ll add
> some extra xxxxxxx. Yeah !

''')

class CommentJsonControllerExtensionsTC(CubicWebTC):

    def setup_database(self):
        self.john = self.create_user(u'John')

    def test_add_and_edit_comment(self):
        # add comment
        self.remote_call('add_comment', self.john.eid, u'yo', u'text/plain')
        comment = self.entity('Any C,CT,F WHERE C content CT, C content_format F, '
                              'C comments P, P eid %s' % self.john.eid)
        self.assertEquals(comment.content, u'yo')
        self.assertEquals(comment.content_format, u'text/plain')
        # edit comment
        self.remote_call('edit_comment', comment.eid, u'yipee', u'text/plain')
        comment2 = self.entity('Any C,CT,F WHERE C content CT, C content_format F, '
                               'C comments P, P eid %s' % self.john.eid)
        self.assertEquals(comment.eid, comment2.eid)
        self.assertEquals(comment2.content, u'yipee')
        self.assertEquals(comment2.content_format, u'text/plain')


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
