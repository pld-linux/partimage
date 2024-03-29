Summary:	Utility to save partitions in a compressed image file
Summary(pl.UTF-8):	Narzędzie do zapisu partycji w skompresowanych plikach
Summary(pt_BR.UTF-8):	Ferramenta para criar e restaurar backup de partições
Name:		partimage
Version:	0.6.9
Release:	6
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/partimage/%{name}-%{version}.tar.bz2
# Source0-md5:	1bc046fd915c5debbafc85729464e513
Source1:	%{name}d.init
Source2:	%{name}d.sysconfig
Source3:	%{name}d.pam
Source4:	%{name}d-ssl.cnf
Patch0:		%{name}-fix_debug.patch
Patch1:		%{name}-descr.patch
Patch2:		%{name}-gzFile.patch
Patch3:		02-openssl.patch
Patch4:		03-openssl11.patch
Patch5:		build.patch
URL:		http://www.partimage.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	gettext-tools
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	newt-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	slang-devel >= 2.0.0
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

%description -l pl.UTF-8
Narzędzie linuksowe do zapisywania partycji w skompresowanych plikach.
Potrafi ono zapisywać partycje:
  - Ext2FS (linuksowy standard),
  - ReiserFS (nowy, potężny system plików z journalem),
  - NTFS (system plików Windows NT),
  - FAT16/32 (system plików DOS i Windows),
  - HPFS (system plików OS/2),
  - XFS (system plików z journalem IBM-a dla AIX),
  - JFS (system plików z journalem SGI dla IRIX-a),
  - HFS (hierarchiczny system plików dla MacOS),
  - UFS (system plików *BSD, Solarisa oraz NextStepa).

Kopiowane sątylko używane bloki. Plik wyjściowy może być podzielony na
wiele mniejszych oraz kompresowany w formacie gzip/bzip2 w celu
zaoszczędzenia miejsca. Pozwala to na zapis całego systemu
Linux/Windows w pojedynczej operacji. W razie problemów (wirusy,
błędy, awaria...) należy po prostu przywrócić system i po kilku
minutach całość jest znowu sprawna. Jest to bardzo użyteczne przy
instalowaniu tego samego na wielu maszynach: wystarczy zainstalować na
jednej z nich, zrobić obraz i przywrócić na pozostałych maszynach. Po
pierwszej instalacji każda następna wymaga tylko kilku minut.

%package server
Summary:	Partimage server
Summary(pl.UTF-8):	Serwer Partimage
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-tools
Provides:	group(partimag)
Provides:	user(partimag)

%description server
Server for Partimage.

%description server -l pl.UTF-8
Server dla Partimage.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-pam \
	--enable-ssl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{partimaged,pam.d},/etc/rc.d/init.d,/etc/sysconfig,/var/spool/partimage}

%{__make} -C src install \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C po install \
	DESTDIR=$RPM_BUILD_ROOT

cat > $RPM_BUILD_ROOT%{_sysconfdir}/partimaged/partimagedusers << EOF
#note, '#' intruduces comments
#add only users allowed to connect to partimaged
# (only one login per line)

#joe # user 'joe' is allowed to connect to partimaged
EOF

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/partimaged
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/partimaged
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/partimaged
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/partimaged/partimaged.cnf

touch $RPM_BUILD_ROOT%{_sysconfdir}/partimaged/partimaged.{csr,cert,key}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
%groupadd -P %{name}-server -g 98 partimag
%useradd -P %{name}-server -u 98 -d %{_sysconfdir}/partimaged -s /bin/false -c "Partimage server" -g partimag partimag

%post server
/sbin/chkconfig --add partimaged
if [ ! -s /etc/partimaged/partimaged.key -o ! -s /etc/partimaged/partimaged.cert ]; then
	echo "Run \"/etc/rc.d/init.d/partimaged init\" to create self-signed SSL certificate." >&2
fi

if [ -f /var/lock/subsys/partimaged ]; then
	/etc/rc.d/init.d/partimaged restart >&2
else
	echo "Run \"/etc/rc.d/init.d/partimaged start\" to start partimage server." >&2
fi

echo

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/partimaged ]; then
		/etc/rc.d/init.d/partimaged stop >&2
	fi
	/sbin/chkconfig --del partimaged
fi

%postun server
if [ "$1" = "0" ]; then
	%userremove partimag
	%groupremove partimag
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README* THANKS BUGS
%attr(755,root,root) %{_sbindir}/partimage

%files server
%defattr(644,root,root,755)
%doc README.partimaged
%attr(755,root,root) %{_sbindir}/partimaged
%attr(754,root,root) /etc/rc.d/init.d/partimaged
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/partimaged
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/partimaged
%dir %{_sysconfdir}/partimaged
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/partimaged/partimaged.cnf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/partimaged/partimaged.csr
%attr(600,partimag,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/partimaged/partimaged.key
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/partimaged/partimaged.cert
%attr(600,partimag,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/partimaged/partimagedusers
%attr(700,partimag,root) %dir /var/spool/partimage
