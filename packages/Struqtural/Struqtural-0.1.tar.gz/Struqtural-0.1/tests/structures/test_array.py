'''
Created on Apr 19, 2010

@author: nathan
'''


import nose
import struqtural.structures.structure as structure
import struqtural.loaders.loader as loader


def get_array():
    data = [["T", "1", "1.5", "a"],
            ["F", "2", "2.5", "b"],
            ["TRUE", "3", "3.5", "c"],
            ["FALSE", "4", "4.5", "d"]]
    headers = ["A", "B", "C", "D"]
    return structure.Structure(loader.CollectionLoader, (headers, data), "B",
                               "Instance")


def test_values():
    t = get_array()
    values1 = list(t.values("A", getattr(t.Instance, "B")))
    values2 = list(t.values("D", "C"))
    assert values1 == [(True, 1), (False, 2), (True, 3), (False, 4)]
    assert values2 == [('a', 1.5), ('b', 2.5), ('c', 3.5), ('d', 4.5)]


def test_delete():
    t = get_array()
    instances = list(t)
    t.delete(instances[0:2])
    assert len(t) == 2
    assert t[0] == instances[2]
    assert t[1] == instances[3]
    t.delete([instances[2]])
    assert len(t) == 1
    assert t[0] == instances[3]


def test_Array():
    res = [[True, 1, 1.5, "a"],
           [False, 2, 2.5, "b"],
           [True, 3, 3.5, "c"],
           [False, 4, 4.5, "d"]]
    t = get_array()
    assert t.name == "instances"
    assert t.primary_keys == ["B"]
    assert t.Instance.__attributes__ == ["A", "B", "C", "D"]
    assert len(t) == 4
    assert len(t.columns) == 4
#    for (name, measure) in measures:
#        assert measure.name == name
    instances = [t.Instance(*r) for r in res]
    assert instances[:2] == t[:2]
    assert t[:] == instances
    assert t[0:4] == instances
    assert t[0:3:2] == [instances[0], instances[2]]
    assert t[4::-1] == list(reversed(instances))


#def test_as_array():
#    res = [(True, 1, 1.5, "a"),
#           (False, 2, 2.5, "b"),
#           (True, 3, 3.5, "c"),
#           (False, 4, 4.5, "d")]
#    t = get_array()
#    dtype = [('A', 'b'), ('B', 'i4'), ('C', 'f8'), ('D', 'S1')]
#    array_ = np.array(res, dtype=dtype)
#    assert all(array_ == t.as_numpy_array())


if __name__ == "__main__":
    import sys
    args = sys.argv + ["-s", "-d"]
    nose.runmodule(argv=args)
