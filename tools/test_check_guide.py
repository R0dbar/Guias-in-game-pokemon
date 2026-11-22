import contextlib
import io
import os
import tempfile
import unittest

from check_guide import (
    check_source,
    load_charmap,
    load_glyph_widths,
    load_ruby_font3_widths,
    main,
    text_lines,
    text_width,
)

CHARMAP = {'A': 0, 'B': 1, ' ': 2, 'é': 3}
WIDTHS = [6, 5, 3, 6]

# Forma de src/data/text/font3_widths.h en pokeruby: dos variantes inglesas (revisiones) y una alemana
RUBY_FONT3 = ("#if ENGLISH\n#if REVISION >= 1\nstatic const u8 sFont3Widths[] = {\n 3, 6, 8,\n};\n#else\n"
              "static const u8 sFont3Widths[] = {\n 3, 7, 6,\n};\n#endif\n#elif GERMAN\n"
              "static const u8 sFont3Widths[] = {\n 9, 9, 9,\n};\n#endif\n")


def pair(en, es):
    return '{ [GUIDE_LANG_EN] = _("%s"), [GUIDE_LANG_ES] = _("%s"), }' % (en, es)


def write_temp(test, name, content):
    d = tempfile.TemporaryDirectory()
    test.addCleanup(d.cleanup)
    path = os.path.join(d.name, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


class TextWidthTest(unittest.TestCase):
    def test_text_width_sums_glyph_widths(self):
        self.assertEqual(text_width("AB A", CHARMAP, WIDTHS), 20)

    def test_text_width_rejects_unknown_char(self):
        self.assertRaises(ValueError, text_width, "Z", CHARMAP, WIDTHS)

    def test_text_lines_splits_on_control_codes(self):
        self.assertEqual(text_lines(r"A\nB\pA\lB"), ["A", "B", "A", "B"])


class CheckSourceTest(unittest.TestCase):
    def test_valid_pair_passes(self):
        self.assertEqual(check_source(pair("AB", "Bé"), CHARMAP, WIDTHS), [])

    def test_array_size_is_not_a_text(self):
        src = "static const u8 *const sGuideEndText[GUIDE_LANG_COUNT] =\n" + pair("A", "A") + ";"
        self.assertEqual(check_source(src, CHARMAP, WIDTHS), [])

    def test_missing_language_reported(self):
        errs = check_source('{ [GUIDE_LANG_EN] = _("A"), }', CHARMAP, WIDTHS)
        self.assertEqual(len(errs), 1)
        self.assertIn("sin pareja de idioma", errs[0])

    def test_line_too_wide_reported(self):
        errs = check_source(pair("A" * 37, "A"), CHARMAP, WIDTHS)  # 37 * 6 = 222 px
        self.assertEqual(len(errs), 1)
        self.assertIn("222 px", errs[0])

    def test_wide_text_split_by_newline_passes(self):
        self.assertEqual(check_source(pair("A" * 30 + r"\n" + "A" * 30, "A"), CHARMAP, WIDTHS), [])

    def test_placeholder_reported(self):
        self.assertIn("placeholder", check_source(pair("{PLAYER}", "A"), CHARMAP, WIDTHS)[0])

    def test_unknown_char_reported(self):
        self.assertIn("carácter no soportado", check_source(pair("Z", "A"), CHARMAP, WIDTHS)[0])


class LoadersTest(unittest.TestCase):
    def test_load_charmap_reads_single_chars(self):
        path = write_temp(self, "charmap.txt",
                          "'A'         = BB\n'é'         = 1B\n'\\''         = B4\nPLAYER = FD 01\n@ comentario\n")
        self.assertEqual(load_charmap(path), {'A': 0xBB, 'é': 0x1B, "'": 0xB4})

    def test_load_glyph_widths_reads_only_that_array(self):
        path = write_temp(self, "fonts.c",
                          "const u8 gFontNormalLatinGlyphWidths[] = {\n 3, 6,\n 8 };\nconst u8 other[] = {1};")
        self.assertEqual(load_glyph_widths(path), [3, 6, 8])

    def test_load_ruby_font3_widths_max_of_english_variants(self):
        path = write_temp(self, "font3_widths.h", RUBY_FONT3)
        self.assertEqual(load_ruby_font3_widths(path), [3, 7, 8])


class MainTest(unittest.TestCase):
    def make_decomp(self, steps_source, game="emerald"):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        widths = "6, " * 0xBC
        if game == "ruby":
            font = {"src/data/text/font3_widths.h":
                    "#if ENGLISH\nstatic const u8 sFont3Widths[] = {\n" + widths + "\n};\n#endif\n"}
        else:
            font = {"src/fonts.c": "const u8 gFontNormalLatinGlyphWidths[] = {\n" + widths + "\n};"}
        files = {"charmap.txt": "'A' = BB\n", "src/data/guide_steps.h": steps_source, **font}
        for name, content in files.items():
            path = os.path.join(d.name, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        return d.name

    def test_main_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main([self.make_decomp(pair("A", "A"))]), 0)
            self.assertEqual(main([self.make_decomp(pair("A" * 37, "A"))]), 1)

    def test_main_uses_ruby_width_limit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main([self.make_decomp(pair("A" * 35, "A"), "ruby")]), 1)  # 210 px > 208
            self.assertEqual(main([self.make_decomp(pair("A" * 34, "A"), "ruby")]), 0)  # 204 px
            self.assertEqual(main([self.make_decomp(pair("A" * 35, "A"))]), 0)          # Esmeralda: 216

    def test_main_without_font_file_fails(self):
        root = self.make_decomp(pair("A", "A"))
        os.remove(os.path.join(root, "src", "fonts.c"))
        self.assertRaises(FileNotFoundError, main, [root])


if __name__ == '__main__':
    unittest.main()
