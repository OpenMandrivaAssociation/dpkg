%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(controllib.pl\\)|perl\\(file\\)'
%else
%define _requires_exceptions perl(controllib.pl)\\|perl(file)
%endif

Summary:	Package maintenance system for Debian Linux
Name:		dpkg
Version:	1.16.8
Release:	3
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://packages.debian.org/unstable/base/dpkg.html
Source0:	ftp://ftp.debian.org/debian/pool/main/d/dpkg/%{name}_%{version}.tar.xz
Source1:	%{name}-pl-man-pages.tar.bz2
Source2:	debsign.sh
Source3:	debsign.1
Patch0:		update-alternatives-1.16.8-mandriva.patch
BuildRequires:	gettext-devel
BuildRequires:	po4a
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	bzip2-devel

%description
This package contains the programs dpkg which used to handle the installation
and removal of packages on a Debian system.

In order to unpack and build Debian source packages you will need
to install the developers' package `dpkg-dev' as well as this one.

dpkg-dev is not provided on your Mandriva Linux system.

%package -n	perl-Dpkg
Summary:	Package maintenance system for Debian Linux
Group:		Development/Perl
BuildArch:	noarch

%description -n	perl-Dpkg
This module provides dpkg functionalities.

%package -n	update-alternatives
Summary:	Alternative management system
Group:		System/Configuration/Packaging
# explicit file provides
Provides:	%{_sbindir}/alternatives
Provides:	%{_sbindir}/update-alternatives

%description -n	update-alternatives
update-alternatives creates, removes, maintains and displays
information about the symbolic links comprising the alternatives
system. It is possible for several programs fulfilling the same or
similar functions to be installed on a single system at the same time.
For example, many systems have several text editors installed at once.
This gives choice to the users of a system, allowing each to use a
different editor, if desired, but makes it difficult for a program to
make a good choice of editor to invoke if the user has not specified a
particular preference.

%prep
%setup -q
%patch0 -p1 -b .rpmman~

%build
CONFIGURE_TOP="$PWD"
mkdir -p dpkg
pushd dpkg
%configure2_5x \
    --enable-shared \
    --disable-dselect \
    --with-admindir=%{_localstatedir}/lib/%{name} \
    --with-zlib \
    --with-bz2 \
    --with-liblzma

%make
popd

mkdir -p update-alternatives
pushd update-alternatives
CFLAGS="%{optflags} -Os" \
%configure2_5x \
    --with-admindir=%{_localstatedir}/lib/rpm/
%make -C lib/compat
%make -C utils/
popd

%install
%makeinstall_std -C dpkg

bzip2 -dc %{SOURCE1} | tar xf - -C %{buildroot}%{_mandir}
install -m 755 %{SOURCE2} %{buildroot}/%{_bindir}/debsign
install -m 644 %{SOURCE3} %{buildroot}/%{_mandir}/man1

# cleanup
rm -fr %{buildroot}%{_datadir}/locale/en/
rm -f %{buildroot}{%{_bindir},%{_sbindir}}/update-alternatives
rm -r %{buildroot}%{_sysconfdir}/alternatives
rm -fr %{buildroot}/usr/share/doc
find %{buildroot} -name "md5sum*" -exec rm -f {} \;
find %{buildroot}%{_mandir} -name "update-alternatives*" -exec rm -f {} \;

%find_lang %{name}
%find_lang dpkg-dev
cat dpkg-dev.lang >> %{name}.lang


install -d -m755 %{buildroot}%{_sysconfdir}/alternatives
install -d -m755 %{buildroot}%{_localstatedir}/lib/rpm/alternatives
install -d -m755 %{buildroot}%{_localstatedir}/log

touch %{buildroot}%{_localstatedir}/log/update-alternatives.log

install -m755 update-alternatives/utils/update-alternatives -D %{buildroot}%{_sbindir}/update-alternatives
install -m644 man/update-alternatives.8 -D %{buildroot}%{_mandir}/man8/update-alternatives.8

# I really doubt the actual usefulness of these..
ln -s update-alternatives %{buildroot}%{_sbindir}/alternatives
ln -sr %{buildroot}%{_localstatedir}/lib/rpm %{buildroot}%{_localstatedir}/lib/alternatives

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(0755,root,root) %{_bindir}/d*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/parsechangelog
%attr(0755,root,root) %dir %{_libdir}/%{name}/parsechangelog/debian
%attr(0755,root,root) %{_sbindir}/*
%exclude %{_sbindir}/alternatives
%exclude %{_sbindir}/update-alternatives
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
%exclude %{_mandir}/man8/update-alternatives.8*
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
%{perl_vendorlib}/Dpkg
%{perl_vendorlib}/Dpkg.pm

%files -n update-alternatives
%dir %{_sysconfdir}/alternatives
%{_sbindir}/alternatives
%{_sbindir}/update-alternatives
%{_mandir}/man8/update-alternatives.8*
%{_localstatedir}/lib/alternatives
%dir %{_localstatedir}/lib/rpm/alternatives
%ghost %{_localstatedir}/log/update-alternatives.log
