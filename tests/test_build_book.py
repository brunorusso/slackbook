from pathlib import Path
import tempfile
import unittest

from tools import build_book


class BuildBookTest(unittest.TestCase):
    def test_main_file_order_and_index(self):
        repo_root = Path(build_book.__file__).resolve().parents[1]
        src_dir = repo_root / "src-book"

        order = build_book.read_main_markdown_order(src_dir / "main.md")
        self.assertEqual(order[0].name, "cover.md")
        self.assertEqual(order[1].name, "preface.md")
        self.assertEqual(order[2].name, "chapter_01.md")

        toc = build_book.build_toc(order)
        self.assertIn('href="#slackware-linux-essentials-version-beta"', toc)
        self.assertIn('href="#11-why-use-slackware"', toc)
        self.assertIn('href="#12-differences-compared-to-other-linux-distributions"', toc)

    def test_generate_html_orders_cover_before_toc_and_rest(self):
        repo_root = Path(build_book.__file__).resolve().parents[1]
        html = build_book.generate_book_html(repo_root / "src-book")
        self.assertLess(html.index('<section id="cover"'), html.index('<nav class="book-toc">'))
        self.assertLess(html.index('<nav class="book-toc">'), html.index('<section id="preface"'))

    def test_copy_asset_directories_preserve_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir) / "src-book"
            output_dir = Path(tmpdir) / "the-book"
            (src_dir / "img" / "nested").mkdir(parents=True)
            (src_dir / "ps-imgs" / "other").mkdir(parents=True)
            (src_dir / "img" / "nested" / "logo.png").write_bytes(b"img-data")
            (src_dir / "ps-imgs" / "other" / "scan.png").write_bytes(b"ps-data")

            build_book.copy_asset_directories(src_dir, output_dir)

            self.assertTrue((output_dir / "img" / "nested" / "logo.png").exists())
            self.assertTrue((output_dir / "ps-imgs" / "other" / "scan.png").exists())
            self.assertEqual((output_dir / "img" / "nested" / "logo.png").read_bytes(), b"img-data")
            self.assertEqual((output_dir / "ps-imgs" / "other" / "scan.png").read_bytes(), b"ps-data")

    def test_cli_flags_parse_html_and_pdf_modes(self):
        html_args = build_book.parse_args(["--html"])
        pdf_args = build_book.parse_args(["--pdf"])

        self.assertEqual(html_args.output_format, "html")
        self.assertEqual(pdf_args.output_format, "pdf")


if __name__ == "__main__":
    unittest.main()
