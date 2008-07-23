Summary:	Package maintenance system for Debian Linux
Name:		dpkg
Version:	1.13.11
Release:	%mkrel 4
License:	GPL
Group:		System/Configuration/Packaging
Url:		http://packages.debian.org/unstable/base/dpkg.html
Source0:	ftp://ftp.debian.org/debian/pool/main/d/dpkg/%{name}_%{version}.tar.bz2
Source1:	%{name}-pl-man-pages.tar.bz2
BuildRequires:	gettext-devel
BuildRequires:	zlib-devel
Provides:	usineagaz = 0.1-0.beta1mdk
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%define _requires_exceptions perl(controllib.pl)\\|perl(file)

%description
This package contains the programs dpkg which used to handle the installation
and removal of packages on a Debian system.

In order to unpack and build Debian source packages you will need
to install the developers' package `dpkg-dev' as well as this one.

dpkg-dev is not provided on your Mandriva Linux system.

%prep

%setup -q

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

# cleanup
rm -fr %{buildroot}%{_datadir}/locale/en/
rm -fr %{buildroot}%{_sysconfdir}/alternatives
rm -f %{buildroot}%{_sbindir}/update-alternatives
rm -fr %{buildroot}/usr/share/doc
find %{buildroot} -name "md5sum*" -exec rm -f {} \;
find %{buildroot}%{_mandir} -name "update-alternatives*" -exec rm -f {} \;

%find_lang %name

%clean
rm -rf %{buildroot}

%files -f dpkg.lang
%defattr(644,root,root,755)
%attr(0755,root,root) %{_bindir}/822-date
%attr(0755,root,root) %{_bindir}/dpkg*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/methods
%dir %{_libdir}/%{name}/parsechangelog
%dir %{_libdir}/%{name}/methods/disk
%dir %{_libdir}/%{name}/methods/floppy
%{_libdir}/%{name}/controllib.pl
%{_libdir}/%{name}/enoent
%attr(0755,root,root) %{_libdir}/%{name}/mksplit
%dir %{_libdir}/%{name}/methods/*/desc*
%dir %{_libdir}/%{name}/methods/*/names
%attr(0755,root,root) %dir %{_libdir}/%{name}/methods/*/install
%attr(0755,root,root) %dir %{_libdir}/%{name}/methods/*/setup
%attr(0755,root,root) %dir %{_libdir}/%{name}/methods/*/update
%attr(0755,root,root) %dir %{_libdir}/%{name}/parsechangelog/debian
%attr(0755,root,root) %{_sbindir}/*
%dir %{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_datadir}/%{name}/cputable
%{_datadir}/%{name}/ostable
%{_localstatedir}/lib/%{name}/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/origins
%config(noreplace) %{_sysconfdir}/%{name}/origins/debian
%{_mandir}/man1/822-date.1*
%{_mandir}/man1/dselect.1*
%{_mandir}/man1/dpkg*
%{_mandir}/man5/*
%{_mandir}/man8/*
%lang(de) %{_mandir}/de/man?/*
%lang(ja) %{_mandir}/ja/man?/*
%lang(pl) %{_mandir}/pl/man?/*
%lang(sv) %{_mandir}/sv/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(ru) %{_mandir}/ru/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(pt_BR) %{_mandir}/pt_BR/man?/*

