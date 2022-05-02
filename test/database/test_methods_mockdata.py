table_name_one = 'tbl_product'
    
# Fields to creata a table
fields_one = {
    'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'NAME': 'TEXT',
    'PRICE': 'REAL',
    'STOCK': 'INTEGER'
}

values_one =   {
    'NAME': 'iPhone',
    'PRICE': 1200.00,
    'STOCK': 230
}

# values to insert into the table
values_list_one = [
    {
        'NAME': 'iPhone',
        'PRICE': 1200.00,
        'STOCK': 230
    },
    {
        'NAME': 'MacBook',
        'PRICE': 2000.00,
        'STOCK': 30
    },
    {
        'NAME': 'AirDots',
        'PRICE': 300.00,
        'STOCK': 50
    }
]

# where clauses
basic_where = [
    {
        'field': 'ID',
        'operator': '=',
        'value': 1
    }
]
    