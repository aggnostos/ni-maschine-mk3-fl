import argparse
from pathlib import Path

from config import cfg

__all__ = ["init_parser"]


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FL Studio MIDI Controller Script")

    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=cfg.OUT_PATH,
        help="Path to output the built script file",
    )

    return parser
