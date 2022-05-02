import psycopg2
from .db_utils import dict_to_create_string, dict_to_insert_string, dict_to_update_string, list_to_where_string

database_config = {
    'HOST': 'localhost',
    'DATABASE': 'wms',
    'USER': 'postgres',
    'PASSOWORD': '@Eduardo404'
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


def execute(sql : str) -> None:
    """ Executes a sql string on database """

    assert isinstance(sql, str), 'sql must be a string'

    with connection() as conn:

        cur = conn.cursor()

        cur.execute(sql)

        cur.close()


def select(sql : str ) -> list:
    """ Runs a sql string on database and returns the result"""

    assert isinstance(sql, str), 'sql must be a string'

    with connection() as conn:

        cur = conn.cursor()

        cur.execute(sql)

        result = cur.fetchall()

        cur.close()
        
    return result


def delete(table_name: str, id: int) -> None:
    """
    Delete an object on database
    """

    assert isinstance(id, int), 'id must be an int'
    assert isinstance(table_name, str), 'table_name must be a valid table on database'

    execute(f'DELETE FROM {table_name} WHERE id = {id}')

    
def insert(table_name: str, values: dict) -> None:
    """
    Insert row on a database table
    """
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    assert isinstance(values, dict), 'values must be a dictionary with the values to insert on database'
    
    del values['id']

    insert_string = f'INSERT INTO {table_name}' + dict_to_insert_string(values)
        
    with connection() as conn:
        cur = conn.cursor()
        cur.execute(insert_string)
        conn.commit()
        

def update(table_name: str, values: dict) -> None:
    """
    Update a row on database
    """
    assert isinstance(table_name, str), 'table_name must be the name of a valid table on database'
    assert isinstance(values, dict), 'values must be a dictionary with the values to insert on database'
    

    update_string = f'UPDATE {table_name} ' + dict_to_update_string(values)
        
    with connection() as conn:
        cur = conn.cursor()
        cur.execute(update_string)
        conn.commit()
        