def field_format(field: any) -> any:
    """
    Format a database field, to make a correct sql string
    """
    
    if isinstance(field, str):
        return f"'{field}'"
    
    if isinstance(field, type):
        return field.id
    
    return field


def dict_to_insert_string(values: dict) -> str:
    """
        Creates a sql insert string
    """
    assert isinstance(values, dict), 'values must be a dictionary with the fields and values to be insert'

    try:
        fields = '(' + ''.join([f'{field},' for field in values])[:-1] + ')'
        insert_values = '(' + ''.join([f"{field_format(field)}," for field in values.values()])[:-1] + ');'
        return fields + ' VALUES ' + insert_values
    except AttributeError as err:
        print(err)


def dict_to_update_string(changes: dict) -> str:
    """
    Transform a dictionary into a string set for update on database
    """
    assert isinstance(changes, dict), 'changes must be a dictionary'
    
    id =  changes.pop('id', changes['id'])
    
    sql = 'SET ' +''.join([f"{key} = {field_format(value)}," for key, value in changes.items()])[:-1]
    
    sql += f" WHERE id = {id}"
    
    return sql


def check_where_clause_dict(dictionary: dict) -> bool:
    """
    Checks if a dictionary has all the required keys to pass on list_to_where_string function
    """
    
    assert isinstance(dictionary, dict), 'dictionary must be a instance of dict'
    
    keys = [key for key in dictionary]
    
    if not 'field' in keys or not 'operator' in keys or not 'value' in keys:
        return False
    
    return True


def list_to_where_string(where: list) -> str:
    """
    Transform a list of dictionaries into a where clause string
    """
    
    assert isinstance(where, list), 'where must be a list of dictionaries'
    

    result = 'WHERE '
    
    try:
        for item in where:
            if not check_where_clause_dict(item):
                raise ValueError('List contains an invalid dictionary')
            
            field = item['field']
            operator = item['operator']
            value = f"'{item['value']}'" if isinstance(item['value'],str) else item['value']
            
            result += f'{field} {operator} {value} and '
    except KeyError as err:
        print(err)
        
    return result[:-4] + ';'