##Printer-Installer Server

a basic django webserver interface for providing the printer list to the Printer-Installer.app


###Quick Start

#####if you don't have virturalenv install it

	$ sudo easy_install virturalenv
	
#####then create your virtural env
	
	$ cd /path/to/www/
	$ virtualenv printerinstaller_env

#####make a user

	sudo dscl . create /Users/printerinstaller home /var/empty
	sudo dscl . create /Users/printerinstaller passwd *
	
	sudo chown -R printerinstaller printerinstaller_env
	sudo su
	
	su printerinstaller
	  
#####turn on the virtual env
	
	$ cd printerinstaller_env
    $ source bin/activate
	
#####insatll printerinstaller_server
	
	$ git clone https://github.com/eahrold/printerinstaller-server.git
	
#####install prerequistis

	$ pip install django
	$ pip install django-bootstrap_toolkit
	
	$ cd printerinstaller-server
	$ cp cp printerinstaller/example_settings.py cp printerinstaller/settings.py
	
	$ python manage.py collectstatic
	$ python manage.py syncdb
	
	$python manage.py runserver
	
