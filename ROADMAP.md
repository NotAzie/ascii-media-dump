# Roadmap

This roadmap tracks the intended direction of ascii-render. Items are
prioritized by usefulness, maintainability, and how well they fit the core
purpose of rendering images and video as ASCII art.

## Current focus

- Stabilize the core rendering pipeline and CLI behavior.
- Improve test coverage around edge cases: very small images, grayscale
  inputs, empty blocks, and color output paths.
- Improve documentation for first-time users and contributors.

## Near term

- Refine default profiles and rendering quality across common fonts.
- Make font discovery more robust across platforms.
- Clarify supported video codecs and output formats on common platforms.
- Add a small set of sample commands and expected outputs in the README.

## Medium term

- Add optional preprocessing helpers people commonly want, such as contrast
  normalization or resize presets, without turning the package into a general
  image editor.
- Improve performance for large inputs where practical.
- Improve portability notes for Windows, macOS, and Linux.

## Longer term

- Explore optional convenience layers such as a minimal web interface or
  reusable library API for embedding the renderer elsewhere.
- Keep the project focused: new output formats and input sources should
  serve the ascii art use case rather than drift into a general multimedia
  tool.

## Out of scope

- Full GUI editors.
- Deep learning-based image restoration or style transfer.
- Turning this into a broad video processing framework with unrelated features.

The roadmap is a guide, not a promise. Practical needs and contributor
energy will determine the order items are completed.
