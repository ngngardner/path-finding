# Generated with tex2nix 0.0.0
{ texlive, extraTexPackages ? {} }:
(texlive.combine ({
    inherit (texlive) scheme-small;
    "xcolor" = texlive."xcolor";
    "times" = texlive."times";
    "placeins" = texlive."placeins";
    "microtype" = texlive."microtype";

} // extraTexPackages))
