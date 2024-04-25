from __future__ import annotations

import matplotlib.pyplot as plt

from pathlib import Path


def walk(file: Path) -> Path | None:
    for parent in [file, *file.parents]:
        if parent.is_dir():
            path = parent.joinpath('venv')

            if path.exists() and path.is_dir():
                return path.parent

    return None


current = Path.cwd()

CWD = walk(current)
ASSET = CWD.joinpath('asset')
FILTER = CWD.joinpath('filter')
GUI = CWD.joinpath('gui')
ACTION = GUI.joinpath('icon')
LIB = CWD.joinpath('lib')

ICON = ASSET.joinpath('pioneer.png')

PALETTE = plt.cm.get_cmap('tab20')
length = len(PALETTE.colors)

color = [
    PALETTE(i)[:3]
    for i in range(length)
]

black = (0, 0, 0)
color.insert(0, black)

COLOR = dict(enumerate(color))
