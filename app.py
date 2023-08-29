import os
from flask import Flask,request,jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app=Flask(__name__)
    client=MongoClient(os.getenv("MONGODB_URI"))
    app.db=client.api

    @app.route("/users/add" , methods=["POST"])
    def add_user():
        if request.method == "POST":
            data=request.get_json()
            username = data.get("username")
            user_email = data.get("userEmail")
            user_password = data.get("userPassword")
            user_role = data.get("userRole")

            user_document = {
                "username": username,
                "user_email": user_email,
                "user_password": user_password,
                "user_role": user_role
            }
            app.db.users.insert_one(user_document)

        response={"message":"Added Successfully"}
        return jsonify(response),200


    return app
