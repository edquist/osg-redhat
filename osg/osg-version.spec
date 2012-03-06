Name:      osg-version
Summary:   OSG Version
Version:   3.0.8
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:   osg-version

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo %{version} > $RPM_BUILD_ROOT%{_sysconfdir}/osg-version
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/osg-version

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -pm 755 %{SOURCE0}  $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sysconfdir}/osg-version
%{_bindir}/osg-version

%changelog
* Tue Feb 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.8-1
- Updated to 3.0.8-1

* Mon Feb 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.7-1
- Updated to 3.0.7-1

* Mon Jan 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.6-1
- Updated to 3.0.6-1

* Mon Dec 12 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.5-1
- Updated to 3.0.5-1

* Mon Dec 05 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.4-1
- Updated to 3.0.4-1

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.3-1
- Updated version of 3.0.3
