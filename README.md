# Guía dentro del juego — Pokémon Esmeralda

Añade a Pokémon Esmeralda una guía que puedes consultar en cualquier momento: te dice **cuál es tu objetivo
actual y a dónde tienes que ir**. Está en inglés y en español; en español, los nombres salen como en el juego
(en inglés) con el nombre español entre paréntesis: `RUSTBORO CITY (Ciudad Férrica)`.

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

Este repo no contiene el juego ni ninguna ROM. Nuestros cambios están en `patches/emerald/`, como parches sobre
el decomp [pret/pokeemerald](https://github.com/pret/pokeemerald), que reconstruye el juego desde código fuente.
No hace falta una ROM original para compilar.

1. Instala las dependencias de tu sistema según el
   [INSTALL.md de pokeemerald](https://github.com/pret/pokeemerald/blob/master/INSTALL.md) (binutils de ARM, libpng…).
2. Desde la raíz de este repo:

   ```sh
   # el decomp, en el commit sobre el que están hechos los parches, con ellos aplicados en la rama guide
   git clone https://github.com/pret/pokeemerald emerald
   git -C emerald checkout -b guide 9103e529c2fbdd7add4a1ff3350c6c1f92112c42
   git -C emerald am "$PWD"/patches/emerald/*.patch
   # el compilador del decomp, instalado dentro de emerald/
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

Hay dos repos git:

- **Este**, con una sola rama, `main`. Es lo que se publica.
- **`emerald/`**, el clon de pokeemerald, dentro de este pero ignorado por él. Nuestros cambios van en su rama local
  `guide`, que no se sube a ningún sitio.

Los cambios del juego se hacen en `emerald/` y se commitean allí, en `guide`; después se exportan como parches a
`patches/emerald/` y se commitean aquí, en `main`. Sin ese último paso, el cambio no llega a este repo.

Comandos, desde la raíz de este repo:

| Para qué | Comando | Resultado esperado |
|---|---|---|
| Compilar la ROM | `make -C emerald -j$(nproc)` | `emerald/pokeemerald.gba` |
| Comprobar los textos de la guía | `python3 tools/check_guide.py emerald` | `OK: <n> pares EN/ES` |
| Tests del comprobador | `python3 -m unittest discover -s tools -v` | `OK` |
| Exportar los cambios del juego | `tools/export_patches.sh` | un `.patch` por commit en `patches/emerald/` |

`check_guide.py` comprueba que cada texto tiene versión EN y ES, que cada línea cabe en la caja (216 px), que todos
los caracteres existen en la fuente del juego y que no hay placeholders `{…}`. No detecta un texto vacío ni una caja
con más de 2 líneas: eso se ve jugando.

### Añadir o cambiar un paso

Los pasos están en `emerald/src/data/guide_steps.h`, en el orden de la historia. Cada uno tiene:

- **Condición:** el flag (`doneFlag`) o la var (`doneVar` ≥ `doneVarMin`) que el juego activa al completarlo.
  Sale del script del juego (`grep -rn "setflag FLAG_" emerald/data/maps/`), y se apunta en un comentario junto al paso.
- **Textos** `objective` (qué hacer) y `location` (a dónde ir), en EN y ES. Cada uno empieza en una caja nueva.
  Una caja admite 2 líneas (un `\n`); para más texto, `\p` abre otra caja.
- **Nombres en español** del [glosario](docs/glosario-emerald.md). Las fuentes usadas están en [docs/fuentes.md](docs/fuentes.md).
  Los textos son propios: no se copia texto de guías con copyright.

Después: comprobar los textos, compilar, probar en el emulador en los dos idiomas, commitear en `emerald/`,
exportar los parches y commitearlos aquí.
