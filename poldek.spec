#
# Conditional build:
%bcond_with	static	# don't use shared libraries
%bcond_without	imode	# don't build interactive mode
#
# required versions (forced to avoid SEGV with mixed db used by rpm and poldek)
%define	ver_db	4.2.50-1
%define	ver_rpm	4.4.1
%define	snap	20050613.22
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.19.0
Release:	1.%{snap}.0
License:	GPL v2
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/snapshots/%{name}-%{version}-cvs%{snap}.tar.bz2
# Source0-md5:	d529239d781c3d9e36577305d46d1a37
Source1:	%{name}.conf
Patch0:		%{name}-prereq.patch
URL:		http://team.pld.org.pl/~mis/poldek/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	bzip2-devel
BuildRequires:	db-devel >= %{ver_db}
BuildRequires:	gettext-autopoint
BuildRequires:	home-etc-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
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
BuildRequires:	libselinux-static
BuildRequires:	ncurses-static
BuildRequires:	openssl-static
BuildRequires:	pcre-static
BuildRequires:	popt-static
BuildRequires:	readline-static
BuildRequires:	rpm-static
BuildRequires:	zlib-static
%endif
Requires(triggerpostun):	sed >= 4.0
Requires:	db >= %{ver_db}
Requires:	openssl >= 0.9.7d
Requires:	rpm >= %{ver_rpm}
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

#'

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

%package libs
Summary:        poldek library
Summary(pl):    Biblioteki poldka
Group:          Libraries

%description libs
poldek library.

%description libs -l pl
Biblioteki poldka.

%package devel
Summary:        Header files for poldek libraries
Summary(pl):    Pliki nag³ówkowe bibliotek poldka
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description devel
Header files for poldek libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek poldka.

%package static
Summary:        poldek static libraries
Summary(pl):    Biblioteki statyczne poldka
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
poldek static libraries.

%description static -l pl
Biblioteki statyczne poldka.

%prep
%setup -q -n %{name}-%{version}-cvs%{snap}
%patch0 -p1

%build
%{__autopoint}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cp -f config.sub trurlib
# glibc 2.3.5 workaround (to be removed when new snap come)
perl -pi -e 's|HAVE_FOPENCOOKIE|HAVE_FOPENCOOKIE_XXX|g' trurlib/nstream.c

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

%{?with_static:rm -f $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}

#
# CHANGE IT WHEN SWITCHING poldek.conf FROM AC TO TH !!!
#
%ifarch i386 i586 i686 ppc sparc alpha amd64 athlon
%define		_ftp_arch	%{_target_cpu}
%else
%ifarch i486
%define		_ftp_arch	i386
%else
%ifarch pentium2 pentium3 pentium4
%define		_ftp_arch	i686
%else
%ifarch sparcv9 sparc64
%define		_ftp_arch	sparc
%endif
%endif
%endif
%endif

%{?with_static:rm -f $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}
sed "s|%%ARCH%%|%{_ftp_arch}|g" < %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pld-source.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%triggerpostun -- poldek <= 0.18.3-5
sed -i -e '/^promoteepoch:.*yes/s/^/#/' %{_sysconfdir}/poldek.conf

# otherwise don't touch
%ifarch i386 i586 i686 ppc sparc alpha amd64 athlon
%triggerpostun -- poldek <= 0.18.7-1
sed -i -e 's://ftp.pld-linux.org://ftp.ac.pld-linux.org:g' /etc/poldek.conf
%endif

%triggerpostun -- poldek < 0.19.0-1.20050613.22.0
if [ -f /etc/poldek.conf.rpmsave ]; then
	awk '/^source/ {
	name = $3;
	path = $4;
	auto = "yes";
	autoup = "yes";
	type = "pdir";

	if (sub(",noauto", "", name)) {
		auto = "no";
	}

	# skip ac sources. already in new config.
	if (name !~ /^ac(-(ready|test|supported|updates-(general|security)))?$/) {
		print "[source]";
		print "name = " name;
		print "type = " type;
		print "path = " path;
		print "auto = " auto;
		print "autoup = " autoup;
		print "";
	}

	}' < /etc/poldek.conf.rpmsave >> /etc/poldek/source.conf
#	mv -f /etc/poldek.conf.rpmsave /etc/poldek.conf.converted.rpmsave
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO conf/*.conf
%dir %{_sysconfdir}/%{name}
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/*.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
%{_infodir}/poldek.info*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
