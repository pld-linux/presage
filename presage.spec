#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	ngram		# ARPA ngram language model
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Presage - the intelligent predictive text entry system
Summary(pl.UTF-8):	Presage - inteligentny, przewidujący system wprowadzania tekstu
Name:		presage
Version:	0.9.1
Release:	0.1
License:	GPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/presage/%{name}-%{version}.tar.gz
# Source0-md5:	9667be297912fa0d432e748526d8dd9e
Patch0:		%{name}-link.patch
Patch1:		%{name}-configure.patch
URL:		http://presage.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
%{?with_ngram:BuildRequires:	cmuclmtk}
BuildRequires:	cppunit-devel >= 1.9.6
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	graphviz
BuildRequires:	glib2-devel >= 1:2.0
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	help2man
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	python-dbus
BuildRequires:	python-devel >= 2.0
BuildRequires:	python-pyatspi
BuildRequires:	python-pygtk-gtk >= 2:2
BuildRequires:	python-wx
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	swig-python >= 2.0
BuildRequires:	tinyxml-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXevie-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Presage (formerly known as Soothsayer) generates predictions by
modelling natural language as a combination of redundant information
sources. Presage computes probabilities for words which are most
likely to be entered next by merging predictions generated by the
different predictive algorithms. Presage's modular and extensible
architecture allows its language model to be extended and customized
to utilize statistical, syntactic, and semantic predictive algorithms.

%description -l pl.UTF-8
Presage (wcześniej znany jako Soothsayer) generuje przewidywania
poprzez modelowanie języka naturalnego jako kombinacji redundantnych
źródeł informacji. Presage wylicza prawdopodobieństwa słów, które są
najbardziej spodziewane być wpisane jako kolejne, łącząc przewidywania
wygenerowane różnymi algorytmami predykcji. Modularna i rozszerzalna
architektura Presage pozwala na rozszerzanie modelu języka i
dostosowywanie go, aby wykorzystywał algorytmy statystyczne,
syntaktyczne oraz semantyczne.

%package libs
Summary:	Presage shared library
Summary(pl.UTF-8):	Biblioteka współdzielona Presage
Group:		Libraries

%description libs
Presage shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona Presage.

%package devel
Summary:	Header files for Presage library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Presage
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Presage library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Presage.

%package static
Summary:	Static Presage library
Summary(pl.UTF-8):	Statyczna biblioteka Presage
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Presage library.

%description static -l pl.UTF-8
Statyczna biblioteka Presage.

%package apidocs
Summary:	API documentation for Presage library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Presage
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Presage library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Presage.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-documentation} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ NEWS README THANKS TODO doc/getting_started.txt
%attr(755,root,root) %{_libdir}/libpresage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpresage.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/presage.xml

%attr(755,root,root) %{_bindir}/gpresagemate

%attr(755,root,root) %{_bindir}/gprompter

# dbus service, R: python-dbus
%attr(755,root,root) %{_bindir}/presage_dbus_python_demo
%attr(755,root,root) %{_bindir}/presage_dbus_service
%{py_sitescriptdir}/presage_dbus_service.py[co]
%{_datadir}/dbus-1/services/org.gnome.presage.service
%{_mandir}/man1/presage_dbus_python_demo.1*
%{_mandir}/man1/presage_dbus_service.1*

%attr(755,root,root) %{_bindir}/presage_demo
%attr(755,root,root) %{_bindir}/presage_demo_text
%attr(755,root,root) %{_bindir}/presage_python_demo
%attr(755,root,root) %{_bindir}/presage_simulator
%attr(755,root,root) %{_bindir}/text2ngram
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/abbreviations_*.txt
%{_datadir}/%{name}/database_*.db
%if %{with ngram}
%{_datadir}/%{name}/vocab*
%endif
# FIXME: location
%doc %{_datadir}/%{name}/html
%{_desktopdir}/gprompter.desktop
%{_iconsdir}/hicolor/scalable/apps/gprompter.svg
%{_pixmapsdir}/gprompter.png
%{_pixmapsdir}/gprompter.xpm
%{_mandir}/man1/gprompter.1*
%{_mandir}/man1/presage_demo.1*
%{_mandir}/man1/presage_demo_text.1*
%{_mandir}/man1/presage_python_demo.1*
%{_mandir}/man1/presage_simulator.1*
%{_mandir}/man1/text2ngram.1*

%attr(755,root,root) %{py_sitedir}/_presage.so
%attr(755,root,root) %{py_sitedir}/presage.py[co]
%{py_sitedir}/python_presage-%{version}-py*.egg-info

# pyprompter, R: python-wxPython
# FIXME: *.pyo
%attr(755,root,root) %{_bindir}/pyprompter
%{py_sitedir}/prompter
%{py_sitedir}/pyprompter-%{version}-py*.egg-info
%{_desktopdir}/pyprompter.desktop
%{_iconsdir}/hicolor/scalable/apps/pyprompter.svg
%{_pixmapsdir}/pyprompter.png
%{_pixmapsdir}/pyprompter.xpm
%{_mandir}/man1/pyprompter.1*

# pypresagemate, R: python-pyatspi, python-pygtk-gtk, python-pygtk-pango, python-Xlib
%attr(755,root,root) %{_bindir}/pypresagemate
%{py_sitescriptdir}/presagemate

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpresage.so
%{_libdir}/libpresage.la
%{_includedir}/presage*.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpresage.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif

#%doc doc/python_binding.txt

# TODO:
#%{_datadir}/presage/presage.png
#%{_datadir}/presage/presage.svg
#%{_datadir}/presage/presage.xpm