from ..database import execute, delete, select

class Product:
    table_name = 'tbl_product'

    def __init__(self, description: str, width: float, height: float, len: float, weight: float, price: float, id: int) -> None:
        """
            Never give the id
        """
        self.id = id
        self.description = description
        self.width = width
        self.height = height
        self.len = len
        self.weight = weight
        self.price = price


    def __str__(self) -> str:
        """ Describes a class object """
        return f'id: {self.id} description: {self.description}'


    def save(self, create: bool = False) -> None:
        """
            If create => creates a row on database with instance values (self)
            Else => update an existing row on database with instance values (self) and id
        """

        if create:
            values = f"('{self.description}', {self.width}, {self.height}, {self.len}, {self.weight}, {self.price});"
            sql = f'INSERT INTO {self.table_name} (description, width, height, len, weight, price) VALUES {values}'
            
        else:
            values = f"description='{self.description}', width={self.width}, height={self.height}, len={self.len}, weight={self.weight}, price={self.price}"
            sql = f'UPDATE {self.table_name} SET {values} WHERE id={self.id}'

        execute(sql)


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

        return cls(id=id, description=result[1], width=result[2],  height=result[3], len=result[4],  weight=result[5], price=result[6])
    

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
                cls( id=row[0], description=row[1], width=row[2], height=row[3], len=row[4], weight=row[5], price=row[6])
            )
            
        return result

    
    def get_cubic_volume(self) -> float:
        """
            Calculate the cubic volume of a product by its length, width and height
        """

        return round(self.len * self.width * self.height,2)