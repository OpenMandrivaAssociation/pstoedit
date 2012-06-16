%define	major	0
%define	libname	%mklibname pstoedit %{major}
%define	devname	%mklibname pstoedit -d

Summary:	Translates PostScript/PDF graphics into other vector formats
Name:		pstoedit
Version:	3.60
Release:	1
License:	GPLv2+
Source0: 	http://prdownloads.sourceforge.net/pstoedit/%{name}-%{version}.tar.gz
URL:		http://www.pstoedit.net/pstoedit
Group:		Graphics
BuildRequires:	bison
BuildRequires:	ghostscript
BuildRequires:  imagemagick-devel
BuildRequires:	plotutils-devel
BuildRequires:	multiarch-utils >= 1.0.3
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

%description -n	%{libname}
This package contains the libraries needed to run programs dynamically
linked with pstoedit libraries.

%package -n	%{devname}
Summary:	Static libraries and header files for pstoedit development
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
%rename		%{_lib}pstoedit0-devel

%description -n	%{devname}
If you want to create applications that will use pstoedit code or
APIs, you'll need to install these packages as well as pstoedit. This
additional package isn't necessary if you simply want to use pstoedit.

%prep
%setup -q

# clean up permissions
find -type f -perm +111 | xargs -r file | grep -v script | cut -d: -f1| xargs -r chmod 0644

#AUTOMAKE=automake-1.9 ACLOCAL=aclocal-1.9 autoreconf --force --install

%build
# needed because of definitions in imagemagick headers that break with -pedantic
sed -ie 's/-pedantic//' configure
%configure2_5x --enable-static
%make

%install
%makeinstall_std

install -m644 doc/pstoedit.1 -D %{buildroot}%{_mandir}/man1/pstoedit.1

rm -f %{buildroot}%{_libdir}/%{name}/*.a

%files
%doc doc/changelog.htm doc/index.htm doc/readme.txt
%doc readme.install examples
%{_bindir}/pstoedit
%{_datadir}/pstoedit
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/*.so.*
%{_libdir}/pstoedit/*.so
%{_libdir}/pstoedit/*.so.%{major}*

%files -n %{devname}
%doc doc/pstoedit.htm
%{_includedir}/pstoedit
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
