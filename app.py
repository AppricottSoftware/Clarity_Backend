from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
import settings
from sqlalchemy.orm import sessionmaker
from User import mysqlUserDb

import pymysql
import json

app = Flask(__name__)

# # Simple routine to run a query on a database and print the results:
# def printAllUsers(conn) :
#     print("Running printAllUsers")
#     cur = conn.cursor()

#     cur.execute("select * from ClarityUsers")
#     for row in cur.fetchall():
#         print(row)

# # Returns true if user was successfully created
# # Return false if user was NOT successfully creatednot
# def registerUser(myConnection, userJson):
#     print("Running registerUser()")
#     # Grabs the user's credentials 
#     email = userJson["email"]
#     password = userJson["password"]
#     cur = myConnection.cursor()
#     addUser = "INSERT INTO `ClarityUsers` (`id`, `email`, `password`) VALUES (NULL, " + "\"" + email + "\"" + ", \"" + password + "\");"
#     cur.execute(addUser)
#     myConnection.commit()

@app.route('/login', methods=['POST'])
def do_admin_login():
    print("Invoking")
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = mysqlUserDb(json_dict) # Dict will be parsed in constructor 
        newUser.registrationUser()
        newUser.terminateConnection()
        return jsonify(json_dict)
    else:
        return


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
