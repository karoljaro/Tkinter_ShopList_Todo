from dataclasses import dataclass, field
from typing import Optional
import uuid

@dataclass
class _Product:
    """
    Domain entity representing a product.
    """
    name: str
    quantity: int
    id: Optional[str] = field(default=None)
    purchased: bool = False

    def __post_init__(self):
        """
        Post-initialization method to set default values and validate fields.
        
        - Generates a unique ID if not provided.
        - Validates that the name is not empty.
        - Validates that the quantity is a positive integer.
        
        :raises ValueError: If the name is empty or the quantity is not a positive integer.
        """
        if self.id is None:
            self.id = str(uuid.uuid4())
        if not self.name:
            raise ValueError('Product name cannot be empty.')
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError('Quantity must be a positive integer.')