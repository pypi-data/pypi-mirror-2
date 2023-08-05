'''
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import nose
import networkx as nx
import struqtural.loaders.loader as loader
import struqtural.structures.graph as graph


#==============================================================================
#                                 Functions
#==============================================================================


def get_directed_acyclic_graph():
    n = [("A", {"A":1, "B":2, "C":3}),
         ("B", {"A":2, "B":3, "C":4}),
         ("C", {"A":3, "B":4, "C":5}),
         ("D", {"A":4, "B":5, "C":6}),
         ("E", {"A":5, "B":6, "C":7}),
         ("F", {"A":6, "B":7, "C":8}),
         ("G", {"A":7, "B":8, "C":9})]
    edges = ((n[2][0], n[3][0]),
             (n[2][0], n[4][0]),
             (n[0][0], n[2][0]),
             (n[2][0], n[5][0]),
             (n[0][0], n[1][0]),
             (n[6][0], n[2][0]))
    g = nx.DiGraph()
    for node in n:
        g.add_node(*node)
    g.add_edges_from(edges)
    return graph.DirectedAcyclicGraph(g)


def get_tree():
    n = [("A", {"A":1, "B":2, "C":3}),
         ("B", {"A":2, "B":3, "C":4}),
         ("C", {"A":3, "B":4, "C":5}),
         ("D", {"A":4, "B":5, "C":6}),
         ("E", {"A":5, "B":6, "C":7}),
         ("F", {"A":6, "B":7, "C":8})]
    edges = ((n[2][0], n[3][0]),
             (n[2][0], n[4][0]),
             (n[0][0], n[2][0]),
             (n[2][0], n[5][0]),
             (n[0][0], n[1][0]))
    g = nx.DiGraph()
    for node in n:
        g.add_node(*node)
    g.add_edges_from(edges)
    return graph.Tree(g)


#==============================================================================
#                                   Tests
#==============================================================================


def test_GraphLoader_int_node():
    g = nx.classes.Graph(name="test")
    e0d = {"i":1, "j":2, "k":3}
    e1d = {"i":2, "j":3, "k":4}
    e2d = {"i":3, "j":4, "k":5}
    g.add_edge(0, 1, e0d)
    g.add_edge(1, 2, e1d)
    g.add_edge(2, 3, e2d)
    n0d = {"a":1, "b":2, "c":3}
    n1d = {"a":2, "b":3, "c":4}
    n2d = {"a":3, "b":4, "c":5}
    n3d = {"a":4, "b":5, "c":6}
    g.node[0] = n0d
    g.node[1] = n1d
    g.node[2] = n2d
    g.node[3] = n3d
    graph_ = graph.Graph(g)
    nodes = list(graph_.query(graph_.Node))
    edges = list(graph_.query(graph_.Edge))
    # First, we need to verify that all nodes are present and have been
    # persisted with all their attributes in tact.
    assert len(nodes) == 4
    assert nodes[0].id == 0
    assert nodes[1].id == 1
    assert nodes[2].id == 2
    assert nodes[3].id == 3
    assert nodes[0].a == 1
    assert nodes[1].a == 2
    assert nodes[2].a == 3
    assert nodes[3].a == 4
    assert nodes[0].b == 2
    assert nodes[1].b == 3
    assert nodes[2].b == 4
    assert nodes[3].b == 5
    assert nodes[0].c == 3
    assert nodes[1].c == 4
    assert nodes[2].c == 5
    assert nodes[3].c == 6
    # Next, we need to verify that all edges are present and have been
    # persisted with all their attributes in tact.
    assert len(edges) == 3
    assert edges[0].start_id == 0
    assert edges[0].end_id == 1
    assert edges[1].start_id == 1
    assert edges[1].end_id == 2
    assert edges[2].start_id == 2
    assert edges[2].end_id == 3
    assert edges[0].start.a == 1
    assert edges[0].start.b == 2
    assert edges[0].start.c == 3
    assert edges[0].end.a == 2
    assert edges[0].end.b == 3
    assert edges[0].end.c == 4


def test_GraphLoader_instance_node():
    data = [{"A":True, "B":1, "C":1.5, "D":"a"},
            {"A":False, "B":2, "C":2.5, "D":"b"},
            {"A":True, "B":3, "C":3.5, "D":"c"},
            {"A":False, "B":4, "C":4.5, "D":"d"}]
    loader1 = loader.CollectionLoader(data, "B", "Instance")
    instances = list(loader1.connector.session.query(loader1.Instance))
    g = nx.classes.DiGraph(name="test")
    g.add_edge(instances[0], instances[1])
    g.add_edge(instances[1], instances[2])
    g.add_edge(instances[2], instances[3])
    graph_ = graph.Graph(g)
    nodes = list(graph_.query(graph_.Node))
    edges = list(graph_.query(graph_.Edge))
    # First, let's verify that all the instances have been pulled in with
    # their attributes in tact.
    assert len(nodes) == 4
    assert nodes[0] == instances[0]
    assert nodes[1] == instances[1]
    assert nodes[2] == instances[2]
    assert nodes[3] == instances[3]
    # Next, let's test that the edge references are correct, and point to the
    # correct nodes.
    assert edges[0].start_B == 1
    assert edges[0].end_B == 2
    assert edges[0].start == nodes[0]
    assert edges[0].end == nodes[1]
    assert edges[1].start_B == 2
    assert edges[1].end_B == 3
    assert edges[1].start == nodes[1]
    assert edges[1].end == nodes[2]
    assert edges[2].start_B == 3
    assert edges[2].end_B == 4
    assert edges[2].start == nodes[2]
    assert edges[2].end == nodes[3]


def test_GraphLoader_composite_pk_instance_node():
    data = [{"A":True, "B":True, "C":1.5, "D":"a"},
            {"A":False, "B":True, "C":2.5, "D":"b"},
            {"A":True, "B":False, "C":3.5, "D":"c"},
            {"A":False, "B":False, "C":4.5, "D":"d"}]
    loader1 = loader.CollectionLoader(data, ["A", "B"], "Instance")
    instances = list(loader1.connector.session.query(loader1.Instance))
    g = nx.classes.DiGraph(name="test")
    g.add_edge(instances[0], instances[1])
    g.add_edge(instances[1], instances[2])
    g.add_edge(instances[2], instances[3])
    graph_ = graph.Graph(g)
    nodes = list(graph_.query(graph_.Node))
    edges = list(graph_.query(graph_.Edge))
    # First, let's verify that all the instances have been pulled in with
    # their attributes in tact.
    assert nodes[0] == instances[0]
    assert nodes[1] == instances[1]
    assert nodes[2] == instances[2]
    assert nodes[3] == instances[3]
    # Next, let's test that the edge references are correct, and point to the
    # correct nodes.  Note the compound node references used here.
    assert edges[0].start_A == True
    assert edges[0].end_A == False
    assert edges[0].start_B == True
    assert edges[0].end_B == True
    assert edges[0].start == nodes[0]
    assert edges[0].end == nodes[1]
    assert edges[1].start_A == False
    assert edges[1].end_A == True
    assert edges[1].start_B == True
    assert edges[1].end_B == False
    assert edges[1].start == nodes[1]
    assert edges[1].end == nodes[2]
    assert edges[2].start_A == True
    assert edges[2].end_A == False
    assert edges[2].start_B == False
    assert edges[2].end_B == False
    assert edges[2].start == nodes[2]
    assert edges[2].end == nodes[3]


def test_DirectedAcyclicGraph():
    order = get_directed_acyclic_graph()
    instances = list(order)
    assert len(order) == 7
    assert len(instances) == 7


def test_DirectedAcyclicGraph_parents():
    order = get_directed_acyclic_graph()
    instances = dict((i.id, i) for i in order)
    parents_a = set(i.id for i in order.parents(instances["A"]))
    parents_b = set(i.id for i in order.parents(instances["B"]))
    parents_c = set(i.id for i in order.parents(instances["C"]))
    parents_d = set(i.id for i in order.parents(instances["D"]))
    parents_e = set(i.id for i in order.parents(instances["E"]))
    parents_f = set(i.id for i in order.parents(instances["F"]))
    parents_g = set(i.id for i in order.parents(instances["G"]))
    assert not parents_a
    assert parents_b == set("A")
    assert parents_c == set("AG")
    assert parents_d == set("ACG")
    assert parents_e == set("ACG")
    assert parents_f == set("ACG")
    assert not parents_g


def test_DirectedAcyclicGraph_children():
    dag = get_directed_acyclic_graph()
    instances = dict((i.id, i) for i in dag.query())
    children_a = set(i.id for i in dag.children(instances["A"]))
    children_b = set(i.id for i in dag.children(instances["B"]))
    children_c = set(i.id for i in dag.children(instances["C"]))
    children_d = set(i.id for i in dag.children(instances["D"]))
    children_e = set(i.id for i in dag.children(instances["E"]))
    children_f = set(i.id for i in dag.children(instances["F"]))
    children_g = set(i.id for i in dag.children(instances["G"]))
    assert len(children_a) == 5
    assert children_a == set("BCDEF")
    assert not children_b
    assert len(children_c) == 3
    assert children_c == set("DEF")
    assert not children_d
    assert not children_e
    assert not children_f
    assert len(children_g) == 4
    assert children_g == set("CDEF")


def test_DirectedAcyclicGraph_siblings():
    dag = get_directed_acyclic_graph()
    instances = dict((i.id, i) for i in dag.query())
    siblings_a = set(i.id for i in dag.siblings(instances["A"]))
    siblings_b = set(i.id for i in dag.siblings(instances["B"]))
    siblings_c = set(i.id for i in dag.siblings(instances["C"]))
    siblings_d = set(i.id for i in dag.siblings(instances["D"]))
    siblings_e = set(i.id for i in dag.siblings(instances["E"]))
    siblings_f = set(i.id for i in dag.siblings(instances["F"]))
    siblings_g = set(i.id for i in dag.siblings(instances["G"]))
    assert siblings_a == set()
    assert siblings_b == set("C")
    assert siblings_c == set("B")
    assert siblings_d == set("EF")
    assert siblings_e == set("DF")
    assert siblings_f == set("DE")
    assert siblings_g == set()


def test_Tree():
    tree = get_tree()
    assert len(tree) == 6


def test_Tree_parents():
    tree = get_tree()
    instances = dict((i.id, i) for i in tree.query())
    parents_a = set(tree.parents(instances["A"]))
    parents_b = set(tree.parents(instances["B"]))
    parents_c = set(tree.parents(instances["C"]))
    parents_d = set(tree.parents(instances["D"]))
    parents_e = set(tree.parents(instances["E"]))
    parents_f = set(tree.parents(instances["F"]))
    assert not parents_a
    assert instances["A"] in parents_b
    assert instances["A"] in parents_c
    assert parents_d == set((instances["C"], instances["A"]))
    assert parents_e == set((instances["C"], instances["A"]))
    assert parents_f == set((instances["C"], instances["A"]))


def test_Tree_children():
    tree = get_tree()
    instances = dict((i.id, i) for i in tree.query())
    children_a = set(tree.children(instances["A"]))
    children_b = set(tree.children(instances["B"]))
    children_c = set(tree.children(instances["C"]))
    children_d = set(tree.children(instances["D"]))
    children_e = set(tree.children(instances["E"]))
    children_f = set(tree.children(instances["F"]))
    assert len(children_a) == 5
    assert children_a == set(i for i in instances.values() if i.id != "A")
    assert not children_b
    assert len(children_c) == 3
    assert children_c == set((instances["D"], instances["E"], instances["F"]))
    assert not children_d
    assert not children_e
    assert not children_f


def test_Tree_siblings():
    tree = get_tree()
    instances = dict((i.id, i) for i in tree.query())
    siblings_a = set(tree.siblings(instances["A"]))
    siblings_b = set(tree.siblings(instances["B"]))
    siblings_c = set(tree.siblings(instances["C"]))
    siblings_d = set(tree.siblings(instances["D"]))
    siblings_e = set(tree.siblings(instances["E"]))
    siblings_f = set(tree.siblings(instances["F"]))
    assert not siblings_a
    assert siblings_b == set((instances["C"],))
    assert siblings_c == set((instances["B"],))
    assert siblings_d == set((instances["E"], instances["F"]))
    assert siblings_e == set((instances["D"], instances["F"]))
    assert siblings_f == set((instances["D"], instances["E"]))
             

if __name__ == "__main__":
    import sys
    args = sys.argv + ["-s", "-d"]
    nose.runmodule(argv=args)