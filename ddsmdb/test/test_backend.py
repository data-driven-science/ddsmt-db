from ddsmdb.common.core import setup_app
from ddsmdb.dbhandler import DBHandler
from flask.ext.testing import TestCase
from flask.ext.testing import Twill
import config

class DatabaseTest(TestCase):
    def create_app(self):
        testport = config.MONGODB_SETTINGS['port']
        testhost = config.MONGODB_SETTINGS['host']
        self.handler =  DBHandler(port=testport, host=testhost)
        app = setup_app(__name__, 'ddsmdb.test.config')
        return app

    def setUp(self):
    	# Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test_db(self):
        """
        Test that the database endpoints are available.
        """
        t = Twill(self.app, host='localhost', port=27018)
        t.browser.go(t.url("/"))
        self.assertTrue(t.browser.get_code() in (200, 201))

    def tearDown(self):
        dbname = config.MONGODB_SETTINGS['db']
        self.handler.delete(dbname)
        self.handler.client.close()
        del self.app


