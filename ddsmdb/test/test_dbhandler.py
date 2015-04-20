import os
from ddsmdb.dbhandler import DBHandler

def test(): 
    """
    Load a small json file and then check that the data is in the
    database. The test needs the check that a JSON object that is a
    list is read into the database correctly and extracted correctly.
    """
    
    import json
    base = os.path.split(__file__)[0]
    filepath = os.path.join(base, os.pardir, 'data', 'test.json')
    with open(filepath, 'r') as f:
        data = json.load(f)

    testport = 27018
    dbname = 'test-db'
    handler = DBHandler(port=testport, verbose=False)

    handler.create(dbname)
    handler.set_data(dbname, data)
    new_data = handler.get_data(dbname)


    assert data == new_data
