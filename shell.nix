{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.gtk4
    pkgs.glib
    pkgs.gobject-introspection
    pkgs.graphene
    pkgs.pango
    pkgs.cairo
    pkgs.harfbuzz
    pkgs.python3Packages.pygobject3
    pkgs.libadwaita
    pkgs.ninja
    pkgs.meson
    pkgs.desktop-file-utils
    pkgs.cmake
    pkgs.adwaita-icon-theme
  ];

  # Ensure that the GI_TYPELIB_PATH, adwaita-icons and PYTHONPATH are set correctly
  shellHook = ''
    export XDG_DATA_DIRS=$HOME/.nix-profile/share:${pkgs.adwaita-icon-theme}/share:${pkgs.adwaita-icon-theme}/share
    gtk4-update-icon-cache ${pkgs.adwaita-icon-theme}/share/icons/*
    export GI_TYPELIB_PATH=${pkgs.glib.out}/lib/girepository-1.0:\
${pkgs.gtk4.out}/lib/girepository-1.0:\
${pkgs.graphene.out}/lib/girepository-1.0:\
${pkgs.pango.out}/lib/girepository-1.0:\
${pkgs.cairo.out}/lib/girepository-1.0:\
${pkgs.harfbuzz.out}/lib/girepository-1.0:\
${pkgs.gdk-pixbuf.out}/lib/girepository-1.0:\
${pkgs.libadwaita.out}/lib/girepository-1.0
  '';
}
