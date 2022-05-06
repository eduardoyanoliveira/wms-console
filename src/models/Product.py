from .abstract import DataBaseModel
class Product(DataBaseModel):
    
    table_name = 'tbl_product'

    def __init__(self, id: int, description: str, width: float, height: float, len: float, weight: float, price: float) -> None:
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
        
        
        if self.id == 0:
            self.save(create=True)


    def __str__(self) -> str:
        """ Describes a class object """
        return f'id: {self.id} description: {self.description}'


    def get_cubic_volume(self) -> float:
        """
            Calculate the cubic volume of a product by its length, width and height
        """

        return round(self.len * self.width * self.height,2)
