from .db_utils import dict_to_create_string, dict_to_insert_string, dict_to_update_string, list_to_where_string
import psycopg2

database_config = {
    'HOST': 'localhost',
    'DATABASE': 'wms',
    'USER': 'postgres',
    'PASSOWORD': '88491662'
}


def connection() -> psycopg2.connect:
    """ Creates a connection to the database """

    conn = psycopg2.connect(
        host=database_config['HOST'],
        database=database_config['DATABASE'],
        user=database_config['USER'],
        password=database_config['PASSOWORD']
    )
    return conn


def show_tables() -> list:
    """
    Select that get all tables on database
    """

    with connection() as conn:
        cur = conn.cursor()
        cur.execute(" SELECT table_name FROM information_schema.tables WHERE table_schema='public' ")
        return cur.fetchall()


def create_table(table_name: str, fields: dict) -> None:
    """
    Create the table on database
    """
    
    assert isinstance(table_name, str), 'table_name must be a string with the name of the table to be created'
    

    # Checks if the table does not already exists on database
    if show_tables() and table_name in show_tables()[0]:
        raise ValueError('This table already exists on database')
    
    # Create the sql string
    create_string = f'CREATE TABLE {table_name}' + dict_to_create_string(fields) 
    
    with connection() as conn:
        cur = conn.cursor()
        cur.execute(create_string)




def drop_table(table_name: str) -> None:
    """
    Drop a given table on database
    """
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    
    with connection() as conn:
        cur = conn.cursor()
        cur.execute(f'DROP TABLE {table_name};')



def get_all_columns(table_name: str) -> list:
    """
    Get all the columns for a given table
    """
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    
    result = []
    
    with connection() as conn:
        cur = connection.cursor()
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
        cols = cur.fetchall()

    
    for col in cols:
        result.append(
            col[0]
        )

    return result;


def insert(table_name: str, values: dict) -> None:
    """
    Insert row on a database table
    """
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    assert isinstance(values, dict), 'values must be a dictionary with the values to insert on database'
    
    insert_string = f'INSERT INTO {table_name}' + dict_to_insert_string(values)
        
    with connection() as conn:
        cur = conn.cursor()
        cur.execute(insert_string)
        conn.commit()
        

def update(table_name: str, changes: dict, where=None) -> None:
    """
    Update a table by the given parameters
    changes =: Dictionary with keys(table field names) and values(values to change in which field)
    where =: where clause
    """
    
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    assert isinstance(changes, dict), 'changes must be a dictionary with the values of the set clause'


    update_string = f'UPDATE {table_name} ' +  dict_to_update_string(changes) + ' ' + (list_to_where_string(where) if where != None else ';')

    with connection() as conn:
        cur = connection.cursor()
        cur.execute(update_string)
        conn.commit()

        

def fetch_data(table_name: str, where: list = None) -> list:
    """
    Retrive from database rows on a table
    """
    
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    
    with connection() as conn:
        cur = connection.cursor()
        cur.execute(f'SELECT * FROM {table_name} {list_to_where_string(where) if where != None else ";"}')
        return cur.fetchall()

    



def get_objects(table_name: str, where: list = None) -> list:
    """
    Retrive from database all rows on a table and transform each row on a python dictionary
    """
    
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    
    columns = tuple([col['name'] for col in get_all_columns(table_name=table_name)])
    rows = fetch_data(table_name=table_name, where=where)

    result = []
    
    for row in rows:
       new_row = dict(zip(columns,row))
       result.append(new_row)
    
    return result
    
     