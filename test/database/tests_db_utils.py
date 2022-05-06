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

import unittest
from database import db_utils   

class TestDictToInsertStringCase(unittest.TestCase):
    
    # values to insert into the table
    values = {
        'NAME': 'iPhone',
        'PRICE': 1200.00,
        'STOCK': 230
    }
    
    def test_values_value_error(self) -> None:    
        with self.assertRaises(AssertionError):
            db_utils.dict_to_insert_string(values='values')
    
    
    def test_dict_to_create_string(self):
        self.assertEqual(db_utils.dict_to_insert_string(self.values), "(NAME,PRICE,STOCK) VALUES ('iPhone',1200.0,230);")
    

class TestDictToUpdateStringCase(unittest.TestCase):
    
    # dictionary with changes to make in a row
    changes = {
        'id': 1,
        'PRICE': 1000.00,
        'STOCK': 30
    }
    
    def test_changes_value_error(self) -> None:
        with self.assertRaises(AssertionError):
            db_utils.dict_to_update_string('changes')
    
    def test_dict_to_update_string(self) -> None:
        self.assertEqual(db_utils.dict_to_update_string(self.changes), 'SET PRICE = 1000.0,STOCK = 30 WHERE id = 1')


class TestCheckWhereClauseDictCase(unittest.TestCase):
    
    def test_dictionary_value_error(self) -> None:
        with self.assertRaises(AssertionError):
            db_utils.check_where_clause_dict('dictionary')
    
    
    def test_dict_with_missing_filed_key(self) -> None:
        self.assertFalse(
            db_utils.check_where_clause_dict(
                {  
                    'value': 1,
                    'operator': '=',
                }
            )
        )
    
    
    def test_dict_with_missing_operator_key(self) -> None:
        self.assertFalse(
            db_utils.check_where_clause_dict(
                {
                    'field': 'ID',
                    'value': 1,
                }
            )
        )
     
    
    def test_dict_with_missing_value_key(self) -> None:
        self.assertFalse(
            db_utils.check_where_clause_dict(
                {
                    'field': 'ID',
                    'operator': '=',
                }
            )
        )
    
    def test_success_check(self) -> None:
        self.assertTrue(
            db_utils.check_where_clause_dict(
                {
                'field': 'ID',
                'operator': '=',
                'value': 1
                }
            )
        )


class TestListToWhereStringCase(unittest.TestCase):
    
      
    # where clause
    where = [
        {
            'field': 'ID',
            'operator': '=',
            'value': 1
        },
        {
            'field': 'NAME',
            'operator': '=',
            'value': 'iPhone'
        }
    ]
    
    def test_where_value_error(self) -> None:
        with self.assertRaises(AssertionError):
            db_utils.list_to_where_string('where')
    
    def test_invalid_dict_error(self) -> None:
        with self.assertRaises(ValueError):
            db_utils.list_to_where_string([{
                'field': 'ID',
                'operator': '=',
            }]) 
            
    def test_list_to_where_string(self) -> None:
        self.assertEqual(db_utils.list_to_where_string(self.where), "WHERE ID = 1 and NAME = 'iPhone' ;")
        
        
    def test_list_to_where_string_unique_index(self) -> None:
        self.assertEqual(
            db_utils.list_to_where_string(
                [{
                    'field': 'ID',
                    'operator': '=',
                    'value': 1
                }]
            ),
        "WHERE ID = 1 ;")

if __name__ == '__main__':
    unittest.main()