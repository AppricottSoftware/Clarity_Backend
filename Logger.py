import logging 

class Logger: 
    def __init__(self):     
        logger = logging.getLogger(__name__)
        hdlr = logging.FileHandler('/var/tmp/clarity.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.WARNING)
        self.logger = logger

    def getLogger(self): 
        return self.logger