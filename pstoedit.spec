%define	major 0
%define	libname	%mklibname pstoedit %{major}
%define libp2edrvlplot %mklibname p2edrvlplot %{major}
%define libp2edrvmagickpp %mklibname p2edrvmagick++ %{major}
%define libp2edrvstd %mklibname p2edrvstd %{major}
%define libp2edrvpptx %mklibname p2edrvpptx %{major}
%define	devname	%mklibname pstoedit -d

Summary:	Translates PostScript/PDF graphics into other vector formats
Name:		pstoedit
Version:	3.73
Release:	1
License:	GPLv2+
Group:		Graphics
Url:		http://www.pstoedit.net/pstoedit
Source0:	https://sourceforge.net/projects/pstoedit/files/pstoedit/%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch1:		pstoedit-3.70-pkgconfig.patch
BuildRequires:	bison
BuildRequires:	ghostscript
BuildRequires:	plotutils-devel
BuildRequires:	pkgconfig(ImageMagick)
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(libpng)

# not compatible
BuildConflicts:	ming-devel
Suggests:	%{libp2edrvlplot} = %{version}-%{release}
Suggests:	%{libp2edrvmagickpp} = %{version}-%{release}
Suggests:	%{libp2edrvstd} = %{version}-%{release}
Suggests:	%{libp2edrvpptx} = %{version}-%{release}

%description
pstoedit translates PostScript and PDF graphics into other vector formats.
Currently pstoedit can generate the following formats:

	- Tgif .obj format (for tgif version >= 3)
	- fig format for xfig
	- pdf Adobe Portable Document Format
	- gnuplot format
	- Flattened PostScript (with or without Bezier curves)
	- DXF - CAD exchange format
	- LWO - LightWave 3D
	- RIB - RenderMan
	- RPL - Real3D
	- Idraw format (a special format of EPS that Idraw can read)
	- Tcl/Tk
	- HPGL
	- AI - Adobe Illustrator Format (based on ps2ai.ps, not a real pstoedit)
	- WMF - Windows Meta Files
	- PIC format for troff/groff
	- MetaPost format per usage with TeX/LaTeX
	- LaTeX2e picture
	- Kontour
	- GNU Metafile (plotutils/libplot)
	- Sketch (http://sketch.sourceforge.net)
	- Mathematica
	- trough ImageMagick to any format supported by ImageMagick

%package -n	%{libname}
Summary:	Pstoedit libraries
Group:		System/Libraries

%description -n	%{libname}
This package contains a shared library for %{name}.

%package -n	%{libp2edrvlplot}
Summary:	Pstoedit libraries
Group:		System/Libraries
Conflicts:	%{_lib}pstoedit0 < 3.62-3

%description -n	%{libp2edrvlplot}
This package contains a shared library for %{name}.

%package -n	%{libp2edrvmagickpp}
Summary:	Pstoedit libraries
Group:		System/Libraries
Conflicts:	%{_lib}pstoedit0 < 3.62-3

%description -n	%{libp2edrvmagickpp}
This package contains a shared library for %{name}.

%package -n	%{libp2edrvstd}
Summary:	Pstoedit libraries
Group:		System/Libraries
Conflicts:	%{_lib}pstoedit0 < 3.62-3

%description -n	%{libp2edrvstd}
This package contains a shared library for %{name}.

%package -n     %{libp2edrvpptx}
Summary:        Pstoedit libraries
Group:          System/Libraries
Conflicts:      %{_lib}pstoedit0 < 3.62-3

%description -n %{libp2edrvpptx}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development libraries and header files for pstoedit development
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libp2edrvlplot} = %{version}-%{release}
Requires:	%{libp2edrvmagickpp} = %{version}-%{release}
Requires:	%{libp2edrvstd} = %{version}-%{release}
Requires:       %{libp2edrvpptx} = %{version}-%{release}
Conflicts:	%{_lib}pstoedit0 < 3.62-3

%description -n	%{devname}
If you want to create applications that will use pstoedit code or
APIs, you'll need to install these packages as well as pstoedit. This
additional package isn't necessary if you simply want to use pstoedit.

%prep
%setup -q
%apply_patches

%build
# needed because of definitions in imagemagick headers that break with -pedantic
sed -ie 's/-pedantic//' configure
%configure
%make

%install
%makeinstall_std

install -m644 doc/pstoedit.1 -D %{buildroot}%{_mandir}/man1/pstoedit.1

%files
%doc doc/changelog.htm doc/pstoedit.htm doc/readme.txt
%doc readme.install examples
%{_bindir}/pstoedit
%{_datadir}/pstoedit
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/libpstoedit.so.%{major}*

%files -n %{libp2edrvlplot}
%{_libdir}/pstoedit/libp2edrvlplot.so.%{major}*
%{_libdir}/pstoedit/libp2edrvlplot.so

%files -n %{libp2edrvmagickpp}
%{_libdir}/pstoedit/libp2edrvmagick++.so.%{major}*
%{_libdir}/pstoedit/libp2edrvmagick++.so

%files -n %{libp2edrvstd}
%{_libdir}/pstoedit/libp2edrvstd.so.%{major}*
%{_libdir}/pstoedit/libp2edrvstd.so

%files -n %{libp2edrvpptx}
%{_libdir}/pstoedit/libp2edrvpptx.so.%{major}*
%{_libdir}/pstoedit/libp2edrvpptx.so

%files -n %{devname}
%doc doc/pstoedit.htm
%{_includedir}/pstoedit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
