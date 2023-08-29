from flask import Flask,request,jsonify
from pymongo import MongoClient

app=Flask(__name__)
client=MongoClient ("mongodb+srv://shanpriya:SHANpriya2023@microblog.nj5juk6.mongodb.net/")
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


if __name__ == "__main__":
    app.run(debug = True)