from main import app, db
from schema.product import Product
from schema.productUpdate import ProductUpdate
from bson.objectid import ObjectId
from utils.json_encode import encode
from fastapi import Form, HTTPException, UploadFile, File
import math
from spec.data.product import products as mock_product

collection = db.product


@app.get("/product/", tags=["product"])
def get_products(page: int = 1, size: int = 10, category: str = None, only_available: bool = False):
    page = page - 1
    if page < 0:
        raise HTTPException(status_code=400, detail="invalid page")
    if size < 0:
        raise HTTPException(status_code=400, detail="invalid size")
    query = {}
    if category != None:
        query["category"] = category
    if only_available:
        query["stock"] = {"$gt": 0}
    cursor = collection.aggregate([
        {"$match": query},
        {
            "$facet": {
                "products": [
                    {"$match": {}},
                    {"$sort": {"name": 1}},
                    {"$skip": page * size},
                    {"$limit": size}
                ],
                "total_item": [
                    {
                        "$group": {
                            "_id": None,
                            "count": {"$sum": 1}
                        }
                    }
                ]
            }
        }
    ])
    products_data = []
    total_item = 0
    for c in cursor:
        for product in c["products"]:
            products_data.append(Product(**product))
        for item in c["total_item"]:
            total_item = item["count"]

    total_page = math.ceil(total_item / size)
    return {"data":
            {
                "products": products_data,
                "total_item": total_item,
                "total_page": total_page
            }}


@app.get("/product/{product_id}", tags=["product"])
def get_product(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})
    if product == None:
        raise HTTPException(status_code=400, detail="product not found")
    return {"data": encode(product)}


@app.post("/product/", tags=["product"])
def create_product(product: Product):
    result = collection.insert_one(product.dict(by_alias=True))
    product = collection.find_one({"_id": ObjectId(result.inserted_id)})
    return {"data": encode(product)}


@app.put("/product/{product_id}", tags=["product"])
def update_product(product_id: str, productUpdate: ProductUpdate):
    data = productUpdate.dict()
    update = {}
    if data["name"] != None:
        update["name"] = data["name"]
    if data["price"] != None:
        update["price"] = data["price"]
    if data["category"] != None:
        update["category"] = data["category"]
    if data["stock"] != None:
        update["stock"] = data["stock"]
    collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update}
    )
    product = collection.find_one({"_id": ObjectId(product_id)})
    if product == None:
        raise HTTPException(status_code=400, detail="product not found")
    return {"data": encode(product)}


@app.delete("/product/{product_id}", tags=["product"])
def delete_product(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})
    if product == None:
        raise HTTPException(status_code=400, detail="product not found")
    collection.delete_one({"_id": ObjectId(product_id)})
    return {"data": encode(product)}


@app.post("/reset-data/", tags=["product"])
def reset_data():
    collection.delete_many({})
    collection.insert_many(mock_product)
    return {"data": "done"}
