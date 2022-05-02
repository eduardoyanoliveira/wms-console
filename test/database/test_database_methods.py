try:
    import os
    import sys
    
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '../../src'
            )
        )
    )
except:
    raise


from unittest import TestCase, main
from unittest.mock import patch
from database import database_methods

class MockSqliteDB(TestCase):
    """
    Create a Mock database for testing
    """
   
    # Test Database connection config 
    database_config = {
        'HOST': 'localhost',
        'DATABASE': 'test_wms',
        'USER': 'postgres',
        'PASSOWORD': '88491662'
    }


    @classmethod
    def setUpClass(cls) -> None:
        
        cls.config_conn = patch.dict(database_methods.database_config, cls.database_config)

  
        with cls.config_conn:
            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute('CREATE TABLE tbl_test (id serial primary key, name varchar(70));')
                conn.commit()

                cur.close()


    @classmethod
    def tearDownClass(cls) -> None:

        with cls.config_conn:
            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute('DROP TABLE tbl_test;')
                conn.commit()

                cur.close()


class TestInsertCase(MockSqliteDB):

    def test_should_insert_a_row_on_table(self) -> None:
        with self.config_conn:
            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute("INSERT INTO tbl_test (name) VALUES ('test');")
                conn.commit()

                cur.close()


            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute("select * FROM  tbl_test WHERE id = 1")
                print('###########', cur.fetchall())
                conn.commit()

                cur.close()


if __name__ == '__main__':
    main()