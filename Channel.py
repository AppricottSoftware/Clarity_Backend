from Logger import Logger as Log 
import settings
import pymysql

class Channel: 
    def __init__(self, channelJson):
        """The constructor"""
        self.token = str(channelJson["uid"])
        self.title = channelJson["title"] 
        self.genres = channelJson["metadata"]
        self.image = channelJson["image"] 
        self.logger = Log().getLogger()

    def getChannelCid(self): 
        self.logger.info("\nFinding Channel Uid, UserID: " + self.token + " in database")
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            checkUser = "SELECT cid FROM channel where uid=\"" + self.token + "\";"
            cursor.execute(checkUser)
            result = cursor.fetchall()
            
            if result : 
                self.logger.info("Found channel... Returning channel ID")
                return result[0][0]
            else : 
                self.logger.warn("Could not find channel for uid: " + self.token)
                return 0
        except Warning as warn:
            self.logger.error("Warning: " + str(warn) + "\nStop\n")


    def initializeUserChannel(self):
        self.logger.info("\nInitializing User's Channel Instance, uid: " + self.token)
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            if (self.image is not None):
                query = ("INSERT INTO `channel` (`uid`, `title`, `image`) "
                         "VALUES (\"{}\", \"{}\", \"{}\");"
                        ).format(self.token, self.title, self.image)
            else:
                query = ("INSERT INTO `channel` (`uid`, `title`) "
                         "VALUES (\"{}\", \"{}\");"
                        ).format(self.token, self.title)
            cursor.execute(query)
            dbConnection.commit()

            cid = self.getChannelCid()
            # print(self.genres)
            for i in self.genres: 
                curr_mid = i["mid"]
                command = "insert into channel_metadata (mid, cid, score) values ({},{},{});".format(curr_mid, cid, 5)
                cursor.execute(command)
                dbConnection.commit()
            dbConnection.close()
            
            self.logger.info("Successful connection termination")
            return cid # Grabbing the channel id 
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None

def getChannelsByToken(token):
    # Should return a dictionary that represents all channels assocated with the given token
    try:
        dbConnection = pymysql.connect(host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database)
        with dbConnection.cursor(pymysql.cursors.DictCursor) as cursor:
            queryChannels = ("SELECT * FROM `channel` WHERE `uid` = \"{}\"").format(str(token))
            cursor.execute(queryChannels)
            channels = cursor.fetchall()
            for channel in channels:
                queryChannelMetadata = ("SELECT M.genre, M.mid, C.score "
                                        "FROM channel_metadata C, metadata M "
                                        "WHERE C.cid = \"{}\" AND C.mid = M.mid").format(str(channel["cid"]))
                cursor.execute(queryChannelMetadata)
                channel["metadata"] = cursor.fetchall()
        return channels
    except Warning as warn:
        return None

def deleteChannelByToken(tokenUid, tokenCid):
    # Should delete a channel
    try:
        dbConnection = pymysql.connect(host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database)
        with dbConnection.cursor(pymysql.cursors.DictCursor) as cursor:
            queryChannels = ("DELETE FROM `channel` WHERE `cid` = \"{}\"").format(str(tokenCid))
            cursor.execute(queryChannels)            
            return getChannelByToken(tokenCid)
    except Warning as warn:
        return None