Summary:	Fast Track protocol filter for Linux Netfilter firewalls
Name:		ftwall 
Version:	1.09
Release:	5
Group:		System/Configuration/Networking
License:	GPL
URL:		http://www.lowth.com/p2pwall/ftwall/
Source0:	ftwall-%{version}.tar.gz
Patch0:		ftwall-1.07-Makefile.patch
Patch1:		ftwall-1.09-gcc43.diff
Patch2:		ftwall-1.09-conflicting_symbol_fix.diff
Patch3:		ftwall-1.09-openssl-0.9.8h_lhash.diff
Patch4:		ftwall-1.09-optflags_fix.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	iptables
Requires:	chkconfig
BuildRequires:	iptables-devel
BuildRequires:	pkgconfig(libipq)
BuildRequires:	openssl-devel
BuildRequires:	perl

%description
ftwall is a program for linux firewalls that allows the control of network
traffic from "Fast Track" peer-to-peer clients like "Kazaa" and it's
derivatives. It is designed to block network traffic from Fast track client
applications running in the "home" (or "green") network from making access to
any peers on the public internet. It is ideal for use in networks where the
security paradigm is "open access" for outbound connections and "tightly
limited" access for inbound ones. Ftwall can be used in such a network to
prevent outbound Fast Track access, hence preventing illegal file downloads and
uploads. Read the ftwall homepage at http://www.lowth.com/p2pwall/ftwall/ for
information about configurating ftwall. Further directions are installed within
this package in /usr/share/doc/ftwall-%{version}

%prep

%setup -q 
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p0

find . -type f | xargs perl -pi -e "s,insmod,modprobe,g"

%build
%serverbuild

%make RPM_OPT_FLAGS="$CFLAGS"

%install
rm -rf %{buildroot}

make mandrake_install

# Offender IP addresses logged here
install -d %{buildroot}/var/log/ftwall.clients

# fix man pages
gunzip %{buildroot}%{_mandir}/man8/*

%post
%_post_service ftwall

%preun
%_preun_service ftwall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc HISTORY README INSTALL libipq.txt
%attr(0755,root,root) %{_initrddir}/*
%{_sbindir}/*
%dir /var/log/ftwall.clients
%{_mandir}/man8/*


%changelog
* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.09-4mdv2010.0
+ Revision: 453592
- fix build
- rebuild

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild

* Sat Oct 25 2008 Oden Eriksson <oeriksson@mandriva.com> 1.09-2mdv2009.1
+ Revision: 297260
- rebuild

* Sun Jul 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1.09-1mdv2009.0
+ Revision: 250442
- 1.09 (last one from 2004...)
- fix build (P1,P2)
- use newer openssl lhash code (P3)
- use %%serverbuild CFLAGS (P4)

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - fix prereq on rpm-helper
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel
    - import ftwall

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Thu Aug 26 2004 Florin <florin@mandrakesoft.com> 1.08-2mdk
- use modprobe instead of insmod

* Wed Jun 02 2004 Florin <florin@mandrakesoft.com> 1.08-1mdk
- first mdk release
