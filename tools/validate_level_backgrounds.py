import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
from PIL import Image, ImageChops, ImageStat

from background import ScrollingBackground


EXPECTED_SIZE = (600, 1536)
VIEWPORT_SIZE = (600, 900)
TEST_OFFSETS = (0, 1, 899, 1534, 1535)


def inspect_background(path):
    path = Path(path)
    with Image.open(path) as source:
        image = source.convert("RGB")

    if image.size != EXPECTED_SIZE:
        raise ValueError(
            f"{path} expected 600x1536, received {image.width}x{image.height}"
        )

    top = image.crop((0, 0, image.width, 1))
    bottom = image.crop((0, image.height - 1, image.width, image.height))
    difference = ImageChops.difference(top, bottom)
    edge_mean = sum(ImageStat.Stat(difference).mean) / 3
    return {"path": path, "size": image.size, "edge_mean": edge_mean}


def validate_viewport_coverage(path):
    pygame.init()
    pygame.display.set_mode((1, 1))
    try:
        surface = pygame.image.load(path).convert()
        scroller = ScrollingBackground(surface)
        sentinel = (1, 254, 1)

        for offset in TEST_OFFSETS:
            target = pygame.Surface(VIEWPORT_SIZE)
            target.fill(sentinel)
            scroller.offset = offset
            scroller.draw(target)
            sentinel_color = target.map_rgb(sentinel)
            pixels = pygame.PixelArray(target)
            try:
                if any(sentinel_color in pixels[x] for x in range(target.get_width())):
                    raise ValueError(f"{path} leaves an uncovered pixel at {offset}")
            finally:
                pixels.close()
    finally:
        pygame.quit()


def validate_levels(
    start_level,
    end_level,
    background_dir=Path("img/background"),
    edge_limit=3.0,
):
    results = []
    background_dir = Path(background_dir)
    for level in range(start_level, end_level + 1):
        path = background_dir / f"lv{level}_background.jpg"
        result = inspect_background(path)
        if result["edge_mean"] > edge_limit:
            raise ValueError(
                f"{path} edge difference {result['edge_mean']:.3f} exceeds "
                f"{edge_limit}"
            )
        validate_viewport_coverage(path)
        results.append(result)
    return results


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate processed level background assets."
    )
    parser.add_argument("--start-level", type=int, required=True)
    parser.add_argument("--end-level", type=int, required=True)
    parser.add_argument(
        "--background-dir",
        type=Path,
        default=Path("img/background"),
    )
    parser.add_argument("--edge-limit", type=float, default=3.0)
    return parser.parse_args()


def main():
    args = parse_args()
    results = validate_levels(
        args.start_level,
        args.end_level,
        args.background_dir,
        args.edge_limit,
    )
    for result in results:
        print(
            f"{result['path']}: size={result['size'][0]}x{result['size'][1]}, "
            f"edge_mean={result['edge_mean']:.3f}, viewport=covered"
        )


if __name__ == "__main__":
    main()
