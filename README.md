##Printer-Installer Server

a basic django webserver interface for providing the printer list to the Printer-Installer.app


###Quick Start

###if you don't have virturalenv install it

	sudo easy_install virturalenv
	
###then create your virtural env
	
	cd /path/to/www/
	virtualenv printerinstaller_env


###make a user  and group
*Get the last user and group in the 400's,  if this command returns nothing than you can set the UniqueID and GroupID to 400*
*This next part is a guide, and will not work if you have a user that is 499, user your best judgment

	USER_ID=$(dscl . list /Users UniqueID | awk '{print $2}'| grep '[4][0-9][0-9]'| sort| tail -1)
	[[ -n $USER_ID ]] && ((USER_ID++)) || USER_ID=400
	
	GROUP_ID=$(dscl. list /Groups PrimaryGroupID | awk '{print $2}'| grep '[4][0-9][0-9]'| sort| tail -1)
	[[ -n $GROUP_ID ]] && ((GROUP_ID++)) || GROUP_ID=400
	
	
Set the user

	sudo dseditgroup -o create -n printerinstaller -i "$GROUP_ID" -n . printerinstaller
	sudo dscl . create /Users/printerinstaller
	sudo dscl . create /Users/printerinstaller passwd *
	sudo dscl . create /Users/printerinstaller UniqueID "$USER_ID"
	sudo dscl . create /Users/printerinstaller PrimaryGroupID "$GROUP_ID"
  
  
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

If ultimatley running via WSGI module on Apache, using the subpath /printers, when the time comes, changed this to 

	RUNNING_ON_APACHE=True

### Additional OS X setup
[Server.app Setup](https://github.com/eahrold/printerinstaller-server/blob/devel/OSX/OS X Install instructions.md)
