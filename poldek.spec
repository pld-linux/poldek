# conditional build
#  --with static   -- don't use shared libraries
#  --without imode -- don't build interactive mode
#  --without curl  -- don't link curl
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narz�dzie do zarz�dzania pakietami RPM
Name:		poldek
Version:	0.17.2
Release:	3
License:	GPL
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		%{name}-bugfix.patch
URL:		http://team.pld.org.pl/~mis/poldek/
%{!?_with_static:Requires:	trurlib >= 0.43.5}
Requires:	/bin/rpm
BuildRequires:	bzip2-devel
BuildRequires:	db3-devel >= 3.1.14-2
BuildRequires:	curl-devel >= 7.8
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	popt-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 4.0
BuildRequires:	trurlib-devel >= 0.43.5
BuildRequires:	zlib-devel
BuildRequires:	/usr/bin/pod2man
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

%{?_without_imode:This version hasn't got interactive mode.}

%description -l pl
poldek jest narz�dziem linii polece� s�u��cym do weryfikacji,
instalacji (w��czaj�c instalacj� systemu od zera), aktualizacji 
i usuwania pakiet�w.

Program mo�e by� u�ywany w trybie wsadowym (jak debianowy apt-get)
lub interaktywnym. Tryb interaktywny posiada interfejs readline 
z dope�nianiem komend i histori�, podobny do trybu shell perlowego 
modu�u CPAN. 

%{?_with_static:Ta wersja jest konsolidowana statycznie.}

%{?_without_imode:Ta wersja nie posiada trybu interaktywnego.}

%prep
%setup -q
%patch0 -p1 

%build
%configure \
	%{?_with_static:--enable-static} \
	%{?_without_imode:--disable-imode} \
	%{?_without_curl:--without-curl}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

# no strip cause program's alpha stage and core may be useful
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{?_with_static:rm -f $RPM_BUILD_ROOT/%{_bindir}/rpmvercmp}
sed "s/i686/%{_target_cpu}/g" < %{SOURCE1} > $RPM_BUILD_ROOT/etc/%{name}.conf

gzip -9nf README* *sample* NEWS TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}*
%doc *.gz
