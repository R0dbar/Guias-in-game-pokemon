# Guía dentro del juego — Pokémon

Añade a los juegos de Pokémon una guía que puedes consultar en cualquier momento: te dice **cuál es tu objetivo
actual y a dónde tienes que ir**. Está en inglés y en español; en español, los nombres salen como en el juego
(en inglés) con el nombre español entre paréntesis: `RUSTBORO CITY (Ciudad Férrica)`.

Es para quien juega en un emulador con su propia copia del juego y no quiere, o no puede, consultar una guía fuera
del juego. La guía se abre desde la mochila (dos objetos, uno por idioma) o desde el menú START.

## Juegos

| Juego | Estado | Detalles |
|---|---|---|
| Pokémon Esmeralda (USA) | Prueba de concepto: hasta la primera medalla | [emerald/](emerald/README.md) |
| Pokémon Rubí y Zafiro (USA) | En preparación | — |

Cada juego tiene su carpeta con todo lo suyo: cómo compilarlo, sus parches, su glosario y sus fuentes.

## Licencia

El contenido de este repo (código, textos de la guía, scripts y documentación) es [MIT](LICENSE): puedes usarlo,
modificarlo y redistribuirlo libremente si mantienes el aviso de copyright con el nombre del autor.

La licencia no cubre el código de los decomps de [pret](https://github.com/pret) que aparece como contexto en los
parches. Pokémon es una marca de Nintendo, Creatures y GAME FREAK; este es un proyecto de fans sin relación con ellos.
Este repo no contiene ningún juego ni ROM.

## Desarrollo

Cada juego se construye sobre un decomp de pret, que reconstruye el juego desde código fuente. Hay un repo git por
pieza:

- **Este**, con una sola rama, `main`. Es lo que se publica.
- **El decomp de cada juego** (por ejemplo, `emerald/pokeemerald/`), clonado dentro de la carpeta del juego e ignorado
  por este repo. Nuestros cambios van en su rama local `guide`, que no se sube a ningún sitio: lo que se publica son
  los parches de `<juego>/patches/`.

Flujo de un cambio en el juego: editar en el decomp → comprobar los textos → compilar → probar en el emulador en los dos
idiomas → commit en el decomp → `tools/export_patches.sh <juego>` → commit de `<juego>/patches/` aquí. Sin ese último
paso, el cambio no llega a este repo. Los comandos de cada juego están en su README.

Herramientas comunes, en `tools/`:

| Para qué | Comando | Resultado esperado |
|---|---|---|
| Comprobar los textos de la guía | `python3 tools/check_guide.py <juego>/<decomp>` | `OK: <n> pares EN/ES` |
| Tests del comprobador | `python3 -m unittest discover -s tools -v` | `OK` |
| Exportar los cambios del juego | `tools/export_patches.sh <juego>` | un `.patch` por commit en `<juego>/patches/` |

`check_guide.py` comprueba que cada texto tiene versión EN y ES, que cada línea cabe en la caja (216 px), que todos
los caracteres existen en la fuente del juego y que no hay placeholders `{…}`. No detecta un texto vacío ni una caja
con más de 2 líneas: eso se ve jugando.

### Añadir o cambiar un paso

Los pasos están en `<juego>/<decomp>/src/data/guide_steps.h`, en el orden de la historia. Cada uno tiene:

- **Condición:** el flag (`doneFlag`) o la var (`doneVar` ≥ `doneVarMin`) que el juego activa al completarlo.
  Sale de los scripts del juego (`grep -rn "setflag FLAG_" <juego>/<decomp>/data/maps/`) y se apunta en un comentario
  junto al paso.
- **Textos** `objective` (qué hacer) y `location` (a dónde ir), en EN y ES. Cada uno empieza en una caja nueva.
  Una caja admite 2 líneas (un `\n`); para más texto, `\p` abre otra caja.
- **Nombres en español** del glosario del juego (`<juego>/glosario.md`). Las fuentes usadas van en `<juego>/fuentes.md`.
  Los textos son propios: no se copia texto de guías con copyright.
