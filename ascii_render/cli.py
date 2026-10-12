"""
Command line interface for ascii_render.

The CLI is intentionally thin. All of the real work lives in ascii_render.core
so the same pipeline can be reused by other callers and tests.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np

from ascii_render.core import (
    PipelineConfig,
    RenderingPipeline,
    CharacterProfile,
)
from ascii_render.profiles import BINARY, BLOCKS, DETAILED, SIMPLE


def _default_font_paths() -> list[Path]:
    return [
        Path(__file__).resolve().parent.parent / "fonts" / "DejaVuSansMono-Bold.ttf",
        (
            Path(__file__).resolve().parent.parent
            / "ASCII-generator-master"
            / "fonts"
            / "DejaVuSansMono-Bold.ttf"
        ),
    ]


def _profile_from_name(name: str) -> CharacterProfile:
    profiles = {
        "simple": SIMPLE,
        "detailed": DETAILED,
        "blocks": BLOCKS,
        "binary": BINARY,
    }
    if name not in profiles:
        raise ValueError(f"Unknown profile: {name!r}. Known: {sorted(profiles)}")
    return profiles[name]


def _pipeline_from_args(args: argparse.Namespace) -> RenderingPipeline:
    profile = _profile_from_name(args.profile)
    font_path = args.font or next((str(p) for p in _default_font_paths() if p.exists()), None)
    config = PipelineConfig(
        character_profile=profile,
        num_cols=args.num_cols,
        font_path=font_path,
        font_size=args.font_size,
        scale_y=args.scale_y,
        background=args.background,
        color=args.color,
        gamma=args.gamma,
        dither=args.dither,
        enhance_edges=args.edges,
        output_path=args.output,
    )
    return RenderingPipeline(config)


def _read_image(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path!r}")
    return image


def _read_video(path: str):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {path!r}")
    return cap


def _write_video_header(
    writer: cv2.VideoWriter | None,
    output_path: str,
    frame_w: int,
    frame_h: int,
    fps: float,
    codec: str,
) -> cv2.VideoWriter:
    if writer is None:
        return cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*codec),
            fps,
            (frame_w, frame_h),
        )
    return writer


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ascii-render", description="Render images and video as ASCII art"
    )
    subparsers = parser.add_subparsers(dest="command")

    image_parser = subparsers.add_parser("image", help="Convert an image to ASCII output")
    image_parser.add_argument("--input", required=True, help="Input image path")
    image_parser.add_argument("--output", required=True, help="Output path (.txt/.png/.html)")
    image_parser.add_argument(
        "--profile",
        default="detailed",
        help="Character profile: simple, detailed, blocks, binary",
    )
    image_parser.add_argument("--num-cols", type=int, default=160)
    image_parser.add_argument("--font-size", type=int, default=12)
    image_parser.add_argument("--scale-y", type=float, default=0.5)
    image_parser.add_argument("--background", choices=("black", "white"), default="black")
    image_parser.add_argument("--color", action="store_true")
    image_parser.add_argument("--gamma", type=float, default=2.2)
    image_parser.add_argument("--dither", action="store_true")
    image_parser.add_argument("--edges", action="store_true")
    image_parser.add_argument("--font", help="Path to a TrueType font")

    video_parser = subparsers.add_parser("video", help="Convert a video to an ASCII video")
    video_parser.add_argument("--input", required=True, help="Input video path")
    video_parser.add_argument("--output", required=True, help="Output video path")
    video_parser.add_argument("--profile", default="detailed")
    video_parser.add_argument("--num-cols", type=int, default=120)
    video_parser.add_argument("--font-size", type=int, default=10)
    video_parser.add_argument("--scale-y", type=float, default=0.5)
    video_parser.add_argument("--background", choices=("black", "white"), default="black")
    video_parser.add_argument("--color", action="store_true")
    video_parser.add_argument("--fps", type=int, default=0, help="Override source frame rate")
    video_parser.add_argument(
        "--codec",
        default="mp4v",
        help="Video codec tag recognized by OpenCV's VideoWriter",
    )
    video_parser.add_argument(
        "--overlay-ratio",
        type=float,
        default=0.0,
        help="Overlay source video in a corner",
    )
    video_parser.add_argument("--font", help="Path to a TrueType font")
    video_parser.add_argument("--gamma", type=float, default=2.2)
    video_parser.add_argument("--dither", action="store_true")
    video_parser.add_argument("--edges", action="store_true")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0

    try:
        if args.command == "image":
            image = _read_image(args.input)
            pipeline = _pipeline_from_args(args)
            pipeline.save(image, args.output)
            print(f"Saved: {args.output}")
            return 0

        if args.command == "video":
            cap = _read_video(args.input)
            source_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            fps = float(args.fps) if args.fps > 0 else source_fps
            pipeline = _pipeline_from_args(args)
            writer: cv2.VideoWriter | None = None
            frame_index = 0
            while True:
                flag, frame = cap.read()
                if not flag:
                    break
                frame_index += 1
                rendered = (
                    pipeline.render_to_color_image(frame)
                    if args.color
                    else pipeline.render_to_monochrome_image(frame)
                )
                frame_np = np.array(rendered)
                frame_np = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
                if writer is None:
                    writer = _write_video_header(
                        writer,
                        args.output,
                        frame_np.shape[1],
                        frame_np.shape[0],
                        fps,
                        args.codec,
                    )
                if args.overlay_ratio and args.overlay_ratio > 0:
                    h, w, _ = frame_np.shape
                    size = (int(w * args.overlay_ratio), int(h * args.overlay_ratio))
                    overlay = cv2.resize(frame, size)
                    frame_np[h - size[1] :, w - size[0] :, :] = overlay
                writer.write(frame_np)
            cap.release()
            if writer:
                writer.release()
            print(f"Saved: {args.output} ({frame_index} frames)")
            return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
