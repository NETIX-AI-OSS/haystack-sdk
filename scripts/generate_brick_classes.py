"""Regenerate haystack_sdk/brick/data/brick_classes.json from a Brick ontology file (dev-only; needs rdflib).

Usage: python scripts/generate_brick_classes.py path/to/Brick.ttl [--check]

The brickschema package bundles the ontology, e.g. ``.venv/lib/python3.14/site-packages/brickschema/ontologies/1.4/Brick.ttl``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import rdflib
from rdflib.namespace import OWL, RDF, RDFS

BRICK = rdflib.Namespace("https://brickschema.org/schema/Brick#")
OUTPUT = Path(__file__).resolve().parents[1] / "haystack_sdk" / "brick" / "data" / "brick_classes.json"

# Checked in order: a class under both Point and Equipment ancestry is classified by the first hit.
KIND_ROOTS = (
    ("point", BRICK.Point),
    ("equipment", BRICK.Equipment),
    ("location", BRICK.Location),
    ("system", BRICK.System),
    ("collection", BRICK.Collection),
)


def _ancestors(graph: rdflib.Graph, cls: rdflib.URIRef) -> set[rdflib.URIRef]:
    seen: set[rdflib.URIRef] = set()
    stack = [cls]
    while stack:
        current = stack.pop()
        for pred in (RDFS.subClassOf, OWL.equivalentClass):
            for parent in graph.objects(current, pred):
                if isinstance(parent, rdflib.URIRef) and parent not in seen:
                    seen.add(parent)
                    stack.append(parent)
    return seen


def build(ontology: Path) -> dict[str, object]:
    graph = rdflib.Graph()
    graph.parse(ontology, format="turtle")
    ontologies = (o for o in graph.subjects(RDF.type, OWL.Ontology) if str(o).endswith("/Brick"))
    version = str(next((graph.value(o, OWL.versionInfo) for o in ontologies), "") or "")
    classes: dict[str, str] = {}
    deprecated: list[str] = []
    for cls in sorted(set(graph.subjects(RDF.type, OWL.Class))):
        if not isinstance(cls, rdflib.URIRef) or not str(cls).startswith(str(BRICK)):
            continue
        local = str(cls)[len(str(BRICK)) :]
        lineage = _ancestors(graph, cls) | {cls}
        classes[local] = next((kind for kind, root in KIND_ROOTS if root in lineage), "other")
        if graph.value(cls, OWL.deprecated) is not None:
            deprecated.append(local)
    return {"version": version, "classes": classes, "deprecated": deprecated}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ontology", type=Path)
    parser.add_argument("--check", action="store_true", help="fail when the checked-in index differs")
    args = parser.parse_args()
    rendered = json.dumps(build(args.ontology), indent=1, sort_keys=True) + "\n"
    if args.check:
        if OUTPUT.read_text() != rendered:
            print(f"{OUTPUT} is out of date; rerun without --check", file=sys.stderr)
            return 1
        return 0
    OUTPUT.write_text(rendered)
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
