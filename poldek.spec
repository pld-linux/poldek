#
# conditional build:
#  --with static	- don't use shared libraries
#  --without imode	- don't build interactive mode
#  --without curl	- don't link curl
#
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.18
Release:	6
License:	GPL v2
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}-%{version}.tar.bz2
Source1:	%{name}.conf
Patch0:		%{name}-vfprogress.patch
Patch1:		%{name}-hold-fix.patch
Patch2:		%{name}-sigsev.patch
URL:		http://team.pld.org.pl/~mis/poldek/
Requires:	rpm >= 4.0.2-62
Requires:	sed
BuildRequires:	bzip2-devel
%{?_with_curl:BuildRequires:	curl-devel >= 7.8}
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	popt-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 4.0.2-62
BuildRequires:	zlib-devel
BuildRequires:	/usr/bin/pod2man
%{?_with_static:BuildRequires:	bzip2-static}
%{?_with_curl:%{?_with_static:BuildRequires:	curl-static}}
%{?_with_static:BuildRequires:	openssl-static}
%{?_with_static:BuildRequires:	pcre-static}
%{?_with_static:BuildRequires:	popt-static}
%{?_with_static:BuildRequires:	rpm-static}
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

%{?_with_static:This version is statically linked.}

%{?_without_imode:This version hasn't got interactive mode.}

%description -l pl
poldek jest narzêdziem linii poleceñ s³u¿±cym do weryfikacji,
instalacji (w³±czaj±c instalacjê systemu od zera), aktualizacji
i usuwania pakietów.

Program mo¿e byæ u¿ywany w trybie wsadowym (jak debianowy apt-get)
lub interaktywnym. Tryb interaktywny posiada interfejs readline
z dope³nianiem komend i histori±, podobny do trybu shell perlowego
modu³u CPAN.

%{?_with_static:Ta wersja jest konsolidowana statycznie.}

%{?_without_imode:Ta wersja nie posiada trybu interaktywnego.}

%prep
%setup -q
%patch0 -p0
%patch1 -p0 
%patch2 -p0

%build
if ! grep -q AM_GNU_GETTEXT_VERSION configure.in ; then
	cp configure.in configure.in.orig
	sed -e 's/AM_GNU_GETTEXT\(.*\)/AM_GNU_GETTEXT\1\
AM_GNU_GETTEXT_VERSION(0.10.40)/' \
		-e 's=po/Makefile.in=po/Makefile.in intl/Makefile=' \
		configure.in.orig >configure.in
	autopoint --force
fi
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{?_with_static:--enable-static} \
	%{?_without_imode:--disable-imode} \
	%{?_with_curl:--with-curl}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

# no strip cause program's beta stage and core may be useful
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{?_with_static:rm -f $RPM_BUILD_ROOT/%{_bindir}/rpmvercmp}
sed "s|/i686/|/%{_target_cpu}/|g" < %{SOURCE1} > $RPM_BUILD_ROOT/etc/%{name}.conf

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
