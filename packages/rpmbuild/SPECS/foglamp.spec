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
Requires:      sudo
AutoReqProv:   no

%description
FogLAMP, the open source platform for the Internet of Things

%files
%{install_path}/*