import ast
from typing import Optional, Set, Tuple, Dict

from settings import MODULES, PACKAGES


__all__ = [
    "ImportsCollector",
    "ImportsRemover",
    "BodyCollector",
    "AllRemover",
    "FlMidiMsgRemover",
    "DocstringRemover",
    "ConstCollector",
    "ConstInliner",
    "ConstRemover",
    "EnumCollector",
    "EnumInliner",
]


class ImportsCollector(ast.NodeVisitor):
    def __init__(self):
        self.imports = ast.Module(body=[], type_ignores=[])

    def visit_Import(self, node: ast.Import) -> None:
        self.imports.body.append(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.imports.body.append(node)


class ImportsRemover(ast.NodeTransformer):
    def __init__(self) -> None:
        self._seen: Set[Tuple[str, ...]] = set()
        self.result: ast.Module = ast.Module(body=[], type_ignores=[])

    def visit_Import(self, node: ast.Import) -> Optional[ast.Import]:
        if self._is_local(node) or self._is_duplicate(node):
            return None
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Optional[ast.ImportFrom]:
        if (
            self._is_local(node)
            or self._is_duplicate(node)
            or self._is_fl_classes(node)
        ):
            return None

        return node

    def _is_local(self, node: ast.AST) -> bool:
        if isinstance(node, ast.ImportFrom):
            return node.module in MODULES or node.module in PACKAGES
        if isinstance(node, ast.Import):
            return any(
                alias.name in MODULES or alias.name in PACKAGES for alias in node.names
            )
        return False

    def _is_duplicate(self, node: ast.AST) -> bool:
        key = self._get_import_key(node)
        if key in self._seen:
            return True
        self._seen.add(key)
        return False

    def _is_fl_classes(self, node: ast.AST) -> bool:
        return isinstance(node, ast.ImportFrom) and node.module == "fl_classes"

    def _get_import_key(self, node: ast.AST) -> Tuple[str, ...]:
        if isinstance(node, ast.Import):
            return ("import", *tuple(sorted(alias.name for alias in node.names)))
        if isinstance(node, ast.ImportFrom):
            return (
                "from",
                node.module or "",
                *tuple(sorted(alias.name for alias in node.names)),
            )
        return ()


class BodyCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.body = ast.Module(body=[], type_ignores=[])

    def visit_Module(self, node: ast.Module) -> None:
        self.generic_visit(node)
        for stmt in node.body:
            if not isinstance(stmt, (ast.Import, ast.ImportFrom)):
                self.body.body.append(stmt)


class AllRemover(ast.NodeTransformer):
    def visit_Assign(self, node: ast.Assign) -> Optional[ast.Assign]:
        if any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            return None
        return node


class FlMidiMsgRemover(ast.NodeTransformer):
    def visit_arg(self, node: ast.arg) -> ast.arg:
        if (
            node.annotation
            and isinstance(node.annotation, ast.Name)
            and node.annotation.id == "FlMidiMsg"
        ):
            node.annotation = None
        return node


class DocstringRemover(ast.NodeTransformer):
    def visit_Module(self, node: ast.Module) -> ast.Module:
        self.generic_visit(node)
        return self._remove_docstring(node)  # type: ignore[return-value]

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.generic_visit(node)
        return self._remove_docstring(node)  # type: ignore[return-value]

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        self.generic_visit(node)
        return self._remove_docstring(node)  # type: ignore[return-value]

    def _remove_docstring(self, node: ast.AST) -> ast.AST:
        body = getattr(node, "body", None)
        if not body:
            return node

        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            body.pop(0)

        return node


type Consts = Dict[str, ast.AST]


class ConstCollector(ast.NodeVisitor):
    def __init__(self):
        self.consts: Consts = {}
        self._is_in_class = False

    def visit_Assign(self, node: ast.Assign) -> None:
        target = node.targets[0]
        if (
            isinstance(target, ast.Name)
            and target.id.isupper()
            and not self._is_in_class
        ):
            self.consts[target.id] = node.value

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        old_in_class = self._is_in_class
        self._is_in_class = True
        self.generic_visit(node)
        self._is_in_class = old_in_class


class ConstInliner(ast.NodeTransformer):
    def __init__(self, constants: Consts):
        self.constants = constants

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if isinstance(node.ctx, ast.Load) and node.id in self.constants:
            return self.visit(self.constants[node.id])
        return node


class ConstRemover(ast.NodeTransformer):
    def __init__(self, constants: Consts):
        self.const_names = set(constants.keys())

    def visit_Assign(self, node: ast.Assign) -> Optional[ast.Assign]:
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id in self.const_names:
            return None
        return node


type Enums = Dict[str, Dict[str, ast.AST]]


class EnumCollector(ast.NodeVisitor):
    def __init__(self):
        self.enums: Enums = {}
        self._curr_enum: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        is_in_enum = any(
            base
            for base in node.bases
            if isinstance(base, ast.Name) and base.id in ("Enum", "IntEnum")
        )

        if is_in_enum:
            self._curr_enum = node.name
            self.enums[self._curr_enum] = {}
        else:
            self._curr_enum = None

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        target = node.targets[0]
        if isinstance(target, ast.Name) and self._curr_enum is not None:
            self.enums[self._curr_enum][target.id] = node.value


class EnumInliner(ast.NodeTransformer):
    def __init__(self, enums: Enums):
        self.enums = enums

    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        if isinstance(node.value, ast.Name):
            enum_name = node.value.id
            member_name = node.attr
            if enum_name in self.enums and member_name in self.enums[enum_name]:
                return self.visit(self.enums[enum_name][member_name])
        return node
