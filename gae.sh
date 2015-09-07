#!/bin/bash

# App source code
maindir="/media/sf_pp-tickets"
# Location of App Engine SDK
gae_dir="/opt/google_appengine"
# Datastore directory
datastore="/home/ubuntu/pp-tickets_db"

# On which IP should server listen on
net_interface="eth1"
myip=`ifconfig | grep $net_interface -A 1 | tail -n 1 | awk '{print($2)}' | awk -F':' '{print($2)}'`

# This is needed for import of production IP
# myip="0.0.0.0"

cd $maindir

txtbld=$(tput bold)
bldred=${txtbld}$(tput setaf 1)
txtrst=$(tput sgr0)


current_branch=`git branch | grep '*' | awk '{print($2)}'`

testing=0

if [ "$#" -eq "1" ] && [ "$1" ==  "test" ]
then
	testing=1
fi

if [ "$#" -eq "1" ] && [ "$1" ==  "upload" ]
then
        upload=1
fi

if [ "$upload" == 1 ]
then
        echo "Uploading"
        export FLASK_CONF=TEST

	cd src
	python apptest.py $gae_dir 2>&1 | tee /tmp/test_out

	isok=`cat /tmp/test_out | grep 'FAILED' | wc -l`

	if [ $isok -eq 0 ]
	then
		echo "Tests are OK"

		cd ..

		echo
		echo "Branch : $bldred $current_branch $txtrst"

		app_version=`cat src/app.yaml | head -n 5 | egrep '^version'| awk '{print($2)}'`
		echo "App version : $app_version"

		version_in_gae=`appcfg.py list_versions src/ 2>&1 | grep "$app_version" | wc -l`

		if [ $version_in_gae -eq 1 ]
		then
			echo "Version $app_version is already in GAE"
			exit 1
		fi

		echo -n "Press [ENTER] to continue..."
		read var_name

		appcfg.py  --noauth_local_webserver update src/


	else
		echo "Tests Failed"
	fi

	exit
fi


if [ $testing -eq 1 ]
then
        echo "Testing"
        export FLASK_CONF=TEST
fi


if [ $testing -eq 1 ]
then
	cd src
	python apptest.py $gae_dir
else
	$gae_dir/dev_appserver.py --skip_sdk_update_check True --host $myip --admin_host $myip --storage_path $datastore --use_mtime_file_watcher true  src/
fi


