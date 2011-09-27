Name:           bestman2
Version:        2.1.3
Release:        1
Summary:        SRM server for Grid Storage Elements

Group:          System Environment/Daemons

#Note, licensing is CR-2404 under BSD license with a grant back provision 
#copyright 2010-2011
License:        BSD
URL:            https://sdm.lbl.gov/bestman/

%define install_root /etc/%{name}

# NOTE: CHANGE THESE EACH RELEASE
%define bestman_url https://codeforge.lbl.gov/frs/download.php/359/bestman2-2.1.3.tar.gz
%define revision 60

Source0:        bestman2.tar.gz
Source1:        bestman2.sh
Source2:        bestman2.init
Source3:        bestman.logrotate
Patch0:		bestman.server.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  java-1.6.0-sun-compat wget ant

Obsoletes: bestman
Provides: bestman

%description
BeStMan 2 - Berkeley Storage Manager

Application server for exporting local file systems securely using the
SRM protocol.  

BeStMan is a full implementation of SRM v2.2, developed by 
Lawrence Berkeley National Laboratory, for disk based storage systems 
and mass storage systems such as HPSS. End users may have their own 
personal BeStMan that manages and provides an SRM interface to their 
local disks or storage systems. It works on top of existing disk-based 
unix file system, and has been reported so far to work on file systems 
such as NFS, PVFS, AFS, GFS, GPFS, PNFS, and Lustre. It also works with 
any existing file transfer service, such as gsiftp, http, https and ftp.

User's guide : http://sdm.lbl.gov/bestman
General support and bug report to <srm@lbl.gov>
Open Science Grid (OSG) support:  osg-storage@opensciencegrid.org
BeStMan Copyright 2010-2011, The Regents of the University of California,
through Lawrence Berkeley National Laboratory.  See LICENSE file for details.

%package common-libs
Summary: Common files BeStMan SRM server client and tester
Group: System Environment/Libraries
Requires:  java
%description common-libs
This package is mostly java libraries (jars) for Bestman.
It contains libraries necessary for Bestman server, client and tester.
It also contains the license, readme, and property files


%package server
Summary: BeStMan SRM server
Group: System Environment/Daemons
Obsoletes: bestman2
Requires: java-1.6.0-sun-compat
Requires: %{name}-common-libs = %{version}-%{release}
Requires: %{name}-server-libs = %{version}-%{release}
Requires: %{name}-server-dep-libs = %{version}-%{release}
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service
%description server
BeStMan SRM server

%package server-libs
Summary: BeStMan Server SRM Java libraries
Group: System Environment/Libraries
Requires:  java
%description server-libs
The BeStMan Server SRM Java libraries

%package server-dep-libs
Summary: BeStMan Server SRM Java libraries
Group: System Environment/Libraries
Requires:  java
%description server-dep-libs
The BeStMan Server SRM Java libraries
This includes all the dependencies and should be 
eventually deprecated once we eventually link
correctly to all the dependencies.

%package client
Summary: Bestman LBNL SRM client
Group: Applications/Internet
Requires: %{name}-client-libs = %{version}-%{release}
Requires: %{name}-common-libs = %{version}-%{release}
%description client
The srm-* client tools

%package client-libs
Summary: Libraries needed for Bestman LBNL SRM client
Group: System Environment/Libraries
Requires:  java
%description client-libs
These are the libraries needed solely for the client 

%package tester
Summary: srmtester application for verifying a SRM endpoint
Group: Applications/Internet
Requires:  java
Requires: %{name}-tester-libs = %{version}-%{release}
Requires: %{name}-common-libs = %{version}-%{release}
%description tester
srmtester application for verifying a SRM endpoint
This application can run through various funcionality of
the SRM v2.2 specification to make sure that all aspects
of the SRM protocol are functioning on an SRM endpoint.

%package tester-libs
Summary: Libraries needed for Bestman LBNL SRM client
Group: System Environment/Libraries
Requires:  java
%description tester-libs
These are the libraries needed solely for the srmtester application 



%prep
%setup -q -n %{name}
pushd bestman2/setup/bestman.in
%patch0 -p0
popd


%build

# NOTE: Upstream package can be created with the following procedure:
# svn checkout -r 50 https://codeforge.lbl.gov/anonscm/bestman
# pushd bestman
# wget https://codeforge.lbl.gov/frs/download.php/316/bestman2-2.1.0-pre2.tar.gz
# tar xvzf bestman2-2.1.0-pre2.tar.gz
# popd
# mv bestman bestman2
# tar cvzf bestman2.tar.gz bestman2
# NOTE: Revision number (50) and url/tarball name may change per release.

./build.configure --with-bestman-url=%{bestman_url} --with-bestman2-version=%{version} --with-revision=%{revision} --with-java-home=/usr/java/latest --enable-cached-src=yes --enable-cached-pkg=yes

make

pushd bestman2

SRM_HOME=%{install_root}
export SRM_HOME
GLOBUS_LOCATION=/usr
export GLOBUS_LOCATION

pushd setup
./configure --with-srm-home=$SRM_HOME \
    --enable-gateway-mode \
    --enable-gums \
    --enable-sudofsmng \
    --with-java-home=/usr/java/latest \
    --with-eventlog-path=/var/log/%{name} \
    --with-cachelog-path=/var/log/%{name} \
    --with-plugin-path=%{_javadir}/bestman2/plugin \
    --with-gums-url=https://GUMS_HOST:8443/gums/services/GUMSAuthorizationServicePort \
    --enable-backup=no \
    --with-bestman2-conf-path=../conf/bestman2.rc
popd

#    --with-certfile-path=/etc/grid-security/http/httpcert.pem \
#    --with-keyfile-path=/etc/grid-security/http/httpkey.pem \
#    --with-gums-certfile-path=/etc/grid-security/http/httpcert.pem \
#    --with-gums-keyfile-path=/etc/grid-security/http/httpkey.pem \

#Fix paths in bestman2.rc
JAVADIR=`echo %{_javadir} |  sed 's/\//\\\\\//g'`
sed -i "s/SRM_HOME=.*/SRM_HOME=\/etc\/bestman2/" conf/bestman2.rc
sed -i "s/SRM_OWNER=.*/SRM_OWNER=bestman/" conf/bestman2.rc
sed -i "s/GridMapFileName=.*/GridMapFileName=\/etc\/bestman2\/conf\/grid-mapfile.empty/" conf/bestman2.rc
sed -i "s/BESTMAN_SYSCONF=.*/BESTMAN_SYSCONF=\/etc\/bestman2\/conf\/bestman2.rc/" conf/bestman2.rc
sed -i "s/BESTMAN_LOG=.*/BESTMAN_LOG=\/var\/log\/bestman2\/bestman2.log/" conf/bestman2.rc
sed -i "s/BESTMAN_LIB=.*/BESTMAN_LIB=$JAVADIR\/bestman2/" conf/bestman2.rc
sed -i "s/EventLogLocation=.*/EventLogLocation=\/var\/log\/bestman2/" conf/bestman2.rc
sed -i "s/X509_CERT_DIR=.*/X509_CERT_DIR=\/etc\/grid-security\/certificates/" conf/bestman2.rc
sed -i "s/BESTMAN_GUMSCERTPATH=.*/BESTMAN_GUMSCERTPATH=\/etc\/grid-security\/http\/httpcert.pem/" conf/bestman2.rc
sed -i "s/BESTMAN_GUMSKEYPATH=.*/BESTMAN_GUMSKEYPATH=\/etc\/grid-security\/http\/httpkey.pem/" conf/bestman2.rc
sed -i "s/CertFileName=.*/CertFileName=\/etc\/grid-security\/http\/httpcert.pem/" conf/bestman2.rc
sed -i "s/KeyFileName=.*/KeyFileName=\/etc\/grid-security\/http\/httpkey.pem/" conf/bestman2.rc
sed -i "s/pluginLib=.*/pluginLib=$JAVADIR\/bestman2\/plugin\//" conf/bestman2.rc

#Fix paths in binaries.  Wish I could do this in configure...
sed -i "s/SRM_HOME=\/.*/SRM_HOME=\/etc\/bestman2/" bin/*

popd

%install
rm -rf $RPM_BUILD_ROOT

pushd bestman2



mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{install_root}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp -arp conf $RPM_BUILD_ROOT%{install_root}
cp -arp lib $RPM_BUILD_ROOT%{_javadir}/%{name}
cp -arp properties $RPM_BUILD_ROOT%{install_root}

install -m 0644 version $RPM_BUILD_ROOT%{install_root}/version
install -m 0755 sbin/bestman.server $RPM_BUILD_ROOT%{_sbindir}/bestman.server


mkdir -p $RPM_BUILD_ROOT%{_bindir}
for i in `ls bin`; do
  install -m 0755 bin/$i $RPM_BUILD_ROOT%{_bindir}/
done

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir
touch $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem

mkdir -p $RPM_BUILD_ROOT%{_var}/log/%{name}

popd

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
getent group bestman >/dev/null || groupadd -r bestman
getent passwd bestman >/dev/null || \
       useradd -r -g bestman -d %{install_root} -c "BeStMan 2 Server user" \
       -s /bin/bash bestman

%post server
/sbin/chkconfig --add %{name}

%preun server
if [ "$1" = "0" ]; then
    /sbin/chkconfig --del %{name}
fi

%postun server
if [ "$1" -ge "1" ] ; then
    /sbin/service bestman2 condrestart >/dev/null 2>&1 || :
fi

%files common-libs
%defattr(-,root,root,-)
%dir %{install_root}
%{_javadir}/bestman2/axis/axis.jar
%{_javadir}/bestman2/axis/commons-discovery-0.2.jar
%{_javadir}/bestman2/axis/commons-logging-1.1.jar
%{_javadir}/bestman2/axis/jaxrpc.jar
%{_javadir}/bestman2/axis/wsdl4j-1.6.2.jar
%{_javadir}/bestman2/axis/xercesImpl-2.9.1.jar
%{_javadir}/bestman2/jglobus/cog-axis-1.8.0.jar
%{_javadir}/bestman2/jglobus/cog-jglobus-1.8.0.jar
%{_javadir}/bestman2/jglobus/cog-url-1.8.0.jar
%{_javadir}/bestman2/jglobus/cryptix-asn1.jar
%{_javadir}/bestman2/jglobus/cryptix32.jar
%{_javadir}/bestman2/jglobus/jce-jdk13-131.jar
%{_javadir}/bestman2/jglobus/log4j-1.2.15.jar
%{_javadir}/bestman2/jglobus/puretls.jar
%{_javadir}/bestman2/bestman2-stub.jar
%config(noreplace) %{install_root}/properties/authmod-unix.properties
%config(noreplace) %{install_root}/properties/authmod-win.properties
%config(noreplace) %{install_root}/properties/log4j.properties
%config(noreplace) %{install_root}/version
%doc bestman2/LICENSE
%doc bestman2/COPYRIGHT
%doc bestman2/CHANGE
%doc bestman2/README


%files client
%defattr(-,root,root,-)
%config(noreplace) %{install_root}/conf/srmclient.conf
%config(noreplace) %{install_root}/conf/srmclient.conf.sample
%config(noreplace) %{install_root}/conf/bestman2.rc
%{_bindir}/srm-copy
%{_bindir}/srm-copy-status
%{_bindir}/srm-extendfilelifetime
%{_bindir}/srm-ls
%{_bindir}/srm-ls-status
%{_bindir}/srm-mkdir
%{_bindir}/srm-mv
%{_bindir}/srm-permission-check
%{_bindir}/srm-permission-get
%{_bindir}/srm-permission-set
%{_bindir}/srm-ping
%{_bindir}/srm-putdone
%{_bindir}/srm-release
%{_bindir}/srm-req-abort
%{_bindir}/srm-req-abortfiles
%{_bindir}/srm-req-resume
%{_bindir}/srm-req-summary
%{_bindir}/srm-req-suspend
%{_bindir}/srm-req-tokens
%{_bindir}/srm-rm
%{_bindir}/srm-rmdir
%{_bindir}/srm-sp-change
%{_bindir}/srm-sp-change-status
%{_bindir}/srm-sp-info
%{_bindir}/srm-sp-purge
%{_bindir}/srm-sp-release
%{_bindir}/srm-sp-reserve
%{_bindir}/srm-sp-reserve-status
%{_bindir}/srm-sp-tokens
%{_bindir}/srm-sp-update
%{_bindir}/srm-sp-update-status
%{_bindir}/srm-transferprotocols
%doc bestman2/LICENSE
%doc bestman2/COPYRIGHT
%doc bestman2/version
%doc bestman2/CHANGE
%doc bestman2/README

%files server
%defattr(-,root,root,-)
%{_sbindir}/bestman.server
%{_bindir}/bestman-diag
%config(noreplace) %{install_root}/conf/WEB-INF
%config(noreplace) %{install_root}/conf/bestman2.gateway.sample.rc
%config(noreplace) %{install_root}/conf/grid-mapfile.empty
%config(noreplace) %{install_root}/conf/bestman-diag-msg.conf
%config(noreplace) %{install_root}/conf/bestman-diag.conf.sample
%config(noreplace) %{install_root}/conf/bestman2.rc
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem
%attr(-,bestman,bestman) %dir %{_var}/log/%{name}
%doc bestman2/docs/README.javaapi


%files client-libs
%{_javadir}/bestman2/bestman2-client.jar
%{_javadir}/bestman2/bestman2-printintf.jar
%{_javadir}/bestman2/bestman2-transfer.jar


%files server-libs
%doc bestman2/LICENSE
%doc bestman2/COPYRIGHT
%doc bestman2/CHANGE
%doc bestman2/README
%{_javadir}/bestman2/bestman2.jar
%{_javadir}/bestman2/bestman2-aux.jar


%files server-dep-libs
%{_javadir}/bestman2/gums/glite-security-trustmanager.jar
%{_javadir}/bestman2/gums/glite-security-util-java.jar
%{_javadir}/bestman2/gums/opensaml-1.0.1.jar
%{_javadir}/bestman2/gums/privilege-1.0.1.3.jar
%{_javadir}/bestman2/gums/vomsjapi-1.9.10.jar
%{_javadir}/bestman2/gums2/commons-collections-3.2.jar
%{_javadir}/bestman2/gums2/commons-lang-2.1.jar
%{_javadir}/bestman2/gums2/joda-time-1.6.jar
%{_javadir}/bestman2/gums2/opensaml-2.3.1.jar
%{_javadir}/bestman2/gums2/openws-1.3.0.jar
%{_javadir}/bestman2/gums2/privilege-xacml-2.2.5.jar
%{_javadir}/bestman2/gums2/velocity-1.5.jar
%{_javadir}/bestman2/gums2/xalan-2.7.1.jar
%{_javadir}/bestman2/gums2/xml-apis-2.9.1.jar
%{_javadir}/bestman2/gums2/xmlsec-1.4.3.jar
%{_javadir}/bestman2/gums2/xmltooling-1.2.1.jar
%{_javadir}/bestman2/jetty/jetty-client-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-continuation-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-deploy-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-http-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-io-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-security-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-server-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-servlet-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-util-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-webapp-7.1.5.v20100705.jar
%{_javadir}/bestman2/jetty/jetty-xml-7.1.5.v20100705.jar
%{_javadir}/bestman2/others/concurrent.jar
%{_javadir}/bestman2/others/jcl-over-slf4j-1.6.0.jar
%{_javadir}/bestman2/others/je-4.0.103.jar
%{_javadir}/bestman2/others/servlet-api-2.5.jar
%{_javadir}/bestman2/others/slf4j-api-1.6.0.jar
%{_javadir}/bestman2/others/slf4j-log4j12-1.6.0.jar
%{_javadir}/bestman2/others/slf4j-simple-1.6.0.jar
%{_javadir}/bestman2/others/which4j.jar
%{_javadir}/bestman2/plugin/LBNL.RFF.README.txt
%{_javadir}/bestman2/plugin/LBNL.RFF.jar
%{_javadir}/bestman2/voms/bcprov-jdk15-139.jar

%files tester
%{_bindir}/srm-tester
%config(noreplace) %{install_root}/conf/srmtester.conf.sample
%config(noreplace) %{install_root}/conf/srmtester.conf


%files tester-libs
%{_javadir}/bestman2/bestman2-tester-driver.jar
%{_javadir}/bestman2/bestman2-tester-main.jar
%{_javadir}/bestman2/bestman2-printintf.jar
%{_javadir}/bestman2/bestman2-transfer.jar


%changelog
* Fri Aug 26 2011 Doug Strain <dstrain@fnal.gov> - 2.1.2-1
- Updated for Bestman 2.1.2

* Mon Aug 08 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.1.1-5
New bestman server patch

* Fri Aug 05 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.1.1-4
get rid of bestman2 dependency of client and server

* Wed Aug 3 2011 Doug Strain <dstrain@fnal.gov> 2.1.1-3
- Changing to use bestman user instead of daemon user.

* Mon Aug 1 2011 Doug Strain <dstrain@fnal.gov> 2.1.1-2
- Fixing dependencies

* Thu Jul 28 2011 Doug Strain <dstrain@fnal.gov> 2.1.1-1
- Updating bestman to 2.1.1.
- Splitting RPMs into multiple RPMS
-  common-libs,tester-libs,server-libs,client-libs,server-dep-libs

* Fri Jul 15 2011 Doug Strain <dstrain@fnal.gov> 2.1.0-3
- Fixing some rpmlint warnings and errors

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.1.0-3
- Fixed java deps to reflect new java strategy.

* Sun Jul 10 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre4-3
- Changed RPM to not require certs

* Mon Jul 07 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre4
- Updated to bestman2.1.0pre4
- Changed the locations to be FHS compliant:
- Moved java jar files to javadir/bestman2
- Moved bestman.server to sbindir
- Moved base location (now only configuration) to /etc/bestman2
- Moved bestman2.rc to /etc/bestman2/conf and added to client package
- Deleted setup directory in favor of combined bestman2.rc/sysconfig

* Mon Jul 01 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre2
- Creating Bestman2 spec file based on Hadoop repository

* Mon Jun 13 2011 Doug Strain <dstrain@fnal.gov> 2.0.13.t5-43
- Creating Bestman2 spec file based on Hadoop repository

* Wed May 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.12-3
- Add log4j.properties to Jetty, allowing the logging of GSI issues
- Fix deps for bestman2-server and -libs

* Tue May 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.12-2
- Split packages into server, libs, and client
- Move everything into FHS locations.

* Tue May 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.12-1
- Update to 2.0.12
- Change bestman2 to a source build
- Fix bestman.server.in so folks don't nuke their install if they run configure again.

* Mon Apr 25 2011 Jeff Dost <jdost@ucsd.edu> 2.0.10-1
- Update to 2.0.10

* Mon Apr 25 2011 Jeff Dost <jdost@ucsd.edu> 2.0.5-2
- Fix bestman.logrotate to point to /var/log/bestman2/*.log

* Wed Jan 26 2011 Jeff Dost <jdost@ucsd.edu> 2.0.5-1
- Update to 2.0.5

* Thu Dec 23 2010 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.4-2
- Patch the configuration file to use the correct port and some initial
  suggestions.

* Tue Dec 21 2010 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.4-1
- Bump to latest upstream version.
- Added "Obsoletes" for original bestman package since we have run
  bestman2 stably for awhile.

* Tue Oct 12 2010 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.2-4
- Fixed the init scripts to behave more like a RHEL init script.
- Added condrestart upon upgrade.

* Wed Sep 22 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.2-1
- Update to 2.0.2

* Thu Jul 1 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.0-3
- Update log file locations so that they don't conflict with earlier bestman

* Thu Jul 1 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.0-2
- Fix path problems in init script

* Tue Jun 8 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.0-1
- Initial package of bestman2, based on original bestman spec file

