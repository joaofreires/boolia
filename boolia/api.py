from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Set, Union

from .parser import parse
from .ast import Node
from .resolver import default_resolver_factory, MissingPolicy
from .functions import FunctionRegistry, DEFAULT_FUNCTIONS


def compile_expr(source: str) -> Node:
    return parse(source)


def evaluate(
    source_or_ast: Union[str, Node],
    *,
    context: Optional[Dict[str, Any]] = None,
    tags: Optional[Set[str]] = None,
    resolver=None,
    on_missing: MissingPolicy = "false",
    default_value: Any = None,
    functions: Optional[FunctionRegistry] = None,
) -> bool:
    node = compile_expr(source_or_ast) if isinstance(source_or_ast, str) else source_or_ast
    ctx = context or {}
    tg = tags or set()
    res = resolver or default_resolver_factory(ctx, on_missing=on_missing, default_value=default_value)
    fns = functions or DEFAULT_FUNCTIONS
    out = node.eval(res, tg, fns)
    return bool(out)


@dataclass
class Rule:
    ast: Node

    def evaluate(self, **kwargs) -> bool:
        return evaluate(self.ast, **kwargs)


def compile_rule(source: str) -> Rule:
    return Rule(compile_expr(source))


class RuleBook:
    def __init__(self):
        self._rules: Dict[str, Rule] = {}

    def add(self, name: str, source: str) -> Rule:
        r = compile_rule(source)
        self._rules[name] = r
        return r

    def replace(self, name: str, source: str) -> Rule:
        return self.add(name, source)

    def get(self, name: str) -> Rule:
        if name not in self._rules:
            raise KeyError(f"Unknown rule: {name}")
        return self._rules[name]

    def evaluate(self, name: str, **kwargs) -> bool:
        return self.get(name).evaluate(**kwargs)

    def names(self):
        return list(self._rules.keys())
