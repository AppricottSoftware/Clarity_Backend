import logging 
import os

class Logger: 
    def __init__(self):     
        self.logger = self.generate_logger()

    def getLogger(self): 
        return self.logger

    def generate_logger(self):
        FILENAME = "/var/log/clarity.log"
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