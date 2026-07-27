Name:           eza
Version:        0.23.5
Release:        1%{?dist}
Summary:        Modern replacement for ls written in Rust

License:        MIT AND Apache-2.0
URL:            https://github.com/eza-community/eza
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  pandoc

Requires:       bash

Obsoletes:      exa < 0.10.1-13

%global debug_package %{nil}

%description
eza is a modern replacement for ls with more features and better defaults.

%package zsh-completion
Summary: Zsh completion for eza
Requires: %{name} = %{version}-%{release}
Requires: zsh

%description zsh-completion
Zsh shell completion files for eza.

%package fish-completion
Summary: Fish completion for eza
Requires: %{name} = %{version}-%{release}
Requires: fish

%description fish-completion
Fish shell completion files for eza.

%prep
%autosetup -n %{name}-%{version}

%build
export CARGO_HOME=$PWD/.cargo
export CARGO_NET_RETRY=10

cargo build \
    --release \
    --locked

%check
cargo test \
    --release \
    --locked

%install

install -Dpm0755 \
    target/release/eza \
    %{buildroot}%{_bindir}/eza

install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5

pandoc -s -t man man/eza.1.md \
    -o %{buildroot}%{_mandir}/man1/eza.1

pandoc -s -t man man/eza_colors.5.md \
    -o %{buildroot}%{_mandir}/man5/eza_colors.5

pandoc -s -t man man/eza_colors-explanation.5.md \
    -o %{buildroot}%{_mandir}/man5/eza_colors-explanation.5

gzip -9 %{buildroot}%{_mandir}/man1/eza.1
gzip -9 %{buildroot}%{_mandir}/man5/*.5

install -Dpm0644 \
    LICENSE.txt \
    %{buildroot}%{_licensedir}/%{name}/LICENSE

install -Dpm0644 \
    completions/bash/eza \
    %{buildroot}%{_datadir}/bash-completion/completions/eza

install -Dpm0644 \
    completions/zsh/_eza \
    %{buildroot}%{_datadir}/zsh/site-functions/_eza

install -Dpm0644 \
    completions/fish/eza.fish \
    %{buildroot}%{_datadir}/fish/vendor_completions.d/eza.fish

%files
%license %{_licensedir}/%{name}/LICENSE
%doc README.md
%doc CHANGELOG.md
%doc INSTALL.md
%doc CONTRIBUTING.md
%doc CODE_OF_CONDUCT.md
%doc SECURITY.md

%{_bindir}/eza
%{_datadir}/bash-completion/completions/eza
%{_mandir}/man1/eza.1.gz
%{_mandir}/man5/eza_colors.5.gz
%{_mandir}/man5/eza_colors-explanation.5.gz

%files zsh-completion
%{_datadir}/zsh/site-functions/_eza

%files fish-completion
%{_datadir}/fish/vendor_completions.d/eza.fish

%changelog
* Mon Jul 27 2026 Your Name <you@example.com> - 0.23.5-1
- Initial package
