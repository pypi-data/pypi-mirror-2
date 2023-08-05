
from cubicweb import ValidationError

from cubicweb.devtools.testlib import CubicWebTC


class HooksTC(CubicWebTC):

    def setup_database(self):
        self.foldr = self.request().create_entity(u'Folder', name=u'xyz')
        self.foldr2 = self.request().create_entity(u'Folder', name=u'xyz2')


    def test_folder_no_conflict(self):
        wp1 = self.execute(u'INSERT Folder F: F name "foo", F filed_under PF '
                           u'WHERE PF eid %(x)s', {'x' : self.foldr.eid})[0][0]
        wp2 = self.execute(u'INSERT Folder F: F name "foo", F filed_under PF '
                           u'WHERE PF eid %(x)s', {'x' : self.foldr2.eid})[0][0]
        self.commit()


    def test_folder_insertion_with_name_conflict(self):
        self.execute(u'INSERT Folder F: F name "foo", F filed_under PF '
                     u'WHERE PF eid %(x)s', {'x' : self.foldr.eid})
        self.commit()
        self.assertRaises(ValidationError, self.execute,
                          u'INSERT Folder F: F name "foo", F filed_under PF '
                          u'WHERE PF eid %(x)s', {'x' : self.foldr.eid})


    def test_folder_update_with_name_conflict(self):
        wp1 = self.execute(u'INSERT Folder F: F name "foo", F filed_under PF '
                           u'WHERE PF eid %(x)s', {'x' : self.foldr.eid})[0][0]
        wp2 = self.execute(u'INSERT Folder F: F name "foo2", F filed_under PF '
                           u'WHERE PF eid %(x)s', {'x' : self.foldr.eid})[0][0]
        self.commit()
        self.assertRaises(ValidationError, self.execute,
                          u'SET X name "foo" WHERE X eid %s' % wp2)


    def test_folder_description_update(self):
        """checks that we can update a F's description
        without having a UNIQUE violation error
        """
        wp1 = self.execute(u'INSERT Folder F: F name "foo", F filed_under PF '
                           u'WHERE PF eid %(x)s', {'x' : self.foldr.eid})[0][0]
        wp2 = self.execute(u'INSERT Folder F: F name "foo2", F filed_under PF '
                           u'WHERE PF eid %(x)s', {'x' : self.foldr.eid})[0][0]
        self.commit()
        # we should be able to update description only
        self.execute('SET X description "foo" WHERE X eid %s' % wp2)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
