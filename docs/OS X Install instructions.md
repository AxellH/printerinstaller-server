*please see the README.md at the root of this project for more general instructions.  The app must be setup prior to these configuration steps*

#OS X Setup#

These are examples of how to get this up and running on an OS X Mountian Lion Server and beyond (it should also work for Lion).

You will need to create three files: 

###1) httpd_printerinstaller.conf
this file should go here: __/Library/Server/Web/Config/apache2/httpd_printerinstaller.conf__

```
# This is the Config file to accompany the os X server webapp 
# edu.loyno.smc.printerinstaller.webapp.plist, 

# if running along side of other webapps and on the same port prefix /printers 
# to subpath all of the Aliases/ScriptAliases/Locations
# if running on a single port you can change them to just /
WSGIScriptAlias /printers /Library/Server/Web/Data/webapps/printerinstaller.wsgi
Alias /printers/static/ /usr/local/www/printerinstaller_env/printerinstaller/printerinstaller/static/
Alias /printers/files/ /Library/Server/Web/Data/Sites/printerinstaller_env/printerinstaller/printerinstaller/files/

<Location /printers/files/private/>
    Order Allow,Deny
    Deny from  all
</Location>

# Uncomment the section below to isolate the virtual environment, However you must only run on a single
# port if you choose to do this, you can't run on both http and https

# WSGIDaemonProcess printerinstaller user=printerinstaller group=printerinstaller
# <Location /printers>
#     WSGIProcessGroup printerinstaller
#     WSGIApplicationGroup %{GLOBAL}
#     Order deny,allow
#     Allow from all
# </Location>

```

###2) com.github.django.printerinstaller.webapp.plist
This file should go here: __/Library/Server/Web/Config/apache2/webapps/com.github.django.printerinstaller.webapp.plist__
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>displayName</key>
	<string>Printer-Installer Server</string>
	<key>includeFiles</key>
	<array>
		<string>/Library/Server/Web/Config/apache2/httpd_printerinstaller.conf</string>
	</array>
	<key>installationIndicatorFilePath</key>
	<string>/Library/Server/Web/Data/webapps/printerinstaller.wsgi</string>
	<key>launchKeys</key>
	<array/>
	<key>name</key>
	<string>com.github.django.printerinstaller.webapp</string>
	<key>requiredModuleNames</key>
	<array>
		<string>wsgi_module</string>
	</array>
</dict>
</plist>

```
###3) printerinstaller.wsgi
Set the "VIR\_ENV\_DIR" to your virtual environment path  
Then, Place this file at: __/Library/Server/Web/Data/WebApps/printerinstaller.wsgi__
```
import os, sys
import site

#set the next line to your printerinstaller environment
VIR_ENV_DIR = '/usr/local/www/printerinstaller_env'

# Use site to load the site-packages directory of our virtualenv
site.addsitedir(os.path.join(VIR_ENV_DIR, 'lib/python2.7/site-packages'))

# Make sure we have the virtualenv and the Django app itself added to our path
sys.path.append(VIR_ENV_DIR)
sys.path.append(os.path.join(VIR_ENV_DIR, 'printerinstaller'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "printerinstaller.settings")
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
```

### After all of the files are installed...

1. open the Server.app  
2. go to Websites   
3. Open the website you wish to enable it on  
4. in the advanced tab check "PrinterInstaller-Server"




