Name:           ftwall 
Version:        1.08
Release:         %mkrel 2
Summary:        Fast Track protocol filter for Linux Netfilter firewalls

Group:          System/Configuration/Networking
License:        GPL
URL:            http://www.lowth.com/p2pwall/ftwall/
Source0:        ftwall-1.08.tar.bz2
Patch0:         ftwall-1.07-Makefile.patch.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires:  openssl-devel perl iptables-devel
Requires:       iptables chkconfig
Requires(post,preun):	rpm-helper

%description
ftwall is a program for linux firewalls that allows the control of
network traffic from "Fast Track" peer-to-peer clients like "Kazaa"
and it's derivatives.
It is designed to block network traffic from Fast track client
applications running in the "home" (or "green") network from making
access to any peers on the public internet. It is ideal for use in
networks where the security paradigm is "open access" for outbound
connections and "tightly limited" access for inbound ones. Ftwall can
be used in such a network to prevent outbound Fast Track access, hence
preventing illegal file downloads and uploads.
Read the ftwall homepage at http://www.lowth.com/p2pwall/ftwall/ for
information about configurating ftwall.  Further directions are
installed within this package in /usr/share/doc/ftwall-%{version}


%prep
%setup -q 
%patch0 -p1

%build

find . -type f | xargs perl -pi -e "s,insmod,modprobe,g"

%make

%install
rm -rf $RPM_BUILD_ROOT
make mandrake_install
# Offender IP addresses logged here
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/ftwall.clients

%clean
rm -rf $RPM_BUILD_ROOT


%post
%_post_service ftwall

%preun
%_preun_service ftwall

%files
%defattr(-,root,root,-)
%doc COPYING HISTORY README INSTALL
%{_sbindir}/*
%attr(755,root,root) %config(noreplace) %{_initrddir}/*
%{_mandir}/man8/*
%dir %{_localstatedir}/log/ftwall.clients


