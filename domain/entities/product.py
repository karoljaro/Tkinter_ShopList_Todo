from typing import Literal

class Product:
     def __init__(self, id: int, name: str, quantity: int) -> None:
        self.id: int = id
        self.name: str = name
        self.quantity: int = quantity
        self.purchased: bool = False
        self.status: Literal['kupione'] | Literal['niekupione'] = "kupione" if self.purchased else "niekupione"