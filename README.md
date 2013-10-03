##Printer-Installer Server

a basic django webserver interface for providing the printer list to the Printer-Installer.app


###Quick Start

###if you don't have virturalenv install it

	sudo easy_install virturalenv
	
###then create your virtural env
	
	cd /path/to/www/
	virtualenv printerinstaller_env


###make a user  
*(make sure the UniqueID is not in use!)*

	sudo dscl . create /Users/printerinstaller
	sudo dscl . create /Users/printerinstaller passwd *
	sudo dscl . create /Users/printerinstaller UniqueID 410
	dscl . create /Users/administrator PrimaryGroupID 20
  
  
###fix permissions then switch to new user	
	sudo chown -R printerinstaller printerinstaller_env
	sudo su ; su printerinstaller
	  
###turn on the virtual env	
	cd printerinstaller_env
    source bin/activate
	
###insatll printerinstaller_server
	
	git clone https://github.com/eahrold/printerinstaller-server.git printerinstaller
	
###install prerequistis

	pip install django
	pip install django-bootstrap_toolkit
	
### configure the app settings

	cd printerinstaller
	cp server/example_settings.py cp server/settings.py
	
	python manage.py collectstatic
	python manage.py syncdb
	
	python manage.py runserver

During initial testing, in the settings.py file you'll want to set
	
	RUNNING_ON_APACHE=False

If ultimatley installing on os x server 10.7 or above this will be changed to 

	RUNNING_ON_APACHE=True

