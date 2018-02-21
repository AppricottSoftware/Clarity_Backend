import logging 
import os
import datetime

class Logger: 
    def __init__(self):     
        self.logger = self.generate_logger()

    def getLogger(self): 
        return self.logger

    def generate_logger(self):
        now = datetime.datetime.now()

        if not os.path.exists("/var/log/messages"):
            os.makedirs("/var/log/messages")

        FILENAME = "/var/log/messages/clarity_log_{}_{}_{}.log".format(now.year, now.month, now.day)
        FORMAT = "%(asctime)s %(levelname)s %(message)s"
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        # Reset the logger.handlers if it already exists.
        if logger.handlers:
            logger.handlers = []
        fh = logging.FileHandler(FILENAME)
        formatter = logging.Formatter(FORMAT)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger