from pydantic import BaseModel, field_validator, Field
from typing import Optional

class ProductDTO(BaseModel):
    id: Optional[str] = None
    name: str
    quantity: int
    purchased: Optional[bool] = Field(default=False)

    @field_validator('quantity')
    def quantity_must_be_positive(cls, v):
        if not isinstance(v, int):
            raise ValueError("Quantity must be an integer")
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v
    
    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Product name cannot be empty.')
        return v