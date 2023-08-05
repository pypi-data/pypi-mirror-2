"""Nosy list unit tests"""

from cubicweb.devtools.testlib import CubicWebTC

class NosyListTestsCubicWebTC(CubicWebTC):
    """test nosylist specific behaviors"""

    def test_nosylist_added_after_adding_interested_in(self):
        user = self.create_user('test')
        self.execute('INSERT ObjectOfInterest O: O name "les fleurs"').get_entity(0, 0)
        rql = 'SET U interested_in O WHERE O name "les fleurs", U login "test"'
        self.execute(rql)
        rql = 'Any U WHERE O nosy_list U, O name "les fleurs", U login "test"'
        rset = self.execute(rql)
        self.assertEquals(len(rset), 1)
        self.assertEquals(rset[0][0], user.eid)

    def test_nosylist_propagation_creating_entity(self):
        user = self.create_user('test')
        self.login("test")
        self.execute('INSERT ObjectOfInterest O: O name "les gateaux"').get_entity(0, 0)
        rql = 'Any U WHERE O nosy_list U, O name "les gateaux"'
        rset = self.execute(rql)
        self.assertEquals(len(rset), 1)
        self.assertEquals(rset[0][0], user.eid)

    def test_nosylist_deletion_after_interested_in_deletion(self):
        user = self.create_user('test')
        self.login("test")
        self.execute('INSERT ObjectOfInterest O: O name "les gateaux"').get_entity(0, 0)
        rql = 'Any U WHERE O nosy_list U, O name "les gateaux"'
        rset = self.execute(rql)
        rql = 'DELETE U interested_in O WHERE O name "les gateaux", U login "test"'
        self.execute(rql)
        rql = 'Any U WHERE O nosy_list U, O name "les gateaux"'
        rset = self.execute(rql)
        self.assertEquals(len(rset), 0)

