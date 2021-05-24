import time
import logging
import traceback
import sys
from Backup import *

class Logging:
    logger = None
    bckp_util = None
    
    #Create variable to use for logging to file
    def __init__(self, config):
        TIME_FORMAT = "%b%d-%Y"
        LOG_FORMAT = "%(asctime)s - %(funcName)s.%(lineno)d - %(message)s"
        timestr = time.strftime(TIME_FORMAT, time.localtime(time.time()))
        log_file = timestr + '.log'
        logging.basicConfig(filename = log_file, level = logging.DEBUG, format=LOG_FORMAT, filemode='a') #append mode
        self.logger = logging.getLogger()
        #check if log file initialized by considering handler already attached or not

        self.bckp_util = Backup(config)
        self.log_start(config, timestr, LOG_FORMAT)

        sys.excepthook = self.exception_log_handler

    def log (self):
        return self.logger

    #Logging a header with some specs
    def log_start(self,config, timestr, LOG_FORMAT):
        self.logger.handlers[0].setFormatter(logging.Formatter("%(message)s"))
        self.logger.info('\n----------------------L-O-G-----------------------\n'+ timestr)
        self.logger.info('\nStart of Backup ' + timestr)
        self.logger.info("\nKey: " + config.get_key()
        +                "\nDatabase: " + config.get_database()
        +                "\nBackup Size: " + str(float(self.bckp_util.backup_size())/(1024**3)) + " GB"
        +                "\nPort: " + str(config.get_port())
        +                "\nLocation: " + config.get_backup_location()
        +                "\nPrefix: " + config.get_backup_prefix()
        +                "\nPartition: " + config.get_partition()
        +                "\nSMTP: " + str(config.get_smtp_server())
        +"\n-------------------------------------------------------\n")
        self.logger.handlers[0].setFormatter(logging.Formatter(LOG_FORMAT))

    def log_end(self):
        LOG_FORMAT = self.logger.handlers[0].formatter._fmt
        self.logger.handlers[0].setFormatter(logging.Formatter("%(message)s"))
        self.logger.info('\nEnd of Backup ' + time.strftime("%Y-%m-%d-%H:%M:%S"))
        self.logger.info("\n--------------------------------------------------")
        self.logger.info("--------------------------------------------------\n\n")
        self.logger.handlers[0].setFormatter(logging.Formatter(LOG_FORMAT))

    def exception_log_handler(self, etype, value, tb):
        self.logger.error("Uncaught {0}: {1}\n{2}".format(str(type(etype)), str(value), traceback.print_tb(tb)))