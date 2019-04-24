%define __spec_install_pre /bin/true

Name:          foglamp
Vendor:        Dianomic Systems, Inc. <info@dianomic.com>
Version:       1.5.00
Release:       0.0.01
BuildArch:     x86_64
Summary:       FogLAMP, the open source platform for the Internet of Things
License:       Apache License
Group: 	       IOT
URL:           http://www.dianomic.com

%define install_path	/usr/local

Prefix:        /usr/local
Requires:      autoconf,curl,libtool,libboost-dev,libboost-system-dev,libboost-thread-dev,libpq-dev,python3-pip,python3-setuptools,sqlite3,sudo
AutoReqProv:   no

%description
FogLAMP, the open source platform for the Internet of Things

%files
%{install_path}/*