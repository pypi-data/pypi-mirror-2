'''
Created on Apr 25, 2010

@author: nathan
'''


import nose
import struqtural.instances as instance


def test_Instance():
    value_names = ["a", "b", "c"]
    value_list = [1, 2, 3]
    value_dict = {"a":1, "b":2, "c":3}
    Instance = instance.create(attributes=value_names)
    i1 = Instance(*value_list)
    i2 = Instance(**value_dict)
    a1 = (getattr(i1, a) for a in i1.__attributes__)
    a2 = (getattr(i2, a) for a in i2.__attributes__)
    v = zip(a1, a2)
    for (v1, v2) in v:
        assert v1 == v2


if __name__ == "__main__":
    import sys
    args = sys.argv + ["-s", "-d"]
    nose.runmodule(argv=args)
