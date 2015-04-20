from ddsmdb.common.core import setup_app
from flask.ext.testing import LiveServerTestCase
import twill

class DatabaseTest(LiveServerTestCase):
    LIVESERVER_PORT = 5210
    def create_app(self):
        app = setup_app(__name__, 'ddsmdb.test.config')
        app.config['LIVESERVER_PORT'] = self.LIVESERVER_PORT
        DatabaseTest.LIVESERVER_PORT += 10
        # try:
        #     browser = twill.get_browser()
        #     browser.go("http://localhost:5200/")
        #     app = setup_app(__name__, 'ddsmdb.test.integrate')
        #     app.config['LIVESERVER_PORT'] = 5210
        #     app.config['TESTING'] = True
        #     app.config['MONGODB_SETTINGS'] = {'db': 'ddsm-integrate','host': 'localhost','port': 27017}
        # except:
        #     app = setup_app(__name__, 'ddsmdb.test.integrate')
        #     app.config['LIVESERVER_PORT'] = 5200
        #     app.config['TESTING'] = True
        #     app.config['MONGODB_SETTINGS'] = {'db': 'ddsm-integrate','host': 'localhost','port': 2701
  
        return app

    def setUp(self):
    	# Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test(self):

    	print "This is a test to check that the api endpoints are working properly."
        browser = twill.get_browser()
        browser.go("http://localhost:27018/")
        self.assertTrue(browser.get_code() in (200, 201))

    # def test_hi(self):
    #     self.assertTrue(True)

    def tearDown(self):
        del self.app
        print "Supposed to tear down the testcase."
        print "Which most likely means to clear the database of all records."

class DummyTest(DatabaseTest):
    def test(self):
        self.assertTrue(True)


class DummyTest1(DatabaseTest):
    def test(self):
        self.assertTrue(True)

