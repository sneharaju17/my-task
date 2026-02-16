from sqlalchemy import Column, Integer, String, Numeric, CheckConstraint
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('stock_quantity >= 0', name='stock_non_negative'),
        CheckConstraint('price >= 0', name='price_non_negative'),
    )

