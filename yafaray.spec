%define oname YafaRay

%if %{_use_internal_dependency_generator}
%define __noautoprovfiles '%{python_sitearch}/(.*)\.so$|%{_libdir}/yafaray'
%else
%define _exclude_files_from_autoprov ^%{python_sitearch}/.*\.so$\\|%{_libdir}/yafaray
%endif

Summary:	A free open-source raytracing render engine
Name:		yafaray
Version:	0.1.1
Release:	2
License:	LGPLv2.1
Group:		Graphics
URL:		https://www.yafray.org/
Source0:	http://static.yafaray.org/sources/%{oname}.%{version}.zip
Source1:	http://static.yafaray.org/sources/%{oname}-blender.%{version}.zip
Source2:	yafaray.rpmlintrc
BuildRequires:	scons
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	jpeg-devel
BuildRequires:	python-devel
BuildRequires:	swig
BuildRequires:	qt4-devel
BuildRequires:	zlib-devel
%rename yafray

%description
YafaRay is a free open-source raytracing render engine.

Raytracing is a rendering technique for generating realistic images by
tracing the path of light through a 3D scene. A render engine consists of
a "faceless" computer program that interacts with a host 3D application
to provide very specific raytracing capabilities "on demand". Blender 3D
is the host application of YafaRay.

%package blender
Summary:	Blender integration scripts
Group:		Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	blender

%description blender
YafRay uses a python-coded settings interface to set lighting and rendering
parameters. This settings interface is launched by an entry automatically
added to the Blender Render menu.

%prep
%setup -q -n %{name}
%setup -q -D -T -a 1 -n %{name}

sed -i -e"s,/lib',/%{_lib}',g" config/linux2-config.py
sed -i -e"s,/lib/,/%{_lib}/,g" config/linux2-config.py
sed -i -e"s,WITH_YF_QT='false',WITH_YF_QT='true',g" config/linux2-config.py

cat << EOF >> config/linux2-config.py
YF_QTDIR = '/usr/lib/qt4'
# unversioned SO is correct by itself when the said shared object is
# meant to be dlopen at runtime, instead of being linked at build time.
#YF_SHLINKFLAGS = "-Wl,-soname,libyafaraycore.so.1"
EOF
sed -i -e"s|REL_CCFLAGS = '-O3 -ffast-math'|REL_CCFLAGS = '-ffast-math -fPIC %{optflags}'|g" config/linux2-config.py
sed -i -e"s|/usr/local|/usr|g" config/linux2-config.py
# fixes %%{buildroot} in libyafaraycore.so
sed -i -e"s,\$YF_LIBOUT,%{_libdir},g" tools/writeconfig.py
sed -i -e"s,\$YF_PLUGINPATH,%{_libdir}/%{name},g" tools/writeconfig.py

%build
scons build
scons swig

%install
scons PREFIX=%{buildroot}%{_prefix} install

mkdir -p %{buildroot}%{_datadir}/blender/scripts
mkdir -p %{buildroot}%{python_sitearch}

cp -p bindings/python/yaf*.py \
      %{buildroot}%{_datadir}/blender/scripts
cp -p bindings/python/_yaf*.so \
      %{buildroot}%{python_sitearch}
cp -p %{name}-blender/yaf*.py \
      %{buildroot}%{_datadir}/blender/scripts

%files
%doc CODING LICENSE INSTALL
%{_bindir}/%{name}-xml
%{_libdir}/%{name}/*.so
%{_libdir}/libyafaraycore.so

%files blender
%{_datadir}/blender/scripts/*
%{_libdir}/libyafarayqt.so
%{_libdir}/libyafarayplugin.so
%{python_sitearch}/_yaf*.so



%changelog
* Sat Sep 01 2012 Andrey Bondrov <abondrov@mandriva.org> 0.1.1-1
+ Revision: 816159
- imported package yafaray

