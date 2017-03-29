
Name: ea-freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 0.91
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
Vendor: cPanel, Inc.
Group: System Environment/Libraries
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# From ftp://ftp.freetds.org/pub/freetds/stable/freetds-stable.tgz
Source0: freetds-stable.tgz

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
%setup -q -n freetds-%{version}

%build 

%configure \
	--prefix=/opt/cpanel/freetds \
        --datadir=/opt/cpanel/freetds \
        --bindir=/opt/cpanel/freetds/bin \
        --mandir=/opt/cpanel/freetds/man \
        --libdir=/opt/cpanel/freetds/%{_lib} \
        --includedir=/opt/cpanel/freetds/include \
        --sysconfdir=/opt/cpanel/freetds/etc \
	--with-tdsver=8.0 \
	--enable-msdblib \
	--enable-dbmfix \
	--with-gnu-ld

make
 
%install 
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/freetds
make install DESTDIR=$RPM_BUILD_ROOT

%clean 
rm -rf $RPM_BUILD_ROOT
 
%files 
%defattr(-, root, root, -) 
/opt/cpanel/freetds
%config(noreplace) /opt/cpanel/freetds/etc/*.conf
 
%files devel 
%defattr (-, root, root, -) 
/opt/cpanel/freetds/include

%changelog
* Fri Mar 24 2017 Dan Muey <dan@cpanel.net> - 0.91-1
- EA-6030: EA4-ify the initial POC
