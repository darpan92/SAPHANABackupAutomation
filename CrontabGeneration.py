from crontab import CronTab 
from Configuration import *
import os
import fnmatch
import json


def get_config_files():
	files = []
	for filename in os.listdir('.'):
		if fnmatch.fnmatch(filename, '*' + 'config_*' + '.json'):
			config_file = filename
			with open(config_file) as file:
				data = json.load(file)
			value = data['Tenant']
			files.append(value)
	return files

def set_crontab(config,dirpath):
	cron = CronTab(user=config.get_sidadm_user())
	job = cron.new(command="cd " + dirpath + " && ./main.sh " + config.get_database(), comment='')
	job.setall(str(config.get_crontab()))
	cron.write()
	remove_comment(config)

def check_crontab(config,dirpath):
	check = True
	cron = CronTab(user=config.get_sidadm_user())
	cronjob = str(config.get_crontab() + " cd " + dirpath + " && ./main.sh " + config.get_database())
	for job in cron:
		if fnmatch.fnmatch(str(job), cronjob):
			check = False
		elif fnmatch.fnmatch(str(job), "*" + config.get_database()):
			print(job)
			cron.remove(job)
			cron.write_to_user(user=config.get_sidadm_user())
			remove_comment(config)
	return check

def remove_comment(config):
	with open("/var/spool/cron/tabs/" + config.get_sidadm_user(), "r+") as file:
		d = file.readlines()
		file.seek(0)
		for line in d:
			if not line.startswith('#'):
				file.write(line)
		file.truncate()

def main():
	dirpath = os.getcwd()
	for tenant in get_config_files():
		config = Configuration(tenant)
		if check_crontab(config,dirpath) == False:
			print("Crontab for " + config.get_database() + " and this time already exists!")
		else:
			set_crontab(config,dirpath)

if __name__ == "__main__":
	main()
