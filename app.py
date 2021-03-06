from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os
import settings
from User import User, getUserEmail, updateEmail, updatePassword, getUserPodcastLength, updatePodcastLength, getPlaybackSpeed, updatePlaybackSpeed, deleteAccount, getCurrentChannel, updateCurrentChannel, getUserSortByDate, updateSortByDate
from Channel import Channel, getChannelsByToken, deleteChannelByToken, getChannelByCid
from Channel_Metadata import Channel_Metadata
from Metadata import Metadata
from Logger import Logger as Log

import cgitb
cgitb.enable()

import pymysql
import json

app = Flask(__name__)

logger = Log().getLogger()

@app.route('/')
def do_admin_root():
    logger.info("HELLO WORLD IP: {}".format(request.remote_addr))

# ------------ Registration & Login ------------
@app.route('/register', methods=['POST'])
def do_admin_register():
    logger.info("\n\nInvoking admin registration IP: {} ".format(request.remote_addr))
    if request.method == "POST":
        # registration to user table
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = User(json_dict)  # Dict will be parsed in constructor

        # Checking for duplicated users
        if newUser.checkDuplicateUsers() is False: 
            return jsonify({u'uid': -1}), 401

        # Registering the user to the db
        newUid = newUser.registrationUser()
        return jsonify({u'uid': newUid}), 201
    else:
        return jsonify({u'uid': -1}), 400 

@app.route('/login', methods=['POST'])
def do_admin_login():
    logger.info("\n\nInvoking admin login IP: {} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        newUser = User(json_dict)  # Dict will be parsed in constructor
        uid = newUser.getUserUid()
        if newUser.validateUser() is True: 
            return jsonify({u'uid': uid}), 201
        else: 
            return jsonify({u'uid': -1}), 401
    else: 
        return jsonify({u'uid': -1}), 400

# ------------ Registration & Login END ------------

# ------------ Getter & Setters for User Info ------------
@app.route('/GET/UserEmail', methods=['GET']) 
def do_admin_GetEmail(): 
    logger.info("\n\nInvoking do_admin_GetEmail IP: {} ".format(request.remote_addr))
    if request.method == "GET":
        json_dict = request.get_json()  # Creates into a dictionary
        uid = json_dict["uid"]
        email = getUserEmail(uid)
        if email is not None: 
            return jsonify({u'email': email}), 200
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400

@app.route('/PUT/emailUpdate', methods=['POST']) 
def do_admin_updateEmail(): 
    logger.info("\n\nInvoking updateEmail IP: {} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary

        if updateEmail(json_dict['uid'], json_dict['newEmail']) is True: 
            return jsonify({u'res': "SUCCESS"}), 200
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400

@app.route('/PUT/passwordUpdate', methods=['POST']) 
def do_admin_updatePassword(): 
    logger.info("\n\nInvoking updatePassword IP: {} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary

        if updatePassword(json_dict['uid'], json_dict['newPassword']) is True:
            return jsonify({u'res': "SUCCESS"}), 200
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400

@app.route('/PUT/deleteAccount', methods=['POST']) 
def do_admin_deleteAccount(): 
    logger.info("\n\nInvoking do_admin_deleteAccount IP: {} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary

        if deleteAccount(json_dict['uid']) is True:
            return jsonify({u'res': "SUCCESS"}), 200
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400
        
# ------------ Getter & Setters for User Info END ------------


# ------------ Getter & Setters for Channels Info ------------
@app.route('/GET/channels', methods=['GET', 'POST'])
def do_admin_GETChannels():
    logger.info("\n\nInvoking admin /GET/channels, IP: {} ".format(request.remote_addr))
    if request.method == "GET":
       userData = request.get_json()
       uid = userData["uid"]
       channels = getChannelsByToken(uid)
       if channels is not None:
           return jsonify(channels), 200
       else:
           return jsonify({u'cid': -1}), 500
    else:
        return jsonify({u'cid': -1}), 400

@app.route('/PUT/channels', methods=['POST'])
def do_admin_PUTChannels():
    logger.info("\n\nInvoking admin /PUT/channels, IP: {} ".format(request.remote_addr))
    if request.method == "POST":
        channelData = request.get_json()
        newChannel = Channel(channelData)
        newCid = newChannel.initializeUserChannel()

        return jsonify({u'cid': newCid}), 201
    else:
        return jsonify({u'cid': -1}), 400

@app.route('/PUT/channels/Delete', methods=['POST'])
def DeleteChannels():
    logger.info("\n\nInvoking /PUT/channels/Delete, IP: {} ".format(request.remote_addr))
    if request.method == "POST":
       userData = request.get_json()
       channels = deleteChannelByToken(userData["uid"], userData["cid"])
       if channels is not None:
           return jsonify(channels), 200
       else:
           return jsonify({u'cid': -1}), 500
    else:
        return jsonify({u'cid': -1}), 400

@app.route('/PUT/channels/Likes', methods=['POST'])
def do_admin_PUTChannelsLikes():
    logger.info("\n\nInvoking admin /PUT/channel/Likes, IP:{} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        
        cid = json_dict["cid"] # Grabbing the cid of the channel
        # For each metadata, update the score according to the cid and the respective mid
        for i in json_dict["metadata"]: 
            mid = i["mid"]
            listOfInstances = Channel_Metadata(mid, cid).getInstance()
            
            if listOfInstances is 0: 
                return jsonify({u"result": "FAILURE"}), 409

            res = Channel_Metadata(mid, cid).upVoteScore(listOfInstances[0]) # Up votes the score
            if res is False: # Sanity Check --- Should not happen 
                return jsonify({u"result": "FAILURE"}), 409

        return jsonify({u"result": "SUCCESS"}), 200
    else: 
        return jsonify({u"result": "FAILURE"}), 400

@app.route('/PUT/channels/Dislikes', methods=['POST'])
def do_admin_PUTChannelsDislikes():
    logger.info("\n\nInvoking admin /PUT/channel/Dislikes, IP:{} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        
        cid = json_dict["cid"] # Grabbing the cid of the channel
        # For each metadata, update the score according to the cid and the respective mid
        for i in json_dict["metadata"]: 
            mid = i["mid"]
            listOfInstances = Channel_Metadata(mid, cid).getInstance()

            if listOfInstances is 0: 
                return jsonify({u"result": "FAILURE"}), 409

            res = Channel_Metadata(mid, cid).downVoteScore(listOfInstances[0]) # Down votes the score
            if res is False: # Sanity Check --- Should not happen 
                return jsonify({u"result": "FAILURE"}), 409

        return jsonify({u"result": "SUCCESS"}), 200
    else: 
        return jsonify({u"result": "FAILURE"}), 400

# ------------ Getter & Setters for Channels Info END ------------


#  ------------ Getter & Setters for Podcast ------------
@app.route('/GET/sortByDate', methods=['GET'])
def do_admin_GETsortByDate():
    logger.info("\n\nInvoking admin /GET/sortByDate, IP:{} ".format(request.remote_addr))
    if request.method == "GET":
        json_dict = request.get_json()  # Creates into a dictionary
        res = getUserSortByDate(json_dict["uid"])
        if res is not None: 
            return jsonify({u'sortByDate': res}), 200
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400

@app.route('/PUT/sortByDate', methods=['POST'])
def do_admin_PUTsortByDate():
    logger.info("\n\nInvoking admin /POST/sortByDate, IP:{} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        logger.info(str(json_dict))
        if updateSortByDate(json_dict["uid"], json_dict["sortByDate"]) is True:
            return jsonify({u"result": "SUCCESS"}), 200
        else: 
            return jsonify({u"result": "FAILURE"}), 200
    else: 
        return jsonify({u"result": "FAILURE"}), 400

@app.route('/GET/podcastLength', methods=['GET'])
def do_admin_GETpodcastLength():
    logger.info("\n\nInvoking admin /GET/podcastLength, IP:{} ".format(request.remote_addr))
    if request.method == "GET":
        json_dict = request.get_json()  # Creates into a dictionary
        res = getUserPodcastLength(json_dict["uid"])
        if res is not None: 
            return jsonify({u'podcastLength': res}), 200
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400

@app.route('/PUT/podcastLength', methods=['POST'])
def do_admin_PUTpodcastLength():
    logger.info("\n\nInvoking admin /GET/podcastLength, IP:{} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        if updatePodcastLength(json_dict["uid"], json_dict["podcastLength"]) is True:
            return jsonify({u"result": "SUCCESS"}), 200
        else: 
            return jsonify({u"result": "FAILURE"}), 200
    else: 
        return jsonify({u"result": "FAILURE"}), 400

@app.route('/GET/playbackSpeed', methods=['GET'])
def do_admin_GETplaybackSpeed():
    logger.info("\n\nInvoking admin /GET/playbackSpeed, IP:{} ".format(request.remote_addr))
    if request.method == "GET":
        json_dict = request.get_json()  # Creates into a dictionary
        res = getPlaybackSpeed(json_dict["uid"])
        if res is not None: 
            return jsonify({u'playbackSpeed': res}), 200
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400

@app.route('/PUT/playbackSpeed', methods=['POST'])
def do_admin_PUTplaybackSpeed():
    logger.info("\n\nInvoking admin /PUT/playbackSpeed, IP:{} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        if updatePlaybackSpeed(json_dict["uid"], json_dict["playbackSpeed"]) is True:
            return jsonify({u"result": "SUCCESS"}), 200
        else: 
            return jsonify({u"result": "FAILURE"}), 200
    else: 
        return jsonify({u"result": "FAILURE"}), 400

@app.route('/GET/currentChannel', methods=['GET'])
def do_admin_GETcurrentChannel():
    logger.info("\n\nInvoking admin /GET/currentChannel, IP:{} ".format(request.remote_addr))
    if request.method == "GET":
        json_dict = request.get_json()  # Creates into a dictionary
        cid = getCurrentChannel(json_dict["uid"])
        if cid is not None: 
            res = getChannelByCid(cid)
            if res is not None:
                return jsonify({u'currentChannel': res}), 200
            else:
                return jsonify({u'res': -1}), 401
        else: 
            return jsonify({u'res': -1}), 401
    else: 
        return jsonify({u'res': -1}), 400

@app.route('/PUT/currentChannel', methods=['POST'])
def do_admin_PUTcurrentChannel():
    logger.info("\n\nInvoking admin /PUT/currentChannel, IP:{} ".format(request.remote_addr))
    if request.method == "POST":
        json_dict = request.get_json()  # Creates into a dictionary
        if updateCurrentChannel(json_dict["uid"], json_dict["currentChannel"]) is True:
            return jsonify({u"result": "SUCCESS"}), 200
        else: 
            return jsonify({u"result": "FAILURE"}), 200
    else: 
        return jsonify({u"result": "FAILURE"}), 400

#  ------------ Getter & Setters for Podcast END------------


if __name__ == "__main__":
    print("SERVER ON!!!\n\n")
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
