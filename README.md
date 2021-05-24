# SAP HANA Automatic Backup 

Consultants and Customers can use this script to setup automatic backups for the different HANA databases that they have.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for easy deployment and use for your SAP HANA project.

### Prerequisites

What things you need to start using our Backup tool

```
SAP HANA Pre-installed
Python 3 or higher
[HDBCLI](https://pypi.org/project/hdbcli/)
```

### SAP HANA Prerequisites

At this time we only support the use of hdbuserstore keys, please follow the instructions below to generate one for you SAP HANA system. 

#### Generating HDBUserStore

[SAP Instructions](https://help.sap.com/viewer/b3ee5778bc2e4a089d3299b82ec762a7/2.0.00/en-US/ddbdd66b632d4fe7b3c2e0e6e341e222.html)
```
hdbuserstore SET <KEY> <ENV> <USERNAME> <PASSWORD>
```

### Installing

To get started just clone the repository to a directory that you want that the SIDadm user has access to

```
git clone https://github.wdf.sap.corp/I504179/SAPHANABackupAutomation.git <directory name>
```

## Deployment

A couple of user inputs are required before we can go ahead and start backing up your databases.

### Configuration
In order to run the program, you will require configuration file(s) for each database that you want to use the program on. 

The configuration file only needs the HDBUserStoreKey, BackupLocation, Tenant, Partition, BackUpPrefix to successfully run. 
SMTPServer, SMTPPort, SenderEmail, SenderPassword, RecieverEmail, S3Bucket, BucketFolder, AWSAccessKey, AWSSecretAccessKey, Sidadm, and Crontab are optional based on what functionality you prefer. 

Please find an example JSON configuration file config_K01.json
```json
{
	"HDBUserStoreKey":"K01BACKUP",
	"BackupLocation":"/sapmnt/Backups",
	"Tenant":"K01",
	"Partition":"/sapmnt",
	"BackUpPrefix":"TestK01",
	"SMTPServer":"smtp.mail.com",
	"SMTPPort":"465",
	"SenderEmail":"YOUR_EMAIL@YOUR_COMPANY.com",
	"SenderPassword":"MYACTUALPASSWORD",
	"RecieverEmail":"DATABASE_ADMIN@YOUR_COMPANY.com",
	"S3Bucket":"MyS3BUCKET",
	"BucketFolder":"OLDBACKUPS",
	"AWSAccessKey":"RANDOMSTRING",
	"AWSSecretAccessKey":"ANOTERHRANDOMSTRING",
	"Sidadm":"hdbadm",
	"Crontab":"* 22 * * *"

}

```

Naming convention: config_DatabaseName.json
Place your config file in the same directory as that of your cloned repository.

You can have as many config files as you'd like, the program currently handles one config file per run. 

### Running the program on a schedule
To run it on a schedule you would need to create a cron job.
open up the cron tab
```
vim crontab -e -u <sid>adm
```

Add a line for each Database that you would like to schedule a backup for
Example entries
```
0 19 * * * cd /usr/sap/HDB/Backup_Automation && ./main.sh K01
0 19 * * * cd /usr/sap/HDB/Backup_Automation && ./main.sh SYSTEMDB
```

Another option to set the cron job would be to run the CrontabGeneration.py file. 
Before running the CrontabGeneration.py make sure you have the Sidadm and Crontab parameters filled out in the json files. 
Command to run is as follows
```
Python -E CrontabGeneration.py
```
Note: If you need to make a modification to your cron job in the future, such as an update to the time it is run, 
you can re-run the CrontabGeneration.py file after you have updated the json files with the new time to update Crontab.

### Running the program ad-hoc
To run the program whenever you would like please naviaget to the directory that you had cloned into. 
```
cd /usr/sap/HDB/Backup_Automation
```

Run the program
```
Python -E main.py <Database Name>
```

Note: If you have both python 2 and python 3, please use python 3 to run the program.

## Update
To update the program please check back with this Github Repository. 
to get the update to your cloned directory run 
```
git pull
```

## Customization or Suggestions
If you would like to customize the build to solve a more unique scenario, you can use the documentation to write your own main.py file using calls from the other classes. 

Or you can contact Pranav Lodha (I504179) or Darpan Patel (I866765) and in our updates we can try and add your suggestion to the Standardized program. 

## Authors

* **Pranav Lodha** - *Initial work* - [SAP People](https://people.wdf.sap.corp/profiles/I504179)
* **Darpan Patel** - *Initial work* - [SAP People](https://people.wdf.sap.corp/profiles/I866765)
* **Fabio Westphal** - *Initial work* - [SAP People](https://people.wdf.sap.corp/profiles/D070532)

## License

TBD

## Acknowledgments

* Thank You to Jayesh Kothari who had the original idea, a SAP Product Expert
* Thank You to Jonathan Kuch who worked with us to improve our understanding of SAP HANA
* Thank You to Surajit Pramanick and Van Vi for their support and help as well!
