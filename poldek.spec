Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narz�dzie do zarz�dzania pakietami RPM
Name:		poldek
Version:	0.16
Release:	2
License:	GPL
Group:		Applications/System
Group(cs):	Aplikace/Syst�m
Group(da):	Programmer/System
Group(de):	Applikationen/System
Group(es):	Aplicaciones/Sistema
Group(fr):	Applications/Syst�me
Group(it):	Applicazioni/Sistema
Group(ja):	���ץꥱ�������/�����ƥ�
Group(no):	Applikasjoner/System
Group(pl):	Aplikacje/System
Group(pt):	Aplica��es/Sistema
Group(pt_BR):	Aplica��es/Sistema
Group(ru):	����������/�������
Group(sv):	Till�mpningar/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}/%{name}-%{version}.tar.gz
%{!?_with_static:Requires:	trurlib >= 0.43.3}
Requires:	/bin/rpm
BuildRequires:	bzip2-devel
BuildRequires:	db3-devel >= 3.1.14-2
BuildRequires:	curl-devel >= 7.8
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	popt-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 3.0.5
BuildRequires:	trurlib-devel >= 0.43.3
BuildRequires:	zlib-devel
BuildRequires:	/usr/bin/pod2man
%{?BOOT:BuildRequires:	bzip2-static}
%{?BOOT:BuildRequires:	curl-static}
%{?BOOT:BuildRequires:	openssl-static}
%{?BOOT:BuildRequires:	popt-static}
%{?BOOT:BuildRequires:	rpm-static}
%{?BOOT:BuildRequires:	trurlib-static}
%{?BOOT:BuildRequires:	zlib-static}
%{?_with_static:BuildRequires:	bzip2-static}
%{?_with_static:BuildRequires:	curl-static}
%{?_with_static:BuildRequires:	openssl-static}
%{?_with_static:BuildRequires:	popt-static}
%{?_with_static:BuildRequires:	rpm-static}
%{?_with_static:BuildRequires:	trurlib-static}
%{?_with_static:BuildRequires:	zlib-static}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
poldek is an RPM package management tool which allows you to easily
perform package verification, installation (including system
installation from scratch), upgrading, and removal.

Program can be used in batch (like apt-get from Debian's APT) or
interactive mode. The interactive mode puts you into a readline
interface with command line autocompletion and history, similar to the
shell mode of Perl's CPAN.

%{?_with_static:This version is statically linked}

%description -l pl
poldek jest narz�dziem linii polece� s�u��cym do weryfikacji,
instalacji i aktualizacji pakiet�w.

%package BOOT
Summary:	poldek for bootdisk
Summary(pl):	poldek dla bootkietki
Group:		Applications/System
Group(cs):	Aplikace/Syst�m
Group(da):	Programmer/System
Group(de):	Applikationen/System
Group(es):	Aplicaciones/Sistema
Group(fr):	Applications/Syst�me
Group(it):	Applicazioni/Sistema
Group(ja):	���ץꥱ�������/�����ƥ�
Group(no):	Applikasjoner/System
Group(pl):	Aplikacje/System
Group(pt):	Aplica��es/Sistema
Group(pt_BR):	Aplica��es/Sistema
Group(ru):	����������/�������
Group(sv):	Till�mpningar/System

%description BOOT
poldek is a cmdline tool which can be used to verify, install and
upgrade given package sets. This version is for boot disk.

%description BOOT -l pl
poldek jest narz�dziem linii polece� s�u��cym do weryfikacji,
instalacji i aktualizacji pakiet�w. To jest wersja dla bootkietki.

%prep 
%setup -q

%build
%if %{?BOOT:1}%{!?BOOT:0}
%configure --enable-static --disable-imode
%{__make} CFLAGS="-O0 -g"
mv -f %{name} %{name}-BOOT
%{__make} clean
%endif

%configure %{?_with_static:--enable-static}
%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%if %{?BOOT:1}%{!?BOOT:0}
install -d $RPM_BUILD_ROOT%{_libdir}/bootdisk/sbin
install %{name}-BOOT $RPM_BUILD_ROOT%{_libdir}/bootdisk/sbin/%{name}
%endif

# no strip cause program's alpha stage and core may be useful
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{?_with_static:rm -f $RPM_BUILD_ROOT/%{_bindir}/rpmvercmp}
sed "s/i686/%{_target_cpu}/g" < poldekrc.sample-pld > $RPM_BUILD_ROOT/etc/%{name}.conf

gzip -9nf README* *sample* NEWS TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}*
%doc *.gz

%if %{?BOOT:1}%{!?BOOT:0}
%files BOOT
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/bootdisk/sbin/poldek
%endif
