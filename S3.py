import boto3
import os
import fnmatch

class S3:

    def __init__(self, config):
        self.config = config
        self.status = self.check_aws_s3()
        

    def backup_to_move(self):
        if self.status == False:
            print("Please confirm that AWS information was provided")
        else:
            database = self.config.get_database()
            files = []
            for filename in os.listdir(self.config.get_backup_location()):
                if fnmatch.fnmatch(filename.casefold(),'*' + database.casefold() + '*.bak'):
                    files.append(str(self.config.get_backup_location()) + "/" + str(filename))
            latest_backup = max(files, key=os.path.getctime) 
            return latest_backup

    def move_to_s3(self,backup):
        if self.status == False:
            print("Please confirm that AWS information was provided")
        else:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=self.config.get_access_key(),
                aws_secret_access_key=self.config.get_secret_access_key(),
            )
            s3.Bucket(self.config.get_s3_bucket()).upload_file(backup, self.config.get_bucket_folder() + backup.replace(self.config.get_backup_location(),''))
            print(backup.replace(self.config.get_backup_location(),'') + " backup moved to s3!")
        
        
    def check_aws_s3(self):
        status = True
        if (self.config.get_access_key() == False or not self.config.get_access_key()):
            print("Please confirm that Access Key was provided")
            status = False
        if (self.config.get_secret_access_key() == False or not self.config.get_secret_access_key()):
            print("Please confirm that AWS Secret Key was provided")
            status = False
        if (self.config.get_s3_bucket() == False or not self.config.get_s3_bucket()):
            print("Please confirm that AWS Bucket was provided")
            status = False
        if (self.config.get_bucket_folder() == False or not self.config.get_bucket_folder()):
            print("Please confirm that AWS Bucket Folder was provided")
            status = False
            
        return status