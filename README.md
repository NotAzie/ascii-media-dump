# ascii-render

ascii-render turns images and video into ASCII art. It ships a small command
line tool and a reusable Python library, so you can render from the terminal
or embed the pipeline directly in your own code.

## Quick start

Install the package in a virtual environment:

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

Render an image to text:

```bash
ascii-render image \
  --input ASCII-generator-master/data/input.jpg \
  --output scratch/output.txt \
  --profile detailed \
  --num-cols 160
```

Render an image to a PNG:

```bash
ascii-render image \
  --input ASCII-generator-master/data/input.jpg \
  --output scratch/output.png \
  --profile simple \
  --num-cols 120 \
  --background black
```

Render a color HTML page:

```bash
ascii-render image \
  --input ASCII-generator-master/data/input.jpg \
  --output scratch/output.html \
  --profile detailed \
  --num-cols 160 \
  --color
```

Render a video:

```bash
ascii-render video \
  --input ASCII-generator-master/data/input.mp4 \
  --output scratch/output.mp4 \
  --profile simple \
  --num-cols 100 \
  --font-size 10 \
  --fps 10
```

## What it does

- Reads common image and video inputs through OpenCV.
- Maps brightness to a character set you choose.
- Supports monochrome and color output.
- Can write text, PNG images, and HTML.
- Can render video frame by frame and write a new video file.

## Profiles

Profiles are ordered character sets used to represent brightness.

- `simple` — a compact 10-character set.
- `detailed` — a richer 70-character set.
- `blocks` — block-style shading characters.
- `binary` — a two-character set.

## Typical tuning

The most useful controls are:

- `--profile` — character set
- `--num-cols` — output width
- `--font-size` — rendered font size when producing images or video
- `--scale-y` — vertical spacing scale
- `--background` — black or white background
- `--color` — produce color output instead of monochrome
- `--gamma` — brightness curve
- `--dither` — enable simple dithering
- `--edges` — emphasize edges

Smaller `--num-cols` values give a chunkier look. Smaller `--font-size` values
fit more characters into a rendered image or video frame.

## Library usage

The same pipeline used by the CLI is available as a library:

```python
from ascii_render import (
    RenderingPipeline,
    PipelineConfig,
    DETAILED,
)
from PIL import Image
import numpy as np

image = np.array(Image.open("input.jpg").convert("RGB"))
config = PipelineConfig(
    character_profile=DETAILED,
    num_cols=160,
    background="black",
)
pipeline = RenderingPipeline(config)

text = pipeline.render_to_text(image)
html = pipeline.render_to_html(image)
png = pipeline.render_to_monochrome_image(image)
png.save("output.png")
```

## Project structure

- `ascii_render/core.py` — stateless rendering pipeline and configuration.
- `ascii_render/cli.py` — command line interface.
- `ascii_render/profiles.py` — public character profiles.
- `tests/` — basic unit tests.

The repository also includes earlier experiments and reference scripts under
`ASCII-generator-master/` for historical context. The maintained implementation
lives in `ascii_render/`.

## Development

Format and lint the code:

```bash
python -m ruff format .
python -m ruff check .
```

Run the tests:

```bash
python -m pytest
```

## Documentation

- `CONTRIBUTING.md` — how to contribute
- `CODE_OF_CONDUCT.md` — community standards
- `SECURITY.md` — how to report security issues
- `ROADMAP.md` — planned direction
- `TODO.md` — known follow-up work

## License

MIT
