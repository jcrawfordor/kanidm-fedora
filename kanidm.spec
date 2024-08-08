#
# spec file for package kanidm
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Name:           kanidm
Version: 1.3.1
Release:        1%{?dist}
Summary:        A identity management service and clients.
License:        ( Apache-2.0 OR BSL-1.0 ) AND ( Apache-2.0 OR ISC OR MIT ) AND ( Apache-2.0 OR MIT ) AND ( Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT ) AND ( CC0-1.0 OR Apache-2.0 ) AND ( MIT OR Apache-2.0 OR Zlib ) AND ( Unlicense OR MIT ) AND ( Zlib OR Apache-2.0 OR MIT ) AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND ISC AND MIT AND MPL-2.0 AND MPL-2.0+
URL:            https://github.com/kanidm/kanidm
Source0:        https://github.com/kanidm/kanidm/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo >= 1.69.0
BuildRequires:  libselinux-devel
BuildRequires:  libudev-devel
BuildRequires:  pam-devel
BuildRequires:  sqlite-devel
BuildRequires:  zstd

BuildRequires:  clang
BuildRequires:  openssl-devel
BuildRequires:  systemd
%{?systemd_requires}

Requires:       %{name}-clients
Requires:       %{name}-unixd-clients

ExclusiveArch:  x86_64 aarch64

%description
An identity management platform written in rust that supports RADIUS, SSH Key management
and more.

%package clients
Summary:        Client tools for interacting with Kanidm
License:        MPL-2.0

%description clients
Client utilities for interactive with kanidm servers

%package server
Summary:        Kanidm server and related tools
License:        MPL-2.0
Requires:       %{name}-clients

%description server
Server for kanidm providing the main authentication and identity service

%package unixd-clients
Summary:        Client nsswitch/pam/ssh integration for consuming kanidm
License:        MPL-2.0
Requires:       %{name}-clients
Requires:       tpm2-tools

%description unixd-clients
A localhost resolver and libraries that allow a system to resolve posix
identities to a kanidm instance.

%package docs
Summary:        Documentation for Kanidm Administration
License:        MPL-2.0

%description docs
Documentation for using and configuring Kanidm.

%define configdir %{_sysconfdir}/%{name}

%prep
%autosetup -n %{name}-%{version}

%build
# Set our build profile, this will autodetect our cpu flags
export KANIDM_BUILD_PROFILE=release_suse_generic
# Show linking info for debugging
# export RUSTC_LOG='rustc_codegen_ssa::back::link=info'
# Dump the target features of this cpu.
rustc --print target-cpus

cargo build --release --features=kanidm_unix_int/selinux

%install
install -D -d -m 0755 %{buildroot}%{_sysconfdir}
install -D -d -m 0755 %{buildroot}%{_sysconfdir}/zsh_completion.d
install -D -d -m 0755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -D -d -m 0755 %{buildroot}%{configdir}
install -D -d -m 0755 %{buildroot}%{_unitdir}
install -D -d -m 0755 %{buildroot}%{_sbindir}
install -D -d -m 0755 %{buildroot}%{_bindir}
install -D -d -m 0755 %{buildroot}%{_libdir}

install -D -d -m 0755 %{buildroot}/%_lib/security
install -D -d -m 0755 %{buildroot}%{_datadir}/kanidm
install -D -d -m 0755 %{buildroot}%{_datadir}/kanidm/docs/
install -D -d -m 0755 %{buildroot}%{_datadir}/kanidm/ui/

install -m 0755 %{_builddir}/%{name}-%{version}/target/release/kanidmd %{buildroot}%{_sbindir}/kanidmd
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/kanidm %{buildroot}%{_bindir}/kanidm
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/kanidm-unix %{buildroot}%{_sbindir}/kanidm-unix
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/kanidm_ssh_authorizedkeys %{buildroot}%{_sbindir}/kanidm_ssh_authorizedkeys
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/kanidm_ssh_authorizedkeys_direct %{buildroot}%{_sbindir}/kanidm_ssh_authorizedkeys_direct
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/kanidm_unixd %{buildroot}%{_sbindir}/kanidm_unixd
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/kanidm_unixd_tasks %{buildroot}%{_sbindir}/kanidm_unixd_tasks
install -m 0644 %{_builddir}/%{name}-%{version}/target/release/libnss_kanidm.so %{buildroot}%{_libdir}/libnss_kanidm.so.2

install -m 0644 %{_builddir}/%{name}-%{version}/target/release/libpam_kanidm.so %{buildroot}/%_lib/security/pam_kanidm.so

install -m 0644 %{_builddir}/%{name}-%{version}/platform/opensuse/kanidmd.service %{buildroot}%{_unitdir}/kanidmd.service
install -m 0644 %{_builddir}/%{name}-%{version}/platform/opensuse/kanidm-unixd.service %{buildroot}%{_unitdir}/kanidm-unixd.service
install -m 0644 %{_builddir}/%{name}-%{version}/platform/opensuse/kanidm-unixd-tasks.service %{buildroot}%{_unitdir}/kanidm-unixd-tasks.service
install -m 0644 %{_builddir}/%{name}-%{version}/examples/server.toml %{buildroot}%{configdir}/server.toml

install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/_kanidmd   %{buildroot}%{_sysconfdir}/zsh_completion.d/_kanidmd
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/_kanidm   %{buildroot}%{_sysconfdir}/zsh_completion.d/_kanidm
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/_kanidm_ssh_authorizedkeys_direct   %{buildroot}%{_sysconfdir}/zsh_completion.d/_kanidm_ssh_authorizedkeys_direct
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/_kanidm_unix   %{buildroot}%{_sysconfdir}/zsh_completion.d/_kanidm_unix
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/_kanidm_ssh_authorizedkeys   %{buildroot}%{_sysconfdir}/zsh_completion.d/_kanidm_ssh_authorizedkeys

install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/kanidmd.bash %{buildroot}%{_sysconfdir}/bash_completion.d/kanidmd.sh
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/kanidm.bash %{buildroot}%{_sysconfdir}/bash_completion.d/kanidm.sh
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/kanidm_ssh_authorizedkeys_direct.bash %{buildroot}%{_sysconfdir}/bash_completion.d/kanidm_ssh_authorizedkeys_direct.sh
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/kanidm_unix.bash %{buildroot}%{_sysconfdir}/bash_completion.d/kanidm_unix.sh
install -m 0755 %{_builddir}/%{name}-%{version}/target/release/build/completions/kanidm_ssh_authorizedkeys.bash %{buildroot}%{_sysconfdir}/bash_completion.d/kanidm_ssh_authorizedkeys.sh

cp -r %{_builddir}/%{name}-%{version}/book/src/ %{buildroot}%{_datadir}/kanidm/docs/
cp -r %{_builddir}/%{name}-%{version}/server/web_ui/pkg %{buildroot}%{_datadir}/kanidm/ui/pkg

## End install

%post server
%systemd_post kanidmd.service

%preun server
%systemd_preun kanidmd.service

%postun server
%systemd_postun_with_restart kanidmd.service

%post unixd-clients
%systemd_post kanidm-unixd.service
%systemd_post kanidm-unixd-tasks.service

%preun unixd-clients
%systemd_preun kanidm-unixd.service
%systemd_preun kanidm-unixd-tasks.service

%postun unixd-clients
%systemd_postun_with_restart kanidm-unixd.service
%systemd_postun_with_restart kanidm-unixd-tasks.service

%files
%defattr(-,root,root)
# percent exclude /usr/.crates.toml

%files clients
%defattr(-,root,root)
%dir %{configdir}
%{_bindir}/kanidm
%dir %{_sysconfdir}/zsh_completion.d
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/zsh_completion.d/_kanidm
%{_sysconfdir}/bash_completion.d/kanidm.sh

%files server
%{_sbindir}/kanidmd
%{_unitdir}/kanidmd.service
%dir %{_datadir}/kanidm
%dir %{_datadir}/kanidm/ui
%dir %{_datadir}/kanidm/ui/pkg
%dir %{_datadir}/kanidm/ui/pkg/external
%{_datadir}/kanidm/ui/pkg/*
%{_datadir}/kanidm/ui/pkg/external/*
%dir %{configdir}
%config(noreplace) %{configdir}/server.toml
%dir %{_sysconfdir}/zsh_completion.d
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/zsh_completion.d/_kanidmd
%{_sysconfdir}/bash_completion.d/kanidmd.sh

%files unixd-clients
%{_libdir}/libnss_kanidm.so.2
%if 0%{?suse_version} > 1549
%{_pam_moduledir}/pam_kanidm.so
%else
/%_lib/security/pam_kanidm.so
%endif
%{_sbindir}/kanidm-unix
%{_sbindir}/kanidm_ssh_authorizedkeys
%{_sbindir}/kanidm_ssh_authorizedkeys_direct
%{_sbindir}/kanidm_unixd
%{_sbindir}/kanidm_unixd_tasks
%{_unitdir}/kanidm-unixd.service
%{_unitdir}/kanidm-unixd-tasks.service
%dir %{_sysconfdir}/zsh_completion.d
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/zsh_completion.d/_kanidm_ssh_authorizedkeys_direct
%{_sysconfdir}/zsh_completion.d/_kanidm_ssh_authorizedkeys
%{_sysconfdir}/zsh_completion.d/_kanidm_unix
%{_sysconfdir}/bash_completion.d/kanidm_ssh_authorizedkeys_direct.sh
%{_sysconfdir}/bash_completion.d/kanidm_ssh_authorizedkeys.sh
%{_sysconfdir}/bash_completion.d/kanidm_unix.sh

%files docs
%dir %{_datadir}/kanidm
%dir %{_datadir}/kanidm/docs
%doc %{_datadir}/kanidm/docs/*
