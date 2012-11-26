#
# Conditional build:
%bcond_with	static	# don't use shared libraries
%bcond_without	imode	# don't build interactive mode
%bcond_without	python	# don't build python bindings
%bcond_with	snap	# install configs for official Th snapshot

# current snapshot name
%define		SNAP	2012

# required versions (forced to avoid SEGV with mixed db used by rpm and poldek)
%define		ver_db		5.2
%define		ver_db_rel	3
%define		ver_rpm		5.4.10

%define		snap	rc6
%define		rel	4%{?with_snap:.%{SNAP}}
Summary:	RPM packages management helper tool
Summary(hu.UTF-8):	RPM csomagkezelést segítő eszköz
Summary(pl.UTF-8):	Pomocnicze narzędzie do zarządzania pakietami RPM
Name:		poldek
Version:	0.30
Release:	1.%{snap}.%{rel}
License:	GPL v2
Group:		Applications/System
#Source0:	http://poldek.pld-linux.org/download/snapshots/%{name}-%{version}-cvs%{snap}.tar.bz2
Source0:	http://carme.pld-linux.org/~megabajt/snaps/poldek/%{name}-%{version}%{snap}.tar.xz
# Source0-md5:	4b528ad356b02efdd72b81f1ecaceb83
Source1:	%{name}.conf
Source2:	%{name}-multilib.conf
Source5:	%{name}-aliases.conf
Source6:	%{name}.desktop
Source7:	%{name}.png
Source8:	%{name}-debuginfo.conf
Source9:	%{name}-aidath.conf
Source10:	%{name}-multilib-aidath.conf
Source11:	%{name}-archive.conf
Source100:	%{name}-snap.conf
Source101:	%{name}-multilib-snap.conf
Source102:	%{name}-debuginfo-snap.conf
Patch0:		%{name}-vserver-packages.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-size-type.patch
Patch3:		%{name}-Os-fail-workaround.patch
Patch4:		%{name}-link-rpmio.patch
Patch5:		%{name}-vrpmlog.patch
Patch6:		%{name}-git.patch
Patch7:		%{name}-db52.patch
URL:		http://poldek.pld-linux.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	check-devel
BuildRequires:	db-devel >= %{ver_db}-%{ver_db_rel}
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	neon-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_python:BuildRequires:	python-devel}
BuildRequires:	readline-devel >= 5.0
BuildRequires:	rpm-devel >= %{ver_rpm}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	swig-python
BuildRequires:	xmlto
BuildRequires:	zlib-devel
%if %{with static}
BuildRequires:	bzip2-static
BuildRequires:	db-static >= %{ver_db}-%{ver_db_rel}
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
Requires:	db >= %{ver_db}-%{ver_db_rel}
Requires:	rpm >= %{ver_rpm}
Requires:	rpm-db-ver = %{ver_db}
#Requires:	rpm-lib = %(rpm -q --qf '%{V}' rpm-lib)
Requires:	rpm-lib >= 5.4.10
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

%description -l hu.UTF-8
poldek egy RPM csomagkezelő eszköz, amely megkönnyíti a
csomagellenőrzést, telepítést (beleértve a rendszertelepítést a
nulláról), frissítést és eltávolítást.

A program használható parancssorból (mint a Debian apt-get programja)
vagy interaktív módban. Az interaktív mód egy readline környezetet
jelent, parancskiegészítéssel és előzményekkel, hasonlóan a Perl CPAN
shell módjához.

%{?with_static:Ez a verzió statikusan linkelt.}

%{!?with_imode:Ennek a verziónak nincs interaktív módja.}

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
Summary(hu.UTF-8):	A poldek könyvtárai
Summary(pl.UTF-8):	Biblioteki poldka
Group:		Libraries

%description libs
poldek libraries.

%description libs -l hu.UTF-8
A poldek könyvtárai.

%description libs -l pl.UTF-8
Biblioteki poldka.

%package devel
Summary:	Header files for poldek libraries
Summary(hu.UTF-8):	A poldek könyvtár fejlesztői fájljai
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek poldka
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rpm-devel >= %{ver_rpm}

%description devel
Header files for poldek libraries.

%description devel -l hu.UTF-8
A poldek könyvtár fejlesztői fájljai.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek poldka.

%package static
Summary:	poldek static libraries
Summary(hu.UTF-8):	poldek statikus könyvtárak
Summary(pl.UTF-8):	Biblioteki statyczne poldka
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
poldek static libraries.

%description static -l hu.UTF-8
poldek statikus könyvtárak.

%description static -l pl.UTF-8
Biblioteki statyczne poldka.

%package -n python-poldek
Summary:	Python modules for poldek
Summary(hu.UTF-8):	Python modulok poldek-hez
Summary(pl.UTF-8):	Moduły języka Python dla poldka
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-poldek
Python modules for poldek.

%description -n python-poldek -l hu.UTF-8
Python modulok poldek-hez.

%description -n python-poldek -l pl.UTF-8
Moduły języka Python dla poldka.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{__rm} m4/libtool.m4 m4/lt*.m4

# cleanup backups after patching
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f
chmod u+x ./configure ./doc/conf-xml2.sh

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
cd tndb
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ../trurlib
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ..

CPPFLAGS="%{rpmcppflags} -std=gnu99"
%configure \
	%{?with_static:--enable-static --disable-shared} \
	%{!?with_imode:--disable-imode} \
	--enable-nls \
	%{?with_python:--with-python}
%{__make} -j1
#	--enable-trace

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}/repos.d,/var/cache/%{name}}

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%{__make} -C python -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{py_sitedir}
%endif

%{?with_static:%{__rm} $RPM_BUILD_ROOT%{_bindir}/rpmvercmp}

%ifarch i486 i686 ppc sparc alpha athlon
	%define		_ftp_arch	%{_target_cpu}
%endif
%ifarch %{x8664}
	%define		_ftp_arch	x86_64
	%define		_ftp_alt_arch	i686
%endif
%ifarch i586
	%define		_ftp_arch	i486
%endif
%ifarch pentium2 pentium3 pentium4
	%define		_ftp_arch	i686
%endif
%ifarch sparcv9 sparc64
	%define		_ftp_arch	sparc
	%define		_ftp_arch	%{_target_cpu}
	%ifarch sparc64
		%define		_ftp_alt_arch	sparcv9
	%endif
%endif

%define	pld_conf %{SOURCE1}
%define	pld_debuginfo_conf %{SOURCE8}
%define	pld_archive_conf %{SOURCE11}

%ifarch %{x8664}
	%define	pld_multilib_conf %{SOURCE2}
%endif

# aidath
%ifarch sparcv9 sparc64
	%define	pld_conf %{SOURCE9}
	%undefine pld_archive_conf
%endif
%ifarch sparc64
	%define pld_multilib_conf %{SOURCE10}
%endif

%{__sed} -e 's|%%ARCH%%|%{_ftp_arch}|g' < %{pld_conf} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld.conf

%if 0%{?pld_multilib_conf:1}
	%{__sed} 's|%%ARCH%%|%{_ftp_alt_arch}|g' < %{pld_multilib_conf} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-multilib.conf
%endif

%if 0%{?pld_debuginfo_conf:1}
%{__sed} -e 's|%%ARCH%%|%{_ftp_arch}|g' < %{pld_debuginfo_conf} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-debuginfo.conf
%endif

%if 0%{?pld_archive_conf:1}
%{__sed} -e 's|%%ARCH%%|%{_ftp_arch}|g' < %{pld_archive_conf} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-archive.conf
%endif

# Always install snapshot configs
%{__sed} -e 's|%%ARCH%%|%{_ftp_arch}|g' \
	-e 's|%%SNAP%%|%{SNAP}|g' < %{SOURCE100} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-%{SNAP}.conf
%{__sed} -e 's|%%ARCH%%|%{_ftp_arch}|g' \
	-e 's|%%SNAP%%|%{SNAP}|g' < %{SOURCE102} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-%{SNAP}-debuginfo.conf
%ifarch %{x8664}
	%{__sed} -e 's|%%ARCH%%|%{_ftp_alt_arch}|g' \
		-e 's|%%SNAP%%|%{SNAP}|g' < %{SOURCE101} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-%{SNAP}-multilib.conf
%endif

%if %{with snap}
%{__sed} -i -e 's|@@SNAP@@||g' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld.conf
%{__sed} -i '/@@SNAP@@.*/d' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-%{SNAP}.conf
%else
%{__sed} -i -e 's|@@SNAP@@||g' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld-%{SNAP}.conf
%{__sed} -i '/@@SNAP@@.*/d' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld.conf
%endif

cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/cli.conf

%if %{with imode}
# add desktop file and icon
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p %{SOURCE7} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
%endif

# sources we don't package
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{rh,fedora,centos}-source.conf
# include them in %doc
%{__rm} -rf configs
cp -a conf configs
%{__rm} -f configs/Makefile*

%if %{with python}
%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_poldekmod.la
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "1" ]; then
	# remove ignore = vserver-packages inside vserver on first install
	{
		while read f ctx; do
			[ "$f" = "VxID:" -o "$f" = "s_context:" ] && break
		done </proc/self/status
	} 2>/dev/null
	if [ -z "$ctx" -o "$ctx" = "0" ]; then
		VSERVER=no
	else
		VSERVER=yes
	fi
	if [ "$VSERVER" = "yes" ]; then
		%{__sed} -i -e '/^ignore/s/vserver-packages//' %{_sysconfdir}/%{name}/poldek.conf
	fi
fi

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
		%{__sed} -i -e "/^#hold =/s/^.*/$hold/" /etc/poldek/poldek.conf
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
%doc ChangeLog README* NEWS TODO configs
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/repos.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/repos.d/*.conf
%attr(755,root,root) %{_bindir}/ipoldek
%attr(755,root,root) %{_bindir}/poldek
%attr(755,root,root) %{_bindir}/rpmvercmp
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_mandir}/man1/%{name}*.1*
%lang(pl) %{_mandir}/pl/man1/%{name}*
%{_infodir}/poldek.info*
%if %{with imode}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%endif
%dir /var/cache/%{name}

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
%if %{without static}
%attr(755,root,root) %{_libdir}/libpoclidek.so
%attr(755,root,root) %{_libdir}/libpoldek.so
%attr(755,root,root) %{_libdir}/libtndb.so
%attr(755,root,root) %{_libdir}/libtrurl.so
%attr(755,root,root) %{_libdir}/libvfile.so
%endif
%{_libdir}/libpoclidek.la
%{_libdir}/libpoldek.la
%{_libdir}/libtndb.la
%{_libdir}/libtrurl.la
%{_libdir}/libvfile.la
%{_includedir}/poldek
%{_includedir}/tndb
%{_includedir}/trurl
%{_includedir}/vfile
%{_pkgconfigdir}/tndb.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtndb.a
%{_libdir}/libtrurl.a

%if %{with python}
%files -n python-poldek
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_poldekmod.so
%{py_sitescriptdir}/poldek.py[co]
%{py_sitescriptdir}/poldekmod.py[co]
%endif
