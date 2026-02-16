from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ProductCreate(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)

    # Custom validation to prevent blank names
    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Product name cannot be blank")
        return value.strip()


class ProductUpdate(BaseModel):
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)


class ProductResponse(BaseModel):
    id: int
    product_name: str
    price: float
    stock_quantity: int

    class Config:
        from_attributes = True
