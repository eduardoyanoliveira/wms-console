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
from models.Product import Product
from models.Address import Address

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

                cur.execute("CREATE TABLE tbl_address(id serial primary key, storehouse_id integer,street_number integer,block_number integer,building_number integer,apartment_number integer,product_id integer,product_qty decimal);")
                
                conn.commit()
                
                cur.execute("CREATE TABLE tbl_storehouse (id serial primary key, name varchar(70));")
                conn.commit()

                cur.execute("CREATE TABLE tbl_product (id serial primary key ,description varchar,width decimal,height integer,len decimal,weight decimal,price decimal,cubic_volume decimal);")
                conn.commit()
                
                cur.execute("ALTER TABLE tbl_address ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES tbl_product(id);")
                cur.execute("ALTER TABLE tbl_address ADD CONSTRAINT fk_storehouse_id FOREIGN KEY (storehouse_id) REFERENCES tbl_storehouse(id);")
                conn.commit()
                
                cur.close()


    @classmethod
    def tearDownClass(cls) -> None:

        with cls.config_conn:
            with database_methods.connection() as conn:
                cur = conn.cursor()

                cur.execute('DROP TABLE tbl_address;')
                cur.execute('DROP TABLE tbl_product;')
                cur.execute('DROP TABLE tbl_storehouse;')
                conn.commit()
                

                cur.close()
                

# Address Tests
class TestAddressCase(MockDB):
    
    def setUp(self) -> None:
        StoreHouse(id=0, name='test')
        Product(id=0, description='iPhone', width=300, height=600, len=5, weight=.250, price=5000)
        
        return super().setUp()
    
    def test_should_create_a_new_address(self) -> None:
        test_st = StoreHouse.get_object_by_id(1)
        test_product = Product.get_object_by_id(1)
        Address(id=0, storehouse_id= test_st.id, street_number=1, block_number=2, building_number=3, apartment_number=5, product_id=test_product.id, product_qty=50)
        
        test_address = Address.get_object_by_id(1)
        
        self.assertEqual(test_address.storehouse_id, 1)
        self.assertEqual(test_address.street_number, 1)
        self.assertEqual(test_address.block_number, 2)
        self.assertEqual(test_address.building_number, 3)
        self.assertEqual(test_address.apartment_number, 5)
        self.assertEqual(test_address.product_id, 1)
        self.assertEqual(test_address.product_qty, 50)
        

if __name__ == '__main__':
    main()