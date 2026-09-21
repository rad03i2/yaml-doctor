from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json
import re

import yaml


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    code: str
    message: str
    line: int | None = None
    column: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DuplicateKeyError(ValueError):
    def __init__(self, key: Any, line: int, column: int):
        super().__init__(f"duplicate key {key!r} at line {line}, column {column}")
        self.key, self.line, self.column = key, line, column


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            exists = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError("while constructing a mapping", node.start_mark, "found an unhashable key", key_node.start_mark) from exc
        if exists:
            raise DuplicateKeyError(key, key_node.start_mark.line + 1, key_node.start_mark.column + 1)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_documents(text: str) -> list[Any]:
    return list(yaml.load_all(text, Loader=UniqueKeyLoader))


def diagnose(text: str, *, max_line_length: int = 120, forbid_tabs: bool = True) -> tuple[list[Any] | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    if text.startswith("\ufeff"):
        diagnostics.append(Diagnostic("warning", "bom", "UTF-8 BOM detected; consider removing it.", 1, 1))
    for number, line in enumerate(text.splitlines(), 1):
        if forbid_tabs and "\t" in line:
            diagnostics.append(Diagnostic("error", "tab", "Tab character detected; YAML indentation should use spaces.", number, line.index("\t") + 1))
        if line.rstrip() != line:
            diagnostics.append(Diagnostic("warning", "trailing-space", "Trailing whitespace detected.", number, len(line.rstrip()) + 1))
        if max_line_length > 0 and len(line) > max_line_length:
            diagnostics.append(Diagnostic("warning", "line-length", f"Line exceeds {max_line_length} characters.", number, max_line_length + 1))
    try:
        docs = load_documents(text)
    except DuplicateKeyError as exc:
        diagnostics.append(Diagnostic("error", "duplicate-key", str(exc), exc.line, exc.column))
        return None, diagnostics
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        diagnostics.append(Diagnostic("error", "syntax", getattr(exc, "problem", None) or str(exc), (mark.line + 1) if mark else None, (mark.column + 1) if mark else None))
        return None, diagnostics
    if not text.strip():
        diagnostics.append(Diagnostic("warning", "empty", "Document is empty."))
    return docs, diagnostics


def format_yaml(text: str, *, sort_keys: bool = False, explicit_start: bool = False) -> str:
    docs = load_documents(text)
    rendered = yaml.safe_dump_all(docs, sort_keys=sort_keys, allow_unicode=True, default_flow_style=False, explicit_start=explicit_start)
    return rendered

_PATH_TOKEN = re.compile(r"([^.[\]]+)|\[(\d+)\]")


def parse_path(path: str) -> list[str | int]:
    if not path:
        raise ValueError("path cannot be empty")
    tokens: list[str | int] = []
    position = 0
    for match in _PATH_TOKEN.finditer(path):
        if match.start() != position and not (path[position:match.start()] == "."):
            raise ValueError(f"invalid path near {path[position:]!r}")
        tokens.append(int(match.group(2)) if match.group(2) is not None else match.group(1))
        position = match.end()
    if position != len(path) or not tokens:
        raise ValueError(f"invalid path {path!r}")
    return tokens


def query(data: Any, path: str) -> Any:
    current = data
    for token in parse_path(path):
        if isinstance(token, int):
            if not isinstance(current, list) or token >= len(current):
                raise KeyError(f"index {token} not found")
            current = current[token]
        else:
            if not isinstance(current, dict) or token not in current:
                raise KeyError(f"key {token!r} not found")
            current = current[token]
    return current


def to_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str)


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")
