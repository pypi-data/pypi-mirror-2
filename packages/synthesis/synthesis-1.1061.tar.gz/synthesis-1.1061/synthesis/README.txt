Synthesis Project
2009-09-09

System Requirements:

	python 2.4+
	Postgresql
	psycopg2
	sqlalchemy
	zope.interface
	lxml
	pyinotify
	inotify (kernel extensions)
	cElementTree (improves performance)
	python-gnupg (http://python-gnupg.googlecode.com/files/gnupg-0.2.1.tar.gz)
	sqlalchemy-migrate 0.4.5 (http://sqlalchemy-migrate.googlecode.com/files/sqlalchemy-migrate-0.4.5.tar.gz)
	
Installation

	Install virtualenv
	virtualenv --no-site-packages Synthesis					# Create an environment for the Project (mine is Synthesis)
	easy_install "SqlAlchemy==0.4.5"					# Install the correct (required) version of SQLAlchemy
	easy_install psycopg2							# Install the Postgres driver
	easy_install zope.interface
	easy_install pyinotify
	
	Under Ubuntu you'll need:
		sudo apt-get install libxml2-dev
		sudo apt-get install libxslt1-dev
	
	easy_install lxml
	easy_install python-dateutil
	easy_install python-gnupg
	easy_install paramiko
	
Main entry point to program is:

	MainProcessor.py
	
Which will loop indefinately waiting for XML files to arrive in input folders specified in:

	conf\settings.py
	
	INPUTFILES_PATH = [
            "/home/[homedir]/synthesis/InputFiles"
            ,"/home/[homedir]/synthesis/InputFiles2"
            ,"/home/[homedir]/synthesis/InputFiles3"
            ]
	
The program issues email notifications specified in the settings file within the section:

	SMTPRECIPIENTS = \
	{
	"/home/[homedir]/synthesis/InputFiles":
		{
		'SMTPTOADDRESS': ['someEmail@yahoo.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': []
		}
	,"/home/[homedir]/synthesis/InputFiles2":
		{
		'SMTPTOADDRESS': ['admin.guy@company.com',],
		'SMTPTOADDRESSCC': ['overseer@company.com',],
		'SMTPTOADDRESSBCC': ['omsbudsman@vendor.com',]
		}
	,"/home/[homedir]/synthesis/InputFiles3":
		{
		'SMTPTOADDRESS': ['receptionist@megaorg.com',],
		'SMTPTOADDRESSCC': [],
		'SMTPTOADDRESSBCC': []
		}
	}

This section contains 1 entry for every entry where input files arrive to be processed.  Each entry
has it's own notification entries which are a dictionary of entries.

The MODE attribute determines if the system operates in TEST vs PROD.  TEST mode cleans up the database for every run processed.

	MODE = 'TEST'

Settings override mechanism:

	'local_settings.py'
	
putting this file in the main folder of the application you can override settings in the
conf\settings.py entries.  Entries must have the same name.

for example:

	# email configuration
	SMTPSERVER = 'smtp.url.com'
	SMTPPORT = 587
	SMTPSENDER = 'mysender@minicorp.com'
	SMTPSENDERPWD = 'mysecret'

will override the same named settings in conf\settings.py:

	SMTPSERVER = 'localhost'
	SMTPPORT = 25
	SMTPSENDER = 'me@localhost'