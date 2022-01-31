import main
from pymongo import MongoClient
from fastapi.testclient import TestClient


def override_get_db():
    return MongoClient("mongodb://admin:admin@localhost:27017/challenge_test?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false")


testdb = override_get_db()
main.db = testdb.challenge_test
client = TestClient(main.app)


def clear_db():
    main.db.product.delete_many({})
    main.db.money.delete_many({})


def test_buy_product_1():
    client.post("/product/init")
    client.post("/money/init")
    response = client.get("/product")
    assert response.status_code == 200
    product_id = response.json()["data"]["products"][0]["_id"]

    response = client.post("/payment", json={
        "product_id": product_id,
        "used_money" : {
            "500": 1
        },
        "accept_changes": True
    })
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["expected_changes"] == 186
    assert data["available_changes"] == 186
    assert data["used_changes"]["100"] == 1
    assert data["used_changes"]["50"] == 1
    assert data["used_changes"]["20"] == 1
    assert data["used_changes"]["10"] == 1
    assert data["used_changes"]["5"] == 1
    assert data["used_changes"]["1"] == 1
    clear_db()

def test_buy_product_2():
    client.post("/product/init")
    client.post("/money/init")
    response = client.get("/product")
    assert response.status_code == 200
    product_id = response.json()["data"]["products"][0]["_id"]

    response = client.post("/payment", json={
        "product_id": product_id,
        "used_money" : {
            "100": 3,
            "20": 1,
        },
        "accept_changes": True
    })
    data = response.json()["data"]
    assert response.status_code == 200
    assert data["expected_changes"] == 6
    assert data["available_changes"] == 6
    assert data["used_changes"]["5"] == 1
    assert data["used_changes"]["1"] == 1
    clear_db()

def test_buy_product_3():
    client.post("/product/init")
    client.post("/money/init")
    response = client.get("/product")
    assert response.status_code == 200
    product_id = response.json()["data"]["products"][0]["_id"]

    response = client.post("/payment", json={
        "product_id": product_id,
        "used_money" : {
            "100": 1,
            "20": 1,
        },
        "accept_changes": True
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "money not enough"
    clear_db()

def test_buy_product_4():
    client.post("/product/init")
    client.post("/money/init")
    response = client.post("/payment", json={
        "used_money" : {
            "100": 1,
            "20": 1,
        },
        "accept_changes": True
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "missing product_id"
    clear_db()

def test_buy_product_5():
    client.post("/product/init")
    client.post("/money/init")
    response = client.get("/product")
    assert response.status_code == 200
    product_id = response.json()["data"]["products"][0]["_id"]

    response = client.post("/payment", json={
        "product_id": product_id,
        "accept_changes": True
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "missing used_money"
    clear_db()

def test_buy_product_6():
    client.post("/product/init")
    client.post("/money/init")

    response = client.post("/payment", json={
        "product_id": "61f78a18fe6b142312699999",
        "used_money" : {
            "100": 1,
            "20": 1,
        },
        "accept_changes": True
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "product not found"
    clear_db()

def test_buy_product_7():
    client.post("/product/init")
    client.post("/money/init")
    response = client.get("/product")
    assert response.status_code == 200
    product_id = response.json()["data"]["products"][0]["_id"]

    response = client.post("/payment", json={
        "product_id": product_id,
        "used_money" : {
            "122": 1,
            "20": 1,
        },
        "accept_changes": True
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "invalid money amount"
    clear_db()