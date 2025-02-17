from typing import Literal, Optional
import uuid

class _Product:
    def __init__(self, name: str, quantity: int, id: Optional[str] = None) -> None:
        self.id: str = id or str(uuid.uuid4())
        self.name: str = name
        self.quantity: int = quantity
        self._purchased: bool = False

    @property
    def purchased(self) -> bool:
        return self._purchased

    @purchased.setter
    def purchased(self, value: bool) -> None:
        self._purchased = value

    @property
    def status(self) -> Literal['kupione', 'niekupione']:
        return "kupione" if self._purchased else "niekupione"

    def purchase(self) -> None:
        self.purchased = True

    def unpurchase(self) -> None:
        self.purchased = False