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
            dbConnection.close()

            if res: 
                self.logger.info("Found instances... returning mid cid instances")
                return res
            else: 
                self.logger.warn("Could not find any instances with mid:{} & cid:{}".format(str(self.mid), str(self.cid)))
                return 0

        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None

# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;
    def update(self, element): 
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



    def upVoteLikes(self): 
        self.logger.info("Invoking upVoteLikes where mid:{} & cid:{}".format(str(self.mid), str(self.cid)))
        try: 
            listOfInstances = self.getInstanceMidCid()
            return listOfInstances
        except Warning as warn: 
            self.logger.error("Warning: " + str(warn) + "\nStop.\n")
            return None