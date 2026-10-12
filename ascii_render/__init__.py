"""ascii_render - render images and video as ASCII art.

The package is intentionally split into a thin CLI and a stateless core
pipeline so the same rendering logic can be reused by other callers,
tests, or bindings without reaching for hidden global state.
"""

from ascii_render.core import (
    CharacterProfile,
    OutputFormat,
    PipelineConfig,
    RenderingPipeline,
)
from ascii_render.profiles import (
    BINARY,
    BLOCKS,
    DETAILED,
    SIMPLE,
)

__all__ = [
    "BINARY",
    "BLOCKS",
    "CharacterProfile",
    "DETAILED",
    "OutputFormat",
    "PipelineConfig",
    "RenderingPipeline",
    "SIMPLE",
]
