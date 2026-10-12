"""Tests for ascii_render.core.

These tests are deliberately narrow but high-signal: they check that the
pipeline is deterministic, that every output format is reachable, and that
the public API contracts hold for the kinds of inputs the package is meant
to accept.
"""

from __future__ import annotations

import cv2
import numpy as np
import pytest
from PIL import Image

from ascii_render.core import (
    CharacterProfile,
    PipelineConfig,
    RenderingPipeline,
)

LIGHT_PROFILE = CharacterProfile(name="light", chars=" .X")


def _rgb_grid(width: int, height: int, value: int = 128) -> np.ndarray:
    return np.full((height, width, 3), value, dtype=np.uint8)


class TestCharacterProfile:
    def test_lookup_bounds_dark(self) -> None:
        profile = CharacterProfile(name="test", chars=" .")
        assert profile.lookup(0.0) == " "

    def test_lookup_bounds_light(self) -> None:
        profile = CharacterProfile(name="test", chars=" .")
        assert profile.lookup(1.0) == "."

    def test_lookup_midpoint(self) -> None:
        profile = CharacterProfile(name="test", chars=" .")
        assert profile.lookup(0.5) in {" ", "."}

    def test_lookup_nan_safe(self) -> None:
        profile = CharacterProfile(name="test", chars=" .")
        assert profile.lookup(float("nan")) in {" ", "."}

    def test_char_count(self) -> None:
        profile = CharacterProfile(name="test", chars="abc")
        assert profile.char_count() == 3


class TestPipelineConfig:
    def test_default_background_is_black(self) -> None:
        config = PipelineConfig()
        assert config.background_color() == (0, 0, 0)

    def test_white_background(self) -> None:
        config = PipelineConfig(background="white")
        assert config.background_color() == (255, 255, 255)

    def test_fontsize_positive(self) -> None:
        config = PipelineConfig(font_size=0)
        assert config.fontsize() == 1
        config = PipelineConfig(font_size=12)
        assert config.fontsize() == 12


class TestRenderingPipelineDeterminism:
    def test_same_image_same_text(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        text_a = pipeline.render_to_text(image)
        text_b = pipeline.render_to_text(image)
        assert text_a == text_b

    def test_render_image_shape(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        grid = pipeline.render_image(image)
        assert grid.shape[1] == 40
        assert grid.shape[0] > 0

    def test_render_to_text_nonempty(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            character_profile=LIGHT_PROFILE,
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 200)
        text = pipeline.render_to_text(image)
        assert text.strip()

    def test_render_to_monochrome_image_is_pil(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="black",
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        out = pipeline.render_to_monochrome_image(image)
        assert isinstance(out, Image.Image)

    def test_render_to_color_image_is_pil(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="black",
            color=True,
            character_profile=LIGHT_PROFILE,
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 200)
        out = pipeline.render_to_color_image(image)
        assert isinstance(out, Image.Image)

    def test_render_to_html_is_html(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="black",
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        text_html = pipeline.render_to_html(image)
        assert "<!DOCTYPE" in text_html
        color_html = pipeline.render_to_html(image)
        assert "<!DOCTYPE" in color_html


class TestRenderingPipelineSave:
    def test_save_txt(self, tmp_path) -> None:
        config = PipelineConfig(
            num_cols=40,
            output_path=str(tmp_path / "out.txt"),
            character_profile=LIGHT_PROFILE,
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 200)
        path = pipeline.save(image)
        assert path.endswith("out.txt")
        assert (tmp_path / "out.txt").exists()
        assert (tmp_path / "out.txt").read_text().strip()

    def test_save_png_black(self, tmp_path) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="black",
            output_path=str(tmp_path / "out.png"),
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        path = pipeline.save(image)
        assert path.endswith("out.png")
        assert (tmp_path / "out.png").exists()
        with Image.open(tmp_path / "out.png") as im:
            assert im.size[0] > 0 and im.size[1] > 0

    def test_save_png_white(self, tmp_path) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="white",
            output_path=str(tmp_path / "out.png"),
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        path = pipeline.save(image)
        assert path.endswith("out.png")
        assert (tmp_path / "out.png").exists()

    def test_save_html(self, tmp_path) -> None:
        config = PipelineConfig(
            num_cols=40,
            output_path=str(tmp_path / "out.html"),
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        path = pipeline.save(image)
        assert path.endswith("out.html")
        assert (tmp_path / "out.html").exists()
        assert "<!DOCTYPE" in (tmp_path / "out.html").read_text()

    def test_save_color_html(self, tmp_path) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="black",
            color=True,
            output_path=str(tmp_path / "out.html"),
            character_profile=LIGHT_PROFILE,
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 200)
        path = pipeline.save(image)
        assert path.endswith("out.html")
        assert "<!DOCTYPE" in (tmp_path / "out.html").read_text()

    def test_save_unsupported_extension(self, tmp_path) -> None:
        config = PipelineConfig(
            num_cols=40,
            output_path=str(tmp_path / "out.xyz"),
            character_profile=CharacterProfile(name="test", chars=" ."),
        )
        pipeline = RenderingPipeline(config)
        image = _rgb_grid(80, 40, 128)
        with pytest.raises(ValueError, match="Unsupported output extension"):
            pipeline.save(image)


class TestRenderingPipelineColorInputHandling:
    def test_grayscale_input_still_produces_color_output_when_enabled(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="black",
            color=True,
            character_profile=LIGHT_PROFILE,
        )
        pipeline = RenderingPipeline(config)
        gray = np.full((40, 80), 200, dtype=np.uint8)
        out = pipeline.render_to_color_image(gray)
        assert isinstance(out, Image.Image)

    def test_bgr_input_produces_color_output_when_enabled(self) -> None:
        config = PipelineConfig(
            num_cols=40,
            background="black",
            color=True,
            character_profile=LIGHT_PROFILE,
        )
        pipeline = RenderingPipeline(config)
        bgr = _rgb_grid(80, 40, 200)
        bgr_bgr = cv2.cvtColor(bgr, cv2.COLOR_RGB2BGR)
        out = pipeline.render_to_color_image(bgr_bgr)
        assert isinstance(out, Image.Image)


@pytest.mark.parametrize("profile_name", ["simple", "detailed", "blocks", "binary"])
def test_cli_profile_names_match_public_profiles(profile_name: str) -> None:
    from ascii_render.profiles import BLOCKS, BINARY, DETAILED, SIMPLE

    profiles = {
        "simple": SIMPLE,
        "detailed": DETAILED,
        "blocks": BLOCKS,
        "binary": BINARY,
    }
    assert profile_name in profiles
    assert profiles[profile_name].name == profile_name
