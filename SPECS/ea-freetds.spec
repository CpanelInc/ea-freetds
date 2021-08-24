%define ea_openssl_ver 1.1.1d-1

Name: ea-freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 1.3.1
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
Vendor: cPanel, Inc.
Group: System Environment/Libraries
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/2

# do not produce debuginfo package
%define debug_package %{nil}

%define _docdir /opt/cpanel/freetds/share/doc/freetds

# From https://www.freetds.org/files/stable/freetds-%{version}.tar.gz
Source0: freetds-%{version}.tar.gz

%if 0%{rhel} < 7
BuildRequires: devtoolset-7-toolchain
BuildRequires: devtoolset-7-libatomic-devel
BuildRequires: devtoolset-7-gcc
BuildRequires: devtoolset-7-gcc-c++
%endif

%if %{__isa_bits} == 64
Provides: libsybdb.so.5()(64bit)
%else
Provides: libsybdb.so.5
%endif
BuildRequires: unixODBC-devel, readline-devel
BuildRequires: libtool
BuildRequires: doxygen, docbook-style-dsssl

%if 0%{rhel} < 8
BuildRequires: ea-openssl11 >= %{ea_openssl_ver}, ea-openssl11-devel >= %{ea_openssl_ver}, libtasn1, libtasn1-devel
Requires: ea-openssl11 >= %{ea_openssl_ver}, ea-openssl11-devel >= %{ea_openssl_ver}, libtasn1, libtasn1-devel
%else
# In C8 we use system openssl. See DESIGN.md in ea-openssl11 git repo for details
BuildRequires: openssl, openssl-devel, libtasn1, libtasn1-devel
Requires: openssl, openssl-devel, libtasn1, libtasn1-devel
%endif

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.


%package libs
Summary: Libraries for %{name}
Requires: %{name} = %{version}-%{release}

%description libs
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.
This package contains the libraries for %{name}.


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.


%package doc
Summary: Development documentation for %{name}
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}, you will need to install
%{name}-doc.


%prep
%setup -q -n freetds-%{version}

%build
%if 0%{?rhel} < 7
. /opt/rh/devtoolset-7/enable
%endif

%configure \
        --prefix=/opt/cpanel/freetds \
        --datadir=/opt/cpanel/freetds \
        --bindir=/opt/cpanel/freetds/bin \
        --mandir=/opt/cpanel/freetds/man \
        --docdir=/opt/cpanel/freetds/share/doc/freetds \
        --libdir=/opt/cpanel/freetds/%{_lib} \
        --includedir=/opt/cpanel/freetds/include \
        --sysconfdir=/opt/cpanel/freetds/etc \
        --enable-msdblib \
        --with-gnu-ld \
        -with-unixodbc="%{_prefix}" \
%if 0%{?rhel} < 8
        --with-openssl=/opt/cpanel/ea-openssl11 \
        LDFLAGS="-Wl,-rpath=/opt/cpanel/ea-openssl11/%{_lib}"
%else
        --with-openssl
%endif

make %{?_smp_mflags} DOCBOOK_DSL="`rpm -ql docbook-style-dsssl | fgrep html/docbook.dsl`"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/freetds
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/opt/cpanel/freetds/%{_lib}/*.a
rm -f $RPM_BUILD_ROOT/opt/cpanel/freetds/%{_lib}/*.la
chmod -x $RPM_BUILD_ROOT/opt/cpanel/freetds/etc/*

rm -f samples/Makefile* samples/*.in samples/README

mkdir samples-odbc
mv -f samples/*odbc* samples-odbc

#  deinstall it for our own way...
#mv -f $RPM_BUILD_ROOT/opt/cpanel/freetds/doc/freetds docdir
#find docdir -type f -print0 | xargs -0 chmod -x


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
/opt/cpanel/freetds/bin/*
%doc AUTHORS.md BUGS.md COPYING.txt NEWS.md README.md TODO.md doc/*.html
%doc %{_docdir}/userguide
%doc %{_docdir}/images
/opt/cpanel/freetds/man/man1/*


%files libs
%doc COPYING_LIB.txt
/opt/cpanel/freetds/%{_lib}/*.so.*
/opt/cpanel/freetds/%{_lib}/libtdsodbc.so
%doc samples-odbc
%config(noreplace) /opt/cpanel/freetds/etc/*.conf
/opt/cpanel/freetds/man/man5/*


%files devel
%doc samples
/opt/cpanel/freetds/%{_lib}/*.so
%exclude /opt/cpanel/freetds/%{_lib}/libtdsodbc.so
/opt/cpanel/freetds/include/*


%files doc
%doc %{_docdir}/reference


%changelog
* Thu Aug 19 2021 Cory McIntire <cory@cpanel.net> - 1.3.1-1
- EA-10057: Update ea-freetds from v1.2.9 to v1.3.1

* Tue Nov 24 2020 Julian Brown <julian.brown@cpanel.net> - 1.2.9-2
- ZC-8005: Replace ea-openssl11 with system openssl on C8

* Tue Nov 03 2020 Cory McIntire <cory@cpanel.net> - 1.2.9-1
- EA-9397: Update ea-freetds from v1.2.5 to v1.2.9

* Fri Sep 18 2020 Cory McIntire <cory@cpanel.net> - 1.2.5-1
- EA-9304: Update ea-freetds from v1.2.3 to v1.2.5

* Thu Jul 09 2020 Cory McIntire <cory@cpanel.net> - 1.2.3-1
- EA-9148: Update ea-freetds from v1.1.24 to v1.2.3

* Wed Jan 22 2020 Tim Mullin <tim@cpanel.net> - 1.1.24-1
- EA-8839: Update to version 1.1.24 and make libtdsodbc.so available

* Tue Sep 24 2019 Daniel Muey <dan@cpanel.net> - 1.1.6-2
- ZC-4361: Update ea-openssl requirement to v1.1.1 (ZC-5583)

* Fri May 17 2019 Cory McIntire <cory@cpanel.net> - 1.1.6-1
- EA-8462: Updated to version 1.1.6

* Mon Apr 16 2018 Rishwanth Yeddula <rish@cpanel.net> - 1.00.27-9
- EA-7382: Update dependency on ea-openssl to require the latest version with versioned symbols.

* Mon Mar 20 2018 Cory McIntire <cory@cpanel.net> - 1.00.27-8
- ZC-3552: Added versioning to ea-openssl requirements.

* Mon Mar 05 2018 Daniel Muey <dan@cpanel.net> - 1.00.27-7
- ZC-3476: Update for ea-openssl shared object

* Sat Oct 28 2017 Cory McIntire <cory@cpanel.net> - 1.00.27-6
- EA-6943: SPEC file whitespace and tab clean up
- Reporter: https://github.com/dkasyanov

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
