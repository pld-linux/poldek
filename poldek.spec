# TODO:
#	- libs/devel subpackages
#
# Conditional build:
%bcond_with	static	# don't use shared libraries
%bcond_without	imode	# don't build interactive mode
#
# required versions (forced to avoid SEGV with mixed db used by rpm and poldek)
%define	ver_db	4.2.50-1
%define	ver_rpm	4.3-0.20030610.29
%define	snap	20041005.23
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.19.0
Release:	0.%{snap}.2
License:	GPL v2
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/snapshots/%{name}-%{version}-cvs%{snap}.tar.bz2
# Source0-md5:	33b8f14d8b7bf4c1538ac441ac3c7eca
Source1:	%{name}.conf
URL:		http://team.pld.org.pl/~mis/poldek/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	bzip2-devel
BuildRequires:	db-devel >= %{ver_db}
BuildRequires:	gettext-autopoint
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	pcre-devel
BuildRequires:	perl-tools-pod
BuildRequires:	popt-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= %{ver_rpm}
BuildRequires:	zlib-devel
%if %{with static}
BuildRequires:	bzip2-static
BuildRequires:	db-static >= %{ver_db}
BuildRequires:	glibc-static
BuildRequires:	ncurses-static
BuildRequires:	openssl-static
BuildRequires:	pcre-static
BuildRequires:	popt-static
BuildRequires:	readline-static
BuildRequires:	rpm-static
BuildRequires:	zlib-static
%endif
Requires:	db >= %{ver_db}
Requires:	ed
Requires:	rpm >= %{ver_rpm}
Requires:	sed
Requires:	openssl >= 0.9.7c
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
poldek is an RPM package management tool which allows you to easily
perform package verification, installation (including system
installation from scratch), upgrading, and removal.

Program can be used in batch (like apt-get from Debian's APT) or
interactive mode. The interactive mode puts you into a readline
interface with command line autocompletion and history, similar to the
shell mode of Perl's CPAN.

%{?with_static:This version is statically linked.}

%{!?with_imode:This version hasn't got interactive mode.}

%description -l pl
poldek jest narzêdziem linii poleceñ s³u¿±cym do weryfikacji,
instalacji (w³±czaj±c instalacjê systemu od zera), aktualizacji i
usuwania pakietów.

Program mo¿e byæ u¿ywany w trybie wsadowym (jak debianowy apt-get) lub
interaktywnym. Tryb interaktywny posiada interfejs readline z
dope³nianiem komend i histori±, podobny do trybu shell perlowego
modu³u CPAN.

%{?with_static:Ta wersja jest konsolidowana statycznie.}

%{!?with_imode:Ta wersja nie posiada trybu interaktywnego.}

%prep
%setup -q -n %{name}-%{version}-cvs%{snap}

%build
%{__autopoint}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cp -f config.sub trurlib
%configure \
	%{?with_static:--enable-static} \
	%{!?with_imode:--disable-imode} \
	--enable-nls
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf poldek $RPM_BUILD_ROOT%{_bindir}/apoldek-get
ln -sf poldek $RPM_BUILD_ROOT%{_bindir}/ipoldek

%{?with_static:rm -f $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}
sed "s|i686|%{_target_cpu}|g" < %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pld-source.conf

%find_lang %{name}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO conf/*.conf
%dir %{_sysconfdir}/%{name}
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/*.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%attr(755,root,root) %{_libdir}/lib*.so.*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
