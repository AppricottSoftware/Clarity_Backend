from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
import settings
from User import mysqlUserDb
from Channel import Channel
from Metadata import Metadata

import cgitb
cgitb.enable()

import pymysql
import json

app = Flask(__name__)


@app.route('/')
def do_admin_root():
    print("HELLO WORLD IP:", request.remote_addr)


@app.route('/register', methods=['POST'])
def do_admin_register():
    print("Invoking admin registration IP:", request.remote_addr)
    if request.method == "POST":

        # registration to user table
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = mysqlUserDb(json_dict)  # Dict will be parsed in constructor
        newUid = newUser.registrationUser()

        # setting up channel tables
        if newUid is None: 
            return jsonify({u'register': u'failure'})
        newChannel = Channel(newUid)
        newCid = newChannel.initializeUserChannel()

        # setting up metadata tables
        if newCid is None: 
            return jsonify({u'register': u'failure'})
        newMetadata = Metadata(newCid)
        res = newMetadata.initializeUserMetadata()

        print("Success: ", res)

        # TODO return a better dictionary with return code
        return jsonify(json_dict)
    else:
        return jsonify({u'register': u'failure'})


@app.route('/login', methods=['POST'])
def do_admin_login():
    print("Invoking admin login IP:", request.remote_addr)
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = mysqlUserDb(json_dict)  # Dict will be parsed in constructor

        if newUser.validateUser(): 
            return jsonify({u'auth': u'success'})
        else: 
            return jsonify({u'auth': u'failure'})


@app.route('/GET/channels', methods=['POST'])
def GETChannels():
    print("Invoking admin GET Channels, IP:", request.remote_addr)






@app.route('/PUT/channels', methods=['POST'])
def PUTChannels():
    print("Invoking admin PUT Channels, IP:", request.remote_addr)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
