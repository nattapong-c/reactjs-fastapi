import main
from pymongo import MongoClient
from fastapi.testclient import TestClient

def override_get_db():
    return MongoClient("mongodb://admin:admin@localhost:27017/challenge_test?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false")

testdb = override_get_db()
main.db = testdb.challenge_test
client = TestClient(main.app)


def clear_product_db():
    main.db.product.delete_many({})


def test_get_products():
    client.post("/product/init")
    response = client.get("/product")
    assert response.status_code == 200
    assert response.json()["data"]["products"][0]["name"] == "item-1"
    clear_product_db()
