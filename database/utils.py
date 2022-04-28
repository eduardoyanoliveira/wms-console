import psycopg2

HOST = 'localhost'
DATABASE = 'wms'
USER = 'postgres'
PASSOWORD = '88491662'


def connection() -> psycopg2.connect:
    """ Creates a connection to the database """

    conn = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSOWORD
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
