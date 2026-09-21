from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import diagnose, format_yaml, query, read_text, to_json

VERSION = "1.0.0"


def _source(path: str) -> str:
    return sys.stdin.read() if path == "-" else read_text(path)


def _write(text: str, output: str | None, force: bool) -> None:
    if not output or output == "-":
        sys.stdout.write(text)
        return
    target = Path(output)
    if target.exists() and not force:
        raise FileExistsError(f"refusing to overwrite {target}; use --force")
    target.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="yaml-doctor", description="Validate, diagnose, format, and inspect YAML safely.")
    p.add_argument("--version", action="version", version=f"yaml-doctor {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = p.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Validate YAML and report diagnostics")
    check.add_argument("files", nargs="+", help="YAML files, or - for stdin")
    check.add_argument("--max-line-length", type=int, default=120)
    check.add_argument("--allow-tabs", action="store_true")
    check.add_argument("--json", action="store_true", dest="as_json")
    check.add_argument("--strict", action="store_true", help="Treat warnings as failure")

    fmt = sub.add_parser("format", help="Normalize YAML formatting")
    fmt.add_argument("file", help="YAML file, or - for stdin")
    fmt.add_argument("-o", "--output")
    fmt.add_argument("--sort-keys", action="store_true")
    fmt.add_argument("--explicit-start", action="store_true")
    fmt.add_argument("--force", action="store_true")

    inspect = sub.add_parser("inspect", help="Show document count and root types")
    inspect.add_argument("file")
    inspect.add_argument("--json", action="store_true", dest="as_json")

    get = sub.add_parser("get", help="Read a value using dotted/list path syntax")
    get.add_argument("file")
    get.add_argument("path", help="Example: services[0].name")
    get.add_argument("--json", action="store_true", dest="as_json")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "check":
            reports, failed = [], False
            for path in args.files:
                _, diags = diagnose(_source(path), max_line_length=args.max_line_length, forbid_tabs=not args.allow_tabs)
                reports.append({"file": path, "diagnostics": [d.to_dict() for d in diags]})
                failed |= any(d.severity == "error" or (args.strict and d.severity == "warning") for d in diags)
            if args.as_json:
                print(json.dumps(reports, ensure_ascii=False, indent=2))
            else:
                for report in reports:
                    if not report["diagnostics"]:
                        print(f"OK {report['file']}")
                    for d in report["diagnostics"]:
                        loc = f":{d['line']}:{d['column']}" if d['line'] else ""
                        print(f"{d['severity'].upper()} {report['file']}{loc} [{d['code']}] {d['message']}")
            return 1 if failed else 0
        if args.command == "format":
            rendered = format_yaml(_source(args.file), sort_keys=args.sort_keys, explicit_start=args.explicit_start)
            _write(rendered, args.output, args.force)
            return 0
        if args.command == "inspect":
            docs, diags = diagnose(_source(args.file))
            if docs is None:
                for d in diags:
                    print(f"ERROR [{d.code}] {d.message}", file=sys.stderr)
                return 1
            info = {"documents": len(docs), "root_types": [type(d).__name__ for d in docs], "diagnostics": [d.to_dict() for d in diags]}
            print(json.dumps(info, ensure_ascii=False, indent=2) if args.as_json else f"documents: {info['documents']}\nroot types: {', '.join(info['root_types'])}")
            return 0
        docs, diags = diagnose(_source(args.file))
        if docs is None:
            raise ValueError(diags[-1].message)
        if len(docs) != 1:
            raise ValueError("get requires exactly one YAML document")
        value = query(docs[0], args.path)
        print(to_json(value) if args.as_json or isinstance(value, (dict, list)) else ("null" if value is None else str(value)))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"yaml-doctor: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
