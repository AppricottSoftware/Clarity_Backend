from Logger import Logger as Log 
import settings
import pymysql

class Channel: 
    """ 
        \author: Patrick Le
        \brief: Class to manage Clarity's Channels objects
    """

    def __init__(self, uid):
        """The constructor"""
        self.uid = uid
        self.logger = Log().getLogger()


    def getChannelCid(self): 
        self.logger.info("\nFinding Channel Uid, UserID: " + self.uid + " in database")
        try: 
            self.dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            self.cursor = self.dbConnection.cursor()
            checkUser = "SELECT cid INTO channel where uid=\"" + self.uid + "\";"
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


    def initializeUserChannel(self): 
        self.logger.info("\nInitializing User's Channel Instance, uid: " + self.uid)
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            command = "INSERT INTO `channel` (`uid`, `name`) VALUES (\"" + self.uid + "\", \"First Channel\");"
            cursor.execute(command)
            dbConnection.commit() # Required to commit changes to the actual database
            dbConnection.close()
            self.logger.info("Successful connection termination")
            return self.getChannelCid() # Grabbing the user's Uid 
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None



