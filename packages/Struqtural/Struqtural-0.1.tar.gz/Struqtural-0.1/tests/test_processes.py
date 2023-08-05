'''
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import nose
import networkx as nx
import struqtural.utilities as util
import struqtural.processes.graph as graph
import struqtural.processes.files as files
import struqtural.processes.typeinference as infer
import struqtural.processes.introspection as introspection

from collections import namedtuple
from datetime import date, time


food_tags = {'Food': [{'id': '3', 'price': '$8.95', 'calories': '900', 'name': 'Berry-Berry Belgian Waffles', 'description': 'light Belgian waffles covered with an assortment of fresh berries and whipped cream'}, {'id': '4', 'price': '$4.50', 'calories': '600', 'name': 'French Toast', 'description': 'thick slices made from our homemade sourdough bread'}, {'id': '1', 'price': '$5.95', 'calories': '650', 'name': 'Belgian Waffles', 'description': 'two of our famous Belgian Waffles with plenty of real maple syrup'}, {'id': '2', 'price': '$7.95', 'calories': '900', 'name': 'Strawberry Belgian Waffles', 'description': 'light Belgian waffles covered with strawberries and whipped cream'}, {'id': '5', 'price': '$6.95', 'calories': '950', 'name': 'Homestyle Breakfast', 'description': 'two eggs, bacon or sausage, toast, and our ever-popular hash browns'}]}
food_relationships = {}
order_tags = {'Line': [{'id': '1', 'price': '10.95', 'part': 'A-10', 'number': '1', 'quantity': '12', 'salesorder_id': '1'}, {'price': '3.99', 'number': '2', 'part': 'B-43', 'salesorder_id': '1', 'id': '2', 'quantity': '600'}], 'SalesOrder': [{'customer': 'Gallagher Industries', 'date': '29.10.00', 'number': '1234', 'id': '1'}]}
order_relationships = {('SalesOrder', 'Line'): {'backref': True, 'primary': ('id',), 'foreign': ['salesorder_id']}}
complex_order_tags = {'Customer': [{'order_id': '1', 'custnum': '007', 'name': 'Bond, Inc.', 'id': '1'}], 'Line': [{'order_id': '1', 'linenum': '1', 'id': '3', 'quantity': '3'}], 'Part': [{'line_id': '3', 'price': '12.95', 'id': '1', 'partnum': 'ABC'}], 'Order': [{'date': '10/29/00', 'number': '123', 'id': '1'}]}
complex_order_relationships = {('Order', 'Line'): {'backref': True, 'primary': ('id',), 'foreign': ['order_id']}, ('Line', 'Part'): {'backref': True, 'primary': ('id',), 'foreign': ['line_id']}, ('Order', 'Customer'): {'backref': True, 'primary': ('id',), 'foreign': ['order_id']}}


#==============================================================================
#                                 Functions
#==============================================================================





#==============================================================================
#                                   Tests
#==============================================================================


def test_parse_csv():
    csv_ = files.parse_csv
    l1 = ["a b c", "1 2 3", "4 5 6", "7 8 9"]
    l2 = ["1 2 3", "4 5 6", "7 8 9"]
    l3 = ["1,2,3", "4,5,6", "7,8,9"]
    h1, t1 = csv_(l1)
    h2, t2 = csv_(l2)
    h3, t3 = csv_(l3)
    e = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    # Verify that the csv document has been correctly parsed into its
    # constituent elements.
    assert h1 == ['a', 'b', 'c']
    assert e == t1
    assert t1 == t2
    assert t2 == t3
    assert h2 == None
    assert h3 == None
    
    
def test_parse_xml():
    formatter = files.SchemaFormatter()
    food = files.parse_xml("data/menu.xml", formatter)
    order = files.parse_xml("data/sales_order.xml", formatter)
    complex_order = files.parse_xml("data/complex_sales_order.xml", formatter)
    assert food[0] == food_tags
    assert food[1] == food_relationships
    assert order[0] == order_tags
    assert order[1] == order_relationships
    assert complex_order[0] == complex_order_tags
    assert complex_order[1] == complex_order_relationships


def test_generate_edge_order():
    g = nx.classes.DiGraph()
    edges = ((1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (7, 3))
    g.add_edges_from(edges)
    order = graph.generate_edge_order(g, sort=True)
    # Verify that the edge order produced is correct.
    assert order == [(None, 1), (1, 2), (1, 3), (3, 4), (3, 5), (3, 6),
                     (None, 7), (7, 3), (3, 4), (3, 5), (3, 6)]


def test_node_table():
    nodes = ((1, {"b": 2.5, "c": True, "d":"w"}),
             (2, {"a": 2, "c": True, "d":"x"}),
             (3, {"a": 1, "b": 3.5, "d":"y"}),
             (4, {"a": 1, "b": 4.5, "c": True}))
    properties = graph.get_node_properties(nodes)
    # Test that the correct values for id have been identified, and all
    # attributes present in the product dictionary are present in the
    # source dictionary.
    for (inode, jnode) in zip(nodes, properties):
        for property_ in jnode:
            if property_ != "id":
                assert inode[1][property_] == jnode[property_]
            else:
                assert inode[0] == jnode[property_]


def test_edge_table():
    edges = ((1, 2, {"b": 2.5, "c": True, "d":"w"}),
             (2, 3, {"a": 2, "c": True, "d":"x"}),
             (3, 4, {"a": 1, "b": 3.5, "d":"y"}),
             (4, 5, {"a": 1, "b": 4.5, "c": True}))
    properties = graph.get_edge_properties(edges)
    # First, test that the correct values are identified when no id is
    # specified.
    for (iedge, jedge) in zip(edges, properties):
        assert "start_id" in jedge
        assert "end_id" in jedge
        for property_ in jedge:
            if property_ == "start_id":
                assert iedge[0] == jedge[property_]
            elif property_ == "end_id":
                assert iedge[1] == jedge[property_]
            else:
                assert iedge[2][property_] == jedge[property_]
    Test = namedtuple("Test", "a b")
    a = Test(1, 2)
    b = Test(3, 4)
    c = Test(5, 6)
    d = Test(7, 8)
    e = Test(8, 9)
    edges2 = ((a, b, {"b": 2.5, "c": True, "d":"w"}),
              (b, c, {"a": 2, "c": True, "d":"x"}),
              (c, d, {"a": 1, "b": 3.5, "d":"y"}),
              (d, e, {"a": 1, "b": 4.5, "c": True}))
    keys = ["a", "b"]
    properties = graph.get_edge_properties(edges2, keys)
    # Next, test that the correct values are identified when a compound id is
    # specified.
    for (iedge, jedge) in zip(edges2, properties):
        for property_ in jedge:
            assert "start_a" in jedge
            assert "end_a" in jedge
            assert "start_b" in jedge
            assert "end_b" in jedge
            if property_ == "start_a":
                assert iedge[0].a == jedge[property_]
            elif property_ == "end_a":
                assert iedge[1].a == jedge[property_]
            elif property_ == "start_b":
                assert iedge[0].b == jedge[property_]
            elif property_ == "end_b":
                assert iedge[1].b == jedge[property_]
            else:
                assert iedge[2][property_] == jedge[property_]


def test_infer_string_types():
    datatype = namedtuple("Data", "A B C D E F")
    data = [datatype("", "1", "1.5", "a", "5/13/79", "10:15 AM"),
            datatype("F", "", "2.5", "b", "5/13/79", "10:15 AM"),
            datatype("TRUE", "3", "", "c", "5/13/79", "10:15 AM"),
            datatype("FALSE", "4", "4.5", "", "5/13/79", "10:15 AM")]
    expected = [datatype(None, 1, 1.5, "a", date(1979, 5, 13), time(10, 15, 00)),
                datatype(False, None, 2.5, "b", date(1979, 5, 13), time(10, 15, 00)),
                datatype(True, 3, None, "c", date(1979, 5, 13), time(10, 15, 00)),
                datatype(False, 4, 4.5, None, date(1979, 5, 13), time(10, 15, 00))]
    types = infer.infer_table_types(data)
    results = infer.strings_to_types(data, types)
    assert results == expected


def test__unique_name():
    res = [[True, 1, 1.5, "a"],
           [False, 2, 2.5, "b"],
           [True, 3, 3.5, "c"],
           [False, 4, 4.5, "d"]]
    name = infer.unique_name(res)
    assert name[0:4] == "data"
    assert int(name[4:])


def test_make_hashable():
    l = [1, 2, 3, 4]
    s = set(l)
    lh = util.make_hashable(l)
    sh = util.make_hashable(s)
    t = (1, 2, 3, 4)
    fs = frozenset(t)
    assert lh == t
    assert sh == fs


def test_as_list():
    t1 = None
    l1 = []
    t2 = "string"
    l2 = ["string"]
    t3 = [1, 2, 3]
    assert util.as_mutable_sequence(t1) == l1
    assert util.as_mutable_sequence(t2) == l2
    assert util.as_mutable_sequence(t3) == t3


def test_as_tuple():
    t1 = None
    l1 = tuple()
    t2 = "string"
    l2 = ("string",)
    t3 = (1, 2, 3)
    assert util.as_sequence(t1) == l1
    assert util.as_sequence(t2) == l2
    assert util.as_sequence(t3) == t3
    

def test_as_set():
    t1 = None
    s1 = set()
    t2 = "string"
    s2 = set(("string",))
    s3 = set((1, 2, 3))
    t4 = ([1, 2], [3, 4], [5, 6])
    s4 = set(((1, 2), (3, 4), (5, 6)))
    assert util.as_mutable_set(t1) == s1
    assert util.as_mutable_set(t2) == s2
    assert util.as_mutable_set(s3) == s3
    assert util.as_mutable_set(t4) == s4
    

def test_as_dict():
    t1 = None
    d1 = dict()
    t2 = "string"
    d2 = {"string":None}
    d3 = {"A":1, "B":2}
    t4 = (("A", 1), ("B", 2), ("C", 3)) 
    d4 = {"A":1, "B":2, "C":3}
    t5 = (([1, 2],"A"), ([3,4],"B"), ([5,6], "C"))
    d5 = {(1,2):"A", (3,4):"B", (5, 6):"C"}
    assert util.as_mutable_mapping(t1) == d1
    assert util.as_mutable_mapping(t2) == d2
    assert util.as_mutable_mapping(d3) == d3
    assert util.as_mutable_mapping(t4) == d4
    assert util.as_mutable_mapping(t5) == d5
    

def test_descendent():
    t1 = "test"
    r1 = basestring
    t2 = str
    assert util.descendant(t1, r1)
    assert util.descendant(t2, r1)


def test_to_date():
    d1 = date(1979, 5, 13)
    d2 = date(2010, 7, 4)
    dates = {"05/13/79":d1, # month day year (american)
             "05/13/1979":d1,
             "5/13/79":d1,
             "5/13/1979":d1,
             "5-13-1979":d1,
             "5.13.1979":d1,
             "1979.05.13":d1, # year month day (iso)
             "13/05/1979":d1, # day month year (european)
             "13.5.79":d1,
             "04-july-2010":d2,
             "04 july 2010":d2,
             "04 july, 2010":d2,
             "july 04, 2010":d2}
    for d in dates:
        assert infer.date_(d) == dates[d]


def test_to_time():
    t1 = time(10, 15, 0)
    t2 = time(20, 30, 0)
    t3 = time(0, 0, 0)
    t4 = time(23, 59, 59)
    times = {"10:15":t1,
             "10:15 AM":t1,
             "10:15:00 AM":t1,
             "20:30:00":t2,
             "8:30:00 pm":t2,
             "8:30:00.0001 pm":t2,
             "00:00:00":t3,
             "23:59:59":t4,
             "23:59:59.9999":t4}
    for t in times:
        assert infer.time_(t) == times[t]

    
def test_all_keys():
    dicts = [{"A":1, "B":2},
             {"B":2, "C":3},
             {"C":3, "D":4}]
    assert not set("ABCD").difference(util.all_keys(dicts))


def test_dicts_to_lists():
    dicts = [{"A":1, "B":2},
             {"B":2, "C":3},
             {"C":3, "D":4}]
    all_keys = util.all_keys(dicts)
    dict_list = util.dicts_to_lists(dicts, all_keys)
    for (index, dict_) in enumerate(dicts):
        assert [dict_.get(k) for k in all_keys] == dict_list[index]


def test_instances_to_dicts():
    mocks = [Mock(1, 2, 3),
             Mock(4, 5, 6),
             Mock(7, 8, 9)]
    # First let's test the basic use case.
    dicts = introspection.instances_to_dicts(mocks, Mock)
    assert dicts[0]["a"] == 1
    assert dicts[0]["b"] == 2
    assert dicts[0]["c"] == 3
    assert dicts[1]["a"] == 4
    assert dicts[1]["b"] == 5
    assert dicts[1]["c"] == 6
    assert dicts[2]["a"] == 7
    assert dicts[2]["b"] == 8
    assert dicts[2]["c"] == 9
    # Now add an attribute to one mock object and verify that it was caught.
    setattr(mocks[0], "d", "X")
    dicts = introspection.instances_to_dicts(mocks, Mock)
    assert dicts[0]["d"] == "X"
    assert dicts[1]["d"] == None
    assert dicts[2]["d"] == None
    # Let's set __attributes__ on Mock and verify that it is working properly.
    Mock.__attributes__ = ["a", "b"]
    dicts = introspection.instances_to_dicts(mocks, Mock)
    assert dicts[0]["a"] == 1
    assert dicts[0]["b"] == 2
    assert "c" not in dicts[0]
    assert "d" not in dicts[0]
    assert dicts[1]["a"] == 4
    assert dicts[1]["b"] == 5
    assert "c" not in dicts[1]
    assert "d" not in dicts[1]
    assert dicts[2]["a"] == 7
    assert dicts[2]["b"] == 8
    assert "c" not in dicts[2]
    assert "d" not in dicts[2]
    # Let's add a non-python object and verify it does what it should.
    mocks[0] = date(1979, 5, 13)
    try:
        passes = False
        dicts = introspection.instances_to_dicts(mocks)
    except ValueError:
        passes = True
    finally:
        assert passes


def test_instances_to_dicts_with_classes():
    foos = [foo(1, "a"), foo(2, "b"), foo(3, "c"), foo(4, "d")]
    bars = [bar(foos[0], 1.0, True, [1, 2, 3], {"A":True, "B":False}),
            bar(foos[1], 2.0, False, [2, 3, 4], {"C":True, "D":False}),
            bar(foos[2], 3.0, True, [3, 4, 5], {"E":True, "F":False}),
            bar(foos[3], 4.0, False, [4, 5, 6], {"G":True, "H":False})]
    bar_dicts = introspection.instances_to_dicts(bars)
    for bar_dict in bar_dicts:
        assert introspection.class_(type(bar_dict["foo"]))


#==============================================================================
#                                  Classes
#==============================================================================


class Mock(object):
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c

class foo(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

class bar(object):
    def __init__(self, foo, c, d, e, f):
        self.foo = foo
        self.c = c
        self.d = d
        self.e = e
        self.f = f
  

if __name__ == "__main__":
    import sys
    args = sys.argv + ["-s", "-d"]
    nose.runmodule(argv=args)
