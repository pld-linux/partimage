Summary:	Utility to save partitions in a compressed image file
Summary(pl):	Narzêdzie do zapisu partycji w skompresowanych plikach
Name:		partimage
Version:	0.3.6
Release:	1
License:	GPL
Vendor:		François Dupoux <fdupoux@partimage.org>
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://prdownloads.sourceforge.net/partimage/%{name}-%{version}.tar.gz
URL:		http://www.partimage.org/
BuildRequires:	e2fsprogs-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	newt-devel
BuildRequires:	slang-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	gettext-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux/UNIX utility to save partitions in a compressed image file
Partition Image is a Linux/UNIX partition imaging utility: it saves
partitions in the Ext2FS (the linux standard), ReiserFS (a new
journalized and powerful file system), NTFS (Windows NT File System)
or FAT16/32 (DOS & Windows file systems), file system formats to an
image file. Only used blocks are copied. The image file can be
compressed in the GZIP/BZIP2 formats to save disk space, and splitted
into multiple files to be copied on amovibles floppies (ZIP for
example), or burned on a CD-R ... This allows to save a full
Linux/Windows system, with an only operation. When problems (viruses,
crash, error, ...), you just have to restore, and after several
minutes, all your system is restored (boot, files, ...), and fully
working. This is very useful when installing the same software on many
machines: just install one of them, create an image, and just restore
the image on all other machines. Then, after the first one, each
installation is automatically made, and only require a few minutes.

%description -l pl
Narzêdzie Linuksowe do zapisywania partycji w skompresowanych plikach.
Potrafi ono zapisywaæ partycje ext2, ReiserFS, NTFS, FAT16/32. Tylko
u¿ywane bloki s± kopiowane. Plik wyj¶ciowy mo¿e byæ podzielony na
wiele mniejszych oraz kompresowany w formacie gzip/bzip2 w celu
zaoszczêdzenia miejsca.

%prep
%setup -q

%build
rm missing
gettextize --copy --force
aclocal
autoconf
automake -a -c
%configure \
	--enable-nls \
	--without-included-gettext
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/html .

gzip -9nf AUTHORS BOOT* ChangeLog README THANKS TODO

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz html
%attr(755,root,root) %{_sbindir}/*
