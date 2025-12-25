"""Build script to generate a single-file MIDI script"""

import ast
import black
import logging
from pathlib import Path
from typing import List

from config import *
from ast_tools import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")


def main() -> None:
    logger.info("Building MIDI script...")

    body_collector = BodyCollector()
    imports_collector = ImportsCollector()
    const_collector = ConstCollector()
    enum_collector = EnumCollector()

    def _process_module(mod_path: Path) -> None:
        source = mod_path.read_text(encoding="utf-8")
        tree = ast.parse(source, mod_path.name)

        body_collector.visit(tree)
        imports_collector.visit(tree)
        const_collector.visit(tree)
        enum_collector.visit(tree)

    for pkg in cfg.PACKAGES:
        pkg_path: Path = cfg.SRC / pkg
        if not Path.exists(pkg_path):
            logger.warning(f"Package {pkg} not found, skipping.")
            continue
        pkg_files: List[Path] = list(pkg_path.glob("*.py"))
        for mod_path in sorted(pkg_files):
            _process_module(mod_path)

    for mod in cfg.MODULES:
        mod_path: Path = cfg.SRC / f"{mod}.py"
        if not Path.exists(mod_path):
            logger.warning(f"Module {mod}.py not found, skipping.")
            continue
        _process_module(mod_path)

    with open(cfg.OUT_PATH, "w", encoding="utf-8") as out:
        out.write(f"# name={cfg.SCRIPT_NAME}\n\n")
        out.write(cfg.HEADER + "\n\n")

        imports = ImportsRemover().visit(imports_collector.imports)
        ast.fix_missing_locations(imports)
        out.write(ast.unparse(imports) + "\n\n\n")

        body = body_collector.body
        consts = const_collector.consts
        enums = enum_collector.enums

        body = AllRemover().visit(body)
        body = FlMidiMsgRemover().visit(body)
        body = DocstringRemover().visit(body)
        body = ConstInliner(consts).visit(body)
        body = ConstRemover(consts).visit(body)
        body = EnumInliner(enums).visit(body)
        ast.fix_missing_locations(body)
        out.write(ast.unparse(body))

    black.format_file_in_place(
        cfg.OUT_PATH,
        fast=True,
        mode=black.FileMode(),
        write_back=black.WriteBack.YES,
    )

    logger.info(f"Done. Built MIDI script at {cfg.OUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
