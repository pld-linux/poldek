# conditional build
#  --with static   -- don't use shared libraries
#  --without imode -- don't build interactive mode
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.16
Release:	3
License:	GPL
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}/%{name}-%{version}.tar.gz
%{!?_with_static:Requires:	trurlib >= 0.43.4}
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
poldek jest narzêdziem linii poleceñ s³u¿±cym do weryfikacji,
instalacji (w³±czaj±c instalacjê systemu od zera), aktualizacji 
pakietów i usuwania pakietów.

Program mo¿e byæ u¿ywany w trybie wsadowym (jak debianowy apt-get)
lub interaktywnym. Tryb interaktywny posiada interfajs readline z
dope³nianiem komend i histori±, podobny do trybu shell CPANa.

%{?_with_static:Ta wersja jest zlinkowana statycznie.}

%{?_without_imode:Ta wersja nie posiada trybu interaktywnego.}

%prep
%setup -q

%build
%configure \
	%{?_with_static:--enable-static} \
	%{?_without_imode:--disable-imode}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

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
