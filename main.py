from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal, Base
from models import Product
from schemas import ProductCreate, ProductUpdate, ProductResponse

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Inventory API")

# ROOT ROUTE (important to avoid Not Found)
@app.get("/")
def home():
    return {"message": "Product Inventory API Running Successfully"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE PRODUCT
@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    existing = db.query(Product).filter(
        Product.product_name == product.product_name
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")

    new_product = Product(
        product_name=product.product_name.strip(),
        price=product.price,
        stock_quantity=product.stock_quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# GET ALL PRODUCTS
@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# GET PRODUCT BY ID
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# UPDATE PRODUCT
@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.stock_quantity is not None:
        product.stock_quantity = product_data.stock_quantity

    db.commit()
    db.refresh(product)

    return product


# DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}




