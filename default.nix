with import <nixpkgs> {};
stdenv.mkDerivation {
    name = "burgerforslag";
    buildInputs = [ (python3.withPackages (ps: with ps; [ pyquery ])) ];
}
