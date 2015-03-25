Summary: CernVM File System OSG Configuration and Public Keys
Name: cvmfs-config-osg
Version: 1.1
Release: 4%{?dist}
%define cvmfsversion 2.1.20
Source0: https://ecsft.cern.ch/dist/cvmfs/cvmfs-%{cvmfsversion}.tar.gz
Source1: 60-osg.conf
Patch0: osgstratum1s.patch
BuildArch: noarch
Group: Applications/System
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: cvmfs-config = %{version}-%{release}
Obsoletes: cvmfs-keys
Obsoletes: cvmfs-init-scripts
Obsoletes: oasis-config

Conflicts: cvmfs < 2.1.20
Conflicts: cvmfs-server < 2.1.20

%description
Default configuration parameters and public keys for CernVM-FS, providing access
to repositories under the cern.ch, egi.eu, and opensciencegrid.org domains

%prep
%setup -q -n cvmfs-%{cvmfsversion}
%patch0 -p0

%install
cp `find mount -mindepth 1 \( -name "*.conf" -o -name "*.pub" \)` .
SOURCE0=cern.ch.pub
SOURCE1=cern-it1.cern.ch.pub
SOURCE2=cern-it2.cern.ch.pub
SOURCE3=cern-it3.cern.ch.pub
SOURCE4=egi.eu.pub
SOURCE5=opensciencegrid.org.pub
SOURCE6=cern.ch.conf
SOURCE7=egi.eu.conf
SOURCE8=opensciencegrid.org.conf
SOURCE11=atlas-nightlies.cern.ch.conf
SOURCE12=cms.cern.ch.conf
SOURCE13=grid.cern.ch.conf
rm -rf $RPM_BUILD_ROOT
for cvmfsdir in keys/cern.ch keys/egi.eu keys/opensciencegrid.org domain.d default.d config.d; do
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/$cvmfsdir
done
for key in ${SOURCE0} ${SOURCE1} ${SOURCE2} ${SOURCE3}; do
    install -D -m 444 "${key}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/keys/cern.ch
done
for key in ${SOURCE4}; do
    install -D -m 444 "${key}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/keys/egi.eu
done
for key in ${SOURCE5}; do
    install -D -m 444 "${key}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/keys/opensciencegrid.org
done
for domainconf in ${SOURCE6} ${SOURCE7} ${SOURCE8}; do
    install -D -m 444 "${domainconf}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/domain.d
done
for defaultconf in %{SOURCE1}; do
    install -D -m 444 "${defaultconf}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/default.d
done
for conf in ${SOURCE11} ${SOURCE12} ${SOURCE13}; do
    install -D -m 444 "${conf}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/config.d
done

%files
%dir %{_sysconfdir}/cvmfs/keys/cern.ch
%dir %{_sysconfdir}/cvmfs/keys/egi.eu
%dir %{_sysconfdir}/cvmfs/keys/opensciencegrid.org
%{_sysconfdir}/cvmfs/keys/cern.ch/*
%{_sysconfdir}/cvmfs/keys/egi.eu/*
%{_sysconfdir}/cvmfs/keys/opensciencegrid.org/*
%config %{_sysconfdir}/cvmfs/domain.d/egi.eu.conf
%config %{_sysconfdir}/cvmfs/domain.d/opensciencegrid.org.conf
%config %{_sysconfdir}/cvmfs/domain.d/cern.ch.conf
%config %{_sysconfdir}/cvmfs/default.d/60-osg.conf
%config %{_sysconfdir}/cvmfs/config.d/*

%changelog
* Wed Mar 24 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-4
- add patch to set egi and osg repo servers to only OSG stratum 1s

* Wed Mar 24 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-3
- add %{?dist} to release number

* Wed Mar 24 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-2
- bump release only to allow koji to rebuild; the first attempt failed
  because of a mysterious error in koji

* Wed Mar 24 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-1
- initial creation, based on cvmfs-config-default.spec
