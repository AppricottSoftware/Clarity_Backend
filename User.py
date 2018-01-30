import os
import json
import settings
import pymysql
from Logger import Logger as Log

class mysqlUserDb: 

    # Constructor to initialize all params 
    def __init__(self, username, email, password): 
        self.username = username
        self.email = email
        self.password = password
        self.logger = Log().getLogger()

        try: 
            self.logger.info("\nChecking MySQL connections...") 
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            self.cursor.execute('select version()')
            self.logger.info("Connection OK, proceeding.")
        except pymysql.Error as error:
            self.logger.error("Error: %s" + error + "\nStop.\n)")

    def updatedb(self, db): 













