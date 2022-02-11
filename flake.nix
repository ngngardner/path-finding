{
  description = "Deep Learning and Neural Nets Project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/d189bf92f9be23f9b0f6c444f6ae29351bb7125c";
    utils = { url = "github:numtide/flake-utils"; };
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShell = pkgs.mkShell {
          packages = [
            # tex
            (pkgs.callPackage ./tex-env.nix {
              extraTexPackages = {
                inherit (pkgs.texlive)
                  latexmk
                  latexindent
                  helvetic
                  courier
                  ;
              };
            })
          ];
        };
      });
}
