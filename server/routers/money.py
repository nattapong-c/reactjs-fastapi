from main import app, db
from schema.money import Money
from schema.moneyUpdate import MoneyUpdate
from bson.objectid import ObjectId
from utils.json_encode import encode
from fastapi import HTTPException
from spec.data.money import money as money_data

collection = db.money
@app.get("/money/", tags=["money"])
def get_money_list():
    money_list = collection.find().sort("amount")
    money_list_data = []
    for money in money_list:
        money_list_data.append(Money(**money))

    return {"data": money_list_data}


@app.get("/money/{money_id}", tags=["money"])
def get_money(money_id: str):
    money = collection.find_one({"_id": ObjectId(money_id)})
    if money == None:
        raise HTTPException(status_code=400, detail="money not found")
    return {"data": encode(money)}


@app.post("/money/", tags=["money"])
def create_money(money: Money):
    result = collection.insert_one(money.dict(by_alias=True))
    money = collection.find_one({"_id": ObjectId(result.inserted_id)})
    return {"data": encode(money)}


@app.put("/money/{money_id}", tags=["money"])
def update_money(money_id: str, moneyUpdate: MoneyUpdate):
    data = moneyUpdate.dict()
    update = {}
    if data["amount"] != None:
        update["amount"] = data["amount"]
    if data["stock"] != None:
        update["stock"] = data["stock"]
    collection.update_one(
        {"_id": ObjectId(money_id)},
        {"$set": update}
    )
    money = collection.find_one({"_id": ObjectId(money_id)})
    if money == None:
        raise HTTPException(status_code=400, detail="money not found")
    return {"data": encode(money)}


@app.delete("/money/{money_id}", tags=["money"])
def delete_money(money_id: str):
    money = collection.find_one({"_id": ObjectId(money_id)})
    if money == None:
        raise HTTPException(status_code=400, detail="money not found")
    collection.delete_one({"_id": ObjectId(money_id)})
    return {"data": encode(money)}

@app.post("/money/init", tags=["money"])
def init_money():
    collection.insert_many(money_data)
    return {"data": "done"}