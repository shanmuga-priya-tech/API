import os
from flask import Flask,request,jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId,json_util
import uuid

load_dotenv()

def create_app():
    app=Flask(__name__)
    client=MongoClient(os.getenv("MONGODB_URI"))
    app.db=client.api

    @app.route("/users")
    def user():
        users=list(app.db.users.find())
        return json_util.dumps(users),200

    @app.route("/users/<user_id>",methods=["GET"])
    def get_user(user_id):
        users=app.db.users.find_one({"user_id":user_id})
        if user:
            user["_id"]=str(user["_id"])
            return jsonify(user),200
        else:
            response={"message":"Incorrect userid"}
            return jsonify(response),400

    @app.route("/users/add" , methods=["POST"])
    def add_user():
            data=request.get_json()
            user=app.db.users.find_one({"$or":[{"username":data.get("username")},
                        {"user_email":data.get("user_email")}]})
            if user:
                response={"message":"User with similar data Already exit"}
                return jsonify(response),400
            else:
                user_id=str(uuid.uuid4())
                data["user_id"]=user_id
                app.db.users.insert_one(data)
                response={"message":"Added Successfully","your user_id":user_id}
                return jsonify(response),200

    return app
