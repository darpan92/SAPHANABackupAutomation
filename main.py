from Configuration import *
from Backup import *
from S3 import *
import time
import logging
from Logging import *
import sys
from EmailNotification import *

config = None
bckp_util = None
logger = None
s3 = None

'''
Main function which will run the program
Capture all the variables properly here
Later on will become its own file
'''
def main():
    # Backup Status
    status = False
    
    # Load config file for database that we need to preform backup on
    tenant = sys.argv[1]
    
    # Load the variables
    config = Configuration(tenant)
    bckp_util = Backup(config)
    logger = Logging(config)
    s3 = S3(config)
    email = EmailNotification(config)
        
    print("Log file Created!")
    
    # Check Disk Size
    logger.log().debug("Checking Disk Size")
    disk_space = bckp_util.disk_size()
    
    # Check Backup Size
    logger.log().debug("Checking Backup Size")
    backup_space = bckp_util.backup_size()
    
    # Check if other backups are running
    logger.log().debug("Checking if other backups are running")
    backup_ids = bckp_util.backup_check()
    
    # Brain
    if (backup_space > disk_space):
        email.space()
        sys.exit("Not enough space for backup, you have been notified via email!")
    elif(len(backup_ids) > 0):
        bckp_util.backup_cancel(backup_ids)
        logger.log().debug("Backup for " + str(config.get_database()) + " has been cancelled!")
        status = bckp_util.full_backup()
    else:
        status = bckp_util.full_backup()
    
    if status == True:
        logger.log().debug("Backup of " + config.get_database() + " has completed!")
        print("Backup of " + config.get_database() + " has completed!")
        backup = s3.backup_to_move()
        s3.move_to_s3(backup)
    else:
        email.fail()
        print("Check logs. The backup was not successful!")
    
    logger.log().debug("Backup of " + config.get_database() + " has status " + str(status))
    
    # End Logging file
    logger.log_end()


if __name__ == "__main__":
    main()