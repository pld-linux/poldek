Summary:	RPM packages management helper tool
Name:		poldek
Version:	0.12
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	%{name}-%{version}.tar.gz
Requires:	/bin/rpm
BuildRequires:	db3-devel >= 3.1.14-2
BuildRequires:	rpm-devel >= 3.0.5
BuildRequires:	zlib-static
BuildRequires:	bzip2-static
BuildRequires:	/usr/bin/pod2man
BuildRequires:	trurlib-devel >= 0.431
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
poldek is a cmdline tool which can be used to verify, install and
upgrade given package sets.

%if %{?BOOT:1}%{!?BOOT:0}
%package BOOT
Summary:	poldek for bootdisk
Group:		Applications/System

%description BOOT
%endif

%prep 
%setup -q 

%build
%if %{?BOOT:1}%{!?BOOT:0}
%configure --enable-static --disable-imode
%{__make}
mv -f %{name} %{name}-BOOT
mv -f rpmvercmp rpmvercmp-BOOT
%{__make} clean
%endif

%configure 
%{__make} 

#CFLAGS="%{!?debug:$RPM_OPT_FLAGS}%{?debug:-O0 -g}" all

%install
rm -rf $RPM_BUILD_ROOT

%if %{?BOOT:1}%{!?BOOT:0}
install -d $RPM_BUILD_ROOT/usr/lib/bootdisk/sbin
install -s %{name}-BOOT $RPM_BUILD_ROOT/usr/lib/bootdisk/sbin/%{name}
install -s rpmvercmp-BOOT $RPM_BUILD_ROOT/usr/lib/bootdisk/sbin/rpmvercmp
%endif

# no strip cause program's alpha stage and core may be useful
%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README* *sample* poldek.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}*
%doc README* *sample*

%if %{?BOOT:1}%{!?BOOT:0}
%files BOOT
%defattr(644,root,root,755)
%attr(755,root,root) /usr/lib/bootdisk/sbin/poldek
%endif
