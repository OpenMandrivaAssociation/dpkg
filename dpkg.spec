%global __requires_exclude perl\\((extra|file|in|--format)\\)

Summary:	Package maintenance system for Debian Linux
Name:		dpkg
Version:	1.21.22
Release:	1
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		https://packages.debian.org/unstable/base/dpkg.html
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
BuildRequires:	pkgconfig(libmd)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	gnutar

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
%autopatch -p1

%build
%configure \
	--disable-dselect \
	--disable-update-alternatives \
	--with-admindir=%{_localstatedir}/lib/%{name} \
	--with-zlib \
	--with-bz2 \
	--with-liblzma
%make_build

%install
%make_install

install -m755 %{SOURCE2} -D %{buildroot}%{_bindir}/debsign
install -m644 %{SOURCE3} -D %{buildroot}%{_mandir}/man1/debsign.1

%find_lang %{name} dpkg-dev %{name}.lang

%files -f %{name}.lang
%doc %{_docdir}/dpkg/*
%{_bindir}/*
#dir #{_libdir}/%{name}
#dir #{_libdir}/%{name}/parsechangelog
#{_libdir}/%{name}/parsechangelog/debian
%dir %{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_datadir}/%{name}/cputable
%{_datadir}/%{name}/ostable
#{_datadir}/%{name}/triplettable
%{_datadir}/dpkg/abitable
%{_datadir}/%{name}/no-pie-compile.specs
%{_datadir}/%{name}/no-pie-link.specs
%{_datadir}/%{name}/pie-compile.specs
%{_datadir}/%{name}/pie-link.specs
%{_datadir}/%{name}/tupletable
%{_datadir}/%{name}/*.mk
%{_datadir}/aclocal/*
%{_datadir}/dpkg/sh/dpkg-error.sh
%{_datadir}/zsh/vendor-completions/_dpkg-parsechangelog
%{_localstatedir}/lib/%{name}/*
%dir %{_sysconfdir}/%{name}
%{_libexecdir}/dpkg/dpkg-db-backup
%lang(de) %{_mandir}/de/man?/*
%lang(ja) %{_mandir}/ja/man?/*
%lang(pl) %{_mandir}/pl/man?/*
%lang(pt) %{_mandir}/pt/man?/*
%lang(sv) %{_mandir}/sv/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(hu) %{_mandir}/hu/man?/*
%lang(it) %{_mandir}/it/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(nl) %{_mandir}/nl/man?/*
%{_includedir}/dpkg/*
%{_mandir}/man*/*
%{_libdir}/libdpkg.a
%{_libdir}/pkgconfig/libdpkg.pc

%files -n perl-Dpkg
%{_datadir}/perl5/vendor_perl/Dpkg*
