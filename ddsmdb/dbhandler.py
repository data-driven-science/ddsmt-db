import subprocess
import pymongo
import os

class DBHandler(object):
    """
    Class to start up and shutdown the database. The class also can
    add data for test purposes. It is used as by the dbhandler.py
    script and the test suite. It can fire up a database instance on
    the current host, but also connect to an exisisting database. 
    
    Start up the Mongo deamon and create a connection.

    >>> testport = 27018
    >>> dbname = 'test-db'
    >>> db = DBHandler(port=testport)

    Create a new database, check that it exists, delete it and
    shutdown the daemon.
    
    >>> db.create(dbname)
    >>> assert 'test-db' in db.info()
    >>> db.delete(dbname)

    Shutdown the daemon.
    
    >>> db.shutdown()

    Start up the deamon.

    >>> db0 = DBHandler(port=testport)
    
    Use a separate instance to access the database.

    >>> db1 = DBHandler(port=testport)

    Create a database.

    >>> db1.create(dbname)
    >>> db1.append_data(dbname, {'my-data' : 1})
    >>> print db.get_data()
    
    """
    def __init__(self, port=27017, dbpath=None, host='localhost'):
        
        if not dbpath:
            dbpath = os.getenv("MONGO_DBPATH", None)
        try:
            self.client = pymongo.MongoClient(host, port)
        except pymongo.errors.ConnectionFailure:
            self.launch(port=port, dbpath=dbpath)
            self.client = pymongo.MongoClient(host, port)
        self.dbpath = dbpath
        self.collection = 'setup-collection'            
        
    def launch(self, port=27017, dbpath=None):
        command = ['mongod']
        if dbpath:
            command.append('--dbpath')
            command.append(dbpath)
        command.append('--port')
        command.append(str(port))
        subprocess.Popen(command)

    def create(self, dbname):
        db = self.client[dbname]
        collection = db[self.collection]
        collection.insert({'setup-data' : True})
    
    def info(self):
        return self.client.database_names()

    def delete(self, dbname):
        self.client.drop_database(dbname)

    def append_data(self, dbname, data):
        db = self.client[dbname]
        collection = db[self.collection]
        collection.insert(data)

    def get_data(self, dbname):
        db = self.client[dbname]
        return db[self.collection].get()
        
    def shutdown(self):
        command = ['mongod']
        command.append('--shutdown')
        if self.dbpath:
            command.append('--dbpath')
            command.append(self.dbpath)
        subprocess.call(command)

