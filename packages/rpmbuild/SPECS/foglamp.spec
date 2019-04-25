%define __spec_install_pre /bin/true

Name:          foglamp
Vendor:        Dianomic Systems, Inc. <info@dianomic.com>
Version:       1.5.02
Release:       0.0.00
BuildArch:     x86_64
Summary:       FogLAMP, the open source platform for the Internet of Things
License:       Apache License
Group: 	       IOT
URL:           http://www.dianomic.com

%define install_path	/usr/local

Prefix:        /usr/local
Requires:      sudo, boost-devel, dbus-devel, glib2-devel, rsyslog, openssl-devel, postgresql-devel, wget, zlib-devel, git, cmake, libuuid-devel
AutoReqProv:   no

%description
FogLAMP, the open source platform for the Internet of Things

%pre
#!/usr/bin/env bash
##--------------------------------------------------------------------
## Copyright (c) 2018 OSIsoft, LLC
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##--------------------------------------------------------------------

##--------------------------------------------------------------------
##
## This script is used to execute pre installation tasks.
##
## Author: Ivan Zoratti, Ashwin Gopalakrishnan, Massimiliano Pinto, Stefano Simonelli
##
##--------------------------------------------------------------------

# FIXME_I
#set -e

PKG_NAME="foglamp"

is_foglamp_installed () {
    set +e
    # FIXME_I
    sudo rm -f /var/run/yum.pid
    rc=`yum list installed ${PKG_NAME} 2> /dev/null | grep -c foglamp`
    echo $rc
    set -e
}

get_foglamp_script () {
    foglamp_script=$(rpm -ql ${PKG_NAME} | grep 'foglamp/bin/foglamp$')
    echo $foglamp_script
}

is_foglamp_running () {
    set +e
    foglamp_script=$(get_foglamp_script)
    foglamp_status_output=$($foglamp_script status 2>&1 | grep 'FogLAMP Uptime')
    rc=$((!$?))
    echo $rc
    set -e
}

get_current_version_file () {
    current_version_file=$(rpm -ql ${PKG_NAME} | grep VERSION)
    echo $current_version_file
}

get_schema_version () {
    version_file=$1
    schema_version=$(grep foglamp_schema $version_file | awk -F = '{print $2}')
    echo $schema_version
}

exists_schema_change_path () {
    echo 1
}

# main

echo " DBG step 1"

# check if foglamp is installed
IS_FOGLAMP_INSTALLED=$(is_foglamp_installed)

echo " DBG step 2 :$IS_FOGLAMP_INSTALLED:"


# if foglamp is installed...
if [ "$IS_FOGLAMP_INSTALLED" -eq "1" ]
then
    echo "FogLAMP is already installed: this is an upgrade/downgrade."

    # exit if foglamp is running
    IS_FOGLAMP_RUNNING=$(is_foglamp_running)
    if [ "$IS_FOGLAMP_RUNNING" -eq "1" ]
    then
        echo "*** ERROR. FogLAMP is currently running. Stop FogLAMP and try again. ***"
        exit 1
    fi

    # Persist current version in case of upgrade/downgrade
    installed_version=`yum list installed ${PKG_NAME} | grep ${PKG_NAME} | awk '{print $2}'`
    if [ "${installed_version}" ]
    then
        # Persist current FogLAMP version: it will be removed by postinstall script
        this_dir=`pwd`
        cd /usr/local/foglamp/
        echo "${installed_version}" > .current_installed_version
        cd ${this_dir}
    fi

    # check schema version file, exit if schema change path does not exist
    CURRENT_VERSION_FILE=$(get_current_version_file)
    CURRENT_SCHEMA_VERSION=$(get_schema_version $CURRENT_VERSION_FILE)
    echo "FogLAMP currently has schema version $CURRENT_SCHEMA_VERSION"
    EXISTS_SCHEMA_CHANGE_PATH=$(exists_schema_change_path)
    if [ "$EXISTS_SCHEMA_CHANGE_PATH" -eq "0" ]
    then
        echo "*** ERROR. There is no schema change path from the installed version to the new version. ***"
        exit 1
    fi

fi



%preun
#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2018 OSIsoft, LLC
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##--------------------------------------------------------------------

##--------------------------------------------------------------------
##
## This script is used to execute before the removal of files associated with the package.
##
## Author: Ivan Zoratti, Ashwin Gopalakrishnan, Stefano Simonelli
##
##----------------------------------------------------------------------------------------

# FIXME_I
#set -e

PKG_NAME="foglamp"

get_foglamp_script () {
    foglamp_script=$(rpm -ql ${PKG_NAME} | grep 'foglamp/bin/foglamp$')
    echo $foglamp_script
}

stop_foglamp_service () {
    systemctl stop foglamp
}

is_foglamp_running () {
    set +e
    foglamp_script=$(get_foglamp_script)
    foglamp_status_output=$($foglamp_script status 2>&1 | grep 'FogLAMP Uptime')
    rc=$((!$?))
    echo $rc
    set -e
}

kill_foglamp () {
    set +e
    foglamp_script=$(get_foglamp_script)
    foglamp_status_output=$($foglamp_script kill 2>&1)
    set -e
}

disable_foglamp_service () {
    sudo systemctl disable foglamp
}

remove_foglamp_service_file () {
    rm -rf /etc/init.d/foglamp
}

reset_systemctl () {
    sudo systemctl daemon-reload
    sudo systemctl reset-failed
}

remove_pycache_files () {
    set -e
    find /usr/local/foglamp -name "*.pyc" -exec rm -rf {} \;
    find /usr/local/foglamp -name "__pycache__" -exec rm -rf {} \;
}

remove_data_files () {
	rm -rf /usr/local/foglamp/data

}

# main

IS_FOGLAMP_RUNNING=$(is_foglamp_running)

if [ "$IS_FOGLAMP_RUNNING" -eq "1" ]
then
    echo "FogLAMP is currently running."
    echo "Stop FogLAMP service."
    stop_foglamp_service
    echo "Kill FogLAMP."
    kill_foglamp
fi

#echo "Remove data directory."
#remove_data_files
echo "Remove python cache files."
remove_pycache_files
echo "Disable FogLAMP service."
disable_foglamp_service
echo "Remove FogLAMP service script"
remove_foglamp_service_file
echo "Reset systemctl"
reset_systemctl


%post
touch  /home/foglamp/flag_post


%files
%{install_path}/*