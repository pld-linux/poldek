#
# Conditional build:
%bcond_without	imode		# don't build interactive mode
%bcond_without	curl		# don't link curl
%bcond_with	static		# don't use shared libraries
#
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.18.3
Release:	6
License:	GPL v2
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}-%{version}.tar.gz
# Source0-md5:	339c54b86bfd733851c0f7125057f446
Source1:	%{name}.conf
Patch0:		%{name}-retr_term.patch
Patch1:		%{name}-sigsegv.patch
URL:		http://team.pld.org.pl/~mis/poldek/
BuildRequires:	/usr/bin/pod2man
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
%{?with_static:BuildRequires:	bzip2-static}
%{?with_curl:BuildRequires:	curl-devel >= 7.8}
%{?with_curl:%{?with_static:BuildRequires:	curl-static}}
%{?with_static:BuildRequires:  db1-static}
%{?with_static:BuildRequires:  db3-static}
BuildRequires:	openssl-devel >= 0.9.6m
%{?with_static:BuildRequires:	openssl-static}
BuildRequires:	pcre-devel
%{?with_static:BuildRequires:	pcre-static}
BuildRequires:	popt-devel
%{?with_static:BuildRequires:	popt-static}
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 4.0.2-62
%{?with_static:BuildRequires:	rpm-static}
BuildRequires:	zlib-devel
%{?with_static:BuildRequires:	zlib-static}
Requires:	ed
Requires:	rpm >= 4.0.2-62
Requires:	sed
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
instalacji (w³±czaj±c instalacjê systemu od zera), aktualizacji
i usuwania pakietów.

Program mo¿e byæ u¿ywany w trybie wsadowym (jak debianowy apt-get)
lub interaktywnym. Tryb interaktywny posiada interfejs readline
z dope³nianiem komend i histori±, podobny do trybu shell perlowego
modu³u CPAN.

%{?with_static:Ta wersja jest konsolidowana statycznie.}

%{!?with_imode:Ta wersja nie posiada trybu interaktywnego.}

%prep
%setup -q
%patch0 -p1
%patch1 -p0

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
	%{?with_static:--enable-static} \
	%{!?with_imode:--disable-imode} \
	%{?with_curl:--with-curl}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

# no strip cause program's beta stage and core may be useful
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{?with_static:rm -f $RPM_BUILD_ROOT/%{_bindir}/rpmvercmp}
sed "s|%%ARCH%%|%{_target_cpu}|g" < %{SOURCE1} > $RPM_BUILD_ROOT/etc/%{name}.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- poldek <= 0.18.3-4
echo -e ',s://ftp.pld-linux.org://ftp.%{_target_cpu}.ra.pld-linux.org:g\n,w' | ed -s /etc/poldek.conf

%triggerpostun -- poldek <= 0.18.3-1
if ! grep -q promoteepoch /etc/poldek.conf ; then
	echo promoteepoch = yes >>/etc/poldek.conf
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO *sample* conf/poldekrc*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
