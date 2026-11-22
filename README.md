# Guía dentro del juego — Pokémon Esmeralda

Añade a Pokémon Esmeralda una guía que puedes consultar en cualquier momento: te dice **cuál es tu objetivo
actual y a dónde tienes que ir**. Está en inglés y en español; en español, los nombres salen como en el juego
(en inglés) con el nombre español entre paréntesis: `RUSTBORO CITY (Ciudad Férrica)`.

**Estado:** prueba de concepto. La guía cubre el principio del juego, hasta la primera medalla.

## En el juego

- **Mochila:** desde la partida nueva tienes `GUIDE (EN)` y `GUÍA (ES)` en KEY ITEMS. USE muestra el paso actual;
  REGISTER lo deja en el botón SELECT.
- **Menú START:** entrada `GUIDE` → eliges `ENGLISH` o `ESPAÑOL` → muestra el paso actual.

La guía solo lee el progreso que el juego ya guarda: funciona con cualquier partida y no cambia la partida guardada.

## Compilar

Este repo no contiene el juego ni ninguna ROM. Nuestros cambios están en `patches/emerald/`, como parches sobre
el decomp [pret/pokeemerald](https://github.com/pret/pokeemerald), que reconstruye el juego desde código fuente.
No hace falta una ROM original para compilar.

1. Instala las dependencias de tu sistema según el
   [INSTALL.md de pokeemerald](https://github.com/pret/pokeemerald/blob/master/INSTALL.md) (binutils de ARM, libpng…).
2. Desde la raíz de este repo:

   ```sh
   git clone https://github.com/pret/pokeemerald emerald
   git -C emerald checkout -b guide 9103e529c2fbdd7add4a1ff3350c6c1f92112c42
   git -C emerald am "$PWD"/patches/emerald/*.patch
   git clone https://github.com/pret/agbcc
   (cd agbcc && ./build.sh && ./install.sh ../emerald)
   make -C emerald -j"$(nproc)"
   ```

3. La ROM sale en `emerald/pokeemerald.gba`. Ábrela con un emulador de GBA, por ejemplo [mGBA](https://mgba.io).

`git am` necesita que tengas configurados `user.name` y `user.email` en git.

## Licencia

El contenido de este repo (código, textos de la guía, scripts y documentación) es [MIT](LICENSE): puedes usarlo,
modificarlo y redistribuirlo libremente si mantienes el aviso de copyright con el nombre del autor.

La licencia no cubre el código de [pret/pokeemerald](https://github.com/pret/pokeemerald) que aparece como contexto
en los parches. Pokémon es una marca de Nintendo, Creatures y GAME FREAK; este es un proyecto de fans sin relación
con ellos.

## Desarrollo

Los cambios del juego se hacen en `emerald/` (rama `guide`) y se commitean allí. Después se exportan como parches
y se commitean en este repo; sin ese paso, el cambio no llega aquí.

| Para qué | Comando |
|---|---|
| Compilar la ROM | `make -C emerald -j$(nproc)` |
| Comprobar los textos de la guía (idiomas y ancho de línea) | `python3 tools/check_guide.py emerald` |
| Tests del comprobador | `python3 -m unittest discover -s tools -v` |
| Exportar los cambios del juego a `patches/emerald/` | `tools/export_patches.sh` |

Los pasos de la guía están en `emerald/src/data/guide_steps.h`. Los nombres españoles salen de
[docs/glosario-emerald.md](docs/glosario-emerald.md) y las fuentes, de [docs/fuentes.md](docs/fuentes.md).
Los textos son propios: no se copia texto de guías con copyright.
