import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.make_vertical_tile import make_vertical_tile


class VerticalTileTests(unittest.TestCase):
    def test_output_has_runtime_dimensions_and_matching_edges(self):
        with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
            source = Path(directory) / "source.png"
            output = Path(directory) / "output.png"
            image = Image.new("RGB", (768, 1536))
            for y in range(image.height):
                color = (y % 256, 20, 40)
                image.paste(color, (0, y, image.width, y + 1))
            image.save(source)

            make_vertical_tile(source, output, 600, 1536, blend_height=96)

            with Image.open(output) as result:
                self.assertEqual(result.size, (600, 1536))
                self.assertEqual(
                    result.crop((0, 0, 600, 1)).tobytes(),
                    result.crop((0, 1535, 600, 1536)).tobytes(),
                )

    def test_jpeg_output_keeps_edge_difference_below_three(self):
        with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
            source = Path("img/background/source/lv8_background_source.png")
            output = Path(directory) / "output.jpg"

            make_vertical_tile(source, output, 600, 1536, blend_height=96)

            with Image.open(output) as result:
                top = result.convert("RGB").crop((0, 0, 600, 1))
                bottom = result.convert("RGB").crop((0, 1535, 600, 1536))
                differences = [
                    abs(a - b)
                    for a, b in zip(top.tobytes(), bottom.tobytes())
                ]
                edge_mean = sum(differences) / len(differences)

            self.assertLessEqual(edge_mean, 3.0)
