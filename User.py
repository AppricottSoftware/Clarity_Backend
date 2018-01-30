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
        self.username = userJson["username"]
        self.firstname = userJson["firstname"]
        self.lastname = userJson["lastname"]
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
        except pymysql.Error as error:
            self.logger.error("Error:" + str(error) + "\nStop.\n)")

    def registrationUser(self): 
        """\brief: adds or updates the db with the user"""
        self.logger.info("\nUpdating Database")
        try: 
            # Checks if the user exists, if so then the username is
            # TODO return a usernameTakenJson
            
            self.cursor = self.dbConnection.cursor()
            self.cursor.execute("SELECT EXISTS(SELECT 1 FROM 'ClarityUsers' WHERE username = 'username')")
            addUser = "INSERT INTO `ClarityUsers` (`id`, `username`, `email`, `password`, `firstname`, `lastname`) VALUES (NULL, " + "\"" + self.username + "\", \"" + self.email + "\", \"" + self.password +  "\", \"" + self.firstname +  "\", \"" + self.lastname + "\");"
            self.cursor.execute(addUser)
            self.dbConnection.commit() # Required to commit changes to the actual database
            self.logger.info("Successful registration user: " + self.username)
            return True 
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")

    def terminateConnection(self): 
        self.dbConnection.close()

