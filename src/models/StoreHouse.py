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


from database import execute, select, delete, insert, update

class StoreHouse:

    table_name = 'tbl_storehouse'

    def __init__(self, name: str, id: int = 0) -> None:
        """
            Never give the id
        """

        self.id = id
        self.name = name 


        if self.id == 0:
            self.save(create=True)

    def __str__(self) -> str:
        """ Describes a class object """

        return f'id {self.id} name {self.name}'


    def save(self, create: bool = False) -> None:
        """
            If create => creates a row on database with instance values (self)
            Else => update an existing row on database with instance values (self) and id
        """

        if create:
            insert(self.table_name, self.__dict__)  
        else:
            update(self.table_name, self.__dict__)


      

    @classmethod
    def delete_object(cls, id : int) -> None:
        """
        Delete an object on database
        """

        delete(cls.table_name, id)
    

    @classmethod
    def get_object_by_id(cls, id : int):
        """
            Gets an object on database by the given id
        """
        assert isinstance(id, int), 'id must be an integer number'

        sql = f'SELECT * FROM {cls.table_name} WHERE id = {id}'
        result = select(sql)[0] 

        return cls(id=id, name=result[1])
    

    @classmethod
    def get_all_objects(cls) -> list:
        """
        Get all rows on database and transform into a instance, then returns a list of these objects
        """
        
        rows = select(f'SELECT * FROM {cls.table_name};')
        
        result = []
        
        # if there are no rows on database, return
        if not len(rows):
            return
        
        for row in rows:
            result.append(
                cls( id=row[0], name=row[1])
            )
            
        return result
    
    def get_props(self) -> None:
        return self.__dict__
    
    


st = StoreHouse.get_object_by_id(1)

st.name = 'São paulo'

st.save()