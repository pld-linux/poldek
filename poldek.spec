#
# Conditional build:
%bcond_with	static	# don't use shared libraries
%bcond_without	imode	# don't build interactive mode
%bcond_with	curl	# link with curl
#
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.18.1
Release:	13
License:	GPL v2
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}-%{version}.tar.bz2
# Source0-md5:	8af8090d401254939911e456e2f09e60
Source1:	%{name}.conf
Patch0:		%{name}-static.patch
Patch1:		%{name}-etc_dir.patch
Patch2:		%{name}-rpm4.2.patch
Patch3:		%{name}-rpm4.1-fix.patch
Patch4:		%{name}-retr_term.patch
Patch5:		%{name}-deps-fix.patch
Patch6:		%{name}-broken-rpmdb.patch
Patch7:		%{name}-epoch0.patch
URL:		http://team.pld.org.pl/~mis/poldek/
BuildRequires:	bzip2-devel
%{?with_curl:BuildRequires:	curl-devel >= 7.8}
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	gettext-autopoint
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	pcre-devel
BuildRequires:	popt-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 4.2.1
BuildRequires:	zlib-devel
BuildRequires:	/usr/bin/pod2man
%{?with_static:BuildRequires:	bzip2-static}
%{?with_curl:%{?with_static:BuildRequires:	curl-static}}
%{?with_static:BuildRequires:	ncurses-static}
%{?with_static:BuildRequires:	openssl-static}
%{?with_static:BuildRequires:	pcre-static}
%{?with_static:BuildRequires:	popt-static}
%{?with_static:BuildRequires:	readline-static}
%{?with_static:BuildRequires:	rpm-static}
%{?with_static:BuildRequires:	zlib-static}
%{?with_static:BuildRequires:	glibc-static}
Requires:	rpm >= 4.2.1
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
%setup -q
%patch0	-p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p1

%build
%{__autopoint}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{?with_static:--enable-static} \
	%{!?with_imode:--disable-imode} \
	%{?with_curl:--with-curl}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_static:rm -f $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}
sed "s|/i686/|/%{_target_cpu}/|g" < %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO *sample* conf/poldekrc*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
