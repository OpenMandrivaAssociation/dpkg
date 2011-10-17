%define _requires_exceptions perl(controllib.pl)\\|perl(file)

Summary:	Package maintenance system for Debian Linux
Name:		dpkg
Version:	1.16.1.1
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://packages.debian.org/unstable/base/dpkg.html
Source0:	ftp://ftp.debian.org/debian/pool/main/d/dpkg/%{name}_%{version}.tar.bz2
Source1:	%{name}-pl-man-pages.tar.bz2
Source2:	debsign.sh
Source3:	debsign.1
Patch3:		gentoo-bug-289094.patch
BuildRequires:	gettext-devel
BuildRequires:	zlib-devel
BuildRequires:	po4a
Provides:	usineagaz = 0.1-0.beta1mdk
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
This package contains the programs dpkg which used to handle the installation
and removal of packages on a Debian system.

In order to unpack and build Debian source packages you will need
to install the developers' package `dpkg-dev' as well as this one.

dpkg-dev is not provided on your Mandriva Linux system.

%package -n	perl-Dpkg
Summary:        Package maintenance system for Debian Linux
Group:          Development/Perl
BuildArch:      noarch

%description -n	perl-Dpkg
This module provides dpkg functionalities.

%prep
%setup -q
%patch3 -p1

%build
%configure2_5x \
    --enable-shared \
    --without-dselect \
    --with-admindir=%{_localstatedir}/lib/%{name}

%make

%install
rm -rf %{buildroot}

%makeinstall_std

bzip2 -dc %{SOURCE1} | tar xf - -C %{buildroot}%{_mandir}
install -m 755 %{SOURCE2} %{buildroot}/%{_bindir}/debsign
install -m 644 %{SOURCE3} %{buildroot}/%{_mandir}/man1

# cleanup
rm -fr %{buildroot}%{_datadir}/locale/en/
rm -fr %{buildroot}%{_sysconfdir}/alternatives
rm -f %{buildroot}%{_bindir}/update-alternatives
rm -f %{buildroot}%{_sbindir}/update-alternatives
rm -fr %{buildroot}/usr/share/doc
find %{buildroot} -name "md5sum*" -exec rm -f {} \;
find %{buildroot}%{_mandir} -name "update-alternatives*" -exec rm -f {} \;

%find_lang %{name}
%find_lang dpkg-dev
cat dpkg-dev.lang >> %{name}.lang

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(0755,root,root) %{_bindir}/d*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/parsechangelog
%attr(0755,root,root) %dir %{_libdir}/%{name}/parsechangelog/debian
%attr(0755,root,root) %{_sbindir}/*
%dir %{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_datadir}/%{name}/cputable
%{_datadir}/%{name}/ostable
%{_datadir}/%{name}/triplettable
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
%lang(es) %{_mandir}/es/man?/*
%{_includedir}/dpkg/*
%{_mandir}/man3/*
%{_libdir}/libdpkg.a
%{_libdir}/pkgconfig/libdpkg.pc

%files -n perl-Dpkg
%defattr(-,root,root)
%{perl_vendorlib}/Dpkg
%{perl_vendorlib}/Dpkg.pm
