#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Cap'n Proto - Insanely Fast Data Serialization Format
Summary(pl.UTF-8):	Cap'n Proto - szaleńczo szybki format serializacji danych
Name:		capnproto-c++
Version:	1.0.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://capnproto.org/install.html
Source0:	https://capnproto.org/%{name}-%{version}.tar.gz
# Source0-md5:	caa55b89c87466c558c9ffd7b40b400b
URL:		https://capnproto.org/
BuildRequires:	libstdc++-devel >= 6:5.0
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cap'n Proto is an insanely fast data interchange format and
capability-based RPC system. Think JSON, except binary. Or think of
Google's Protocol Buffers, except faster.

%description -l pl.UTF-8
Cap'n Proto to bardzo szybki format wymiany danych oraz system RPC
oparty na możliwościach. Coś jak JSON, ale binarny. Albo coś jak
Google Protocol Buffers, ale szybszy.

%package devel
Summary:	Header files for Cap'n Proto libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Cap'n Proto
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:5.0

%description devel
Header files for Cap'n Proto libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Cap'n Proto.

%package static
Summary:	Static Cap'n Proto libraries
Summary(pl.UTF-8):	Statyczne biblioteki Cap'n Proto
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Cap'n Proto libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Cap'n Proto.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt
%attr(755,root,root) %{_bindir}/capnp
%attr(755,root,root) %{_bindir}/capnpc
%attr(755,root,root) %{_bindir}/capnpc-c++
%attr(755,root,root) %{_bindir}/capnpc-capnp
%attr(755,root,root) %{_libdir}/libcapnp-%{version}.so
%attr(755,root,root) %{_libdir}/libcapnp-json-%{version}.so
%attr(755,root,root) %{_libdir}/libcapnp-rpc-%{version}.so
%attr(755,root,root) %{_libdir}/libcapnp-websocket-%{version}.so
%attr(755,root,root) %{_libdir}/libcapnpc-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-async-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-gzip-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-http-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-test-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-tls-%{version}.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcapnp.so
%attr(755,root,root) %{_libdir}/libcapnp-json.so
%attr(755,root,root) %{_libdir}/libcapnp-rpc.so
%attr(755,root,root) %{_libdir}/libcapnp-websocket.so
%attr(755,root,root) %{_libdir}/libcapnpc.so
%attr(755,root,root) %{_libdir}/libkj.so
%attr(755,root,root) %{_libdir}/libkj-async.so
%attr(755,root,root) %{_libdir}/libkj-gzip.so
%attr(755,root,root) %{_libdir}/libkj-http.so
%attr(755,root,root) %{_libdir}/libkj-test.so
%attr(755,root,root) %{_libdir}/libkj-tls.so
%{_includedir}/capnp
%{_includedir}/kj
%{_pkgconfigdir}/capnp.pc
%{_pkgconfigdir}/capnp-json.pc
%{_pkgconfigdir}/capnp-rpc.pc
%{_pkgconfigdir}/capnp-websocket.pc
%{_pkgconfigdir}/capnpc.pc
%{_pkgconfigdir}/kj.pc
%{_pkgconfigdir}/kj-async.pc
%{_pkgconfigdir}/kj-gzip.pc
%{_pkgconfigdir}/kj-http.pc
%{_pkgconfigdir}/kj-test.pc
%{_pkgconfigdir}/kj-tls.pc
%{_libdir}/cmake/CapnProto

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcapnp.a
%{_libdir}/libcapnp-json.a
%{_libdir}/libcapnp-rpc.a
%{_libdir}/libcapnp-websocket.a
%{_libdir}/libcapnpc.a
%{_libdir}/libkj.a
%{_libdir}/libkj-async.a
%{_libdir}/libkj-gzip.a
%{_libdir}/libkj-http.a
%{_libdir}/libkj-test.a
%{_libdir}/libkj-tls.a
%endif
