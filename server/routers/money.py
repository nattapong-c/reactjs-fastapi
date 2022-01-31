import main
from schema.money import Money
from schema.moneyUpdate import MoneyUpdate
from bson.objectid import ObjectId
from utils.json_encode import encode
from fastapi import HTTPException
from spec.data.money import money as money_data


@main.app.get("/money/", tags=["money"])
def get_money_list():
    money_list = main.db.money.find().sort("amount")
    money_list_data = []
    for money in money_list:
        money_list_data.append(Money(**money))

    return {"data": money_list_data}


@main.app.get("/money/{money_id}", tags=["money"])
def get_money(money_id: str):
    money = main.db.money.find_one({"_id": ObjectId(money_id)})
    if money == None:
        raise HTTPException(status_code=400, detail="money not found")
    return {"data": encode(money)}


@main.app.post("/money/", tags=["money"])
def create_money(money: Money):
    result = main.db.money.insert_one(money.dict(by_alias=True))
    money = main.db.money.find_one({"_id": ObjectId(result.inserted_id)})
    return {"data": encode(money)}


@main.app.put("/money/{money_id}", tags=["money"])
def update_money(money_id: str, moneyUpdate: MoneyUpdate):
    data = moneyUpdate.dict()
    update = {}
    if data["amount"] != None:
        update["amount"] = data["amount"]
    if data["stock"] != None:
        update["stock"] = data["stock"]
    main.db.money.update_one(
        {"_id": ObjectId(money_id)},
        {"$set": update}
    )
    money = main.db.money.find_one({"_id": ObjectId(money_id)})
    if money == None:
        raise HTTPException(status_code=400, detail="money not found")
    return {"data": encode(money)}


@main.app.delete("/money/{money_id}", tags=["money"])
def delete_money(money_id: str):
    money = main.db.money.find_one({"_id": ObjectId(money_id)})
    if money == None:
        raise HTTPException(status_code=400, detail="money not found")
    main.db.money.delete_one({"_id": ObjectId(money_id)})
    return {"data": encode(money)}

@main.app.post("/money/init", tags=["money"])
def init_money():
    main.db.money.delete_many({})
    main.db.money.insert_many(money_data)
    return {"data": "done"}