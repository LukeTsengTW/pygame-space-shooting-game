import argparse
from pathlib import Path

from PIL import Image, ImageChops


def make_vertical_tile(
    source_path,
    output_path,
    width=600,
    height=1536,
    blend_height=96,
):
    source_path = Path(source_path)
    output_path = Path(output_path)

    with Image.open(source_path) as source:
        image = source.convert("RGB")

    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    image = resized.crop((left, top, left + width, top + height))

    half = height // 2
    image = ImageChops.offset(image, 0, half)

    blend_height = min(blend_height, half)
    upper = image.crop((0, half - blend_height, width, half))
    lower = image.crop((0, half, width, half + blend_height))
    mask = Image.new("L", (width, blend_height))
    denominator = max(1, blend_height - 1)
    for y in range(blend_height):
        alpha = round(255 * y / denominator)
        mask.paste(alpha, (0, y, width, y + 1))
    image.paste(Image.composite(lower, upper, mask), (0, half - blend_height // 2))

    first_row = image.crop((0, 0, width, 1))
    image.paste(first_row, (0, height - 1))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_options = {"quality": 100, "subsampling": 0} if output_path.suffix.lower() in {".jpg", ".jpeg"} else {}
    image.save(output_path, **save_options)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a vertically tileable game background."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=600)
    parser.add_argument("--height", type=int, default=1536)
    parser.add_argument("--blend-height", type=int, default=96)
    return parser.parse_args()


def main():
    args = parse_args()
    make_vertical_tile(
        args.source,
        args.output,
        width=args.width,
        height=args.height,
        blend_height=args.blend_height,
    )


if __name__ == "__main__":
    main()
