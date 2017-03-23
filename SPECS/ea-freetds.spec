
Name: freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 0.91
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
Group: System Environment/Libraries
Vendor: cPanel, Inc
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: ftp://ftp.freetds.org/pub/freetds/stable/freetds-stable.tgz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description 
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.

%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.


%prep 
%setup -q

%build 

%configure \
	--prefix=/usr/local/freetds \
	--with-tdsver=8.0 \
	--enable-msdblib \
	--enable-dbmfix \
	--with-gnu-ld

make
 
%install 
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean 
rm -rf $RPM_BUILD_ROOT
 
%files 
%defattr(-, root, root, -) 
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/libct.*
%{_libdir}/libsybdb.*
%config(noreplace) %{_sysconfdir}/*.conf
%doc AUTHORS BUGS COPYING* NEWS README TODO doc/*.html
%doc doc/doc/freetds-%{version}/userguide doc/images
%{_mandir}/*/*

 
%files devel 
%defattr (-, root, root, -) 
%doc samples
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%{_includedir}/*

%changelog

