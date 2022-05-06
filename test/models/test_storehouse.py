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
from models.StoreHouse import StoreHouse


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

                cur.execute("CREATE TABLE tbl_storehouse (id serial primary key, name varchar(70));")
                conn.commit()

                cur.close()


    @classmethod
    def tearDownClass(cls) -> None:

        with cls.config_conn:
            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute('DROP TABLE tbl_storehouse;')
                conn.commit()
                

                cur.close()


# StoreHouse Tests
class TestStoreHouseCase(MockDB):
    
    def test_should_create_a_row_on_database(self) -> None:
        with self.config_conn:
            StoreHouse(name='test')
            st = StoreHouse.get_object_by_id(1)
            
            self.assertIsInstance(st, StoreHouse, msg='st should be an instance of StoreHouse')
            self.assertEqual(st.id, 1)
            self.assertEqual(st.name, 'test')


    def test_should_return_all_objects_of_the_class_on_database(self) -> None:
        with self.config_conn:
            StoreHouse(name='another test')
            storehouses = StoreHouse.get_all_objects()
            
            self.assertEqual(len(storehouses), 2)


    def test_should_delete_an_object_on_database(self) -> None:
        with self.config_conn:
            StoreHouse(name='other test')
            StoreHouse.delete_object(1)
            storehouses = StoreHouse.get_all_objects()
            
            self.assertEqual(len(storehouses), 1)
            
    def test_should_update_an_object_on_database(self) -> None:
        with self.config_conn:
            StoreHouse(name='other test')
            st = StoreHouse.get_object_by_id(1)
            st.name = 'update test'
            st.save()
            new_st = StoreHouse.get_object_by_id(1)
            
            self.assertEqual(new_st.name, 'other test')
    
    
if __name__ == '__main__':
    main()