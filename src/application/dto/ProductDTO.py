from pydantic import BaseModel, field_validator, Field
from typing import Optional


class ProductDTO(BaseModel):
    """
    Data transfer object for product.
    """

    id: Optional[str] = None
    name: str
    quantity: int
    purchased: Optional[bool] = Field(default=False)

    @field_validator("quantity")
    def quantity_must_be_positive(cls, v):
        """
        Validate that the quantity is a positive integer.

        :param v: The quantity value.
        :return: The validated quantity.
        :raises ValueError: If the quantity is not a positive integer.
        """
        if not isinstance(v, int):
            raise ValueError("Quantity must be an integer")
        if v <= 0:
            raise ValueError("Quantity must be positive")
        return v

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        """
        Validate that the name is not empty.

        :param v: The name value.
        :return: The validated name.
        :raises ValueError: If the name is empty.
        """
        if not v:
            raise ValueError("Product name cannot be empty.")
        return v
