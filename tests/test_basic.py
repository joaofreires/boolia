from boolia import evaluate


def test_and_or():
    assert evaluate("true and false or true") is True


def test_dotted_and_tags():
    ctx = {"house": {"light": {"on": False}}}
    assert evaluate("(car and elephant) or house.light.on", context=ctx, tags={"car"}) is False
    ctx["house"]["light"]["on"] = True
    assert evaluate("(car and elephant) or house.light.on", context=ctx, tags={"car"}) is True


def test_comparisons_in():
    ctx = {"user": {"age": 21, "roles": ["admin", "ops"]}}
    assert evaluate("user.age >= 18 and 'admin' in user.roles", context=ctx)


def test_object_attribute_resolution():
    class Obj:
        flag = True

    ctx = {"obj": Obj()}
    assert evaluate("obj.flag", context=ctx) is True


def test_object_method_resolution():
    class ObjA:
        flag = True

        def get_flag(self):
            return self.flag

    class ObjB:
        def get_obj_a(self):
            return ObjA()

    ctx = {"obj": ObjB()}
    assert evaluate("obj.get_obj_a.get_flag", context=ctx) is True
