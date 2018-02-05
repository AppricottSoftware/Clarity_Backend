import os
import json
import settings
import pymysql
from Logger import Logger as Log

class mysqlUserDb: 
    """
        \author: Patrick Le 
        \brief: Creates a User object w/ db function for db interactions
    """

    def __init__(self, userJson): 
        """The constructor"""
        if 'username' in userJson: 
            self.email = userJson["email"]
            self.password = userJson["password"]
            self.logger = Log().getLogger()
        else: 
            self.email = userJson["email"]
            self.password = userJson["password"]
            self.logger = Log().getLogger()
        # Testing db connection
        try: 
            self.logger.info("\nChecking MySQL connections...") 
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            self.cursor.execute('select version()')
            self.logger.info("Connection OK, proceeding.")
            self.dbConnection.close()
        except pymysql.Error as error:
            self.logger.error("Error:" + str(error) + "\nStop.\n)")

    def registrationUser(self): 
        """\brief: adds or updates the db with the user"""
        self.logger.info("\nUpdating Database")
        try: 
            # Checks if the user exists, if so then the username is
            # TODO return a usernameTakenJson
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            addUser = "INSERT INTO `users` (`email`, `password`) VALUES (\"" + self.email + "\", \"" + self.password +  "\");"
            self.cursor.execute(addUser)
            self.dbConnection.commit() # Required to commit changes to the actual database
            self.logger.info("Successful registration user: " + self.username)
            self.dbConnection.close()
            self.logger.info("Successful connection termination")
            return True 
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")

    def getUserPassword(self) :
        print("Running getUserPassword()")
        checkUser = "Select password from users where email=\"" + self.email + "\";"
        self.cursor.execute(checkUser)

        self.cursor.execute(checkUser)
        result = self.cursor.fetchall()
        if result : 
            print("Found user... Returning User")
            return result[0][0]
        else : 
            return 0

    def validateUser(self): 
        self.logger.info("\nValidating User")
        try: 
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            userRealPassword = self.getUserPassword()
            if self.password == userRealPassword: 
                print("Authenication Successful")
                return True
            else: 
                print("Authenication Failure") 
                return False
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")

