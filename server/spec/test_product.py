# from main import app
# from database.mongo import connectDB
# from fastapi.testclient import TestClient
# from bson import ObjectId


# client = TestClient(app)
# connection = connectDB()
# db = connection.challenge_test
# collection = db.product


# app.dependency_overrides["db"] = db


# def test_get_product():
#     id = ObjectId()
#     collection.insert_one({"_id": id, "name": "test1", "price": 30, "category": "food", "stock": 5})
#     response = client.get("/product/"+str(id))
#     print(str(id))
#     assert response.status_code == 200
#     # assert response.json() == {"data":{"_id": id, "name": "test1", "price": 30, "category": "food", "stock": 5}}


# connection.drop_database("challenge_test")
# connection.close()
