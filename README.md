# boolia

A tiny, safe **boolean expression** engine: like Jinja for logic.

- **Grammar**: `and`, `or`, `not`, parentheses, comparisons (`== != > >= <= <`), `in`
- **Values**: numbers, strings, booleans, `null/None`, identifiers, dotted paths (`user.age`, `house.light.on`)
- **Tags**: bare identifiers evaluate `True` if present in a `tags: set[str]`
- **Functions**: user-registered, safe callables (`starts_with`, `matches`, ...)
- **RuleBook**: name your rules and evaluate them later
- **Missing policy**: choose to **raise** or substitute **None/False/custom default**

```py
from boolia import evaluate, RuleBook, DEFAULT_FUNCTIONS

expr = "(car and elephant) or house.light.on"
print(evaluate(expr, context={"house": {"light": {"on": True}}}, tags={"car"}))  # True
```

## Install (local)

```bash
pip install -e .[dev]
pytest -q
```

## Quick start

```py
from boolia import evaluate, DEFAULT_FUNCTIONS

ctx  = {"user": {"age": 21, "roles": ["admin", "ops"]}}
tags = {"beta"}
expr = "user.age >= 18 and 'admin' in user.roles"
print(evaluate(expr, context=ctx, tags=tags))  # True
```

### Functions

```py
from boolia import evaluate, DEFAULT_FUNCTIONS

DEFAULT_FUNCTIONS.register("starts_with", lambda s, p: str(s).startswith(str(p)))

expr = "starts_with(user.name, 'Jo')"
print(evaluate(expr, context={"user": {"name": "João"}}))  # True
```

### RuleBook

```py
from boolia import RuleBook, DEFAULT_FUNCTIONS

rules = RuleBook()
rules.add("adult", "user.age >= 18")
rules.add("brazilian", "starts_with(user.country, 'Br')")
rules.add("eligible", "adult() and (brazilian() or contains(user.roles, 'vip'))")

# Expose rule names as functions
DEFAULT_FUNCTIONS.register("adult",     lambda **kw: rules.get("adult").evaluate(**kw))
DEFAULT_FUNCTIONS.register("brazilian", lambda **kw: rules.get("brazilian").evaluate(**kw))

ok = rules.evaluate("eligible", context={"user": {"age": 22, "country": "Brazil", "roles": ["member"]}})
print(ok)  # True
```

### Missing policy

```py
from boolia import evaluate, MissingVariableError

try:
    evaluate("user.age >= 18 and house.light.on", context={"user": {"age": 20}}, on_missing="raise")
except MissingVariableError as e:
    print(e)  # Missing variable/path: house.light.on

print(evaluate("score >= 10", context={}, on_missing="default", default_value=0))  # False
print(evaluate("flag and beta", context={}, tags={"beta"}, on_missing="none"))     # False (flag is None)
```

### Notes

- Use `on_missing="none"` if you want **tags to override** missing bare identifiers.
- For stricter semantics on dotted paths, keep `on_missing="raise"` and allow tags only for bare names.
