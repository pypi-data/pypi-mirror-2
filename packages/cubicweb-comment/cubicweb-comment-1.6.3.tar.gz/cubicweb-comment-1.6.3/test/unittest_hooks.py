from cubicweb.devtools.testlib import CubicWebTC

class CommentViewsTC(CubicWebTC):

    def setup_database(self):
        self.blog = self.request().create_entity('BlogEntry', title=u"une news !", content=u"cubicweb c'est beau")
        self.request().create_entity('Comment', content=u"Yo !")
        self.execute('SET C comments B WHERE B title "une news !", C content "Yo !"')

    def test_notif_after_add_relation_comments(self):
        req = self.session
        c = self.entity('Comment X', req=req)
        req.set_pool()
        v = self.vreg['views'].select('notif_after_add_relation_comments', req,
                                      rset=c.cw_rset, row=0)
        content = v.render(row=0)
        self.assertTextEquals(content,
                          '''Yo !


i18n_by_author_field: admin
url: http://testing.fr/cubicweb/blogentry/%s''' %
                          c.comments[0].eid)
        self.assertEquals(v.subject(), 'new comment for blogentry une news !')


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
