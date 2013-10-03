*please see the README.md at the root of this project for more general instructions*

#OS X Setup#

These are examples of how to configre this to function on an OS X Mountian Lion Server (it should also work for Lion)
It uses the webappctl control, but can also be used with the server app.

this project was forked with the intention of running on sub-path of /printers (eg http://your.server.com/printers)
and that is represented in the included httpd_printerinstaller.conf file with the WSGIScriptAlias line

	WSGIScriptAlias /printers /Library/Server/Web/Data/webapps/printerinstaller.wsgi


the other primary change in this fork was to allow for multiple django-wsgi apps to be run side-by side hence the renaming of /static/ directive in the settings.py file to /static_printerinstaller/.  With that set you can Alias more than one set of static files properly.

	Alias /static_printerinstaller/ /path/to/your/printerinstaller_env/printerinstaller/static/

####To install (on 10.8 )####
Edit printerinstaller.wsgi specifiying your virtualenv directory and place in 

	/Library/Server/Web/Data/webapps/

Now copy the edit the httpd_printerinstaller.conf  and place that file in

	/Library/Server/Web/Config/apache2/

and finally place com.aapps.printerinstaller.plist in 

	/Library/Server/Web/Config/apache2/webapps/


