#
# Conditional build:
%bcond_with	static	# don't use shared libraries
%bcond_without	imode	# don't build interactive mode
%bcond_with	curl	# link with curl
#
# required versions (forced to avoid SEGV with mixed db used by rpm and poldek)
%define	ver_db	4.3.27-1
%define	ver_rpm	4.3-0.20040107.34
Summary:	RPM packages management helper tool
Summary(pl):	Pomocnicze narzêdzie do zarz±dzania pakietami RPM
Name:		poldek
Version:	0.18.8
Release:	6
License:	GPL v2
Group:		Applications/System
Source0:	http://team.pld.org.pl/~mis/poldek/download/%{name}-%{version}.tar.bz2
# Source0-md5:	f7e2978c7f8b35b0b07d0278dd299881
Source1:	%{name}.conf
Patch0:		%{name}-etc_dir.patch
Patch1:		%{name}-retr_term.patch
Patch2:		%{name}-simplestatic.patch
Patch3:		%{name}-gcc4.patch
Patch4:		%{name}-cookie.patch
URL:		http://team.pld.org.pl/~mis/poldek/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	bzip2-devel
%{?with_curl:BuildRequires:	curl-devel >= 7.8}
BuildRequires:	db-devel >= %{ver_db}
BuildRequires:	gettext-autopoint
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
BuildRequires:	popt-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= %{ver_rpm}
BuildRequires:	zlib-devel
BuildRequires:	perl-tools-pod
%if %{with static}
BuildRequires:	bzip2-static
%{?with_curl:BuildRequires:	curl-static}
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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1

%build
%{__autopoint}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cp -f config.sub trurlib
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

sed "s|%%ARCH%%|%{_ftp_arch}|g" < %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- poldek <= 0.18.3-5
if grep -q '^promoteepoch.*yes' %{_sysconfdir}/poldek.conf ; then
	echo -e ',s:^promoteepoch:# promoteepoch:g\n,w' | ed -s %{_sysconfdir}/poldek.conf
fi

# otherwise don't touch
%ifarch i386 i586 i686 ppc sparc alpha amd64 athlon
%triggerpostun -- poldek <= 0.18.7-1
echo -e ',s://ftp.pld-linux.org://ftp.%{_target_cpu}.ac.pld-linux.org:g\n,w' |\
	ed -s /etc/poldek.conf ||:
%endif

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO *sample* conf/poldekrc*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
