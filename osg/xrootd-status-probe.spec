
Name: xrootd-status-probe
Version: 0.0.3
Release: 4%{?dist}
Summary: Probes to check the health of an Xrootd server

Group: System/Monitoring
License: GPL
URL: svn://t2.unl.edu/brian/xrootd_status_probe
Source0: %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: xrootd-client-devel

%description

%prep
%setup -q

%build
%configure --with-xrootd-inc=/usr/include/xrootd
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/xrdcp_*
%{_bindir}/cmsd_*
%{_defaultdocdir}/xrootd-status-probe/README

%changelog
* Wed Apr 03 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.3-4
- Bump to rebuild against xrootd 3.3.1

* Thu Mar 29 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.3-3
- Rebuild for Xrootd 3.2.

* Fri Nov 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.3-2
- Rebuild against new Xrootd version.


