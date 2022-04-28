from database.utils import execute, select

class StoreHouse:

    table_name = 'tbl_storehouse'

    def __init__(self, name: str, qty_street: int, qty_building : int, qty_apartment : int, id: int = 0) -> None:
        """
            Never give the id
        """

        self.id = id
        self.name = name 
        self.qty_street = qty_street
        self.qty_building = qty_building
        self.qty_apartment = qty_apartment

        if self.id == 0:
            self.save(create=True)

    @classmethod
    def get_object(cls, sql : str):
        result = select(sql)[0] 

        id = result[0]
        name = result[1]
        qty_street = result[2]
        qty_building = result[3]
        qty_apartment = result[4]

        return cls(name, qty_street, qty_building, qty_apartment, id)

    def save(self, create: bool = False) -> None:
        """
            If create => creates a row on database with instance values (self)
            Else => update an existing row on database with instance values (self) and id
        """

        if create:
            values = f"('{self.name}', {self.qty_street}, {self.qty_building}, {self.qty_apartment});"
            sql = f'INSERT INTO {self.table_name} (name, qty_street, qty_building, qty_apartment) VALUES {values}'
            
        else:
            values = f"name='{self.name}', qty_street={self.qty_street}, qty_building={self.qty_building}, qty_apartment={self.qty_apartment}"
            sql = f'UPDATE {self.table_name} SET {values} WHERE id={self.id}'

        execute(sql)



    def __str__(self) -> str:
        """ Describes a class object """

        return f'id {self.id} name {self.name}'
    

    def generate_address(self) -> None:
        """
            Generates automaticly the storehouse's address by
            number of streets, buildings, apartments
        """

        address = []

        for st in range(1, self.qty_street + 1):
            for bl in [1, 2]:
                for bu in range(1, self.qty_building + 1):
                    for ap in range(1, self.qty_apartment + 1):
                        address.append(
                            {
                                'storehouse': self.id,
                                'street': st,
                                'block': bl,
                                'building': bu,
                                'apartment': ap
                            }
                        )

        return address


st = StoreHouse.get_object(f'SELECT * FROM {StoreHouse.table_name} WHERE id = 1')

print(st)

sth = StoreHouse('Bahia', 3, 12, 4)