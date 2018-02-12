from Logger import Logger as Log 
import settings
import pymysql

class Channel: 
    """ 
        \authors: Patrick Le, Guthrie Price
        \brief: Class to manage Clarity's Channels objects
    """

    def __init__(self, uid, genres, title, image=None):
        """The constructor"""
        self.uid = str(uid)
        self.title = title 
        self.genres = genres
        self.logger = Log().getLogger()

    def getChannelCid(self): 
        self.logger.info("\nFinding Channel Uid, UserID: " + str(self.uid) + " in database")
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            checkUser = "SELECT cid FROM channel where uid=\"" + str(self.uid) + "\";"
            cursor.execute(checkUser)
            result = cursor.fetchall()
            
            if result : 
                self.logger.info("Found channel... Returning channel ID")
                return result[0][0]
            else : 
                self.logger.warn("Could not find user " + self.email)
                return 0
        except Warning as warn:
            self.logger.error("Warning: " + str(warn) + "\nStop\n")


    def initializeUserChannel(self):
        self.logger.info("\nInitializing User's Channel Instance, uid: " + str(self.uid))
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            if (self.image is not None):
                query = ("INSERT INTO `channel` (`uid`, `title`, `image`) "
                         "VALUES (\"{}\"), (\"{}\"), (\"{}\");"
                        ).format(self.uid, self.title, self.image)
            else:
                query = ("INSERT INTO `channel` (`uid`, `title`) "
                         "VALUES (\"{}\"), (\"{}\");"
                        ).format(self.uid, self.title)
            cursor.execute(query)
            cid = self.getChannelCid()
            query = ("INSERT INTO `channel_metadata` (`mid`, `cid`) "
                       "VALUES (\"{}\", \"{}\")"
                      ).format(metadata[0], cid)
            for metadata in self.metadata[1:]:
                query += ",(\"{}\", \"{}\")".format(metadata, cid)
            query += ";"
            cursor.execute(query)
            dbConnection.commit() # Required to commit changes to the actual database
            dbConnection.close()
            self.logger.info("Successful connection termination")
            return cid # Grabbing the channel id 
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None
