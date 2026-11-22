# Guía dentro del juego — Pokémon Rubí y Zafiro

La guía del proyecto ([README general](../README.md)) para Pokémon Rubí y Zafiro, versión USA (en inglés).
Los mismos parches sirven para los dos juegos.

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

Se construye sobre el decomp [pret/pokeruby](https://github.com/pret/pokeruby), que reconstruye los dos juegos desde
código fuente. Nuestros cambios están en [`patches/`](patches), como parches sobre ese decomp. No hace falta una ROM
original para compilar.

1. Instala las dependencias de tu sistema según el
   [INSTALL.md de pokeruby](https://github.com/pret/pokeruby/blob/master/INSTALL.md). Pide devkitARM, pero bastan las
   binutils de ARM del sistema (`arm-none-eabi-binutils`) si compilas con `CPP=cpp`, como abajo: el Makefile de
   pokeruby busca `arm-none-eabi-cpp`, que esas binutils no traen, y `CPP=cpp` usa el preprocesador del sistema.
   Con él, el juego original sale idéntico al oficial.
2. Desde la raíz del repo (no desde esta carpeta):

   ```sh
   # el decomp, en el commit sobre el que están hechos los parches, con ellos aplicados en la rama guide
   git clone https://github.com/pret/pokeruby ruby/pokeruby
   git -C ruby/pokeruby checkout -b guide 5784633ce4ef7ade1a7f2d2d0c288e3d5e6cdd7f
   git -C ruby/pokeruby am "$PWD"/ruby/patches/*.patch
   # el compilador del decomp, instalado dentro del decomp (si ya tienes agbcc/ de otro juego, basta con install.sh)
   git clone https://github.com/pret/agbcc
   (cd agbcc && ./build.sh && ./install.sh ../ruby/pokeruby)
   make -C ruby/pokeruby -j"$(nproc)" CPP=cpp
   make -C ruby/pokeruby sapphire -j"$(nproc)" CPP=cpp
   ```

3. Las ROMs salen en `ruby/pokeruby/pokeruby.gba` (Rubí) y `ruby/pokeruby/pokesapphire.gba` (Zafiro). Ábrelas con un
   emulador de GBA, por ejemplo [mGBA](https://mgba.io).

`git am` necesita que tengas configurados `user.name` y `user.email` en git.

## Comandos

Desde la raíz del repo:

| Para qué | Comando | Resultado esperado |
|---|---|---|
| Compilar Rubí | `make -C ruby/pokeruby -j$(nproc) CPP=cpp` | `ruby/pokeruby/pokeruby.gba` |
| Compilar Zafiro | `make -C ruby/pokeruby sapphire -j$(nproc) CPP=cpp` | `ruby/pokeruby/pokesapphire.gba` |
| Comprobar los textos de la guía | `python3 tools/check_guide.py ruby/pokeruby` | `OK: 11 pares EN/ES` |
| Tests del comprobador | `python3 -m unittest discover -s tools -v` | `OK` |
| Exportar los cambios del juego | `tools/export_patches.sh ruby` | un `.patch` por commit en `ruby/patches/` |

Los pasos de la guía están en `ruby/pokeruby/src/data/guide_steps.h`. Los nombres españoles salen del
[glosario](glosario.md) y las fuentes usadas están en [fuentes.md](fuentes.md). Licencia: [MIT](../LICENSE).
