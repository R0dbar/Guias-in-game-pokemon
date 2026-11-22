# Guía dentro del juego — Pokémon Esmeralda

La guía del proyecto ([README general](../README.md)) para Pokémon Esmeralda, versión USA (en inglés).

**Estado:** prueba de concepto. La guía cubre el principio del juego, hasta la primera medalla (5 pasos).
Después muestra un mensaje de fin.

## En el juego

Hay dos formas de abrir la guía; las dos muestran lo mismo:

- **Mochila:** en KEY ITEMS están `GUIDE (EN)` y `GUÍA (ES)`, uno por idioma. USE muestra el paso actual;
  REGISTER lo deja en el botón SELECT para abrirlo desde el mapa.
- **Menú START:** entrada `GUIDE` → eliges `ENGLISH` o `ESPAÑOL` → muestra el paso actual. B cierra sin mostrar nada.

El mensaje tiene dos partes: primero el objetivo y, al pulsar A, a dónde ir.

La guía solo lee el progreso que el juego ya guarda y no escribe nada en la partida. Los dos objetos se reciben al
empezar una partida nueva: una partida guardada antes de instalar la guía no los tiene, pero sí la entrada del menú START.

## Compilar

Se construye sobre el decomp [pret/pokeemerald](https://github.com/pret/pokeemerald), que reconstruye el juego desde
código fuente. Nuestros cambios están en [`patches/`](patches), como parches sobre ese decomp. No hace falta una ROM
original para compilar.

1. Instala las dependencias de tu sistema según el
   [INSTALL.md de pokeemerald](https://github.com/pret/pokeemerald/blob/master/INSTALL.md) (binutils de ARM, libpng…).
2. Desde la raíz del repo (no desde esta carpeta):

   ```sh
   # el decomp, en el commit sobre el que están hechos los parches, con ellos aplicados en la rama guide
   git clone https://github.com/pret/pokeemerald emerald/pokeemerald
   git -C emerald/pokeemerald checkout -b guide 9103e529c2fbdd7add4a1ff3350c6c1f92112c42
   git -C emerald/pokeemerald am "$PWD"/emerald/patches/*.patch
   # el compilador del decomp, instalado dentro del decomp (si ya tienes agbcc/ de otro juego, basta con install.sh)
   git clone https://github.com/pret/agbcc
   (cd agbcc && ./build.sh && ./install.sh ../emerald/pokeemerald)
   make -C emerald/pokeemerald -j"$(nproc)"
   ```

3. La ROM sale en `emerald/pokeemerald/pokeemerald.gba`. Ábrela con un emulador de GBA, por ejemplo [mGBA](https://mgba.io).

`git am` necesita que tengas configurados `user.name` y `user.email` en git.

## Comandos

Desde la raíz del repo:

| Para qué | Comando | Resultado esperado |
|---|---|---|
| Compilar la ROM | `make -C emerald/pokeemerald -j$(nproc)` | `emerald/pokeemerald/pokeemerald.gba` |
| Comprobar los textos de la guía | `python3 tools/check_guide.py emerald/pokeemerald` | `OK: 11 pares EN/ES` |
| Tests del comprobador | `python3 -m unittest discover -s tools -v` | `OK` |
| Exportar los cambios del juego | `tools/export_patches.sh emerald` | un `.patch` por commit en `emerald/patches/` |

Los pasos de la guía están en `emerald/pokeemerald/src/data/guide_steps.h`. Los nombres españoles salen del
[glosario](glosario.md) y las fuentes usadas están en [fuentes.md](fuentes.md). Licencia: [MIT](../LICENSE).
