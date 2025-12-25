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
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=cfg.SCRIPT_NAME,
        help="Name of the script as it appears in FL Studio",
    )

    return parser
