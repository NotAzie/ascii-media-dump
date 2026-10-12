"""
Core rendering abstractions for ascii_render.

This module is deliberately stateless and deterministic so it can be used from
a CLI, a GUI, or a web backend without hidden global state.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


class OutputFormat(enum.Enum):
    TEXT = "text"
    MONOCHROME_PNG = "monochrome_png"
    COLOR_PNG = "color_png"
    HTML = "html"


@dataclass(frozen=True)
class CharacterProfile:
    """A character set plus metadata about its ordering and density."""

    name: str
    chars: str
    density_sorted: bool = True

    def char_count(self) -> int:
        return len(self.chars)

    def lookup(self, normalized_brightness: float) -> str:
        # Normalized brightness is 0.0 (dark) to 1.0 (light).
        if np.isnan(normalized_brightness):
            normalized_brightness = 0.0
        index = min(int(normalized_brightness * (self.char_count() - 1)), self.char_count() - 1)
        return self.chars[index]


@dataclass
class PipelineConfig:
    """Tuning knobs for the rendering pipeline.

    The defaults are conservative and designed to produce good-looking output
    for a wide range of inputs with minimal user tuning.
    """

    character_profile: CharacterProfile = field(default_factory=lambda: _default_profile())
    num_cols: int = 160
    font_path: str | None = None
    font_size: int = 12
    scale_y: float = 0.5
    background: str = "black"
    color: bool = False
    gamma: float = 2.2
    dither: bool = False
    enhance_edges: bool = False
    brightness: float = 1.0
    contrast: float = 1.0
    output_path: str | None = None

    def fontsize(self) -> int:
        return max(1, self.font_size)

    def background_color(self) -> tuple[int, int, int]:
        return (255, 255, 255) if self.background.lower() == "white" else (0, 0, 0)


def _default_profile() -> CharacterProfile:
    return CharacterProfile(
        name="default",
        chars="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    )


class RenderingPipeline:
    """Convert an image into ASCII output in a variety of formats."""

    def __init__(self, config: PipelineConfig | None = None) -> None:
        self.config = config or PipelineConfig()

    def render_image(self, image: np.ndarray) -> np.ndarray:
        config = self.config
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image

        height, width = gray.shape
        cell_width = width / config.num_cols
        cell_height = config.scale_y * cell_width
        num_rows = int(height / cell_height)

        normalized = gray.astype(np.float32) / 255.0
        normalized = np.clip(normalized**config.gamma, 0.0, 1.0)

        if config.brightness != 1.0 or config.contrast != 1.0:
            normalized = np.clip((normalized - 0.5) * config.contrast + 0.5, 0.0, 1.0)
            normalized = np.clip(normalized * config.brightness, 0.0, 1.0)

        if config.enhance_edges:
            gray_f = gray.astype(np.float32)
            gx = cv2.Sobel(gray_f, cv2.CV_32F, 1, 0, ksize=3)
            gy = cv2.Sobel(gray_f, cv2.CV_32F, 0, 1, ksize=3)
            edges = cv2.magnitude(gx, gy)
            edges = np.clip(edges / (edges.max() + 1e-6), 0.0, 1.0)
            normalized = np.clip(normalized * (1.0 + edges * 0.4), 0.0, 1.0)

        char_grid = np.full((num_rows, config.num_cols), "", dtype=object)
        for i in range(num_rows):
            row_start = int(i * cell_height)
            row_end = int((i + 1) * cell_height)
            row_end = min(row_end, height)
            for j in range(config.num_cols):
                col_start = int(j * cell_width)
                col_end = int((j + 1) * cell_width)
                col_end = min(col_end, width)
                block = normalized[row_start:row_end, col_start:col_end]
                avg_brightness = float(block.mean()) if block.size else 0.0
                avg_brightness = 0.0 if np.isnan(avg_brightness) else avg_brightness
                char_grid[i, j] = config.character_profile.lookup(avg_brightness)

        return char_grid

    def render_to_text(self, image: np.ndarray) -> str:
        grid = self.render_image(image)
        return "\n".join("".join(row) for row in grid)

    def render_to_monochrome_image(self, image: np.ndarray) -> Image.Image:
        config = self.config
        grid = self.render_image(image)
        font = _load_font(config.font_path, config.fontsize())
        char_width, char_height = _measure_glyph(font, "A")

        char_map = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
        }
        bg = char_map.get(config.background.lower(), (0, 0, 0))
        fg = (255, 255, 255) if bg == (0, 0, 0) else (0, 0, 0)

        out_width = char_width * config.num_cols
        out_height = int(config.scale_y * char_height * grid.shape[0])
        out_image = Image.new("RGB", (out_width, out_height), bg)
        draw = ImageDraw.Draw(out_image)

        for i in range(grid.shape[0]):
            line = "".join(grid[i, j] for j in range(config.num_cols))
            y = int(i * char_height * config.scale_y)
            draw.text((0, y), line, fill=fg, font=font)

        bbox = (
            ImageOps.invert(out_image).getbbox() if bg == (255, 255, 255) else out_image.getbbox()
        )
        if bbox:
            out_image = out_image.crop(bbox)
        return out_image

    def render_to_color_image(self, image: np.ndarray) -> Image.Image:
        config = self.config
        bgr = (
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if image.ndim == 3
            else cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        )
        grid = self.render_image(image)
        font = _load_font(config.font_path, config.fontsize())
        char_width, char_height = _measure_glyph(font, "A")

        bg = config.background_color()
        out_width = char_width * config.num_cols
        out_height = int(config.scale_y * char_height * grid.shape[0])
        out_image = Image.new("RGB", (out_width, out_height), bg)
        draw = ImageDraw.Draw(out_image)

        cell_height = config.scale_y * (bgr.shape[0] / config.num_cols)
        cell_width = bgr.shape[1] / config.num_cols

        for i in range(grid.shape[0]):
            row_start = int(i * cell_height)
            row_end = int((i + 1) * cell_height)
            row_end = min(row_end, bgr.shape[0])
            y = int(i * char_height * config.scale_y)
            for j in range(config.num_cols):
                col_start = int(j * cell_width)
                col_end = int((j + 1) * cell_width)
                col_end = min(col_end, bgr.shape[1])
                block = bgr[row_start:row_end, col_start:col_end]
                if block.size:
                    avg_color = tuple(int(x) for x in block.reshape(-1, 3).mean(axis=0))
                else:
                    avg_color = bg
                draw.text((int(j * char_width), y), grid[i, j], fill=avg_color, font=font)

        bbox = (
            ImageOps.invert(out_image).getbbox() if bg == (255, 255, 255) else out_image.getbbox()
        )
        if bbox:
            out_image = out_image.crop(bbox)
        return out_image

    def render_to_html(self, image: np.ndarray) -> str:
        config = self.config
        if not config.color:
            text = self.render_to_text(image)
            body = "".join(f"<div>{line}</div>" for line in text.splitlines())
            return (
                "<!DOCTYPE html><html><head><meta charset='utf-8'>"
                "<style>body{background:#000;color:#fff;font-family:monospace;font-size:10px;line-height:1}div{white-space:pre}</style></head><body>"
                f"{body}</body></html>"
            )

        grid = self.render_image(image)
        bgr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cell_height = config.scale_y * (bgr.shape[0] / config.num_cols)
        cell_width = bgr.shape[1] / config.num_cols
        rows: list[str] = []
        for i in range(grid.shape[0]):
            spans: list[str] = []
            row_start = int(i * cell_height)
            row_end = int((i + 1) * cell_height)
            row_end = min(row_end, bgr.shape[0])
            for j in range(config.num_cols):
                col_start = int(j * cell_width)
                col_end = int((j + 1) * cell_width)
                col_end = min(col_end, bgr.shape[1])
                block = bgr[row_start:row_end, col_start:col_end]
                if block.size:
                    r, g, b = (int(x) for x in block.reshape(-1, 3).mean(axis=0))
                else:
                    r = g = b = 0
                spans.append(f'<span style="color:rgb({r},{g},{b})">{grid[i, j]}</span>')
            rows.append("".join(spans))
        body = "".join(f"<div>{row}</div>" for row in rows)
        return (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<style>body{background:#000;color:#fff;font-family:monospace;font-size:10px;line-height:1}div{white-space:pre;display:block}</style></head><body>"
            f"{body}</body></html>"
        )

    def save(self, image: np.ndarray, output_path: str | None = None) -> str:
        config = self.config
        path = output_path or config.output_path
        if not path:
            raise ValueError("No output path configured")

        suffix = path.lower()
        if suffix.endswith(".txt"):
            payload = self.render_to_text(image)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(payload)
            return path
        if suffix.endswith(".png"):
            if config.color:
                img = self.render_to_color_image(image)
            else:
                img = self.render_to_monochrome_image(image)
            img.save(path)
            return path
        if suffix.endswith(".html") or suffix.endswith(".htm"):
            payload = self.render_to_html(image)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(payload)
            return path
        raise ValueError(f"Unsupported output extension: {path!r}")


def _measure_glyph(font: ImageFont.FreeTypeFont, sample_char: str = "A") -> tuple[int, int]:
    bbox = font.getbbox(sample_char)
    if bbox is None:
        return (0, 0)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])


def _load_font(path: str | None, size: int) -> ImageFont.FreeTypeFont:
    if path:
        return ImageFont.truetype(path, size=size)
    for candidate in ("DejaVuSansMono-Bold.ttf", "DejaVuSansMono.ttf", "Consolas", "Courier New"):
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()
