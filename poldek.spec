#
# Conditional build:
%bcond_with	static	# don't use shared libraries
%bcond_without	imode	# don't build interactive mode
%bcond_without	python	# don't build python bindings
#
# required versions (forced to avoid SEGV with mixed db used by rpm and poldek)
%define	ver_db	4.3.27-1
%define	ver_rpm	4.4.9-56
#
%define		snap	20080519.22
%define		rel		1
Summary:	RPM packages management helper tool
Summary(pl.UTF-8):	Pomocnicze narzędzie do zarządzania pakietami RPM
Name:		poldek
Version:	0.30
Release:	0.%{snap}.%{rel}
License:	GPL v2
Group:		Applications/System
#Source0:	http://poldek.pld-linux.org/download/snapshots/%{name}-%{version}-cvs%{snap}.tar.bz2
Source0:	%{name}-%{version}-cvs%{snap}.tar.bz2
# Source0-md5:	41c50bb17f8ac2b50d8838c8a346d0ec
Source1:	%{name}.conf
Source2:	%{name}-multilib.conf
Source3:	%{name}-ti.conf
Source4:	%{name}-multilib-ti.conf
Source5:	%{name}-aliases.conf
Source6:	%{name}.desktop
Source7:	%{name}.png
Patch0:		%{name}-vserver-packages.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-abort-on-upgrade.patch
URL:		http://poldek.pld-linux.org/
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
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_python:BuildRequires:	python-devel}
BuildRequires:	readline-devel >= 5.0
BuildRequires:	rpm-devel >= %{ver_rpm}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	xmlto
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
Requires(triggerpostun):	awk
Requires(triggerpostun):	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	db >= %{ver_db}
Requires:	rpm >= %{ver_rpm}
Requires:	rpm-lib = %(rpm -q --qf '%{V}' rpm-lib)
# vf* scripts use sed
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
#'vim

%description -l pl.UTF-8
poldek jest narzędziem linii poleceń służącym do weryfikacji,
instalacji (włączając instalację systemu od zera), aktualizacji i
usuwania pakietów.

Program może być używany w trybie wsadowym (jak debianowy apt-get) lub
interaktywnym. Tryb interaktywny posiada interfejs readline z
dopełnianiem komend i historią, podobny do trybu shell perlowego
modułu CPAN.

%{?with_static:Ta wersja jest konsolidowana statycznie.}

%{!?with_imode:Ta wersja nie posiada trybu interaktywnego.}

%package libs
Summary:	poldek libraries
Summary(pl.UTF-8):	Biblioteki poldka
Group:		Libraries

%description libs
poldek libraries.

%description libs -l pl.UTF-8
Biblioteki poldka.

%package devel
Summary:	Header files for poldek libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek poldka
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for poldek libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek poldka.

%package static
Summary:	poldek static libraries
Summary(pl.UTF-8):	Biblioteki statyczne poldka
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
poldek static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne poldka.

%package -n python-poldek
Summary:	Python modules for poldek
Summary(pl.UTF-8):	Moduły języka Python dla poldka
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-poldek
Python modules for poldek.

%description -n python-poldek -l pl.UTF-8
Moduły języka Python dla poldka.

%prep
%setup -q -n %{name}-%{version}%{?snap:-cvs%{snap}}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# cleanup backups after patching
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%{__autopoint}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
cp -f config.sub trurlib

CPPFLAGS="-std=gnu99"
%configure \
	%{?with_static:--enable-static --disable-shared} \
	%{!?with_imode:--disable-imode} \
	--enable-nls \
	%{?with_python:--with-python}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%{__make} -C python install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{py_sitedir}
%endif

%{?with_static:rm -f $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}

%ifarch i486 i686 ppc sparc alpha athlon
%define		_ftp_arch	%{_target_cpu}
%endif
%ifarch %{x8664}
%define		_ftp_arch	x86_64
%define		_ftp_alt_arch	i686
%endif
%ifarch i586
%if "%{pld_release}" == "ti"
%define		_ftp_arch	i586
%else
%define		_ftp_arch	i486
%endif
%endif
%ifarch pentium2 pentium3 pentium4
%define		_ftp_arch	i686
%endif
%ifarch sparcv9 sparc64
%define		_ftp_arch	sparc
%endif

%{?with_static:rm -f $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}

%if "%{pld_release}" == "ti"
sed -e '
	s|%%ARCH%%|%{_ftp_arch}|g
' < %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld.conf

%ifarch %{x8664}
sed '
	s|%%ARCH%%|%{_ftp_alt_arch}|g
' < %{SOURCE4} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-multilib.conf
%endif
%else
sed -e '
	s|%%ARCH%%|%{_ftp_arch}|g
' < %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld.conf

%ifarch %{x8664}
sed '
	s|%%ARCH%%|%{_ftp_alt_arch}|g
' < %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-multilib.conf
%endif
%endif

install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/aliases.conf

%if %{with imode}
# add desktop file and icon
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
install %{SOURCE6} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
install %{SOURCE7} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
%endif

# sources we don't package
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{rh,pld,fedora,centos}-source.conf
# include them in %doc
rm -rf configs
cp -a conf configs
rm -f configs/Makefile*

%if %{with python}
%py_postclean
rm -f $RPM_BUILD_ROOT%{py_sitedir}/_poldekmod.la
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%triggerpostun -- poldek < 0.19.0-1.20050613.22.0
if [ -f /etc/poldek.conf.rpmsave ]; then
	awk '/^source/ {
	name = $3;
	path = $4;
	auto = "yes";
	autoup = "yes";
	type = "pdir";
	pri = "";

	if (sub(",noauto", "", name)) {
		auto = "no";
	}

	# process pri=\d+
	if (match(name, /,pri=[0-9]+/)) {
		pri = substr(name, RSTART + 5, RLENGTH - 5);
		name = substr(name, 1, RSTART - 1) substr(name, RSTART + RLENGTH);
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
		if (pri) {
			print "pri = " pri;
		}
	}

	}' < /etc/poldek.conf.rpmsave >> /etc/poldek/source.conf
	echo "Converted old custom sources from /etc/poldek.conf.rpmsave to new poldek format in /etc/poldek/source.conf"

	# copy hold=
	hold=$(grep ^hold /etc/poldek.conf.rpmsave)
	if [ "$hold" ]; then
		sed -i -e "/^#hold =/s/^.*/$hold/" /etc/poldek/poldek.conf
	fi
fi

%triggerpostun -- poldek < 0.30-0.20080225.00.1
if ! grep -q '^%%includedir repos.d' %{_sysconfdir}/%{name}/poldek.conf; then
	%{__sed} -i -e '/^%%include source.conf/{
		a
		a# /etc/poldek/repos.d/*.conf
		a%%includedir repos.d
	}' %{_sysconfdir}/%{name}/poldek.conf
fi

%{__sed} -i -e '/%%include %%{_distro}-source.conf/d' %{_sysconfdir}/%{name}/poldek.conf
%{__sed} -i -e '/%%include %%{_distro}-multilib-source.conf/d' %{_sysconfdir}/%{name}/poldek.conf

if [ -f %{_sysconfdir}/%{name}/pld-source.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/%{name}/repos.d/pld.conf{,.rpmnew}
	cp -f %{_sysconfdir}/%{name}/pld-source.conf.rpmsave %{_sysconfdir}/%{name}/repos.d/pld.conf
fi

%ifarch %{x8664}
if [ -f %{_sysconfdir}/%{name}/pld-multilib-source.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/%{name}/repos.d/pld-multilib.conf{,.rpmnew}
	cp -f %{_sysconfdir}/%{name}/pld-multilib-source.conf.rpmsave %{_sysconfdir}/%{name}/repos.d/pld-multilib.conf
fi
%endif

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO configs
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/repos.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/repos.d/*.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
%{_infodir}/poldek.info*
%if %{with imode}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%endif

%if %{without static}
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpoclidek.so.*.*.*
%attr(755,root,root) %{_libdir}/libpoldek.so.*.*.*
%attr(755,root,root) %{_libdir}/libtndb.so.*.*.*
%attr(755,root,root) %{_libdir}/libtrurl.so.*.*.*
%attr(755,root,root) %{_libdir}/libvfile.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpoclidek.so.0
%attr(755,root,root) %ghost %{_libdir}/libpoldek.so.2
%attr(755,root,root) %ghost %{_libdir}/libtndb.so.0
%attr(755,root,root) %ghost %{_libdir}/libtrurl.so.0
%attr(755,root,root) %ghost %{_libdir}/libvfile.so.0
%endif

%files devel
%defattr(644,root,root,755)
%{!?with_static:%attr(755,root,root) %{_libdir}/lib*.so}
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with python}
%files -n python-poldek
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_poldekmod.so
%{py_sitescriptdir}/poldek.py[co]
%{py_sitescriptdir}/poldekmod.py[co]
%endif
