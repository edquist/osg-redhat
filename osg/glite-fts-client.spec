Name:		glite-fts-client
Version:	3.7.4
Release:	1
Summary:	gLite FTS client

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.transfer-cli
# Retrieved on Jul 5 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.transfer-cli.tar.gz?view=tar&pathrev=glite-data-transfer-cli_R_3_7_4_1
Source0:        org.glite.data.transfer-cli.tar.gz
Source1:        stdsoap2.c
Patch0:         glite_fts_client_fedora.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:	CGSI-gSOAP
BuildRequires:  automake autoconf libtool 
BuildRequires:  CGSI-gSOAP-devel
BuildRequires:  glite-build-common-cpp
BuildRequires:  glite-data-build
BuildRequires:  glite-data-util-c-devel
BuildRequires:  glite-data-delegation-cli-devel
BuildRequires:  glite-data-transfer-interface
BuildRequires:  /usr/bin/xsltproc

%description
%{summary}

%prep
%setup -n org.glite.data.transfer-cli

%patch0 -p0

cp %SOURCE1 .

%build
./bootstrap
%configure --with-channel-wsdl=/usr/share/glite-data-transfer-interface/interface/org.glite.data-channel-3.7.0.wsdl --with-fts-wsdl=/usr/share/glite-data-transfer-interface/interface/org.glite.data-fts-3.7.0.wsdl --with-gsoap-version=2.7.13 --with-version=%{version} 

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages/fts.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages/fts.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/python2.4/site-packages/fts*
%{_libdir}/lib*.so.*

%{_mandir}/man1/glite*
%{_bindir}/glite-transfer*

%changelog
* Tue Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.1.3-1
- Initial OSG packaging.


%package devel
Summary: C libraries and headers for working with FTS
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}

%files devel
%{_includedir}/glite/data/transfer*
%{_libdir}/libglite_data_transfer_api_simple_c.so
%{_libdir}/libglite_data_transfer_channel_api_c.so
%{_libdir}/libglite_data_transfer_channel_api_simple_c.so
%{_libdir}/libglite_data_transfer_fts_api_c.so
%{_libdir}/libglite_data_transfer_fts_api_simple_c.so

%package doc
Summary: Documentation files for FTS
Group: Documentation

%description doc
%{summary}

%files doc
%defattr(-,root,root)
%doc %{_docdir}/glite-data-transfer-cli

