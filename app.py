from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
import settings
from sqlalchemy.orm import sessionmaker
from User import mysqlUserDb

import pymysql
import json

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def do_admin_register():
    print("Invoking admin registration")
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = mysqlUserDb(json_dict) # Dict will be parsed in constructor 
        newUser.registrationUser()
        return jsonify(json_dict) #TODO return a better dictionary with return code
    else:
        return

@app.route('/login', methods=['POST'])
def do_admin_login(): 
    print("Invoking admin login")
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = mysqlUserDb(json_dict) # Dict will be parsed in constructor 
        newUser.validateUser()
        return jsonify(json_dict) #TODO return a better dictionary with return code
    else:
        return

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
