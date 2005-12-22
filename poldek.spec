#
# Conditional build:
%bcond_with	static	# don't use shared libraries
%bcond_without	imode	# don't build interactive mode
#
# required versions (forced to avoid SEGV with mixed db used by rpm and poldek)
%define	ver_db	4.2.50-1
%define	ver_rpm	4.4.1
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.20
Release:	3
License:	GPL v2
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}-%{version}.tar.bz2
# Source0-md5:	61c0c03ee4a9de36339fc943b6901266
Source1:	%{name}.conf
Source2:	%{name}-multilib.conf
Source3:	%{name}-aliases.conf
Patch0:		%{name}-cvs-fixes.patch
Patch1:		%{name}-ask-abort.patch
Patch2:		%{name}-obsoletes.patch
Patch3:		%{name}-completion.patch
Patch4:		%{name}-notimestamps.patch
URL:		http://team.pld.org.pl/~mis/poldek/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	check
BuildRequires:	db-devel >= %{ver_db}
BuildRequires:	gettext-autopoint
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
BuildRequires:	perl-tools-pod
BuildRequires:	popt-devel
BuildRequires:	readline-devel >= 5.0
BuildRequires:	rpm-devel >= %{ver_rpm}
BuildRequires:	zlib-devel
%if %{with static}
BuildRequires:	bzip2-static
BuildRequires:	db-static >= %{ver_db}
BuildRequires:	glibc-static
BuildRequires:	libselinux-static
BuildRequires:	libxml2-static
BuildRequires:	ncurses-static
BuildRequires:	openssl-static
BuildRequires:	pcre-static
BuildRequires:	popt-static
BuildRequires:	readline-static
BuildRequires:	rpm-static
BuildRequires:	zlib-static
%endif
Requires(triggerpostun):	sed >= 4.0
Requires(triggerpostun):	awk
Requires:       %{name}-libs = %{version}-%{release}
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
Summary:        poldek libraries
Summary(pl):    Biblioteki poldka
Group:          Libraries

%description libs
poldek libraries.

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
%setup -q
%patch0 -p2
%patch1 -p0
%patch2 -p0
%patch3 -p2
%patch4 -p1

%build
%{__autopoint}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cp -f config.sub trurlib

%configure \
	%{?with_static:--enable-static --disable-shared} \
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
%ifarch i386 i586 i686 ppc sparc alpha athlon
%define		_ftp_arch	%{_target_cpu}
%else
%ifarch %{x8664}
%define		_ftp_arch	amd64
%define		_ftp_alt_arch	i686
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
%endif

%{?with_static:rm -f $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}

sed -e "s|%%ARCH%%|%{_ftp_arch}|g" \
%ifarch %{x8664}
	-e "s|%%ALT_ARCH%%|%{_ftp_alt_arch}|g" \
%else
	-e '/%%ALT_ARCH%%/d' \
%endif
	< %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pld-source.conf

%ifarch %{x8664}
sed "s|%%ARCH%%|%{_ftp_alt_arch}|g" < %{SOURCE2} >> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pld-source.conf
%endif

install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/aliases.conf

# get rid of non-pld sources
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{rh,fedora}-source.conf
# include them in %doc
rm -rf configs
cp -a conf configs
rm -f configs/Makefile*

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
if [ -f /etc/poldek.conf ]; then
	sed -i -e '/^promoteepoch:.*yes/s/^/#/' /etc/poldek.conf
fi

# otherwise don't touch
%ifarch i386 i586 i686 ppc sparc alpha amd64 athlon
%triggerpostun -- poldek <= 0.18.7-1
if [ -f /etc/poldek.conf ]; then
	sed -i -e 's://ftp.pld-linux.org://ftp.ac.pld-linux.org:g' /etc/poldek.conf
fi
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
		print "";
		print "[source]";
		print "name = " name;
		print "type = " type;
		print "path = " path;
		print "auto = " auto;
		print "autoup = " autoup;
	}

	}' < /etc/poldek.conf.rpmsave >> /etc/poldek/source.conf
	echo "Converted old custom sources from /etc/poldek.conf.rpmsave to new poldek format in /etc/poldek/source.conf"

	# copy hold=
	hold=$(grep ^hold /etc/poldek.conf.rpmsave)
	if [ "$hold" ]; then
		sed -i -e "/^#hold =/s/^.*/$hold/" /etc/poldek/poldek.conf
	fi
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO configs/
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}/*.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
%{_infodir}/poldek.info*

%if %{without static}
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%endif

%files devel
%defattr(644,root,root,755)
%{!?with_static:%attr(755,root,root) %{_libdir}/lib*.so}
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
