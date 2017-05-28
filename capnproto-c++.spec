#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Cap'n Proto - Insanely Fast Data Serialization Format
Summary(pl.UTF-8):	Cap'n Proto - szaleńczo szybki format serializacji danych
Name:		capnproto-c++
Version:	0.6.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://capnproto.org/install.html
Source0:	https://capnproto.org/%{name}-%{version}.tar.gz
# Source0-md5:	da2a4ccc521e7af7752ec4e2ea4ee951
URL:		https://capnproto.org/
BuildRequires:	cmake >= 3.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpmbuild(macros) >= 1.605
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
Requires:	libstdc++-devel >= 6:4.7

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
# initialize cmake to generate CapnProtoTargets files
install -d build-cmake
cd build-cmake
%cmake ..
cd ..
# but use autotools (cmake doesn't use library sonames)
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

# cmake support (omitted when installing using autotools)
# (note: cmake install seems to omit necessary FindCapnProto.cmake file)
install -d $RPM_BUILD_ROOT{%{_libdir}/cmake/CapnProto,%{_datadir}/cmake/Modules}
cp -p cmake/FindCapnProto.cmake $RPM_BUILD_ROOT%{_datadir}/cmake/Modules
cp -p cmake/Capn*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/CapnProto
cp -p build-cmake/cmake/CapnProtoConfig*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/CapnProto
cp -p build-cmake/CMakeFiles/Export/_usr/%{_lib}/cmake/CapnProto/CapnProtoTargets*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/CapnProto

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
%attr(755,root,root) %{_libdir}/libcapnpc-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-async-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-http-%{version}.so
%attr(755,root,root) %{_libdir}/libkj-test-%{version}.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcapnp.so
%attr(755,root,root) %{_libdir}/libcapnp-json.so
%attr(755,root,root) %{_libdir}/libcapnp-rpc.so
%attr(755,root,root) %{_libdir}/libcapnpc.so
%attr(755,root,root) %{_libdir}/libkj.so
%attr(755,root,root) %{_libdir}/libkj-async.so
%attr(755,root,root) %{_libdir}/libkj-http.so
%attr(755,root,root) %{_libdir}/libkj-test.so
%{_includedir}/capnp
%{_includedir}/kj
%{_pkgconfigdir}/capnp.pc
%{_pkgconfigdir}/capnp-rpc.pc
%{_pkgconfigdir}/kj.pc
%{_pkgconfigdir}/kj-async.pc
%{_libdir}/cmake/CapnProto
%{_datadir}/cmake/Modules/FindCapnProto.cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcapnp.a
%{_libdir}/libcapnp-json.a
%{_libdir}/libcapnp-rpc.a
%{_libdir}/libcapnpc.a
%{_libdir}/libkj.a
%{_libdir}/libkj-async.a
%{_libdir}/libkj-http.a
%{_libdir}/libkj-test.a
%endif
