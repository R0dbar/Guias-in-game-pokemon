"""Comprueba los textos de src/data/guide_steps.h de un decomp.

Detecta: un texto sin su pareja EN/ES, una línea de más de 216 px, un carácter que no está en charmap.txt
y placeholders {…}. No detecta: un texto vacío _(""), una caja de más de 2 líneas ni un texto de más de
GUIDE_TEXT_LEN bytes (eso lo para la compilación).

Uso: python3 tools/check_guide.py <dir_decomp>
"""
import os
import re
import sys

MAX_WIDTH = 216  # ventana de texto de 27 tiles

_TEXT = r'_\("((?:[^"\\]|\\.)*)"\)'
_PAIR = re.compile(r'\{\s*\[GUIDE_LANG_EN\]\s*=\s*' + _TEXT
                   + r'\s*,\s*\[GUIDE_LANG_ES\]\s*=\s*' + _TEXT + r'\s*,?\s*\}')
_ANY_LANG = re.compile(r'\[GUIDE_LANG_(?!COUNT\])[A-Z]+\]\s*=')  # GUIDE_LANG_COUNT es el tamaño, no un texto


def load_charmap(path):
    charmap = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r"^'(\\'|[^\\])'\s*=\s*([0-9A-Fa-f]{2})\b", line)
            if m:
                charmap[m.group(1).replace("\\'", "'")] = int(m.group(2), 16)
    return charmap


def load_glyph_widths(path):
    with open(path, encoding='utf-8') as f:
        body = re.search(r'gFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\}', f.read(), re.S).group(1)
    return [int(n) for n in re.findall(r'\d+', body)]


def text_lines(text):
    return re.split(r'\\[nlp]', text)


def text_width(line, charmap, widths):
    width = 0
    for c in line:
        if c not in charmap:
            raise ValueError(f"carácter no soportado: {c!r}")
        width += widths[charmap[c]]
    return width


def _line_of(source, pos):
    return source.count('\n', 0, pos) + 1


def find_text_pairs(source):
    return [(_line_of(source, m.start()), m.group(1), m.group(2)) for m in _PAIR.finditer(source)]


def check_source(source, charmap, widths, max_width=MAX_WIDTH):
    pairs = find_text_pairs(source)
    errors = []

    paired = [range(m.start(), m.end()) for m in _PAIR.finditer(source)]
    for m in _ANY_LANG.finditer(source):
        if not any(m.start() in r for r in paired):
            errors.append(f"{_line_of(source, m.start())}: texto sin pareja de idioma")
            break

    for line_no, *texts in pairs:
        for text in texts:
            if '{' in text:
                errors.append(f"{line_no}: placeholder no admitido en {text!r}")
                continue
            for line in text_lines(text):
                try:
                    px = text_width(line, charmap, widths)
                except ValueError as e:
                    errors.append(f"{line_no}: {e} en {line!r}")
                    continue
                if px > max_width:
                    errors.append(f"{line_no}: línea de {px} px (máx. {max_width}): {line!r}")
    return errors


def main(argv):
    root = argv[0]
    steps_path = os.path.join(root, 'src', 'data', 'guide_steps.h')
    with open(steps_path, encoding='utf-8') as f:
        source = f.read()
    errors = check_source(source,
                          load_charmap(os.path.join(root, 'charmap.txt')),
                          load_glyph_widths(os.path.join(root, 'src', 'fonts.c')))
    for e in errors:
        print(f"{steps_path}:{e}")
    if errors:
        return 1
    print(f"OK: {len(find_text_pairs(source))} pares EN/ES")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
