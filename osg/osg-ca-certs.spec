Name:           osg-ca-certs
Version:        1.24
Release:        2
Summary:        OSG Packaging of the IGTF CA Certs and OSG-specific CAs, in the new OpenSSL 0.9.8/1.0.0 format

Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

# Note: currently, one needs a valid client certificate to access the source tarball
# https://osg-svn.rtinfo.indiana.edu/cadist/release/osg-certificates-1.20NEW.tar.gz
Source0:        osg-certificates-1.24NEW.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       grid-certificates = 7

Conflicts:      osg-ca-scripts

Obsoletes:      vdt-ca-certs
Obsoletes:      osg-ca-certs-experimental

%description
%{summary}

%prep
%setup -q -n certificates

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/grid-security/certificates
chmod 0644 * 
cp -p * $RPM_BUILD_ROOT/etc/grid-security/certificates/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,-)
%dir %attr(0755,root,root) /etc/grid-security/certificates
/etc/grid-security/certificates/*
%doc

%changelog
* Thu Nov 28 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.24-2
- use cp -p instead of install to maintain symlink

* Thu Oct 11 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.24-1
- New CA release

* Thu Sep 27 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.23-1
- New CA release

* Thu Sep 9 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.22-2
- Added osg-ca-certs-experimental in Obsoletes line 

* Thu Sep 8 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.22-1
- Released 1.22
- Changed name from osg-ca-certs-experimental to osg-ca-certs
- Added an Obsoletes line to vdt-ca-certs to make sure that there is an upgrade path for people using the VDT RPM

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.20-3
Fix conflicts line.

* Wed Aug 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.20-2
- Fix directory ownership issue.

* Mon Aug 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.20-1
- Initial version, based on osg-ca-certs spec file.

