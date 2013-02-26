%define	major	0
%define	libname	%mklibname pstoedit %{major}
%define	devname	%mklibname pstoedit -d

Summary:	Translates PostScript/PDF graphics into other vector formats
Name:		pstoedit
Version:	3.61
Release:	2
License:	GPLv2+
Source0:	http://prdownloads.sourceforge.net/pstoedit/%{name}-%{version}.tar.gz
URL:		http://www.pstoedit.net/pstoedit
Group:		Graphics
BuildRequires:	bison
BuildRequires:	ghostscript
BuildRequires:	pkgconfig(ImageMagick)
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


%changelog
* Sat Jun 16 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 3.60-1
+ Revision: 805979
- add version to license
- use %%{EVRD}
- use %%rename macro
- drop excessive provides/requires
- cleanups
- fix %%files
- drop libtool files
- new version

* Thu Jul 15 2010 Funda Wang <fwang@mandriva.org> 3.50-3mdv2011.0
+ Revision: 553470
- rebuild for new imagemagick

* Thu Jan 14 2010 Funda Wang <fwang@mandriva.org> 3.50-2mdv2010.1
+ Revision: 491445
- rebuild for new imagemagick

* Tue Jan 05 2010 Luc Menut <lmenut@mandriva.org> 3.50-1mdv2010.1
+ Revision: 486514
- update to version 3.50
  update source URL
  drop gcc-4.3 patch
  rediff module-build patch

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Jan 30 2009 Funda Wang <fwang@mandriva.org> 3.45-7mdv2009.1
+ Revision: 335485
- new devel package name policy
- drop verison from modules
- add gcc 4.3 patch

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Apr 22 2008 Lev Givon <lev@mandriva.org> 3.45-5mdv2009.0
+ Revision: 196624
- Add plotutils-devel build dependency to ensure svg support.

  + Funda Wang <fwang@mandriva.org>
    - add buildroot
    - rebuild

* Tue Jan 22 2008 Lev Givon <lev@mandriva.org> 3.45-3mdv2008.1
+ Revision: 156013
- Rebuild against updated plotutils so as to provide svg support.

* Tue Jan 08 2008 Oden Eriksson <oeriksson@mandriva.com> 3.45-2mdv2008.1
+ Revision: 146515
- rebuilt against new imagemagick libs (6.3.7)

* Thu Dec 27 2007 Jérôme Soyer <saispo@mandriva.org> 3.45-1mdv2008.1
+ Revision: 138401
- New release

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Feb 24 2007 Emmanuel Andry <eandry@mandriva.org> 3.44-2mdv2007.0
+ Revision: 125338
- rebuild for latest ImageMagick

* Mon Jan 15 2007 Lenny Cartier <lenny@mandriva.com> 3.44-1mdv2007.1
+ Revision: 109213
- Update to 3.44
- Import pstoedit

* Sat Oct 01 2005 Lenny Cartier <lenny@mandriva.com> 3.42-1mdk
- 3.42

* Fri Sep 02 2005 Marcel Pol <mpol@mandriva.org> 3.40-7mdk
- rebuild for new ImageMagick

* Wed Aug 17 2005 Abel Cheung <deaddog@mandriva.org> 3.40-6mdk
- Abandon autogen.sh completely in favor of autoreconf, so patch0
  can be dropped
- Patch2: eliminate automake complaining about unquoted m4 macros

* Wed Aug 17 2005 Michael Scherer <misc@mandriva.org> 3.40-5mdk
- Rebuild for lack of libdpstk.so.1

* Sat Aug 06 2005 Giuseppe Ghibò <ghibo@mandriva.com> 3.40-4mdk
- Rebuilt against latest ImageMagick.
- Rebuilt Patch0 for aclocal-1.9.

* Sat Jul 30 2005 Lenny Cartier <lenny@mandriva.com> 3.40-3mdk
- rebuild for dependencies

* Sun May 08 2005 Giuseppe Ghibò <ghibo@mandriva.com> 3.40-2mdk
- Fixed BuildConflicts for x86-64.

* Sat Mar 19 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.40-1mdk
- Release 3.40.

* Sat Feb 05 2005 Abel Cheung <deaddog@mandrake.org> 3.33-9mdk
- rebuild

* Mon Jan 17 2005 Abel Cheung <deaddog@mandrake.org> 3.33-8mdk
- rebuild

* Wed Dec 15 2004 Abel Cheung <deaddog@deaddog.org> 3.33-7mdk
- rebuild

* Sun Aug 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.33-6mdk
- Rebuilt against ImageMagick 6.0.4.

* Wed Jun 30 2004 Abel Cheung <deaddog@deaddog.org> 3.33-5mdk
- P0: Fix build
- P1: Allow parallel build
- Add missing buildrequires
- Other build cleanup

