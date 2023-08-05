from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.web.views import management, startup, wdoc
from cubes.folder import views

class ClassifiableEntityTC(CubicWebTC):
    def setup_database(self):
        self.request().create_entity('Card', title=u"blah !")

    def test_subject_filed_under_vocabulary(self):
        req = self.request()
        r1 = req.create_entity('Folder', name=u"root1")
        r2 = req.create_entity('Folder', name=u"root2")
        c1 = req.create_entity('Folder', name=u"child1", filed_under=r1)
        itree_c1 = c1.cw_adapt_to('ITree')
        self.assertEquals([x.name for x in itree_c1.iterparents()], [u'root1'])
        self.assertEquals([x.name for x in itree_c1.iterparents(strict=False)],
                          [u'child1', u'root1'])
        # on a new entity
        e = self.vreg['etypes'].etype_class('Card')(req)
        form = self.vreg['forms'].select('edition', req, entity=e)
        field = form.field_by_name('filed_under', 'subject', eschema=e.e_schema)
        rschema = e.e_schema.subjrels['filed_under']
        folders = list(field.vocabulary(form))
        self.assertEquals(len(folders), 3)
        self.assertEquals(folders[0][0], u'root1')
        self.assertEquals(folders[1][0], u'root1 > child1')
        self.assertEquals(folders[2][0], u'root2')
        # on an existant unclassified entity
        e = self.execute('Any X WHERE X is Card').get_entity(0, 0)
        form = self.vreg['forms'].select('edition', req, entity=e)
        field = form.field_by_name('filed_under', 'subject', eschema=e.e_schema)
        folders = list(field.vocabulary(form))
        self.assertEquals(len(folders), 3)
        self.assertEquals(folders[0][0], u'root1')
        self.assertEquals(folders[1][0], u'root1 > child1')
        self.assertEquals(folders[2][0], u'root2')
        # on an existant classified entity
        self.execute('SET X filed_under Y WHERE X eid %s, Y name "child1"' % e.eid)
        assert e.filed_under
        folders = list(field.vocabulary(form))
        self.assertEquals(len(folders), 3)
        self.assertEquals(folders[0][0], u'root1')
        self.assertEquals(folders[1][0], u'root1 > child1')
        self.assertEquals(folders[2][0], u'root2')
        # on an existant classified entity LIMIT SET
        folders = list(field.vocabulary(form, limit=10))
        self.assertEquals(len(folders), 2)
        self.assertEquals(folders[0][0], u'root1')
        self.assertEquals(folders[1][0], u'root2')
        # on an existant folder entity, don't propose itself and descendants
        form = self.vreg['forms'].select('edition', req, entity=r1)
        field = form.field_by_name('filed_under', 'subject', eschema=e.e_schema)
        folders = list(field.vocabulary(form))
        self.assertEquals(len(folders), 1)
        self.assertEquals(folders[0][0], u'root2')

    def test_possible_views(self):
        req = self.request()
        possibleviews = self.pviews(req, None)
        self.failUnless(('tree', views.FolderTreeView) in possibleviews,
                        possibleviews)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
