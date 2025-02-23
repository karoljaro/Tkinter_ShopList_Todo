from dataclasses import dataclass, field
from typing import Optional
import uuid

@dataclass
class _Product:
    name: str
    quantity: int
    id: Optional[str] = field(default=None)
    purchased: bool = False

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if not self.name:
            raise ValueError('Product name cannot be empty.')
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError('Quantity must be a positive integer.')