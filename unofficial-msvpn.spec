
%define pmc https://packages.microsoft.com

%define msvpn_name microsoft-azurevpnclient
%define msvpn_version 3.0.0
%define msvpn_path /ubuntu/22.04/prod/pool/main/m/%{msvpn_name}
%define msvpn_deb %{msvpn_name}_%{msvpn_version}_amd64.deb
%define msvpn_dir %{msvpn_name}-%{msvpn_version}


Name:           unofficial-msvpn
Version:        0.0.6
Release:        1%{?dist}
Summary:        Dynamic rpm packager for msvpn
License:        GPLv3

Source1:        microsoft-azurevpnclient
# http://cacerts.digicert.com/DigiCertGlobalRootG2.crt converted to PEM
Source2:        DigiCertGlobalRootG2.pem

Requires:       zenity

Requires(pre):  wget >= 2

Requires(post): dpkg
Requires(post): /usr/bin/setcap
Requires(post): /usr/bin/install
Requires(post): /usr/bin/mktemp

%description
Dynamic rpm packager for msvpn

%install
install -D -m 0755 -t %{buildroot}%{_bindir} %{SOURCE1}
install -D -m 0644 -t %{buildroot}%{_sysconfdir}/pki/tls/certs %{SOURCE2}
install -d %{buildroot}%{_datarootdir}/%{name}-%{version}/debs
install -d %{buildroot}%{_datarootdir}/%{name}-%{version}/logs
install -d %{buildroot}%{_datarootdir}/doc/microsoft-azurevpnclient
install -d %{buildroot}/opt/microsoft/microsoft-azurevpnclient/lib
install -d %{buildroot}/opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/shaders
install -d %{buildroot}/opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/fluent_ui/fonts
install -d %{buildroot}/opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/fluent_ui/assets
install -d %{buildroot}/opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/cupertino_icons/assets
install -d %{buildroot}/opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/fonts
install -d %{buildroot}/opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/assets/images

%pre
install -d %{_datarootdir}/%{name}-%{version}/logs
{
wget -O %{_datarootdir}/%{name}-%{version}/debs/%{msvpn_deb} "%{pmc}/%{msvpn_path}/%{msvpn_deb}"
} > %{_datarootdir}/%{name}-%{version}/logs/pre.log

%post
{
TMPDIR=$(mktemp -d)
pushd ${TMPDIR}

dpkg-deb -x %{_datarootdir}/%{name}-%{version}/debs/%{msvpn_deb} %{msvpn_dir}
pushd %{msvpn_dir}

pushd opt/microsoft/microsoft-azurevpnclient/lib
install -v -m 0755 -t /opt/microsoft/microsoft-azurevpnclient/lib \
        libLinuxCore.so \
        libXplatSharedLibrary.so \
        libapp.so \
        libflutter_linux_gtk.so \
        libflutter_secure_storage_linux_plugin.so \
        libflutter_window_close_plugin.so \
        libmat.so \
        liburl_launcher_linux_plugin.so
popd

pushd opt/microsoft/microsoft-azurevpnclient/data
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data \
        icudtl.dat
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets \
        flutter_assets/AssetManifest.bin \
        flutter_assets/AssetManifest.json \
        flutter_assets/FontManifest.json \
        flutter_assets/NOTICES.Z \
        flutter_assets/version.json
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/shaders \
        flutter_assets/shaders/ink_sparkle.frag
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/fluent_ui/fonts \
        flutter_assets/packages/fluent_ui/fonts/FluentIcons.ttf
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/fluent_ui/assets \
        flutter_assets/packages/fluent_ui/assets/AcrylicNoise.png
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/cupertino_icons/assets \
        flutter_assets/packages/cupertino_icons/assets/CupertinoIcons.ttf
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/fonts \
        flutter_assets/fonts/MaterialIcons-Regular.otf
install -v -m 0644 -t /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/assets/images \
        flutter_assets/assets/images/logo.png \
        flutter_assets/assets/images/capture.png
popd

install -v -m 0644 -t /var/lib/polkit-1/localauthority/50-local.d \
        var/lib/polkit-1/localauthority/50-local.d/10-microsoft-azurevpnclient.pkla

install -v -m 0755 -t /opt/microsoft/microsoft-azurevpnclient \
        opt/microsoft/microsoft-azurevpnclient/microsoft-azurevpnclient

install -v -m 0644 -t %{_datarootdir}/icons \
        usr/share/icons/microsoft-azurevpnclient.png
install -v -m 0644 -t %{_datarootdir}/polkit-1/rules.d \
        usr/share/polkit-1/rules.d/microsoft-azurevpnclient.rules
install -v -m 0644 -t %{_datarootdir}/applications \
        usr/share/applications/microsoft-azurevpnclient.desktop
install -v -m 0644 -t %{_datarootdir}/doc/microsoft-azurevpnclient \
        usr/share/doc/microsoft-azurevpnclient/copyright \
        usr/share/doc/microsoft-azurevpnclient/NOTICE.txt.gz \
        usr/share/doc/microsoft-azurevpnclient/changelog.gz

popd
rm -rf "%{msvpn_dir}"

popd
rmdir ${TMPDIR}

# The program needs net admin capability to be able to manage the tun interface
setcap cap_net_admin+eip /opt/microsoft/microsoft-azurevpnclient/microsoft-azurevpnclient
} > %{_datarootdir}/%{name}-%{version}/logs/post.log

%files
%{_bindir}/microsoft-azurevpnclient
%{_sysconfdir}/pki/tls/certs/DigiCertGlobalRootG2.pem
/opt/microsoft/microsoft-azurevpnclient
%{_datarootdir}/doc/microsoft-azurevpnclient

%{_datarootdir}/%{name}-%{version}
%ghost %{_datarootdir}/%{name}-%{version}/logs/pre.log
%ghost %{_datarootdir}/%{name}-%{version}/logs/post.log
%ghost %{_datarootdir}/%{name}-%{version}/debs/%{msvpn_deb}

%ghost /opt/microsoft/microsoft-azurevpnclient/lib/libflutter_linux_gtk.so
%ghost /opt/microsoft/microsoft-azurevpnclient/lib/liburl_launcher_linux_plugin.so
%ghost /opt/microsoft/microsoft-azurevpnclient/lib/libflutter_window_close_plugin.so
%ghost /opt/microsoft/microsoft-azurevpnclient/lib/libapp.so
%ghost /opt/microsoft/microsoft-azurevpnclient/lib/libLinuxCore.so
%ghost /opt/microsoft/microsoft-azurevpnclient/lib/libflutter_secure_storage_linux_plugin.so
%ghost /opt/microsoft/microsoft-azurevpnclient/lib/libXplatSharedLibrary.so
%ghost /opt/microsoft/microsoft-azurevpnclient/lib/libmat.so
%ghost /opt/microsoft/microsoft-azurevpnclient/data/icudtl.dat
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/AssetManifest.bin
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/shaders/ink_sparkle.frag
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/fluent_ui/fonts/FluentIcons.ttf
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/fluent_ui/assets/AcrylicNoise.png
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/packages/cupertino_icons/assets/CupertinoIcons.ttf
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/version.json
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/FontManifest.json
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/NOTICES.Z
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/AssetManifest.json
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/fonts/MaterialIcons-Regular.otf
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/assets/images/logo.png
%ghost /opt/microsoft/microsoft-azurevpnclient/data/flutter_assets/assets/images/capture.png
%ghost /opt/microsoft/microsoft-azurevpnclient/microsoft-azurevpnclient

%ghost /var/lib/polkit-1/localauthority/50-local.d/10-microsoft-azurevpnclient.pkla

%ghost %{_datarootdir}/icons/microsoft-azurevpnclient.png
%ghost %{_datarootdir}/polkit-1/rules.d/microsoft-azurevpnclient.rules
%ghost %{_datarootdir}/applications/microsoft-azurevpnclient.desktop

%ghost %{_datarootdir}/doc/microsoft-azurevpnclient/copyright
%ghost %{_datarootdir}/doc/microsoft-azurevpnclient/NOTICE.txt.gz
%ghost %{_datarootdir}/doc/microsoft-azurevpnclient/changelog.gz

%changelog
* Thu Feb 19 2026 Dan Streetman <ddstreet@ieee.org> - 0.0.6-1
- add admin net cap to binary so it can manage the tun interface

* Thu Feb 19 2026 Dan Streetman <ddstreet@ieee.org> - 0.0.5-1
- fix missing -t install line

* Thu Feb 19 2026 Dan Streetman <ddstreet@ieee.org> - 0.0.4-1
- add root CA the application needs

* Thu Feb 19 2026 Dan Streetman <ddstreet@ieee.org> - 0.0.3-1
- add polkit file from deb

* Thu Feb 19 2026 Dan Streetman <ddstreet@ieee.org> - 0.0.2-1
- add zenity dep

* Wed Feb 18 2026 ddstreet
- 
