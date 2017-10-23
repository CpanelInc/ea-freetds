
Name: ea-freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 1.00.27
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 6
Release: %{release_prefix}%{?dist}.cpanel
Vendor: cPanel, Inc.
Group: System Environment/Libraries
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/2

# From ftp://ftp.freetds.org/pub/freetds/stable/freetds-patched.tar.gz
Source0: freetds-patched.tar.gz

%if %{__isa_bits} == 64
Provides: libsybdb.so.5()(64bit)
%else
Provides: libsybdb.so.5
%endif
BuildRequires: ea-openssl ea-openssl-devel libtasn1 libtasn1-devel 
Requires: ea-openssl ea-openssl-devel libtasn1 libtasn1-devel 

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


export OPENSSL_CFLAGS="-I/opt/cpanel/ea-openssl/include"
export OPENSSL_LIBS="-L/opt/cpanel/ea-openssl/lib -lssl -lcrypto"
export LDFLAGS="-L$LIBDIR/lib -ldl"


%configure \
	--prefix=/opt/cpanel/freetds \
        --datadir=/opt/cpanel/freetds \
        --bindir=/opt/cpanel/freetds/bin \
        --mandir=/opt/cpanel/freetds/man \
        --libdir=/opt/cpanel/freetds/%{_lib} \
        --includedir=/opt/cpanel/freetds/include \
        --sysconfdir=/opt/cpanel/freetds/etc \
        --enable-msdblib \
	    --with-gnu-ld \
        --with-openssl=/opt/cpanel/ea-openssl \

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
* Mon Oct 23 2017 Cory McIntire <cory@cpanel.net> - 1.00.27-5
- EA-6911: FreeTDS not building on CentOS 7
- Now building against OpenSSL

* Tue Oct 03 2017 Cory McIntire <cory@cpanel.net> - 1.00.27-5
- EA-4653: Add requires that PHP 5.x needs

* Thu Sep 21 2017 Dan MUey <dan@cpanel.net> - 1.00.27-4
- EA-6612: Enable TLS

* Wed Jun 14 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 1.00.27-3
- Add libsybdb provides

* Sun Apr 09 2017 Eugene Zamriy <eugene@zamriy.info> - 1.00.27-2
- Disabled automatic Provides / Requires generation to avoid conflicts with EPEL package
- Removed duplicate BuildRoot definition

* Wed Apr 05 2017 Dan Muey <dan@cpanel.net> - 1.00.27-1
- EA-6137: Update ea-freetds from 0.91 to 1.0

* Fri Mar 24 2017 Dan Muey <dan@cpanel.net> - 0.91-1
- EA-6030: EA4-ify the initial POC
