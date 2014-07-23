%define name panda-common
%define version 0.0.5.3
%define unmangled_version 0.0.5.3
%define release 1

Summary:  PanDA Common Package
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Panda Team <hn-atlas-panda-pathena@cern.ch>
Packager: Panda Team <hn-atlas-panda-pathena@cern.ch>
Provides: panda-common
Requires: python
Url: https://twiki.cern.ch/twiki/bin/view/Atlas/PanDA

%description
This package contains PanDA Common Components

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
