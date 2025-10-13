from boolia import RuleBook, DEFAULT_FUNCTIONS

rules = RuleBook()
rules.add("adult", "user.age >= 18")
rules.add("brazilian", "starts_with(user.country, 'Br')")
rules.add("eligible", "adult() and (brazilian() or contains(user.roles, 'vip'))")

DEFAULT_FUNCTIONS.register("adult", lambda **kw: rules.get("adult").evaluate(**kw))
DEFAULT_FUNCTIONS.register("brazilian", lambda **kw: rules.get("brazilian").evaluate(**kw))

ok = rules.evaluate("eligible", context={"user": {"age": 22, "country": "Brazil", "roles": ["member"]}})
print(ok)
