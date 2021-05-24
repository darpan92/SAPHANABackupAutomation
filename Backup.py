from hdbcli import dbapi
import sys
import shutil
import time


class Backup:
    config = None

    def __init__(self, config_instance):
        self.config = config_instance
    '''
    Check the size of the backup
    '''
    def backup_size(self):
        # Function backupsize() returns the estimated backup size of the database specified in the database parameter
        conn = dbapi.connect(key= self.config.get_key() )
        sql = "select sum(allocated_page_size) from M_CONVERTER_STATISTICS"
        cursor = conn.cursor()
        cursor.execute(sql)
        size = [item for x in cursor for item in x]
        y = ','.join( str(a) for a in size)
        print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Backup Size:", time.strftime("%Y-%m-%d-%H:%M:%S"))
        return int(y)

    '''
    Check if disksize is large enough for backup
    '''
    def disk_size(self):
        path = self.config.get_partition()
        usage = shutil.disk_usage(path)
        print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Disk Size:", usage.free)
        return usage.free

    '''
    Check to see if any other backups are running
    '''
    def backup_check(self):

        # Function backup_check() checks to see if a backup of specified db is running
        conn = dbapi.connect(key=self.config.get_key())
        sql = "select BACKUP_ID from SYS.M_BACKUP_CATALOG where STATE_NAME = 'running';"
        cursor = conn.cursor()
        cursor.execute(sql)
        backup_ids = [item for x in cursor for item in x]
        print(time.strftime("%Y-%m-%d-%H:%M:%S"), "The following Backups were running:", backup_ids)
        return backup_ids
        
    '''
    Function backupcancel() takes the result set from backupcheck() and cancels all backups running
    The backupid and userstore key are used to cancel the backups and create a connection to the database respectively 
    A boolean True is returned if completed successfully 
    '''
    def backup_cancel(self, backup_ids):
        for ids in backup_ids:
            conn = dbapi.connect(key= self.config.get_key())
            sql ="BACKUP CANCEL " + str(ids) + ";"
            cursor = conn.cursor()
            backup = cursor.execute(sql)
        print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Backup was cancelled")
        return backup

    '''
    Function fullbackup() takes a backup of the db that is specified in the self.configuration file under the parameter database
    A boolean True is returned if completed successfully
    '''
    def full_backup(self):
        conn = dbapi.connect(key= self.config.get_key())
        sql ="BACKUP DATA USING FILE (" + "'" + str(self.config.get_backup_location()) + "'" + ", " + "\'" + self.config.get_backup_prefix() + "_" + time.strftime("%Y-%m-%d-%H:%M:%S") + "\'" + ")"
        time.sleep(3)
        cursor = conn.cursor()
        print(sql)
        backup = cursor.execute(sql)
        print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Backup was completed Successfully")
        return backup
        