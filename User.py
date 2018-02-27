import json
import settings
import pymysql
from Logger import Logger as Log

class User: 
    def __init__(self, userJson): 
        """The constructor"""
        self.email = userJson["email"]
        self.password = userJson["password"]
        self.logger = Log().getLogger()

    def getUserUid(self):
        self.logger.info("\nFinding User Uid, " + self.email + " in database")
        try: 
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            checkUser = "SELECT uid FROM users WHERE email=\"" + self.email + "\";"
            self.cursor.execute(checkUser)
            result = self.cursor.fetchall()
            if result : 
                self.logger.info("Found user... Returning User")
                return result[0][0]
            else : 
                self.logger.warn("Could not find user " + self.email)
                return 0
        except Warning as warn:
            self.logger.error("Waring: " + str(warn) + "\nStop\n")

    def checkDuplicateUsers(self): 
        self.logger.info("\nSearching for dup emails: " + self.email)
        try: 
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            checkUser = "SELECT EXISTS(SELECT 1 FROM users WHERE email = \"" + self.email + "\");"
            self.cursor.execute(checkUser)
            result = self.cursor.fetchall()[0][0]
            if result is 1: 
                self.logger.warn("Invalid registration... User already exists")
                return False
            else : 
                self.logger.info("User does not exists, Executing Registration code" + self.email)
                return True
        except Warning as warn:
            self.logger.error("Waring: " + str(warn) + "\nStop\n")
            return False

    def registrationUser(self): 
        """\brief: adds or updates the db with the user"""
        self.logger.info("\nUpdating Database")
        try: 
            # Checks if the user exists, if so then the username is
            # TODO return a usernameTakenJson
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            command = "INSERT INTO `users` (`email`, `password`) VALUES (\"" + self.email + "\", \"" + self.password +  "\");"
            self.cursor.execute(command)
            self.dbConnection.commit() # Required to commit changes to the actual database
            self.logger.info("Successful registration user: " + self.email)
            self.dbConnection.close()
            self.logger.info("Successful connection termination")
            return self.getUserUid() # Grabbing the user's Uid 
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None

    def getUserPassword(self) :
        self.logger.info("Running getUserPassword()")
        checkUser = "Select password from users where email=\"" + self.email + "\";"
        self.cursor.execute(checkUser)
        result = self.cursor.fetchall()
        if result : 
            self.logger.info("Found user... Returning User")
            return result[0][0]
        else : 
            self.logger.warn("Could not find user " + self.email)
            return 0

    def validateUser(self): 
        self.logger.info("\nValidating User")
        try: 
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            userRealPassword = self.getUserPassword()
            if self.password == userRealPassword: 
                self.logger.info("Authenication Successful")
                return True
            else: 
                self.logger.info("Authenication Failure") 
                return False
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return False

    def getUserPodcastSpeed(self): 
        self.logger.info("\nRunning getUserPodcastSpeed()")
        checkUser = "Select podcastLength from users where email=\"" + self.email + "\";"
        self.cursor.execute(checkUser)
        result = self.cursor.fetchall()
        if result : 
            self.logger.info("Found Podcast Speed... Returning")
            return result[0][0]
        else : 
            self.logger.warn("Could not find email " + self.email)
            return 0

def updateEmail(uid, newEmail): 
    logger = Log().getLogger()
    logger.info("\nUpdating User's Email Address")
    try: 
        dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
        cursor = dbConnection.cursor()
        query = "update users set email=\"{}\" where uid=\"{}\"".format(newEmail, uid);
        cursor.execute(query)
        dbConnection.commit() # Required to commit changes to the actual database
        logger.info("Successful update to user's uid: " + str(uid) + " to email: " + str(newEmail))
        dbConnection.close()
        logger.info("Successful connection termination")
        return True
    except Warning as warn: 
        logger.error("Warning: " + str(warn) + "\nStop.\n")
        return False

def getUserEmail(uid): 
    logger = Log().getLogger()
    logger.info("\nFinding User Email with: {}".format(str(uid)))
    try: 
        dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
        cursor = dbConnection.cursor()
        checkUser = "SELECT email FROM users WHERE uid=\"" + str(uid) + "\";"
        cursor.execute(checkUser)
        result = cursor.fetchall()
        if result : 
            logger.info("Found user... Returning User")
            return result[0][0]
        else : 
            logger.warn("Could not find user with uid: " + str(uid))
            return None
    except Warning as warn:
        logger.error("Waring: " + str(warn) + "\nStop\n")
        return None

def updatePassword(uid, newPassword): 
    logger = Log().getLogger()
    logger.info("\nUpdating User's Password")
    try: 
        dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
        cursor = dbConnection.cursor()
        query = "update users set password=\"{}\" where uid=\"{}\"".format(newPassword, uid)
        cursor.execute(query)
        dbConnection.commit() # Required to commit changes to the actual database
        logger.info("Successful update to user " + str(uid) + "'s password " + str(newPassword))
        dbConnection.close()
        logger.info("Successful connection termination")
        return True
    except Warning as warn: 
        self.logger.error("Warning: " + str(warn) + "\nStop.\n")
        return False