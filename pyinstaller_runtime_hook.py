"""PyInstaller runtime hook.

The game loads every asset with a path relative to the project root
(e.g. ``img/...``, ``music/...``, ``sound_effect/...``, ``font.ttf``).
``config.py`` even loads sounds at import time. When frozen, the current
working directory is wherever the user launched the .exe, so those
relative paths would break.

This hook runs before any application code (including imports), and
points the working directory at the bundled resources so every relative
path keeps working unchanged.
"""
import os
import sys

if getattr(sys, "frozen", False):
    # In both onefile and onedir builds, bundled data lives under _MEIPASS.
    os.chdir(getattr(sys, "_MEIPASS"))
