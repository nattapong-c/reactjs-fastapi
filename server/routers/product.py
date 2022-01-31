from typing import Optional
from main import app, db
from schema.product import Product
from schema.productResponse import ProductResponse
from bson.objectid import ObjectId
from utils.json_encode import encode
from fastapi import File, Form, HTTPException, UploadFile
import math
# from spec.data.product import products as mock_product
import gridfs
import base64

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
    fs = gridfs.GridFS(db, "product_image")
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
            image = fs.get(product["image"]).read()
            image_base64 = base64.b64encode(image)
            products_data.append(ProductResponse(
                id=product["_id"], name=product["name"], category=product["category"], stock=product["stock"], price=product["price"], image=image_base64))
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
    fs = gridfs.GridFS(db, "product_image")
    id = ""
    try:
        id = ObjectId(product_id)
    except:
        raise HTTPException(status_code=400, detail="product not found")
    product = collection.find_one({"_id": id})
    if product == None:
        raise HTTPException(status_code=400, detail="product not found")
    image = fs.get(product["image"]).read()
    image_base64 = base64.b64encode(image)
    product = encode(product)
    product["image"] = image_base64
    return {"data": product}


@app.post("/product/create", tags=["product"])
async def create_product(file: UploadFile, name: str = Form(...), price: int = Form(...), category: str = Form(...), stock: int = Form(...)):
    image_allow = ["image/png", "image/jpeg"]
    if file.content_type not in image_allow:
        raise HTTPException(
            status_code=400, detail="file not allow. must be .png or .jpeg")
    fs = gridfs.GridFS(db, "product_image")
    content = await file.read()
    image_id = fs.put(content)
    product = Product(name=name, price=price,
                      category=category, stock=stock, image=image_id)

    result = collection.insert_one(product.dict(by_alias=True))
    product = collection.find_one({"_id": ObjectId(result.inserted_id)})
    return {"data": encode(product)}


@app.put("/product/{product_id}", tags=["product"])
async def update_product(product_id: str, file: Optional[UploadFile] = File(None), name: Optional[str] = Form(None), price: Optional[int] = Form(None), category: Optional[str] = Form(None), stock: Optional[int] = Form(None)):
    update = {}
    if name != None:
        update["name"] = name
    if price != None:
        update["price"] = price
    if category != None:
        update["category"] = category
    if stock != None:
        update["stock"] = stock
    if file != None:
        image_allow = ["image/png", "image/jpeg"]
        if file.content_type not in image_allow:
            raise HTTPException(
                status_code=400, detail="file not allow. must be .png or .jpeg")
        fs = gridfs.GridFS(db, "product_image")
        content = await file.read()
        image_id = fs.put(content)
        update["image"] = image_id

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


# @app.post("/reset-data/", tags=["product"])
# def reset_data():
#     collection.delete_many({})
#     collection.insert_many(mock_product)
#     return {"data": "done"}
