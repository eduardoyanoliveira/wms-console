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
from database import database_methods, database_test_config


class MockDB(TestCase):
    """
    Create a Mock database for testing
    """
   
    # Test Database connection config 
    database_config = database_test_config

    @classmethod
    def setUpClass(cls) -> None:
        
        cls.config_conn = patch.dict(database_methods.database_config, cls.database_config)

  
        with cls.config_conn:
            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute('CREATE TABLE tbl_test (id serial primary key, name varchar(70));')
                conn.commit()
                
                cur.execute('CREATE TABLE tbl_product (id serial primary key, name text, price decimal, stock integer);')
                conn.commit()

                cur.close()


    @classmethod
    def tearDownClass(cls) -> None:

        with cls.config_conn:
            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute('DROP TABLE tbl_test;')
                conn.commit()
                
                cur.execute('DROP TABLE tbl_product;')
                conn.commit()

                cur.close()


# ShowTable Funciton Tests 
class TestShowTablesCase(MockDB):
    
    def test_select_all_tables(self) -> None:
        with self.config_conn:
            self.assertIsInstance(database_methods.show_tables(), list)
            

# Insert Function Tests
class TestInsertCase(MockDB):
    
    def test_should_raises_an_error_if_the_parameter_table_name_is_not_a_string(self) -> None:
        with self.assertRaises(AssertionError):
            database_methods.insert(table_name=2, values={'name': 'Test'})
    
    
    def test_should_raises_an_error_if_the_parameter_values_is_not_a_dictionary(self) -> None:
        with self.assertRaises(AssertionError):
            database_methods.insert(table_name='tbl_test', values=('name', 'Test'))


    def test_should_raise_an_error_if_table_name_is_not_a_valid_table_on_database(self) -> None:
        with self.assertRaises(ValueError):
            database_methods.insert(table_name='tbl_store', values={'name': 'Test'})


    def test_should_insert_a_row_on_tbl_test(self) -> None:
        
        with self.config_conn:
            database_methods.insert('tbl_test', {'name': 'Test'})
            result = database_methods.select('SELECT * FROM tbl_test')
            self.assertEqual(len(result), 1)
    
    
    def test_should_insert_a_row_on_tbl_product(self) -> None:
        
        with self.config_conn:
            database_methods.insert('tbl_product', {'name': 'Test', 'price': 12.5, 'stock': 23})
            result = database_methods.select('SELECT * FROM tbl_product')
            self.assertEqual(len(result), 1)


# Update Function Tests
class TestUpdateCase(MockDB):
    
    def test_should_raises_an_error_if_the_parameter_table_name_is_not_a_string(self) -> None:
        with self.assertRaises(AssertionError):
            database_methods.update(table_name=2, values={'name': 'Test'})
    
    
    def test_should_raises_an_error_if_the_parameter_values_is_not_a_dictionary(self) -> None:
        with self.assertRaises(AssertionError):
            database_methods.update(table_name='tbl_test', values=('name', 'Test'))


    def test_should_raise_an_error_if_table_name_is_not_a_valid_table_on_database(self) -> None:
        with self.assertRaises(ValueError):
            database_methods.update(table_name='tbl_store', values={'name': 'Test'})
            
            
    def test_should_update_a_row_on_the_table_on_database(self) -> None:
        with self.config_conn:
            database_methods.insert('tbl_product', {'name': 'Test', 'price': 12.5, 'stock': 23})
            database_methods.update(table_name='tbl_product', values={'id': 1, 'name': 'iPhone'})
            product = database_methods.select('SELECT * FROM tbl_product WHERE id = 1')
            self.assertEqual(product[0][1], 'iPhone')


# Delete Funciton Tests
class TestDeleteCase(MockDB):
    
    def test_should_raises_an_error_if_the_parameter_table_name_is_not_a_string(self) -> None:
        with self.assertRaises(AssertionError):
            database_methods.delete(table_name=2, id=1)
    
    
    def test_should_raises_an_error_if_the_parameter_values_is_not_an_integer(self) -> None:
        with self.assertRaises(AssertionError):
            database_methods.delete(table_name='tbl_test', id='1')


    def test_should_raise_an_error_if_table_name_is_not_a_valid_table_on_database(self) -> None:
        with self.assertRaises(ValueError):
            database_methods.delete(table_name='tbl_store', id=1)
      
            
    def test_should_delete_a_row_on_the_table_on_database(self) -> None:
        with self.config_conn:
            database_methods.insert('tbl_product', {'name': 'Test', 'price': 12.5, 'stock': 23})
            database_methods.delete(table_name='tbl_product', id=1)
            products = database_methods.select('SELECT * FROM tbl_product')
            self.assertEqual(len(products), 0)
            
            
if __name__ == '__main__':
    main()