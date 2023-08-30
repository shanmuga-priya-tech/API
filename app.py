import os
from flask import Flask,request,jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv()

def create_app():
    app=Flask(__name__)
    client=MongoClient(os.getenv("MONGODB_URI"))
    app.db=client.api

    @app.route("/users")
    def user():
        user = [{"user_id":entry.get("user_id"), 
                "user_name":entry.get("username"), 
                "user_email":entry.get("user_email"),
                "user_password":entry.get("user_password"),
                "user_role":entry.get("user_role")}for entry in app.db.users.find({})]
        users=json.dumps(user,default=str)#convert objectid to str
        return users

    @app.route("/users/<user_id>",methods=["GET"])
    def get_user(user_id):
        users=app.db.users.find_one({"user_id":user_id})
        person=json.dumps(users,default=str)#convert objectid to str
        return person

    @app.route("/users/add" , methods=["POST"])
    def add_user():
        if request.method == "POST":
            data=request.get_json()
            user_id=data.get("user_id")
            username = data.get("username")
            user_email = data.get("userEmail")
            user_password = data.get("userPassword")
            user_role = data.get("userRole")

            user_document = {
                "user_id": user_id,
                "username": username,
                "user_email": user_email,
                "user_password": user_password,
                "user_role": user_role
            }
            user=app.db.users.find_one({"user_id":user_id,
                                        "username":username,
                                        "user_email":user_email,
                                        "user_password":user_password})
            if user:
                response={"message":"User with similar data Already exit"}
                return jsonify(response),400
            else:
                app.db.users.insert_one(user_document)
                response={"message":"Added Successfully"}
                return jsonify(response),200

    return app
