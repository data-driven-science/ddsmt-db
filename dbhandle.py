import click

from ddsmdb.dbhandler import DBHandler
import json
import pprint

@click.command()
@click.option('--launch/--no-launch', default=True, help="run mongod with `--dbpath`")
@click.option('--info/--no-info', default=False, help="the names of the databases")
@click.option('--create/--no-create', default=False, help="create a database")
@click.option('--delete/--no-delete', default=False, help="delete a database")
@click.option('--dbname', default=None, help="the name of the db")
@click.option('--shutdown/--no-shutdown', default=False, help='shutdown the database server using `--dbpath`')
@click.option('--dbpath', default=None, help='specify the dbpath to run or remove')
@click.option('--verbose/--no-verbose', default=False, help="dump mongod output to stdout")
@click.option('--port', default=None, type=int, help="the port number")
@click.option('--host', default=None, help="the host")
@click.option('--jsonfile', default=None, help="upload JSON data to database")
@click.option('--view/--no-view', default=False, help="dump the data in the database to screeen")

def handle(launch,
           info,
           create,
           delete,
           dbname,
           shutdown,
           dbpath,
           verbose,
           port,
           host,
           jsonfile,
           view):

    if shutdown:
        launch = False
        
    handler = DBHandler(port=port, dbpath=dbpath, host=host, launch=launch, verbose=verbose)

    if create or delete or jsonfile or view:
        if not dbname:
            dbname = click.prompt('enter a db name', type=str)
            
    if create:
        handler.create(dbname)

    if info:
        info = handler.info()
        click.echo(info)
        
    if delete:
        handler.delete(dbname)

    if jsonfile:
        with open(jsonfile, 'r') as f:
            data = json.load(f)
        handler.create(dbname)
        handler.set_data(dbname, data)

    if view:
        data = handler.get_data(dbname)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(data)
        
    if shutdown:
        handler.shutdown()
        
if __name__ == "__main__":
    handle()
    

