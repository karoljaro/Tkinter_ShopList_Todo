from typing import Literal, Optional
import uuid

class _Product:
    def __init__(self, name: str, quantity: int, id: Optional[str] = None, purchased: bool = False) -> None:
        self.id: str = id or str(uuid.uuid4())
        self.name: str = name
        self.quantity: int = quantity
        self.purchased: bool = purchased

    @property
    def status(self) -> Literal['kupione', 'niekupione']:
        return "kupione" if self.purchased else "niekupione"

    def purchase(self) -> None:
        self.purchased = True

    def unpurchase(self) -> None:
        self.purchased = False