Summary:	RPM packages management helper tool
Name:		poldek
Version:	0.1
Release:	1
License:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source:		%{name}-%{version}.tar.gz
Requires:	/bin/rpm
BuildRequires:  db3-devel >= 3.1.14-2
BuildRequires:	rpm-devel >= 3.0.5
BuildRequires:	zlib-devel, zlib-static
BuildRequires:	bzip2-devel, bzip2-static
BuildRequires:	/usr/bin/pod2man
BuildRequires:  trurlib-devel >= 0.42
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
poldek is a cmdline tool which can be used to verify, install and
upgrade given package sets. 

%prep 
%setup -q 

%build
make CFLAGS="$RPM_OPT_FLAGS" all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

# no strip cause program's alpha stage and core may be useful
make install DESTDIR=$RPM_BUILD_ROOT%{_prefix}

gzip -9nf README* *sample* poldek.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%doc README* *sample*
