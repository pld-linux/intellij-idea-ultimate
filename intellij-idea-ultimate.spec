%define		product	idea
%define		proddir	%{product}-IU
%include	/usr/lib/rpm/macros.java
Summary:	IntelliJ IDEA - The Most Intelligent Java IDE
Name:		intellij-idea-ultimate
Version:	2019.1.2
Release:	1
License:	IntelliJ IDEA Commercial
Group:		Development/Tools
Source0:	http://download.jetbrains.com/idea/ideaIU-%{version}.tar.gz
# NoSource0-md5:	e6eb04ace9489c1b63ce40903871d917
NoSource:	0
Source1:	%{product}.desktop
Patch0:		xdg-paths.patch
URL:		http://www.jetbrains.org/
BuildRequires:	desktop-file-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.596
Requires:	%{name}-libs = %{version}-%{release}
Requires:	desktop-file-utils
Requires:	jre >= 1.8
%ifarch %{x8664}
Suggests:	%{name}-jre = %{version}-%{release}
%endif
Suggests:	java-jdbc-mysql
Suggests:	jdk >= 1.6
Suggests:	open
Suggests:	python
Conflicts:	intellij-idea
Conflicts:	java-jdbc-mysql < 5.1.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# disable debuginfo package, not useful
%define		_enable_debug_packages	0

# don't strip fsnotifier, it's size is checked for "outdated binary"
# https://bugs.archlinux.org/task/34703
# http://git.jetbrains.org/?p=idea/community.git;a=blob;f=platform/platform-impl/src/com/intellij/openapi/vfs/impl/local/FileWatcher.java;h=004311b96a35df1ffc2c87baba78a8b2a8809f7d;hb=376b939fd6d6ec4c12191a5f90503d9d62c501da#l173
%define		_noautostrip	.*/fsnotifier.*

# use /usr/lib, 64bit files do not conflict with 32bit files (64 suffix)
# this allows to install both arch files and to use 32bit jdk on 64bit os
%define		_appdir		%{_prefix}/lib/%{proddir}

# rpm5 is so damn slow, so i use this for development:
%define		_noautoreqfiles	.*\.jar

%description
IntelliJ IDEA is a code-centric IDE focused on developer productivity.
The editor deeply understands your code and knows its way around the
codebase, makes great suggestions right when you need them, and is
always ready to help you shape your code.

%package libs
Summary:	Libraries for IntelliJ IDEA
Group:		Libraries/Java
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description libs
Libraries for IntelliJ IDEA.

%package jre
Summary:	Bundled JRE recommended for running IntelliJ IDEA
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description jre
Bundled JRE recommended for running IntelliJ IDEA.

%prep
%setup -qc
mv %{proddir}-*/* .
%patch0 -p1

# keep only single arch files (don't want to pull 32bit deps by default),
# if you want to mix, install rpm from both arch
%ifarch %{ix86}
rm bin/%{product}64.vmoptions
rm bin/fsnotifier64
rm bin/libyjpagent-linux64.so
%endif
%ifarch %{x8664}
rm bin/%{product}.vmoptions
rm bin/fsnotifier
rm bin/libyjpagent-linux.so
%endif
rm bin/fsnotifier-arm
chmod a+rx bin/*.so bin/fsnotifier*
mv bin/%{product}.png .

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -l build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -a$l bin build.txt help lib license plugins $RPM_BUILD_ROOT%{_appdir}
%ifarch %{x8664}
cp -a$l jre64 $RPM_BUILD_ROOT%{_appdir}
%endif
cp -p %{product}.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{product}.png
ln -s %{_pixmapsdir}/%{product}.png $RPM_BUILD_ROOT%{_appdir}/bin/%{product}.png
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{product}.desktop
ln -s %{_appdir}/bin/%{product}.sh $RPM_BUILD_ROOT%{_bindir}/%{product}
rm -r $RPM_BUILD_ROOT%{_appdir}/lib/pty4j-native/linux/ppc64le

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{product}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

# base package contains arch specific files
%files
%defattr(644,root,root,755)
%doc Install-Linux-tar.txt
%attr(755,root,root) %{_bindir}/%{product}
%dir %{_appdir}/bin
%{_appdir}/bin/%{product}*.vmoptions
%{_appdir}/bin/%{product}.png
%{_appdir}/bin/%{product}.properties
%{_appdir}/bin/%{product}.svg
%{_appdir}/bin/appletviewer.policy
%{_appdir}/bin/log.xml
%attr(755,root,root) %{_appdir}/bin/%{product}.sh
%attr(755,root,root) %{_appdir}/bin/format.sh
%attr(755,root,root) %{_appdir}/bin/inspect.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier*
%attr(755,root,root) %{_appdir}/bin/libyjpagent*.so
%attr(755,root,root) %{_appdir}/bin/printenv.py
%attr(755,root,root) %{_appdir}/bin/restart.py
%ifarch %{x8664}
%attr(755,root,root) %{_appdir}/bin/libdbm64.so
%endif
%{_desktopdir}/%{product}.desktop
%{_pixmapsdir}/%{product}.png

# this package contains arch independant files
%files libs
%defattr(644,root,root,755)
%dir %{_appdir}
%{_appdir}/build.txt
%{_appdir}/lib
%{_appdir}/license
%{_appdir}/plugins
%{_appdir}/help

%ifarch %{x8664}
%files jre
%defattr(644,root,root,755)
%dir %{_appdir}/jre64
%dir %{_appdir}/jre64/bin
%attr(755,root,root) %{_appdir}/jre64/bin/clhsdb
%attr(755,root,root) %{_appdir}/jre64/bin/hsdb
%attr(755,root,root) %{_appdir}/jre64/bin/java
%attr(755,root,root) %{_appdir}/jre64/bin/jjs
%attr(755,root,root) %{_appdir}/jre64/bin/keytool
%attr(755,root,root) %{_appdir}/jre64/bin/orbd
%attr(755,root,root) %{_appdir}/jre64/bin/pack200
%attr(755,root,root) %{_appdir}/jre64/bin/policytool
%attr(755,root,root) %{_appdir}/jre64/bin/rmid
%attr(755,root,root) %{_appdir}/jre64/bin/rmiregistry
%attr(755,root,root) %{_appdir}/jre64/bin/servertool
%attr(755,root,root) %{_appdir}/jre64/bin/tnameserv
%attr(755,root,root) %{_appdir}/jre64/bin/unpack200
%{_appdir}/jre64/lib
%{_appdir}/jre64/ASSEMBLY_EXCEPTION
%{_appdir}/jre64/LICENSE
%{_appdir}/jre64/release
%{_appdir}/jre64/THIRD_PARTY_README
%endif
