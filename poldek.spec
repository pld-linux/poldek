Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narz�dzie do pakiet�w RPM
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
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	/usr/bin/pod2man
BuildRequires:	trurlib-devel >= 0.43.1
%{?BOOT:BuildRequires:	zlib-static}
%{?BOOT:BuildRequires:	bzip2-static}
%{?BOOT:BuildRequires:	trurlib-static}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
poldek is a cmdline tool which can be used to verify, install and
upgrade given package sets.

%description -l pl
poldek jest narz�dziem linii polece� s�u��cym do weryfikacji, instalacji i upgrade'u zestaw�w pakiet�w.

%if %{?BOOT:1}%{!?BOOT:0}
%package BOOT
Summary:	poldek for bootdisk
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System

%description BOOT
poldek is a cmdline tool which can be used to verify, install and
upgrade given package sets.
This version is for boot disk.

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

%install
rm -rf $RPM_BUILD_ROOT

%if %{?BOOT:1}%{!?BOOT:0}
install -d $RPM_BUILD_ROOT%{_libdir}/bootdisk/sbin
install %{name}-BOOT $RPM_BUILD_ROOT%{_libdir}/bootdisk/sbin/%{name}
install rpmvercmp-BOOT $RPM_BUILD_ROOT%{_libdir}/bootdisk/sbin/rpmvercmp
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
%attr(755,root,root) %{_libdir}/bootdisk/sbin/poldek
%endif
