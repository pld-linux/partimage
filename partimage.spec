
# [ug]id for partimaged
%define		_id		98

Summary:	Utility to save partitions in a compressed image file
Summary(pl):	Narz�dzie do zapisu partycji w skompresowanych plikach
Summary(pt_BR):	Ferramenta para criar e restaurar backup de parti��es
Name:		partimage
Version:	0.6.2
Release:	1
License:	GPL v2
Vendor:		Fran�ois Dupoux <fdupoux@partimage.org>
Group:		Applications/System
Source0:	http://dl.sourceforge.net/partimage/%{name}-%{version}.tar.bz2
# Source0-md5:	c52ca81f23876cf9baa0dfcaa44d52ac
Source1:	%{name}d.init
Source2:	%{name}d.sysconfig
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

  - Ext2FS (the Linux standard)
  - ReiserFS (a new, powerful journalling file system)
  - NTFS (Windows NT File System)
  - FAT16/32 (DOS & Windows file systems)
  - HPFS (OS/2 File System)
  - JFS (IBM Jounalized File System for AIX)
  - XFS (SGI Jounalized File System for IRIX)
  - HFS (Hierarchical File System for MacOS)
  - UFS (*BSD, Solaris and NextStep file systems)

file system formats to an image file. Only used blocks are copied. The
image file can be compressed in the GZIP/BZIP2 formats to save disk
space, and splitted into multiple files to be copied on amovibles
floppies (ZIP for example), or burned on a CD-R ... This allows to
save a full Linux/Windows system, with an only operation. When
problems (viruses, crash, error, ...), you just have to restore, and
after several minutes, all your system is restored (boot, files, ...),
and fully working. This is very useful when installing the same
software on many machines: just install one of them, create an image,
and just restore the image on all other machines. Then, after the
first one, each installation is automatically made, and only require a
few minutes.

%description -l pl
Narz�dzie Linuksowe do zapisywania partycji w skompresowanych plikach.
Potrafi ono zapisywa� partycje
   - Ext2FS (linuksowy standard),
   - ReiserFS (nowy, pot�ny system plik�w z journalem),
   - NTFS (system plik�w Windows NT),
   - FAT16/32 (system plik�w DOS i Windows),
   - HPFS (system plik�w OS/2),
   - XFS (system plik�w z journalem IBM-a dla AIX),
   - JFS (system plik�w z journalem SGI dla IRIX-a),
   - HFS (hierarchiczny system plik�w dla MacOS),
   - UFS (system plik�w *BSD, Solarisa oraz NextStepa).
Kopiowane s� tylko u�ywane bloki. Plik wyj�ciowy mo�e by� podzielony
na wiele mniejszych oraz kompresowany w formacie gzip/bzip2 w celu
zaoszcz�dzenia miejsca. Pozwala to na zapis ca�ego systemu
Linux/Windows w pojedy�czej operacji. W razie problem�w (wirusy,
b��dy, awaria...) nale�y po prostu przywr�ci� system i po kilku
minutach ca�o�� jest znowy sprawna. Jest to bardzo u�yteczne przy
instalowaniu tego samego na wielu maszynach: wystarczy zainstalowa� na
jednej z nich, zrobi� obraz i przywr�ci� na pozosta�ych maszynach. Po
pierwszej instalacji ka�da nast�pna wymaga tylko kilku minut.

%package server
Summary:	Partimage server
Summary(pl):	Serwer Partimage
Group:		Applications/System
Requires:	%{name} = %{version}
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post,preun):/sbin/chkconfig

%description server
Server for Partimage. Very alpha stage, don't use it!!

%description server -l pl
Server dla Partimage. Nie u�ywaj, bardzo wczesna wersja!!

%prep
%setup -q

%build
rm -f missing
%{__gettextize}
%{__aclocal} -I macros
%{__autoconf}
%{__automake}

%configure \
	--enable-nls \
	--without-included-gettext \
	--disable-ssl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sysconfdir}/partimaged,/etc/rc.d/init.d,/etc/sysconfig}

%{__make} -C src install \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C po install \
	DESTDIR=$RPM_BUILD_ROOT

cat > $RPM_BUILD_ROOT%{_sysconfdir}/partimaged/partimagedusers << EOF
#note, '#' intruduces comments
#add only users allowed to connect to partimaged
# (only one login per line)

#joe # user 'joe' is allowed to coonnect to partimaged
EOF

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/partimaged
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/partimaged

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

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
	/usr/sbin/useradd -u %{_id} -r -d %{_sysconfdir}/partimaged -s /bin/false -c "Partimage server" -g partimag partimag 1>&2
fi

%post server
/sbin/chkconfig --add partimaged
if [ -f /var/lock/subsys/partimaged ]; then
	/etc/rc.d/init.d/partimaged restart >&2
else
	echo "Run \"/etc/rc.d/init.d/partimaged start\" to start partimage server." >&2
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/partimaged ]; then
		/etc/rc.d/init.d/partimaged stop >&2
	fi
	/sbin/chkconfig --del partimaged
fi

%postun server
if [ "$1" = "0" ]; then
	/usr/sbin/userdel partimag 2>/dev/null
	/usr/sbin/groupdel partimag 2>/dev/null
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BOOT* ChangeLog README* THANKS TODO BUGS
%attr(755,root,root) %{_sbindir}/partimage

%files server
%defattr(644,root,root,755)
%doc README.partimaged
%attr(755,root,root) %{_sbindir}/partimaged
%attr(754,root,root) /etc/rc.d/init.d/partimaged
%dir %{_sysconfdir}/partimaged
%attr(600,partimag,root) %config(noreplace) %{_sysconfdir}/partimaged/partimagedusers
