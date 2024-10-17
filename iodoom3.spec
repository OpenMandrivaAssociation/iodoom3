Name:		iodoom3
Version:	1.3.1.1304
Release:	5
Summary:	Doom 3 engine
Group:		Games/Arcade
License:	GPLv3+
URL:		https://www.iodoom3.org
# From git, see more at http://www.iodoom3.org/download/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.png
Patch0:		iodoom3-1.3.1.1304-datapath.patch
# https://github.com/albertz/iodoom3/commit/350616aab643eceb106631af81d3bb960a0dcb70
Patch1:		iodoom3-1.3.1.1304-x86_64.patch
BuildRequires:	imagemagick
BuildRequires:	scons
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(zlib)
Provides:	doom3 = 1.3.1
# 64 bit build is too buggy, segfaults at start and requires lots of patching
ExclusiveArch:	%{ix86}

%description
On November 22, 2011 id Software released the source code to Doom 3.
This project aims to build upon that source code release by cleaning up,
fixing bugs, and adding features. The permant goal is to create the
open-source Doom 3 distribution upon which people base their games and
projects. Project developers also seek to have the perfect version of the
game engine for playing Doom 3, it’s expansion pack Resurrection of Evil,
and all popular mods.

WARNING! Playing Doom 3 still requires a legitimate copy of the game.
You can purchase a copy from Steam or your favorite retailer.

Place "base" folder from the Doom 3 installation to:
%{_gamesdatadir}/doom3/


%prep
%setup -q
%patch0 -p1
sed -i s,"/usr/lib/libz.a","%{_libdir}/libz.a",g neo/sys/scons/SConscript.curl
# Ask CD-KEY only for network game
sed -i s,"ID_ENFORCE_KEY 1","ID_ENFORCE_KEY 0",g neo/framework/BuildDefines.h

%build
pushd neo
%scons TARGET_MONO=1 TARGET_CORE=0 TARGET_GAME=0 TARGET_D3XP=0
popd
for N in 16 32 64 128; do convert %{SOURCE1} -resize ${N}x${N} $N.png; done

%install
install -D neo/doom-mon* %{buildroot}%{_gamesbindir}/%{name}
install -D 16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D 32.png %{buildroot}%{_liconsdir}/%{name}.png
install -D 64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -D 128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Doom 3
Comment=A first-person science fiction horror video game
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

mkdir -p %{buildroot}%{_gamesdatadir}/doom3

%files
%doc README.txt COPYING.txt id-readme.txt
%{_gamesbindir}/%{name}
%dir %{_gamesdatadir}/doom3
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png

