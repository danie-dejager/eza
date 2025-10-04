Name:           eza
Version:        0.23.4
Release:        1%{?dist}
Summary:        Modern replacement for ls written in Rust

License:        MIT AND Apache-2.0 
URL:            https://github.com/eza-community/eza
Source0:        https://github.com/eza-community/eza/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  pandoc
Requires:       bash

Obsoletes:      exa < 0.10.1-13

%global debug_package %{nil}

%description
eza is a modern replacement for ls with more features and better defaults.

%package zsh-completion
Summary:        Zsh completion for eza
Requires:       zsh
Requires:       %{name}

%description zsh-completion
This package contains zsh shell completions for eza.

%package fish-completion
Summary:        Fish shell completion for eza
Requires:       fish
Requires:       %{name}

%description fish-completion
This package contains fish shell completions for eza.

%prep
%autosetup

%build
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo build --release

%check
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo test --release --all --locked

%install
install -Dm755 target/release/eza %{buildroot}%{_bindir}/eza
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
pandoc -s -t man man/eza.1.md -o %{buildroot}%{_mandir}/man1/eza.1
pandoc -s -t man man/eza_colors.5.md -o %{buildroot}%{_mandir}/man5/eza_colors.5
pandoc -s -t man man/eza_colors-explanation.5.md -o %{buildroot}%{_mandir}/man5/eza_colors-explanation.5
gzip -9 %{buildroot}%{_mandir}/man?/*
install -Dm644 LICENSE.txt %{buildroot}%{_licensedir}/%{name}/LICENSE

# Bash completion
install -Dm644 completions/bash/eza \
  %{buildroot}%{_datadir}/bash-completion/completions/eza

# Zsh completion
install -Dm644 completions/zsh/_eza \
  %{buildroot}%{_datadir}/zsh/site-functions/_eza

# Fish completion
install -Dm644 completions/fish/eza.fish \
  %{buildroot}%{_datadir}/fish/vendor_completions.d/eza.fish

%files
%license %{_licensedir}/%{name}/LICENSE
%doc CHANGELOG.md
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc INSTALL.md
%doc README.md
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
