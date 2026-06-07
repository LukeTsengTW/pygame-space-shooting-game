import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.validate_level_backgrounds import inspect_background, validate_levels


class LevelBackgroundValidationTests(unittest.TestCase):
    def test_cli_can_start_from_the_project_root(self):
        result = subprocess.run(
            [
                sys.executable,
                "tools/validate_level_backgrounds.py",
                "--help",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_inspect_background_reports_size_and_edge_difference(self):
        with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
            path = Path(directory) / "background.jpg"
            image = Image.new("RGB", (600, 1536), (5, 10, 20))
            image.save(path, quality=92, subsampling=0)

            result = inspect_background(path)

            self.assertEqual(result["size"], (600, 1536))
            self.assertEqual(result["edge_mean"], 0)

    def test_inspect_background_rejects_wrong_dimensions(self):
        with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
            path = Path(directory) / "background.jpg"
            Image.new("RGB", (600, 900), (5, 10, 20)).save(path)

            with self.assertRaisesRegex(ValueError, "expected 600x1536"):
                inspect_background(path)

    def test_validate_levels_requires_every_file_in_range(self):
        with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
            background_dir = Path(directory)
            image = Image.new("RGB", (600, 1536), (5, 10, 20))
            image.save(background_dir / "lv2_background.jpg")

            with self.assertRaises(FileNotFoundError):
                validate_levels(2, 3, background_dir)
