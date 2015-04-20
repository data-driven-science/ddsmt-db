import subprocess
import pymongo
import os
import time

class DBHandler(object):
    """
    Class to start up and shutdown the database. The class also can
    add data for test purposes. It is used as by the dbhandler.py
    script and the test suite. It can fire up a database instance on
    the current host, but also connect to an exisisting database. 
    
    Start up the Mongo deamon and create a connection.

    >>> testport = 27018
    >>> dbname = 'test-db'
    >>> handler = DBHandler(port=testport, verbose=False)

    Create a new database, check that it exists, delete it and
    shutdown the daemon.
    
    >>> handler.create(dbname)
    >>> assert dbname in handler.info()

    Add some data to the database.

    >>> handler.set_data(dbname, {'my data' : 1})
    >>> assert handler.get_data(dbname)[0]['my data'] == 1

    """
    def __init__(self, port=None, dbpath=None, host=None, launch=True, verbose=False):
        if not dbpath:
            dbpath = os.getenv("MONGO_DBPATH", None)
        if launch:
            self.launch(port=port, dbpath=dbpath, verbose=verbose)
        if host is None:
            host = 'localhost'
        for count in range(4, 0, -1):
            try:
                self.client = pymongo.MongoClient(host, port)
            except pymongo.errors.ConnectionFailure:
                if count == 1:
                    raise
                time.sleep(5)
            else:
                break
            
        self.dbpath = dbpath
        self.verbose = verbose
        
    def launch(self, port=None, dbpath=None, verbose=False):
        command = ['mongod']
        if dbpath:
            command.append('--dbpath')
            command.append(dbpath)
        if port:
            command.append('--port')
            command.append(str(port))
        if verbose:
            stdout = None
        else:
            stdout = open(os.devnull, 'w')
        subprocess.Popen(command, stdout=stdout)

    def create(self, dbname):
        db = self.client[dbname]
        self.delete(dbname)
        db = self.client[dbname]
        collection = db.test
        collection.insert({})
        collection.drop()
        
    def info(self):
        return self.client.database_names()

    def delete(self, dbname):
        self.client.drop_database(dbname)

    def set_data(self, dbname, data):
        db = self.client[dbname]
        collection = db.test
        collection.drop()
        collection = db.test
        collection.insert(data)
            
    def get_data(self, dbname):
        db = self.client[dbname]
        return list(db.test.find())
        
    def shutdown(self):
        command = ['mongod']
        command.append('--shutdown')
        if self.dbpath:
            command.append('--dbpath')
            command.append(self.dbpath)
        if self.verbose:
            stdout = None
        else:
            stdout = open(os.devnull, 'w')
        subprocess.Popen(command, stdout=stdout)

    
