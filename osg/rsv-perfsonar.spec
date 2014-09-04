Name:      rsv-perfsonar
Version:   0.0.1
Release:   3%{?dist}
Summary:   RSV Metrics to monitor pefsonar
Packager:  OSG-Software
Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: rsv
Requires: esmond

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
Requires: python-simplejson
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}

%prep
%setup -n %{name}

%install
rm -fr $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README
%defattr(-,root,root,-)
%{_libexecdir}/rsv/probes/perfsonar-simple-local-probe
%{_libexecdir}/rsv/probes/network-monitoring-local-probe
%{_libexecdir}/rsv/probes/worker-scripts/esmond*
%{_libexecdir}/rsv/metrics/org.osg.general.perfsonar-simple
%{_libexecdir}/rsv/metrics/org.osg.local.network-monitoring-local
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.general.perfsonar-simple.meta
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.local.network-monitoring-local.meta
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.general.perfsonar-simple.conf
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.local.network-monitoring-local.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-perfsonar-metrics
#%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/
%attr(-,rsv,rsv)  %{_sysconfdir}/rsv

%changelog
* Thu Sep 04 2014 <efajardo@physics.ucsd.edu> - 0.0.1-3
- Removed the different rsv* requirements and added rsv.

* Wed Sep 03 2014 <efajardo@physics.ucsd.edu> - 0.0.1-2
- Removed the log from the rsv log from the files not to collide with the rsv-metrics

* Fri Aug 29 2014  <efajardo@physics.ucsd.edu> - 0.0.1-1
- Creating a first RPM for rsv-perfsonar