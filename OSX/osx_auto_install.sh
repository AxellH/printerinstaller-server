#!/bin/bash

#set -xv

PROJECT_NAME='printerinstaller'
PROJECT_SETTINGS_DIR="server"
EXAMPLE_SETTINGS_FILE="settings_example.py"

GIT_REPO="https://github.com/eahrold/printerinstaller-server.git"
USER_NAME='printerinstaller'
GROUP_NAME='printerinstaller'

OSX_WEBAPP_PLIST='/OSX/edu.loyno.smc.printerinstaller.webapp.plist'
APACHE_CONFIG_FILE='/OSX/httpd_printerinstaller.conf'
WSGI_FILE='/OSX/printerinstaller.wsgi'

VIRENV_NAME='printerinstaller_env'
PIP_REQUIREMENTS="setup/requirements.txt"
OSX_SERVER_WSGI_DIR="/Library/Server/Web/Data/WebApps/"
OSX_SERVER_APACHE_DIR="/Library/Server/Web/Config/apache2/"

pre_condition_test(){
	[[ -z $(which git) ]] && echo you must first install git. you can download it from Apple. && exit 1
}

make_user_and_group(){
	local USER_EXISTS=$(dscl . list /Users | grep -c "${USER_NAME}")
	local GROUP_EXISTS=$(dscl . list /Groups | grep -c "${GROUP_NAME}")
	
	if [ $USER_EXISTS -eq 0]; then
		USER_ID=$(check_ID Users UniqueID)
		dscl . create /Users/"${USER_NAME}"
		dscl . create /Users/"${USER_NAME}" passwd *
		dscl . create /Users/"${USER_NAME}" UniqueID "${USER_ID}"
	fi
	
	if [ $GROUP_EXISTS -eq 0 ]; then
		GROUP_ID=$(check_ID Groups PrimaryGroupID)
		dseditgroup -o create -i "${GROUP_ID}" -n . "${GROUP_NAME}"
	fi
	
	### this is outside of the conditional statement 
	### to correct any previously set GroupID
	dscl . create /Users/"${USER_NAME}" PrimaryGroupID "${GROUP_ID}"
}

check_ID(){
	# $1 is the dscl path and $2 is the Match
	local ID=$(/usr/bin/dscl . list /$1 $2 | awk '{print $2}'| grep '[4][0-9][0-9]'| sort| tail -1)
	[[ -n $ID ]] && ((ID++)) || ID=400
	
	local RC=0
	while [ $RC -eq 0 ]; do
		local IDCK=$(/usr/bin/dscl . list /$1 $2 | awk '{print $2}'| grep -c ${ID})
		if [ $IDCK -eq 0 ]; then
			read -e -p "Using ${ID} for ${2}: [(Y)es/(N)o]? " -n 1 -r
			if [[ $REPLY =~ ^[Yy]$ ]];then
			    RC=1
			fi 
		else
			cecho alert "That %2 is in use"
			read -e -p "Please specify another:" ID
		fi
	done
	echo $ID
	
}

function install(){
	local VEV=$(which virtualenv)
	[[ -z "${VEV}" ]] && easy_install virturalenv
	"${VEV}" "${VIR_ENV}"
		
	cd "${VIR_ENV}"
    bash -c "source bin/activate"

	git clone "${GIT_REPO}" ./"${PROJECT_NAME}"
	pip install -r ./"${PROJECT_NAME}/${PIP_REQUIREMENTS}"
	cd "${PROJECT_NAME}"
	
	configure
}

configure(){
	cp "${PROJECT_SETTINGS_DIR}/${EXAMPLE_SETTINGS_FILE}" "${PROJECT_SETTINGS_DIR}/settings.py"
	local SETTINGS_FILE="${PROJECT_SETTINGS_DIR}/settings.py"
	
	read -e -p "Run in DEBUG mode [Y(es)/N(o)]? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]];then
		sed -ie 's/^DEBUG =.*/DEBUG = True/' "${SETTINGS_FILE}"
	fi
	
	read -e -p "Allow All Hosts [Y(es)/N(o)]? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]];then
		sed -ie "s/^ALLOWED_HOSTS =.*/ALLOWED_HOSTS = ['*']/" "${SETTINGS_FILE}"
	fi
	
	python manage.py collectstatic
	python manage.py syncdb
	
	cread warn "Would you like to run on os x server [Y(es)/N(o)]? " yesno
	if [[ $REPLY =~ ^[Yy]$ ]];then
		sed -ie 's/^RUNNING_ON_APACHE=.*/RUNNING_ON_APACHE=True/' "${SETTINGS_FILE}"
		
	else
		cread alert "Do you Want to start the test server now [Y(es)/N(o)]?" yesno
		if [[ $REPLY =~ ^[Yy]$ ]];then
			python manage.py runserver
		fi
	fi
	
	
}

install_ox_components(){
	echo ""
}

set_permissions(){
	chown -R "${USER_NAME}":"${GROUP_NAME}" "${VIR_ENV}"
}

cecho(){	
	case "$1" in
		alert) local COLOR=$(printf "\\e[1;31m")
		;;
		warn|warning) local COLOR=$(printf "\\e[1;35m")
		;;
		attention) local COLOR=$(printf "\\e[1;32m")
		;;
		notice) local COLOR=$(printf "\\e[1;34m")
		;;
		*) local COLOR=$(printf "\\e[0;30m")
		;;
	esac
	
	if [ -z "${2}" ];then
		local MESSAGE="${1}"
	else
		local MESSAGE="${2}"
	fi

	local RESET=$(printf "\\e[0m")	
	echo "${COLOR}${MESSAGE}${RESET} ${3}"	
}

cread(){	
	case "$1" in
		alert) local COLOR=$(printf "\\e[1;31m")
		;;
		warn) local COLOR=$(printf "\\e[1;35m")
		;;
		attention) local COLOR=$(printf "\\e[1;32m")
		;;
		notice) local COLOR=$(printf "\\e[1;34m")
		;;
		*) local COLOR=$(printf "\\e[0;30m")
		;;
	esac
	
	local MESSAGE="${2}"
	local RESET=$(printf "\\e[0m")	
	if [ -z ${3} ];then
		read -e -p "${COLOR}${MESSAGE}${RESET} "
	elif [ "${3}" == "yesno" ];then
		read -e -p "${COLOR}${MESSAGE}${RESET} " -n 1 -r
	else
		read -e -p "${COLOR}${MESSAGE}${RESET} " VAR
		eval $3="'$VAR'"
	fi
}


main(){
	pre_condition_test
	
	
	
	RC=0
	cecho alert "You are about to run the $PROJECT_NAME installer"
	cecho alert "There's a few things to get out of the way"
	echo ""
	cecho warn "First we need to determine what user should run the webapp" 
	cecho notice "1) create a new user and group" "(recommended)"
	cecho notice "2) yourself" "(fine for testing)"
	cecho notice "3) the www user" "(if you've had issues running any other way)" 
	
	
	while [ $RC -eq 0 ]; do
		read -e -p "Please Choose: " -n 1 -r
		if [[ $REPLY -eq 1 ]];then
			make_user_and_group
			RC=1
		elif [[ $REPLY -eq 2 ]];then
			USER_NAME=$(who | grep console | head -1 |awk '{print $1}')
			GROUP_NAME=$(dscl . read /Users/${USER_NAME} PrimaryGroupID|awk '{print $2}')
			RC=1
			
		elif [[ $REPLY -eq 3 ]];then
			USER_NAME='www'
			GROUP_NAME='www'
			RC=1
		fi
	done
	echo using user $USER_NAME
	echo using group $GROUP_NAME
	
	cread alert "will you be running on OS X Server" yesno
	if [[ $REPLY =~ ^[Yy]$ ]];then
		VIR_ENV=$(eval echo "${VIR_ENV}/${VIRENV_NAME}")
	fi 
	
	RC=0
	while [ $RC -eq 0 ]; do
		read -e -p "Where Would you like to install the Virtual Environment:" VIR_ENV
		TDIR=$(eval echo "${VIR_ENV}")
		if [ -d  "${TDIR}" ]; then	
			cecho attention "The Path to VirtualEnv is: " "${VIR_ENV}"
			cread attention "Is this Correct [Y(es)/N(o)/C(ancel)]? " yesno
			if [[ $REPLY =~ ^[Yy]$ ]];then
				VIR_ENV=$(eval echo "${VIR_ENV}/${VIRENV_NAME}")
			    RC=1
			elif [[ $REPLY =~ ^[Cc]$ ]];then
				exit 1
			fi 
		else
			cecho alert "That's not a valad path, please try again"
		fi
	done

	install

}

main

exit 0