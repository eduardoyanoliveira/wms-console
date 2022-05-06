from .abstract import DataBaseModel

class StoreHouse(DataBaseModel):

    table_name = 'tbl_storehouse'

    def __init__(self, id: int, name: str) -> None:
        """
            Never give the id
        """
        
        self.id = id
        self.name = name 


        if self.id == 0:
            self.save(create=True)


    def __str__(self) -> str:
        """ Describes a class object """
        
        return f'name {self.name}'


