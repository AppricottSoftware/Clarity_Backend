from Logger import Logger as Log 
import settings
import pymysql

class Channel_Metadata: 
    def __init__(self, mid, cid):
        self.mid = mid
        self.cid = cid 
        self.logger = Log().getLogger()

    def getInstanceMidCid(self): 
        self.logger.info("Invoking getInstanceMidCid where mid:{} & cid:{}".format(str(self.mid), str(self.cid)))
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            command = "select * from channel_metadata where mid={} && cid={}".format(str(self.mid), str(self.cid))
            cursor.execute(command)
            res = cursor.fetchall()

            if res: 
                self.logger.info("Found instances... returning mid cid instances")
                dbConnection.close()
                return res
            else: 
                self.logger.warn("Could not find any instances with mid:{} & cid:{}... Adding them into the user's channel_metadata".format(str(self.mid), str(self.cid)))
                command = "insert into channel_metadata (mid, cid, score) values ({},{},{});".format(self.mid, self.cid, 5)
                cursor.execute(command)
                dbConnection.commit()

                command = "select * from channel_metadata where mid={} && cid={}".format(str(self.mid), str(self.cid))
                cursor.execute(command)
                res = cursor.fetchall()

                dbConnection.close()
                return res
                
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None

    def upVoteScore(self, element): 
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            command = "update channel_metadata set score={} where mid={} && cid={}".format(element[2]+1, element[0], element[1])
            cursor.execute(command)
            dbConnection.commit() # Required to commit changes to the actual database
            dbConnection.close()
            return True
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return False

    def getInstance(self): 
        self.logger.info("Invoking upVoteLikes where mid:{} & cid:{}".format(str(self.mid), str(self.cid)))
        try: 
            listOfInstances = self.getInstanceMidCid()
            return listOfInstances
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None

    def downVoteScore(self, element): 
        try: 
            dbConnection = pymysql.connect( host=settings.hostname, user=settings.username, passwd=settings.password, db=settings.database )
            cursor = dbConnection.cursor()
            command = "update channel_metadata set score={} where mid={} && cid={}".format(element[2]-1, element[0], element[1])
            cursor.execute(command)
            dbConnection.commit() # Required to commit changes to the actual database
            dbConnection.close()
            return True
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return False
