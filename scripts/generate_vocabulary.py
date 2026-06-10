#!/usr/bin/env python
"""Regenerate vocabulary .py files from their JSON sources.

Reads each ``haystack_sdk/vocabulary/data/*.json`` and emits a sibling
``.py`` file containing frozen dataclass constants and a ``Vocabulary``
binding. Run as part of pre-commit; CI fails if the generated files
diverge from the JSON sources.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "haystack_sdk" / "vocabulary" / "data"
OUT_DIR = REPO_ROOT / "haystack_sdk" / "vocabulary"

# Maps the JSON filename stem -> (module filename stem, constant name, vocab name).
PACKS: list[tuple[str, str, str, str]] = [
    ("core_tags", "core", "CORE", "core"),
    ("fdd_tags", "fdd", "FDD", "fdd"),
    ("netix_custom_tags", "netix_custom", "NETIX_CUSTOM", "netix_custom"),
    ("retail_mall_tags", "retail_mall", "RETAIL_MALL", "retail_mall"),
    ("smart_residential_tags", "residential", "RESIDENTIAL", "residential"),
    ("healthcare_tags", "healthcare", "HEALTHCARE", "healthcare"),
    ("water_treatment_tags", "water_treatment", "WATER_TREATMENT", "water_treatment"),
    ("district_cooling_tags", "district_cooling", "DISTRICT_COOLING", "district_cooling"),
]

VOCAB_VERSION = "1.0.0"

HEADER = '''"""AUTO-GENERATED from haystack_sdk/vocabulary/data/{json_name}.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary


'''


@dataclass
class TagRow:
    name: str
    display_name: str
    kind: int
    namespace: str
    doc: str
    supertype: str | None
    unit_quantity: str | None


def load_rows(path: Path) -> list[TagRow]:
    payload = json.loads(path.read_text())
    rows: list[TagRow] = []
    for entry in payload:
        rows.append(
            TagRow(
                name=entry["name"],
                display_name=entry.get("display_name", entry["name"]),
                kind=int(entry.get("kind", 0)),
                namespace=entry.get("namespace", "phIoT"),
                doc=entry.get("doc", ""),
                supertype=entry.get("supertype"),
                unit_quantity=entry.get("unit_quantity"),
            )
        )
    return rows


def constant_name(tag_name: str) -> str:
    """Convert a tag name to a Python constant name.

    ``equipType`` → ``EQUIP_TYPE``; ``co2`` → ``CO2``; ``ahu`` → ``AHU``.
    """
    out: list[str] = []
    prev_lower = False
    for ch in tag_name:
        if ch == "-":
            out.append("_")
            prev_lower = False
            continue
        if ch.isupper() and prev_lower:
            out.append("_")
        out.append(ch.upper())
        prev_lower = ch.islower()
    name = "".join(out)
    if name and name[0].isdigit():
        name = "_" + name
    return name


def render_tagdef(row: TagRow) -> str:
    parts = [
        f"name={row.name!r}",
        f"display_name={row.display_name!r}",
        f"kind={row.kind}",
        f"namespace={row.namespace!r}",
        f"doc={row.doc!r}",
    ]
    if row.supertype:
        parts.append(f"supertype={row.supertype!r}")
    if row.unit_quantity:
        parts.append(f"unit_quantity={row.unit_quantity!r}")
    return "TagDef(" + ", ".join(parts) + ")"


def render_module(json_stem: str, vocab_name: str, rows: list[TagRow]) -> str:
    """Render a vocabulary module.

    Each pack module exports a single :class:`Vocabulary` named ``PACK`` plus
    one :class:`TagDef` constant per row. The ``PACK`` indirection avoids any
    collision with tag-named constants (e.g. a tag named ``retailMall`` would
    otherwise shadow the pack constant named ``RETAIL_MALL``). ``__init__.py``
    re-exports ``PACK`` under the public pack constant name.

    ``vocab_name`` is embedded in the generated Vocabulary so the object carries
    its semantic name at runtime.
    """
    lines: list[str] = [HEADER.format(json_name=json_stem)]

    used_names: set[str] = {"PACK"}  # reserve the pack-level export
    consts: list[str] = []
    for row in rows:
        base = constant_name(row.name)
        const = base
        suffix = 2
        while const in used_names:
            const = f"{base}_{suffix}"
            suffix += 1
        used_names.add(const)
        consts.append(const)
        lines.append(f"{const} = {render_tagdef(row)}")

    lines.append("")
    lines.append("PACK = Vocabulary(")
    lines.append(f"    name={vocab_name!r},")
    lines.append(f"    version={VOCAB_VERSION!r},")
    lines.append("    tags=(")
    for c in consts:
        lines.append(f"        {c},")
    lines.append("    ),")
    lines.append(")")
    lines.append("")
    return "\n".join(lines)


def _ruff_format(text: str) -> str:
    """Pipe text through ruff so generator output matches the lint config.

    Runs both ``ruff check --fix`` (for isort + autofixes) and ``ruff format``
    (for whitespace/formatting) so the result matches what CI expects.
    """
    try:
        fixed = subprocess.run(
            ["ruff", "check", "--fix", "--exit-zero", "--stdin-filename", "generated.py", "-"],
            input=text,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        formatted = subprocess.run(
            ["ruff", "format", "--stdin-filename", "generated.py", "-"],
            input=fixed,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        return formatted
    except OSError:
        # ruff not on PATH or subprocess error — return as-is.
        return text
    except subprocess.CalledProcessError:
        # ruff exited non-zero — return as-is.
        return text


def main(check_only: bool = False) -> int:
    failures: list[str] = []
    for json_stem, py_stem, _constant_var, vocab_name in PACKS:
        json_path = DATA_DIR / f"{json_stem}.json"
        py_path = OUT_DIR / f"{py_stem}.py"
        rows = load_rows(json_path)
        rendered = _ruff_format(render_module(json_stem, vocab_name, rows))
        if check_only:
            if not py_path.exists() or py_path.read_text() != rendered:
                failures.append(str(py_path))
        else:
            py_path.write_text(rendered)
            print(f"wrote {py_path.relative_to(REPO_ROOT)}", file=sys.stderr)

    if check_only and failures:
        print(
            "Vocabulary modules out of sync. Regenerate with `python scripts/generate_vocabulary.py`:",
            file=sys.stderr,
        )
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    check = "--check" in sys.argv
    raise SystemExit(main(check_only=check))
