from Logger import Logger as Log 
import settings
import pymysql

class PublicApi: 
    def __init__(self, lid):
        """The constructor"""
        self.lid = str(lid)
        self.logger = Log().getLogger()

    def isValidApiKey(self): 
        self.logger.info("\nChecking if Api Key:{}".format(self.lid))
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            checkUser = "SELECT ApiCounts FROM apikeys where lid=\"" + self.lid + "\";"
            cursor.execute(checkUser)
            result = cursor.fetchall()
            
            if result : 
                if result[0][0] > 0: 
                    return True
                else: 
                    return False
            else :
                self.logger.error("Could not find apiKey's count for lid: " + self.lid)
                return -1
        except Warning as warn:
            self.logger.error("Warning: " + str(warn) + "\nStop\n")
            return -1

    def getApiKey(self): 
        self.logger.info("\nGetting API Key for lid:{}".format(self.lid))
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            checkUser = "SELECT ApiKey FROM apikeys where lid=\"" + self.lid + "\";"
            cursor.execute(checkUser)
            result = cursor.fetchall()
            
            if result : 
                return result[0][0] > 0: 
            else :
                self.logger.error("Could not find apiKey's count for lid: " + self.lid)
                return -1
        except Warning as warn:
            self.logger.error("Warning: " + str(warn) + "\nStop\n")
            return -1

    def getApiCount(self): 
        self.logger.info("\nGetting API Key Count for lid:{}".format(self.lid))
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            checkUser = "SELECT ApiCounts FROM apikeys where lid=\"" + self.lid + "\";"
            cursor.execute(checkUser)
            result = cursor.fetchall()
            
            if result : 
                return result[0][0]: 
            else :
                self.logger.error("Could not find apiKey's count for lid: " + self.lid)
                return -1
        except Warning as warn:
            self.logger.error("Warning: " + str(warn) + "\nStop\n")
            return -1

    def callApiKey(self): 
        self.logger.info("\Calling API Key with lid:{} for searching...".format(self.lid))
        try: 
            res = getApiKey()

            if res < 0: 
                return -1

            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            command = "update apikeys set ApiKey={} where lid={}".format(res-1, self.lid)
            cursor.execute(command)
            result = cursor.fetchall()
            
            if result : 
                return True: 
            else :
                self.logger.error("Could not find apiKey's count for lid: " + self.lid)
                return False
        except Warning as warn:
            self.logger.error("Warning: " + str(warn) + "\nStop\n")
            return False

        

