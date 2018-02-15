from Logger import Logger as Log 
import settings
import pymysql

class Metadata: 
    def __init__(self, cid):
        """The constructor"""
        self.cid = str(cid)
        self.logger = Log().getLogger()

    def getChannelMetadataMid(self): 
        self.logger.info("\nFinding Channel Metadata, UserID: " + str(self.cid) + " in database")
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            checkUser = "SELECT mid FROM channel_metadata where cid=\"" + str(self.cid) + "\";"
            cursor.execute(checkUser)
            result = cursor.fetchall()
            
            if result : 
                self.logger.info("Found user... Returning User")
                return result[0][0]
            else : 
                self.logger.warn("Could not find metadata: ", self.cid)
                return 0
        except Warning as warn:
            self.logger.error("Waring: " + str(warn) + "\nStop\n")

    def initializeChannelMetadata(self):
        self.logger.info("\nInitializing User's Channel's Metadata Instance, cid: " + str(self.cid))
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            command = "INSERT INTO `channel_metadata` (`cid`) VALUES (\"" + str(self.cid) + "\");"
            cursor.execute(command)
            dbConnection.commit() # Required to commit changes to the actual database
            dbConnection.close()
            self.logger.info("Successful connection termination")
            return self.getChannelMetadataMid() # Grabbing the user's Uid 
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None

