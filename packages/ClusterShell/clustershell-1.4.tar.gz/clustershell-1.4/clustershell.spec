%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:          clustershell
Version:       1.4
Release:       1%{?dist}
Summary:       Python framework for efficient cluster administration

Group:         System Environment/Base
License:       CeCILL-C
URL:           http://clustershell.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:     noarch
BuildRequires: python-devel python-setuptools

%description
Tools and event-based Python library to execute commands on cluster nodes in
parallel depending on selected engine and worker mechanisms. The library
provides also advanced NodeSet and NodeGroups handling methods to ease and
improve administration of large compute clusters or server farms. Three
convenient command line utilities, clush, clubak and nodeset, allow traditional
shell scripts to benefit some useful features offered by the library.

%package -n vim-%{name}
Summary:       VIM files for ClusterShell
Group:         System Environment/Base
Requires:      clustershell = %{version}-%{release}, vim-common

%description -n vim-%{name}
Syntax highlighting in the VIM editor for ClusterShell configuration files.


%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# config files
install -d %{buildroot}/%{_sysconfdir}/clustershell
install -p -m 0644 conf/*.conf %{buildroot}/%{_sysconfdir}/clustershell/

# man pages
install -d %{buildroot}/%{_mandir}/{man1,man5}
install -p -m 0644 doc/man/man1/clubak.1 %{buildroot}/%{_mandir}/man1/
install -p -m 0644 doc/man/man1/clush.1 %{buildroot}/%{_mandir}/man1/
install -p -m 0644 doc/man/man1/nodeset.1 %{buildroot}/%{_mandir}/man1/
install -p -m 0644 doc/man/man5/clush.conf.5 %{buildroot}/%{_mandir}/man5/
install -p -m 0644 doc/man/man5/groups.conf.5 %{buildroot}/%{_mandir}/man5/

# vim addons
%define vimdatadir %{_datadir}/vim/vimfiles
install -d %{buildroot}/%{vimdatadir}/{ftdetect,syntax}
install -p -m 0644 doc/extras/vim/ftdetect/clustershell.vim %{buildroot}/%{vimdatadir}/ftdetect/
install -p -m 0644 doc/extras/vim/syntax/clushconf.vim %{buildroot}/%{vimdatadir}/syntax/
install -p -m 0644 doc/extras/vim/syntax/groupsconf.vim %{buildroot}/%{vimdatadir}/syntax/


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README ChangeLog Licence_CeCILL-C_V1-en.txt Licence_CeCILL-C_V1-fr.txt
%{_mandir}/man1/clubak.1*
%{_mandir}/man1/clush.1*
%{_mandir}/man1/nodeset.1*
%{_mandir}/man5/clush.conf.5*
%{_mandir}/man5/groups.conf.5*
%dir %{_sysconfdir}/clustershell
%config(noreplace) %{_sysconfdir}/clustershell/clush.conf
%config(noreplace) %{_sysconfdir}/clustershell/groups.conf
%{python_sitelib}/ClusterShell/
%{python_sitelib}/ClusterShell-*-py?.?.egg-info
%{_bindir}/clubak
%{_bindir}/clush
%{_bindir}/nodeset

%files -n vim-%{name}
%defattr(-,root,root,-)
%{vimdatadir}/ftdetect/clustershell.vim
%{vimdatadir}/syntax/clushconf.vim
%{vimdatadir}/syntax/groupsconf.vim

%changelog
* Sat Jan 15 2011 Stephane Thiell <stephane.thiell@cea.fr> 1.4-1
- update to 1.4

* Wed Oct 20 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3.3-1
- update to 1.3.3

* Fri Sep 10 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3.2-1
- renamed Vim subpackage to vim-clustershell
- update to 1.3.2

* Sun Sep 05 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3.1-2
- added -vim subpackage for .vim files

* Fri Sep 03 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3.1-1
- removed -n from setup line
- own clustershell config directory for proper uninstall
- install vim syntax addons in vimfiles, thus avoiding vim version detection
- update to 1.3.1

* Sun Aug 22 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3-4
- fixed BuildRoot tag in accordance with EPEL guidelines
- python_sitelib definition: prefer global vs define
- preserve timestamps and fix permissions when installing files

* Sat Aug 21 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3-3
- use a full URL to the package in Source0

* Fri Aug 20 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3-2
- various improvements per first review request

* Thu Aug 19 2010 Stephane Thiell <stephane.thiell@cea.fr> 1.3-1
- initial build candidate for Fedora
