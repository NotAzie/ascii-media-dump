"""Opinionated character profiles for ascii_render.

Re-export the built-in profiles so callers can compose them without
depending on the exact character string ordering used in the CLI.
"""

from ascii_render.core import CharacterProfile

SIMPLE = CharacterProfile(
    name="simple",
    chars="@%#*+=-:. ",
)

DETAILED = CharacterProfile(
    name="detailed",
    chars="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
)

BLOCKS = CharacterProfile(
    name="blocks",
    chars="█▓▒░ ",
)

BINARY = CharacterProfile(
    name="binary",
    chars="01 ",
)

__all__ = [
    "SIMPLE",
    "DETAILED",
    "BLOCKS",
    "BINARY",
]
