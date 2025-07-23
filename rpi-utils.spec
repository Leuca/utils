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

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Conflicts:      rpi-userland

Provides:       vcgencmd

Source:         {{{ git_dir_pack }}}

Patch0:         rpi-utils-drop-apt-command.patch
Patch1:         rpi-utils-dtoverlay-path.patch

%description
A collection of scripts and simple applications for the Raspberry Pi including:
  * dtmerge - A tool for applying compiled DT overlays (*.dtbo) to base Device Tree files (*.dtb). Also includes the dtoverlay and dtparam utilities.
  * otpset - A short script to help with reading and setting the customer OTP bits.
  * overlaycheck - A tool for validating the overlay files and README in a kernel source tree.
  * ovmerge - A tool for merging DT overlay source files (*-overlay.dts), flattening and sorting .dts files for easy comparison, displaying the include tree, etc.
  * pinctrl - A more powerful replacement for raspi-gpio, a tool for displaying and modifying the GPIO and pin muxing state of a system, bypassing the kernel.
  * raspinfo - A short script to dump information about the Pi. Intended for the submission of bug reports.
  * vclog - A tool to get VideoCore 'assert' or 'msg' logs with optional -f to wait for new logs to arrive.

%package libs
Summary:        Shared libraries for rpi-utils

%description libs
This package includes shared libraries used by rpi-utils

%package devel
Summary:        Development files for rpi-utils

%description devel
This package includes development files relative to rpi-utils

%prep
{{{ git_dir_setup_macro }}}
%autopatch -p1

%build
%cmake -DCFLAGS="-fPIC"
%cmake_build


%install
%cmake_install

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


%files libs
%{_libdir}/libdtovl.so.*
%{_libdir}/libgpiolib.so.*
%{_libdir}/libpio.so.*


%files devel
%{_includedir}/dtoverlay.h
%{_includedir}/gpiolib.h
%{_includedir}/piolib/hardware/clocks.h
%{_includedir}/piolib/hardware/gpio.h
%{_includedir}/piolib/hardware/pio.h
%{_includedir}/piolib/hardware/pio_instructions.h
%{_includedir}/piolib/hardware/timer.h
%{_includedir}/piolib/pico/stdlib.h
%{_includedir}/piolib/pio_platform.h
%{_includedir}/piolib/piolib.h
%{_libdir}/libdtovl.so
%{_libdir}/libgpiolib.so
%{_libdir}/libpio.so


%changelog
{{{ git_dir_changelog }}}
