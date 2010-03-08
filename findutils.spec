Summary:	The GNU versions of find utilities (find and xargs)
Name:		findutils
Version:	4.5.5
Release:	%mkrel 1
License:	GPLv3
Group:		File tools
URL:		http://www.gnu.org/software/findutils/findutils.html
Source0:	ftp://ftp.gnu.org/pub/gnu/findutils/findutils-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Requires(post):	info-install
Requires(preun): info-install
BuildRequires:	gettext-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

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
%setup -q

%build
%configure2_5x \
	--disable-rpath \
	--enable-leaf-optimisation \
	--enable-d_type-optimization \
	--with-fts

%make

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}/bin
mv %{buildroot}%{_bindir}/find %{buildroot}/bin
ln -sf ../../bin/find %{buildroot}%{_bindir}/find

%{find_lang} %{name}

%post
%_install_info find.info

%preun
%_remove_install_info find.info

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc NEWS README
/bin/find
%{_bindir}/find
%{_bindir}/oldfind
%{_bindir}/xargs
%{_mandir}/man1/find.1*
%{_mandir}/man1/xargs.1*
%{_infodir}/find*
%{_bindir}/locate
%{_bindir}/updatedb
%{_libdir}/bigram
%{_libdir}/code
%{_libdir}/frcode
%{_mandir}/man1/locate.1.lzma
%{_mandir}/man1/updatedb.1.lzma
%{_mandir}/man5/locatedb.5.lzma
