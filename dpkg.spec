%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(controllib.pl\\)|perl\\(file\\)'
%else
%define _requires_exceptions perl(controllib.pl)\\|perl(file)
%endif

Summary:	Package maintenance system for Debian Linux
Name:		dpkg
Version:	1.18.4
Release:	2
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://packages.debian.org/unstable/base/dpkg.html
Source0:	ftp://ftp.debian.org/debian/pool/main/d/dpkg/%{name}_%{version}.tar.xz
Source2:	debsign.sh
Source3:	debsign.1
Source4:	dpkg.rpmlintrc
# (tpg) not needed as it got obsoleted by chkconfig implementation
#Patch0:		update-alternatives-1.17.4-mandriva.patch
#Patch1:		dpkg-1.17.10-update-alternatives-use-relative-symlinks.patch
BuildRequires:	flex
BuildRequires:	po4a
BuildRequires:	bzip2-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(zlib)

%description
This package contains the programs dpkg which used to handle the installation
and removal of packages on a Debian system.

In order to unpack and build Debian source packages you will need
to install the developers' package `dpkg-dev' as well as this one.

dpkg-dev is not provided on your %{distribution} system.

%package -n perl-Dpkg
Summary:	Package maintenance system for Debian Linux
Group:		Development/Perl
BuildArch:	noarch

%description -n	perl-Dpkg
This module provides dpkg functionalities.

%prep
%setup -q
%apply_patches

%build
%configure \
	--disable-dselect \
	--disable-update-alternatives \
	--with-admindir=%{_localstatedir}/lib/%{name} \
	--with-zlib \
	--with-bz2 \
	--with-liblzma
%make

%install
%makeinstall_std

install -m755 %{SOURCE2} -D %{buildroot}%{_bindir}/debsign
install -m644 %{SOURCE3} -D %{buildroot}%{_mandir}/man1/debsign.1

%find_lang %{name} dpkg-dev %{name}.lang

%files -f %{name}.lang
%{_bindir}/d*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/parsechangelog
%dir %{_libdir}/%{name}/parsechangelog/debian
%{_sbindir}/*
%dir %{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_datadir}/%{name}/cputable
%{_datadir}/%{name}/ostable
%{_datadir}/%{name}/triplettable
%{_datadir}/dpkg/abitable
%{_datadir}/%{name}/*.mk
%{_localstatedir}/lib/%{name}/*
%dir %{_sysconfdir}/%{name}
%{_mandir}/man1/d*
%{_mandir}/man5/*
%{_mandir}/man8/*
%lang(de) %{_mandir}/de/man?/*
%lang(ja) %{_mandir}/ja/man?/*
%lang(pl) %{_mandir}/pl/man?/*
%lang(sv) %{_mandir}/sv/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(hu) %{_mandir}/hu/man?/*
%lang(it) %{_mandir}/it/man?/*
%lang(es) %{_mandir}/es/man?/*
%{_includedir}/dpkg/*
%{_mandir}/man3/*
%{_libdir}/libdpkg.a
%{_libdir}/pkgconfig/libdpkg.pc

%files -n perl-Dpkg
%{perl_vendorlib}/Dpkg
%{perl_vendorlib}/Dpkg.pm
