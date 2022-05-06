from .abstract import DataBaseModel

class Address(DataBaseModel):
    
    table_name = 'tbl_address'
    
    def __init__(self, id: int, storehouse_id: int, street_number: int, block_number : int, building_number : int, apartment_number : int, product_id : int, product_qty : int) -> None:
        
        self.id = id
        self.storehouse_id= storehouse_id
        self.street_number = street_number
        self.block_number = block_number
        self.building_number = building_number
        self.apartment_number = apartment_number
        self.product_id = product_id
        self.product_qty = product_qty

          
        if self.id == 0:
            self.save(create=True)
        
    
    def __str__(self) -> str:
        """ Describes a class object """
        return f'id: {self.id}'
