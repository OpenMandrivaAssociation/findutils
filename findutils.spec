%global optflags %{optflags} -O3

Summary:	The GNU versions of find utilities (find and xargs)
Name:		findutils
Version:	4.6.0
Release:	3
License:	GPLv3
Group:		File tools
Url:		http://www.gnu.org/software/findutils/findutils.html
Source0:	ftp://alpha.gnu.org/gnu/findutils/%{name}-%{version}.tar.gz

# prevent mbrtowc tests from failing (#1294016)
Patch0:		findutils-4.6.0-mbrtowc-tests.patch
# do not build locate
Patch1:		findutils-4.5.15-no-locate.patch
# fix build failure with glibc-2.28
# https://lists.gnu.org/r/bug-gnulib/2018-03/msg00000.html
Patch2:		findutils-4.6.0-gnulib-fflush.patch
# add a new option -xautofs to find to not descend into directories on autofs
# file systems
Patch3:		findutils-4.4.2-xautofs.patch
# eliminate compile-time warnings
Patch4:		findutils-4.5.13-warnings.patch
# clarify exit status handling of -exec cmd {} + in find(1) man page (#1325049)
Patch5:		findutils-4.6.0-man-exec.patch
# make sure that find -exec + passes all arguments (upstream bug #48030)
Patch6:		findutils-4.6.0-exec-args.patch
# fix build failure with glibc-2.25+
Patch7: findutils-4.6.0-gnulib-makedev.patch
# avoid SIGSEGV in case the internal -noop option is used (#1346471)
Patch9:		findutils-4.6.0-internal-noop.patch
# test-lock: disable the rwlock test
Patch10:	findutils-4.6.0-test-lock.patch
# import gnulib's FTS module from upstream commit 281b825e (#1544429)
Patch11:	findutils-4.6.0-fts-update.patch
# implement the -noleaf option of find (#1252549)
Patch12:	findutils-4.6.0-leaf-opt.patch
# fix programming mistakes detected by static analysis
Patch13:	findutils-4.6.0-covscan.patch

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
%apply_patches

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
#make check

%install
%make_install

install -d %{buildroot}/bin
mv %{buildroot}%{_bindir}/find %{buildroot}/bin
ln -sf ../../bin/find %{buildroot}%{_bindir}/find
# (tpg) compat symlink
ln -sf ../../bin/find %{buildroot}%{_bindir}/oldfind

%find_lang %{name}

%files -f %{name}.lang
%doc NEWS README
/bin/find
%{_bindir}/find
%{_bindir}/oldfind
%{_bindir}/xargs
%{_mandir}/man1/find.1*
%{_mandir}/man1/xargs.1*
%{_infodir}/find*
