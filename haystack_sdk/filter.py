"""Haystack 4 filter expression parser and evaluator.

Grammar::

    filter      := orExpr
    orExpr      := andExpr ("or" andExpr)*
    andExpr     := term ("and" term)*
    term        := "not" term | "(" orExpr ")" | cmp
    cmp         := path (("==" | "!=" | "<" | ">" | "<=" | ">=") val)?
    path        := name ("->" name)*
    name        := ALPHA (ALPHA | DIGIT | "_")*
    val         := ref | str | number | "true" | "false"
    ref         := "@" REFCHAR+
    str         := '"' ... '"'
    number      := ["-"] DIGIT+ ["." DIGIT+]

Path traversal across entities (``equipRef->siteRef``) requires a graph
resolver; the default evaluator treats multi-element paths as no-match.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# AST node types
# ---------------------------------------------------------------------------


@dataclass
class FilterNode:
    """Base class for filter AST nodes."""


@dataclass
class MarkerNode(FilterNode):
    """A bare marker name — present if the key exists in the entity."""

    name: str


@dataclass
class CmpNode(FilterNode):
    """A comparison: path op value."""

    path: list[str]
    op: str  # "==", "!=", "<", ">", "<=", ">="
    value: Any


@dataclass
class AndNode(FilterNode):
    children: list[FilterNode]


@dataclass
class OrNode(FilterNode):
    children: list[FilterNode]


@dataclass
class NotNode(FilterNode):
    child: FilterNode


@dataclass
class FilterAST:
    """Parsed filter result + convenience properties.

    ``markers`` and ``refs`` extract top-level flat predicates (useful for
    simple legacy callers); the full expression is in ``node``.
    """

    node: FilterNode | None = None
    markers: list[str] = field(default_factory=list)
    refs: dict[str, str] = field(default_factory=dict)

    @property
    def is_empty(self) -> bool:
        return self.node is None

    def evaluate(
        self,
        entity: dict[str, Any],
        *,
        resolver: Callable[[str], dict[str, Any] | None] | None = None,
    ) -> bool:
        if self.node is None:
            return True
        return evaluate_filter(entity, self.node, resolver=resolver)


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(
    r"""
    (?P<LPAREN>\()
    |(?P<RPAREN>\))
    |(?P<ARROW>->)
    |(?P<OP>==|!=|<=|>=|<|>)
    |(?P<REF>@[\w.\-]+)
    |(?P<STRING>"(?:[^"\\]|\\.)*")
    |(?P<NUMBER>-?\d+(?:\.\d+)?)
    |(?P<NAME>[a-zA-Z_]\w*)
    """,
    re.VERBOSE,
)


def _tokenize(text: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    for m in _TOKEN_RE.finditer(text):
        for kind in ("LPAREN", "RPAREN", "ARROW", "OP", "REF", "STRING", "NUMBER", "NAME"):
            val = m.group(kind)
            if val is not None:
                tokens.append((kind, val))
                break
    return tokens


# ---------------------------------------------------------------------------
# Recursive descent parser
# ---------------------------------------------------------------------------


class _Parser:
    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> tuple[str, str] | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self) -> tuple[str, str]:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _expect(self, kind: str) -> tuple[str, str]:
        tok = self._peek()
        if tok is None or tok[0] != kind:
            raise ValueError(f"Expected {kind}, got {tok}")
        return self._advance()

    def _at_keyword(self, kw: str) -> bool:
        tok = self._peek()
        return tok is not None and tok[0] == "NAME" and tok[1] == kw

    def parse(self) -> FilterNode | None:
        if not self.tokens:
            return None
        return self._or_expr()

    def _or_expr(self) -> FilterNode:
        children = [self._and_expr()]
        while self._at_keyword("or"):
            self._advance()
            children.append(self._and_expr())
        return children[0] if len(children) == 1 else OrNode(children=children)

    def _and_expr(self) -> FilterNode:
        children = [self._term()]
        while self._at_keyword("and"):
            self._advance()
            children.append(self._term())
        return children[0] if len(children) == 1 else AndNode(children=children)

    def _term(self) -> FilterNode:
        tok = self._peek()
        if tok is None:
            raise ValueError("Unexpected end of filter expression")
        if self._at_keyword("not"):
            self._advance()
            return NotNode(child=self._term())
        if tok[0] == "LPAREN":
            self._advance()
            node = self._or_expr()
            self._expect("RPAREN")
            return node
        return self._cmp()

    def _cmp(self) -> FilterNode:
        path = self._path()
        tok = self._peek()
        if tok is not None and tok[0] == "OP":
            op = self._advance()[1]
            value = self._val()
            return CmpNode(path=path, op=op, value=value)
        return MarkerNode(name=path[0] if len(path) == 1 else path[-1])

    def _path(self) -> list[str]:
        parts = [self._expect("NAME")[1]]
        while self._peek() and self._peek()[0] == "ARROW":  # type: ignore[index]
            self._advance()
            parts.append(self._expect("NAME")[1])
        return parts

    def _val(self) -> Any:
        tok = self._peek()
        if tok is None:
            raise ValueError("Expected value")
        if tok[0] == "REF":
            return self._advance()[1]
        if tok[0] == "STRING":
            return self._advance()[1][1:-1]
        if tok[0] == "NUMBER":
            raw = self._advance()[1]
            return float(raw) if "." in raw else int(raw)
        if tok[0] == "NAME" and tok[1] in ("true", "false"):
            self._advance()
            return tok[1] == "true"
        raise ValueError(f"Unexpected token for value: {tok}")


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------


_EQUALITY_OPS = {"==", "!="}
_NUMERIC_OPS: dict[str, Callable[[Any, Any], bool]] = {
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
}


def evaluate_filter(
    entity: dict[str, Any],
    node: FilterNode,
    *,
    resolver: Callable[[str], dict[str, Any] | None] | None = None,
) -> bool:
    """Evaluate a parsed filter AST against an entity dict.

    ``resolver`` is an optional callback that resolves a ref string
    (e.g. ``"@equip1"``) to another entity dict, enabling path traversals
    like ``equipRef->siteRef``.
    """
    if isinstance(node, MarkerNode):
        return entity.get(node.name) is not None
    if isinstance(node, CmpNode):
        val = _resolve_path(entity, node.path, resolver)
        return _compare(val, node.op, node.value)
    if isinstance(node, AndNode):
        return all(evaluate_filter(entity, c, resolver=resolver) for c in node.children)
    if isinstance(node, OrNode):
        return any(evaluate_filter(entity, c, resolver=resolver) for c in node.children)
    if isinstance(node, NotNode):
        return not evaluate_filter(entity, node.child, resolver=resolver)
    return False


def _resolve_path(
    entity: dict[str, Any],
    path: list[str],
    resolver: Callable[[str], dict[str, Any] | None] | None,
) -> Any:
    if not path:
        return None
    if len(path) == 1:
        return entity.get(path[0])
    if resolver is None:
        return None
    current = entity
    for step in path[:-1]:
        ref = current.get(step)
        if not isinstance(ref, str):
            return None
        nxt = resolver(ref)
        if nxt is None:
            return None
        current = nxt
    return current.get(path[-1])


def _compare(entity_val: Any, op: str, filter_val: Any) -> bool:
    if entity_val is None:
        return False
    ev = _normalize_val(entity_val)
    if op in _EQUALITY_OPS:
        result = ev == filter_val
        return result if op == "==" else not result
    fn = _NUMERIC_OPS.get(op)
    return _numeric_cmp(ev, filter_val, fn) if fn else False


def _normalize_val(val: Any) -> Any:
    if not isinstance(val, str):
        return val
    if val.startswith("s:"):
        return val[2:]
    if val.startswith("n:"):
        try:
            num_str = val[2:].split(" ")[0]
            return float(num_str) if "." in num_str else int(num_str)
        except ValueError:
            return val
    if val.startswith("r:"):
        return val[2:].split(" ")[0]
    return val


def _numeric_cmp(a: Any, b: Any, op: Callable[[Any, Any], bool]) -> bool:
    try:
        return op(float(a), float(b))
    except TypeError, ValueError:
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_filter(filter_str: str) -> FilterAST:
    """Parse a Haystack filter string into a :class:`FilterAST`."""
    result = FilterAST()
    if not filter_str or not filter_str.strip():
        return result
    tokens = _tokenize(filter_str)
    if not tokens:
        return result
    result.node = _Parser(tokens).parse()
    _extract_compat(result.node, result.markers, result.refs)
    return result


def _extract_compat(node: FilterNode | None, markers: list[str], refs: dict[str, str]) -> None:
    if node is None:
        return
    if isinstance(node, MarkerNode):
        markers.append(node.name)
    elif isinstance(node, CmpNode):
        if node.op == "==" and len(node.path) == 1 and isinstance(node.value, str) and node.value.startswith("@"):
            refs[node.path[0]] = node.value
    elif isinstance(node, AndNode):
        for child in node.children:
            _extract_compat(child, markers, refs)
