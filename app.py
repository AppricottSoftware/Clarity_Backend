from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
import settings
from User import User
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
        newUser = User(json_dict)  # Dict will be parsed in constructor

        # Checking for duplicated users
        if newUser.checkDuplicateUsers() is False: 
            return jsonify({u'userId': u'-1'})


        newUid = newUser.registrationUser()
        # TODO return a better dictionary with return code
        return jsonify({u'userId': u'newUid'})
    else:
        return jsonify({u'userId': u'NotPostRequest'})


@app.route('/login', methods=['POST'])
def do_admin_login():
    print("Invoking admin login IP:", request.remote_addr)
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = User(json_dict)  # Dict will be parsed in constructor

        if newUser.validateUser(): 
            return jsonify({u'auth': u'success'})
        else: 
            return jsonify({u'auth': u'failure'})


@app.route('/GET/channels', methods=['POST'])
def GETChannels():
    print("Invoking admin /GET/channels, IP:", request.remote_addr)

@app.route('/PUT/channels', methods=['POST'])
def PUTChannels():
    print("Invoking admin /PUT/channels, IP:", request.remote_addr)

@app.route('/PUT/channels/Likes', methods=['POST'])
def PUTChannelsLikes():
    print("Invoking admin /PUT/channel/Likes, IP:", request.remote_addr)

@app.route('/PUT/channels/Dislikes', methods=['POST'])
def PUTChannelsDislikes():
    print("Invoking admin /PUT/channel/Dislikes, IP:", request.remote_addr)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
