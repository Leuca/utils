%global major 0
%global minor 0
%global patch 0

Name:           rpi-{{{ git_dir_name }}}
Version:        {{{ git_dir_version lead=%{major}.%{minor} follow=%{patch} }}}
Release:        1%{?dist}
Summary:        A collection of scripts and simple applications for Raspberry Pi

License:        BSD-3
URL:            https://github.com/raspberrypi/userland
VCS:            {{{ git_dir_vcs }}}

ExclusiveArch:  aarch64

BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  libfdt-devel

Conflicts:      rpi-userland

Provides:       vcgencmd

Source:         {{{ git_dir_pack }}}

Patch0:         rpi-utils-drop-apt-command.patch

%description
A collection of scripts and simple applications for the Raspberry Pi including:
  * dtmerge - A tool for applying compiled DT overlays (*.dtbo) to base Device Tree files (*.dtb). Also includes the dtoverlay and dtparam utilities.
  * otpset - A short script to help with reading and setting the customer OTP bits.
  * overlaycheck - A tool for validating the overlay files and README in a kernel source tree.
  * ovmerge - A tool for merging DT overlay source files (*-overlay.dts), flattening and sorting .dts files for easy comparison, displaying the include tree, etc.
  * pinctrl - A more powerful replacement for raspi-gpio, a tool for displaying and modifying the GPIO and pin muxing state of a system, bypassing the kernel.
  * raspinfo - A short script to dump information about the Pi. Intended for the submission of bug reports.
  * vclog - A tool to get VideoCore 'assert' or 'msg' logs with optional -f to wait for new logs to arrive.

%prep
{{{ git_dir_setup_macro }}}
%autopatch -p1

%build
export PROGRAMS=($(cat CMakeLists.txt | grep add_subdirectory | cut -d"(" -f 2 | cut -d")" -f 1))

# Compiling vclog without position independent code causes a compilation error for some reason
sed -i 's/-pedantic/-pedantic -fPIC/g' vclog/CMakeLists.txt

# This is a workaround to prevent undefined references in pinctrl
for PROGRAM in "${PROGRAMS[@]}"
do
	pushd $PROGRAM
	%cmake
	%cmake_build
	popd
done

%install
export PROGRAMS=($(cat CMakeLists.txt | grep add_subdirectory | cut -d"(" -f 2 | cut -d")" -f 1))

for PROGRAM in "${PROGRAMS[@]}"
do
	pushd $PROGRAM
	%cmake_install
	popd
done

# Relocate overlaycheck_exclusions.txt
mkdir -p %{buildroot}%{_datadir}/overlaycheck
mv %{buildroot}%{_bindir}/overlaycheck_exclusions.txt %{buildroot}%{_datadir}/overlaycheck
sed -i 's!my $exclusions_file = $0 . "_exclusions.txt"!my $exclusions_file = "/usr/share/overlaycheck/overlaycheck_exclusions.txt"!g' %{buildroot}%{_bindir}/overlaycheck

%files
%license LICENCE
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/overlaycheck/overlaycheck_exclusions.txt

%changelog
{{{ git_dir_changelog }}}
