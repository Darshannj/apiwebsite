from flask import Flask, jsonify, request
from flask_cors import CORS
from database_students import get_database
app = Flask(__name__)
CORS(app)

@app.route("/" ,                methods = ["GET"])
@app.route("/showallmessages" , methods = ["GET"])
def showallmessages():
    allmessages = None
    db = get_database()
    message_cursor = db.execute("select * from message")
    allmessages = message_cursor.fetchall()

    final_result = []

    for eachmessage in allmessages:
        message_dict = {}
        message_dict["id"]          =     eachmessage["id"]
        message_dict["first_name"]  =     eachmessage["first_name"]
        message_dict["last_name"]   =     eachmessage["last_name"]
        message_dict["email"]       =     eachmessage["email"]
        message_dict["comments"]    =     eachmessage["comments"]
        final_result.append(message_dict) 
    return jsonify({"data" : final_result})


@app.route("/onemessage/<int:id>" , methods = ["GET"])
def onemessage(id):
    onemessage = None
    db = get_database()
    onemessage_cursor = db.execute("select * from message where id = ?", [id])
    onemessage =onemessage_cursor.fetchone()

    return jsonify({"One Messages Fetched -" : 
                    { "id"              : onemessage["id"] ,
                      "first_name"      : onemessage["first_name"], 
                      "last_name"       : onemessage["last_name"], 
                      "email"           : onemessage["email"],
                    "Comments"          : onemessage["comments"]  }
                    })


@app.route("/deletemessage/<int:id>" , methods = ["DELETE"])
def odeletemessage(id):
    db = get_database()
    db.execute("delete from message where id = ?" , [id])
    db.commit()
    return jsonify({"Message- " : "Message successfully deleted"})


@app.route("/insertmessage" , methods = ["POST"])
def insertmessage():
    new_message_data  = request.get_json()
    first_name        = new_message_data["first_name"]
    last_name         = new_message_data["last_name"]
    email             = new_message_data["email"]
    comments          = new_message_data["comments"]

    db = get_database()
    db.execute("insert into message (first_name, last_name,  email, comments) values (?,?, ?,?)",[first_name, last_name,  email, comments])
    db.commit()
    return jsonify({"Message - " : "Message successfully inserted."})


@app.route("/updatemessage/<int:id>" , methods = ["PUT"])
def updatemessage(id):
    new_message_data  = request.get_json()
    first_name        = new_message_data["first_name"]
    last_name         = new_message_data["last_name"]
    email             = new_message_data["email"]
    comments          = new_message_data["comments"]

    db = get_database()
    db.execute("update message set first_name = ? , last_name = ?, email =? , comments = ? where id = ?", [first_name, last_name, email, comments, id])
    db.commit()

    return jsonify({"Message - " : "Message successfully updated."})

if __name__ == "__main__":
    app.run(debug = True)