#!/bin/sh
# Exporta los commits de emerald/ (rama guide) sobre pokeemerald@9103e52 a patches/emerald/, un .patch por commit.
# Ejecutar tras cada commit en emerald/ y commitear patches/ en el repo principal.
set -eu
cd "$(dirname "$0")/.."
BASE=9103e529c2fbdd7add4a1ff3350c6c1f92112c42

if ! git -C emerald diff --quiet HEAD; then
    echo "aviso: emerald/ tiene cambios sin commitear; no se exportan" >&2
fi
rm -rf patches/emerald
git -C emerald format-patch --quiet --no-signature -o ../patches/emerald "$BASE..guide"
ls patches/emerald
