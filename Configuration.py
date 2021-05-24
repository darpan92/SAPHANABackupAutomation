import json
import os
import fnmatch
import logging
import time
import sys


class Configuration:
    def __init__(self, tenant):
        self.tenant = tenant
        self.key = self.set_key()
        self.backup_location = self.set_backup_location()
        self.database = self.set_database()
        self.partition = self.set_partition()
        self.backup_prefix = self.set_backup_prefix()
        self.smtp = self.set_smtp_server()
        self.port = self.set_port()
        self.sender_email = self.set_sender_email()
        self.sender_password = self.set_sender_password()
        self.receiver_email = self.set_receiver_email()
        self.access_key = self.set_access_key()
        self.secret_access_key = self.set_secret_access_key()
        self.s3_bucket = self.set_s3_bucket()
        self.bucket_folder = self.set_bucket_folder()
        self.sidadm_user =  self.set_sidadm_user()
        self.crontab = self.set_crontab()

    def load_parameters(self, item):
        for filename in os.listdir('.'):
            if fnmatch.fnmatch(filename, '*' + self.tenant + '.json'):
                config_file = filename
        with open(config_file) as file:
            data = json.load(file)
        value = data[item]
        return value
    
    def set_key(self):
        try:
            self.key = self.load_parameters('HDBUserStoreKey')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting Key Valye")
            return self.key
        except:
            return sys.exit("Please Check config for key")
        
    def get_key(self):
        return self.key
        
    def set_backup_location(self):
        try:
            self.backup_location = self.load_parameters('BackupLocation')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting Backup Location")
            return self.backup_location
        except:
            return sys.exit("Please Check config for backup location")
        
    def get_backup_location(self):
        return self.backup_location
        
    def set_database(self):
        try:
            self.database = self.load_parameters('Tenant')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting Value of Database to backup")
            return self.database
        except:
            return sys.exit("Please Check config for tenant")
    
    def get_database(self):
        return self.database
        
    def set_partition(self):
        try:
            self.partition = self.load_parameters('Partition')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting Location of Backup Drive (check space)")
            return self.partition
        except:
            return sys.exit("Please Check config for partition")
        
    def get_partition(self):
        return self.partition
        
    def set_smtp_server(self):
        try:
            self.smtp = self.load_parameters('SMTPServer')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting SMTP Server value")
            return self.smtp
        except:
            return False
        
    def get_smtp_server(self):
        return self.smtp
        
    def set_port(self):
        try:
            self.port = self.load_parameters('SMTPPort')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting port value")
            return self.port
        except:
            return False
        
    def get_port(self):
        return self.port
        
    def set_sender_email(self):
        try:
            self.sender_email = self.load_parameters('SenderEmail')
            return self.sender_email
        except:
            return False
    
    def get_sender_email(self):
        return self.sender_email
        
    def set_sender_password(self):
        try:
            self.sender_password = self.load_parameters('SenderPassword')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting Email Address to be used for email notifications")
            return self.sender_password
        except:
            return False
        
    def get_sender_password(self):
        return self.sender_password
        
    def set_receiver_email(self):
        try:
            self.reciever_email = self.load_parameters('RecieverEmail')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting email for person to recieve email notifications")
            return self.reciever_email
        except:
            return False
        
    def get_receiver_email(self):
        return self.reciever_email
        
    def set_backup_prefix(self):
        try:
            self.backup_prefix = self.load_parameters('BackUpPrefix')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting prefix for backup name")
            return self.backup_prefix
        except:
            return sys.exit("Please Check config for backup prefix")
        
    def get_backup_prefix(self):
        return self.backup_prefix
        
    def set_access_key(self):
        try:
            self.access_key = self.load_parameters('AWSAccessKey')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting AWS Access Key")
            return self.access_key
        except:
            return False

    def get_access_key(self):
        return self.access_key

    def set_secret_access_key(self):
        try:
            self.secret_access_key = self.load_parameters('AWSSecretAccessKey')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting AWS Secret Access Key")
            return self.secret_access_key
        except:
            return False

    def get_secret_access_key(self):
        return self.secret_access_key

    def set_s3_bucket(self):
        try:
            self.s3_bucket = self.load_parameters('S3Bucket')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting S3 Bucket Name")
            return self.s3_bucket
        except:
            return False

    def get_s3_bucket(self):
        return self.s3_bucket

    def set_bucket_folder(self):
        try:
            self.bucket_folder = self.load_parameters('BucketFolder')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting S3 Bucket Folder")
            return self.bucket_folder
        except:
            return False

    def get_bucket_folder(self):
        return self.bucket_folder

    def set_sidadm_user(self):
        try:
            self.sidadm_user = self.load_parameters('Sidadm')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting Sidadm User")
            return self.sidadm_user
        except:
            return False

    def get_sidadm_user(self):
        return self.sidadm_user

    def set_crontab(self):
        try:
            self.crontab = self.load_parameters('Crontab')
            print(time.strftime("%Y-%m-%d-%H:%M:%S"), "Setting Crontab")
            return self.crontab
        except:
            return False

    def get_crontab(self):
        return self.crontab