from email.mime.text import MIMEText
import subprocess
import smtplib
import ssl
from Configuration import Configuration

class EmailNotification:
    def __init__(self, config):
        self.config = config
        self.status = self.check_email()
        
    def space(self):
        if self.status == False:
            print("Email information was not provided in config file, please check the config file again")
        else:
            msg = MIMEText("Server cannot take backup because disk space is low on partition" + str(self.config.get_partition()))
            msg['Subject'] = "Not Enough Space " + self.config.get_database()
            msg['From'] = self.config.get_sender_email()
            msg['To'] = self.config.get_receiver_email()
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(self.config.get_smtp_server(), self.config.get_port(), context=context)
            server.login(self.config.get_sender_email(),self.config.get_sender_password())
            server.sendmail(self.config.get_sender_email(),self.config.get_receiver_email(), msg.as_string())
        
    def success(self):
        if self.status == False:
            print("Email information was not provided in config file, please check the config file again")
        else:
            msg = MIMEText("Congrats Backup was taken Successfully:", self.config.get_database())
            msg['Subject'] = "Success " + self.config.get_database()
            msg['From'] = self.config.get_sender_email()
            msg['To'] = self.config.get_receiver_email()
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(self.config.get_smtp_server(), self.config.get_port(), context=context)
            server.login(self.config.get_sender_email(),self.config.get_sender_password())
            server.sendmail(self.config.get_sender_email(),self.config.get_receiver_email(), msg.as_string())
            
    def fail(self):
        if self.status == False:
            print("Email information was not provided in config file, please check the config file again")
        else:
            msg = MIMEText("Backup was not successfully please review logs: ", self.config.get_database())
            msg['Subject'] = "Fail"
            msg['From'] = self.config.get_sender_email()
            msg['To'] = self.config.get_receiver_email()
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(self.config.get_smtp_server(), self.config.get_port(), context=context)
            server.login(self.config.get_sender_email(),self.config.get_sender_password())
            server.sendmail(self.config.get_sender_email(),self.config.get_receiver_email(), msg.as_string())
        
    def check_email(self):
        status = True
        if (self.config.get_sender_email() == False or not self.config.get_sender_email()):
            print("Please confirm that Sender Email was provided")
            status = False
        if (self.config.get_receiver_email() == False or not self.config.get_receiver_email()):
            print("Please confirm that Receiver Email was provided")
            status = False
        if (self.config.get_sender_password() == False or not self.config.get_sender_password()):
            print("Please confirm that Sender Email Password was provided")
            status = False
        if (self.config.get_smtp_server() == False or not self.config.get_smtp_server()):
            print("Please confirm that SMTP server was provided")
            status = False
        if (self.config.get_port() == False or self.config.get_port() == ""):
            print("Please confirm that SMTP port was provided")
            status = False
            
        return status