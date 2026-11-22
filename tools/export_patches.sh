#!/bin/sh
# Exporta los commits de la rama guide del decomp de un juego a <juego>/patches/, un .patch por commit.
# Uso: tools/export_patches.sh <juego>. Ejecutar tras cada commit en el decomp y commitear <juego>/patches/ en el repo principal.
# Cada juego nuevo se añade al case con su decomp y el commit de pret sobre el que van los parches.
set -eu
cd "$(dirname "$0")/.."

case "${1-}" in
    emerald) DECOMP=emerald/pokeemerald BASE=9103e529c2fbdd7add4a1ff3350c6c1f92112c42 ;;
    *) echo "uso: tools/export_patches.sh emerald" >&2; exit 2 ;;
esac
OUT="$PWD/$1/patches"

if ! git -C "$DECOMP" diff --quiet HEAD; then
    echo "aviso: $DECOMP tiene cambios sin commitear; no se exportan" >&2
fi
rm -rf "$OUT"
git -C "$DECOMP" format-patch --quiet --no-signature -o "$OUT" "$BASE..guide"
ls "$OUT"
