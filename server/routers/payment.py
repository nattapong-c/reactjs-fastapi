import main
from bson.objectid import ObjectId
from fastapi import HTTPException, Request
import json
from pymongo import DESCENDING, UpdateOne


@main.app.post("/payment", tags=["payment"])
async def buy_product(req: Request):
    body = await req.body()
    body = json.loads(body)

    if "product_id" not in body:
        raise HTTPException(status_code=400, detail={
                            "error": "missing product_id"})
    if "used_money" not in body:
        raise HTTPException(status_code=400, detail={
                            "error": "missing used_money"})

    product_id = ObjectId(body["product_id"])
    product = main.db.product.find_one({"_id": product_id})
    if product == None:
        raise HTTPException(status_code=400, detail={
                            "error": "product not found"})
    if product["stock"] <= 0:
        raise HTTPException(status_code=400, detail={
                            "error": "product out of stock"})

    used_money = body["used_money"]
    money_amount = []
    for amount in used_money:
        money_amount.append(int(amount))

    money_list = main.db.money.find({"amount": {"$in": money_amount}})
    money_list_count = main.db.money.count_documents({"amount": {"$in": money_amount}})
    if len(money_amount) != money_list_count:
        raise HTTPException(status_code=400, detail={
                            "error": "invalid money amount"})

    paid_amount = 0
    for info in money_list:
        count = used_money[str(info["amount"])]
        paid_amount += (info["amount"] * count)

    if paid_amount < product["price"]:
        raise HTTPException(status_code=400, detail={
                            "error": "money not enough"})

    changes = paid_amount - product["price"]
    expected_changes = paid_amount - product["price"]
    available_changes = 0
    used_changes = {}
    bulk_update_money = []
    money_available = main.db.money.find().sort(
        "amount", direction=DESCENDING)

    for info in money_available:
        amount_req = int(info["amount"])
        amount = info["amount"]
        stock = info["stock"]
        if str(amount) in used_money:
            stock += used_money[str(amount)]

        while changes >= amount and stock > 0:
            if amount in used_changes:
                used_changes[amount] += 1
            else:
                used_changes[amount] = 1
            changes -= amount
            available_changes += amount
            stock -= 1
        bulk_update_money.append(
            UpdateOne(
                {"amount": amount_req},
                {"$set": {"stock": stock}}
            )
        )
    if changes == 0:
        main.db.product.update_one(
            {"_id": product_id},
            {"$inc": {"stock": -1}}
        )
        main.db.money.bulk_write(bulk_update_money)
    else:
        if expected_changes > available_changes and "accept_changes" in body:
            if body["accept_changes"]:
                main.db.product.update_one(
                    {"_id": product_id},
                    {"$inc": {"stock": -1}}
                )
                main.db.money.bulk_write(bulk_update_money)
            else:
                raise HTTPException(status_code=400, detail={
                                    "error": "change not enough", "can_accept": True, "expected_changes": expected_changes, "available_changes": available_changes})
        else:
            raise HTTPException(status_code=400, detail={
                                "error": "change not enough", "can_accept": True, "expected_changes": expected_changes, "available_changes": available_changes})

    return {
        "data": {
            "expected_changes": expected_changes,
            "available_changes": available_changes,
            "used_changes": used_changes
        }
    }
