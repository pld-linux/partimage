
# (g)id for partimaged
%define		_id		93

Summary:	Utility to save partitions in a compressed image file
Summary(pl):	Narzêdzie do zapisu partycji w skompresowanych plikach
Name:		partimage
Version:	0.7.0
Release:	1
License:	GPL
Vendor:		François Dupoux <fdupoux@partimage.org>
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://prdownloads.sourceforge.net/partimage/%{name}-%{version}.tar.bz2
Source1:	%{name}d.init
URL:		http://www.partimage.org/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	bzip2-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	gettext-devel
BuildRequires:	newt-devel
BuildRequires:	slang-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux/UNIX utility to save partitions in a compressed image file
Partition Image is a Linux/UNIX partition imaging utility: it saves
partitions in the:

  - Ext2FS   (the Linux standard)
  - ReiserFS (a new, powerful journalling file system)
  - NTFS     (Windows NT File System)
  - FAT16/32 (DOS & Windows file systems)
  - HPFS     (OS/2 File System)
  - JFS      (IBM Jounalized File System for AIX)
  - XFS      (SGI Jounalized File System for IRIX)
  - HFS      (Hierarchical File System for MacOS)
  - UFS      (*BSD, Solaris and NextStep file systems)

file system formats to an image file. Only used blocks are copied.
The image file can be compressed in the GZIP/BZIP2 formats to save
disk space, and splitted into multiple files to be copied on amovibles
floppies (ZIP for example), or burned on a CD-R ... This allows to 
save a full Linux/Windows system, with an only operation. When 
problems (viruses, crash, error, ...), you just have to restore, and
after several minutes, all your system is restored (boot, files, ...),
and fully working. This is very useful when installing the same
software on many machines: just install one of them, create an image,
and just restore the image on all other machines. Then, after the
first one, each installation is automatically made, and only require
a few minutes.

%description -l pl
Narzêdzie Linuksowe do zapisywania partycji w skompresowanych plikach.
Potrafi ono zapisywaæ partycje ext2, ReiserFS, NTFS, FAT16/32, HPFS,
XFS, JFS, HFS, UFS. Kopiowane s± tylko u¿ywane bloki. Plik wyj¶ciowy
mo¿e byæ podzielony na wiele mniejszych oraz kompresowany w formacie
gzip/bzip2 w celu zaoszczêdzenia miejsca.


%package server
Summary:	Partimage server
Summary(pl):	Partimage server
Group:		Applications/System
Requires:	%{name} = %{version}

%description server
Server for Partimage. Very alpha stage, don't use it!

%description server -l pl
Server dla Partimage.

%prep
%setup -q

%build
rm missing
gettextize --copy --force
aclocal -I macros
autoconf
automake -a -c

%configure \
	--enable-nls \
	--without-included-gettext \
	--disable-ssl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	DESTDIR=$RPM_BUILD_ROOT \
	install \

%{__make} -C po \
	DESTDIR=$RPM_BUILD_ROOT \
	install

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/partimaged
cat > $RPM_BUILD_ROOT/%{_sysconfdir}/partimaged/partimagedusers << EOF
#note, '#' intruduces comments
#add only users allowed to connect to partimaged
# (only one login per line)

#joe # user 'joe' is allowed to coonnect to partimaged
EOF
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/partimaged

gzip -9nf AUTHORS BOOT* ChangeLog README* THANKS TODO BUGS

%find_lang %{name}

%pre server
if [ -n "`/usr/bin/getgid partimag`" ]; then
	if [ "`/usr/bin/getgid partimag`" != "%{_id}" ]; then
		echo "Warning: group partimag hasn't gid=%{_id}. Correct this before installing partimage." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g %{_id} -r -f partimag
fi
if [ -n "`/bin/id -u partimag 2>/dev/null`" ]; then
	if [ "`/bin/id -u partimag`" != "%{_id}" ]; then
		echo "Warning: user partimag hasn't uid=%{_id}. Corrent this before installing partimage." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u %{_id} -r -d /etc/partimaged -s /bin/false -c "Partimage server" -g partimag partimag 1>&2
fi

%post server
/sbin/chkconfig --add partimaged
if [ -f /var/lock/subsys/partimage ]; then
	/etc/rc.d/init.d/partimage restart >&2
else
	echo "Run \"/etc/rc.d/init.d/partimage start\" to start partimage server." >&2
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/partimage ]; then
		/etc/rc.d/init.d/partimage stop >&2
	fi
	/sbin/chkconfig --del partimaged
fi

%postun server
if [ $1 = 0 ]; then
	/usr/sbin/userdel partimag 2>/dev/null
	/usr/sbin/groupdel partimag 2>/dev/null
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {AUTHORS,BOOT*,ChangeLog,README,THANKS,TODO,BUGS}.gz
%attr(755,root,root) %{_sbindir}/*

%files server
%defattr(644,root,root,755)
%doc README.partimaged.gz
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/partimaged
%dir %{_sysconfdir}/partimaged
%attr(600,partimag,root) %config(noreplace) %{_sysconfdir}/partimaged/partimagedusers
