%define	major 0
%define	libname	%mklibname pstoedit %{major}
%define oldlibp2edrvlplot %mklibname p2edrvlplot 0
%define oldlibp2edrvmagickpp %mklibname p2edrvmagick++ 0
%define oldlibp2edrvstd %mklibname p2edrvstd 0
%define oldlibp2edrvpptx %mklibname p2edrvpptx 0
%define	devname	%mklibname pstoedit -d

Summary:	Translates PostScript/PDF graphics into other vector formats
Name:		pstoedit
Version:	4.02
Release:	1
License:	GPLv2+
Group:		Graphics
Url:		https://www.pstoedit.net/pstoedit
Source0:	https://sourceforge.net/projects/pstoedit/files/pstoedit/%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:		pstoedit-fix-locating-ImageMagick.patch
BuildRequires:	bison
BuildRequires:	ghostscript
BuildRequires:	plotutils-devel
BuildRequires:	pkgconfig(MagickCore)
BuildRequires:	pkgconfig(Magick++)
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	imagemagick
# For GUI
BuildRequires:	qmake-qt6
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Widgets)

# not compatible
BuildConflicts:	ming-devel

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
%rename	%{oldlibp2edrvlplot}
%rename %{oldlibp2edrvmagickpp}
%rename %{oldlibp2edrvstd}
%rename %{oldlibp2edrvpptx}

%description -n	%{libname}
This package contains a shared library for %{name}.

%package gui
Summary:	Graphical user interface for pstoedit
Group:		Graphics
Requires:	%{name} = %{EVRD}

%description gui
Graphical user interface for pstoedit, a PostScript/PDF to
vector graphics converter

%package -n	%{devname}
Summary:	Development libraries and header files for pstoedit development
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Conflicts:	%{_lib}pstoedit0 < 3.62-3

%description -n	%{devname}
If you want to create applications that will use pstoedit code or
APIs, you'll need to install these packages as well as pstoedit. This
additional package isn't necessary if you simply want to use pstoedit.

%prep
%autosetup -p1
sed -i -e 's,qmake6,qmake-qt6,g' configure* QT/PstoeditQtGui/Make*
%configure

%build
%make_build
export PATH=%{_qtdir}/bin:${PATH}
cd QT/PstoeditQtGui
%make_build GUI || :
sed -i -e 's,\.\./\.\./\.\./,../../,g' Makefile.qt
%make_build -f Makefile.qt

%install
%make_install
install -m644 doc/pstoedit.1 -D %{buildroot}%{_mandir}/man1/pstoedit.1

cd QT/PstoeditQtGui
install -m755 PstoeditQtGui %{buildroot}%{_bindir}
for size in 16 22 24 32 44 48 64 72 96 128; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
	convert *.ico -gravity center -scale ${size}x${size} -extent ${size}x${size} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

%files
%doc doc/changelog.htm doc/pstoedit.htm doc/readme.txt
%doc readme.install examples
%{_bindir}/pstoedit
%{_datadir}/pstoedit
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/libpstoedit.so.%{major}*
%dir %{_libdir}/pstoedit
%{_libdir}/pstoedit/libp2edrvlplot.so
%{_libdir}/pstoedit/libp2edrvmagick++.so
%{_libdir}/pstoedit/libp2edrvstd.so
%{_libdir}/pstoedit/libp2edrvpptx.so

%files -n %{devname}
%doc doc/pstoedit.htm
%doc %{_docdir}/pstoedit
%{_includedir}/pstoedit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4

%files gui
%{_bindir}/PstoeditQtGui
%{_datadir}/applications/PstoeditQtGui.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
