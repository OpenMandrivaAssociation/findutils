%ifnarch riscv64
%global optflags %{optflags} -O3 --rtlib=compiler-rt
%else
%global optflags %{optflags} -O3
%endif

Summary:	The GNU versions of find utilities (find and xargs)
Name:		findutils
Version:	4.9.0
Release:	3
License:	GPLv3
Group:		File tools
Url:		http://www.gnu.org/software/findutils/findutils.html
Source0:	https://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.xz
Patch0:		findutils-4.9.0-fix-clang.patch

# do not build locate
Patch1:		https://src.fedoraproject.org/rpms/findutils/raw/master/f/findutils-4.5.15-no-locate.patch
# add a new option -xautofs to find to not descend into directories on autofs file systems
Patch3:		https://src.fedoraproject.org/rpms/findutils/raw/master/f/findutils-4.4.2-xautofs.patch
# eliminate compile-time warnings
Patch4:		https://src.fedoraproject.org/rpms/findutils/raw/master/f/findutils-4.5.13-warnings.patch
# test-lock: disable the rwlock test
Patch10:	https://src.fedoraproject.org/rpms/findutils/raw/master/f/findutils-4.6.0-test-lock.patch
# implement the -noleaf option of find (#1252549)
Patch12:	https://src.fedoraproject.org/rpms/findutils/raw/master/f/findutils-4.6.0-leaf-opt.patch

BuildRequires:	texinfo
BuildRequires:	gettext-devel

%description
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a filename pattern). The xargs utility builds and executes
command lines from standard input arguments (usually lists of file
names generated by the find command).

You should install findutils because it includes tools that are very
useful for finding things on your system.

%prep
%autosetup -p1
rm -rf locate

%build
# Don't build or install locate because it conflicts with slocate,
# which is a secure version of locate.
sed -i '/^SUBDIRS/s/locate//' Makefile.in
libtoolize --copy --force
autoreconf -fiv

%configure \
	--enable-leaf-optimisation \
	--enable-d_type-optimization \
	--with-packager="%{vendor}" \
	--with-packager-bug-reports="%{bugurl}" \
	--with-fts

%make_build

%check
# fails because they need py2
make check

%install
%make_install
%find_lang %{name}

%files -f %{name}.lang
%doc NEWS README
%{_bindir}/find
%{_bindir}/xargs
%doc %{_mandir}/man1/find.1*
%doc %{_mandir}/man1/xargs.1*
%doc %{_infodir}/find*
