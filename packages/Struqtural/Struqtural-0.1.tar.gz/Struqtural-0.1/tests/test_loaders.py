'''
Created on Apr 19, 2010

@author: nathan
'''

import cStringIO
import copy
import datetime
import nose
import struqtural.loaders.loader as loader
import struqtural.loaders.file as file_


def test_CollectionLoader():
    data = [["T", "1", "1.5", "a"],
            ["F", "2", "2.5", "b"],
            ["TRUE", "3", "3.5", "c"],
            ["FALSE", "4", "4.5", "d"]]
    columns = ["A", "B", "C", "D"]
    loader1 = loader.CollectionLoader((columns, data), "B", "Instance")
    instances = list(loader1.connector.session.query(loader1.Instance))
    # Test that all rows have been converted to instances, all types have been
    # properly identified and correct values have been assigned in each case.
    assert len(instances) == 4
    assert instances[0].A == True
    assert instances[1].A == False
    assert instances[2].A == True
    assert instances[3].A == False
    assert instances[0].B == 1
    assert instances[1].B == 2
    assert instances[2].B == 3
    assert instances[3].B == 4
    assert instances[0].C == 1.5
    assert instances[1].C == 2.5
    assert instances[2].C == 3.5
    assert instances[3].C == 4.5
    assert instances[0].D == "a"
    assert instances[1].D == "b"
    assert instances[2].D == "c"
    assert instances[3].D == "d"
    data2 = [{"A":True, "B":1, "C":1.5, "D":"a"},
             {"A":False, "B":2, "C":2.5, "D":"b"},
             {"A":True, "B":3, "C":3.5, "D":"c"},
             {"A":False, "B":4, "C":4.5, "D":"d"}]
    loader2 = loader.CollectionLoader(data2, "B", "test2", loader1.connector)
    instances2 = list(loader2.connector.session.query(loader1.Instance))
    # Now test that instances generated using from dictionary data are
    # equivalent to their list based bretheren.
    assert instances[0] == instances2[0]
    assert instances[1] == instances2[1]
    assert instances[2] == instances2[2]
    assert instances[3] == instances2[3]


def get_mock():
    class Mock(object):
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c
    return Mock


def test_ObjectLoader():
    Mock = get_mock()
    mocks = [Mock(1, 2, 3), Mock(4, 5, 6), Mock(7, 8, 9)]
    loader1 = loader.ObjectLoader(mocks, "a")
    results = list(loader1.connector.session.query(loader1.Instance))
    assert len(results) == 3
    assert results[0].a == 1
    assert results[0].b == 2
    assert results[0].c == 3
    assert results[1].a == 4
    assert results[1].b == 5
    assert results[1].c == 6
    assert results[2].a == 7
    assert results[2].b == 8
    assert results[2].c == 9

    
def test_ObjectLoader_pickling():
    Mock = get_mock()
    mocks = [Mock(1, 2, 3), Mock(4, 5, 6), Mock(7, 8, 9)]
    mocks[0].d = ["a", "b", "c"]
    mocks[1].e = {"d":10, "e":11}
    loader1 = loader.ObjectLoader(mocks)
    results = list(loader1.connector.session.query(loader1.Instance))
    assert len(results) == 3
    assert results[0].d == ["a", "b", "c"]
    assert results[1].e == {"d":10, "e":11}


def test_InstanceLoader():
    # Note that while this still works, this sort of input is on the way out.
    data1 = [[True, 1, 1.5, "a"],
             [False, 2, 2.5, "b"],
             [True, 3, 3.5, "c"],
             [False, 4, 4.5, "d"]]
    columns1 = ["A", "B", "C", "D"]
    copy.deepcopy(data1)
    loader1 = loader.CollectionLoader((columns1, data1), "B", "test")
    loader3 = loader.InstanceLoader(loader1.Instance, query=loader1.Query)
    instances1 = list(loader1.connector.session.query(loader1.Instance))
    instances3 = list(loader3.connector.session.query(loader3.Instance))
    for (one, three) in zip(instances1, instances3):
        assert one == three


def test_JoinLoader():
    new_table = loader.CollectionLoader
    data1 = [[True, 1, 1.5, "a"],
             [False, 2, 2.5, "b"],
             [True, 3, 3.5, "c"],
             [False, 4, 4.5, "d"]]
    data2 = copy.deepcopy(data1)
    data3 = copy.deepcopy(data1)
    data4 = copy.deepcopy(data1)
    data5 = copy.deepcopy(data1)
    data6 = copy.deepcopy(data1)
    columns1 = ["A", "B", "C", "D"]
    columns2 = ["E", "F", "G", "H"]
    columns3 = ["I", "J", "K", "L"]
    columns4 = ["A", "B", "C", "D"]
    columns5 = ["E", "B", "F", "G"]
    columns6 = ["H", "B", "I", "J"]
    loader1 = new_table((columns1, data1), "B", "test1")
    loader2 = new_table((columns2, data2), "F", "test2", loader1.connector)
    loader3 = new_table((columns3, data3), "J", "test3", loader1.connector)
    loader4 = new_table((columns4, data4), "B", "test4")
    loader5 = new_table((columns5, data5), "B", "test5", loader4.connector)
    loader6 = new_table((columns6, data6), "B", "test6", loader4.connector)
    loader7 = loader.JoinLoader(loader1, (loader2, {"B":"F"}),
                                 (loader3, {"B":"J"}))
    instances = list(loader7.connector.session.query(loader7.Instance))
    # Test the common case where the join condition is specified.
    for instance in instances:
        assert instance.A == instance.E and instance.A == instance.I
        assert instance.C == instance.G and instance.C == instance.K
        assert instance.D == instance.H and instance.D == instance.L
    loader8 = loader.JoinLoader(loader4, loader5, loader6)
    instances = list(loader8.connector.session.query(loader8.Instance))
    # Test that join key inference works properly.
    for instance in instances:
        assert instance.A == instance.E and instance.A == instance.H
        assert instance.C == instance.F and instance.C == instance.I
        assert instance.D == instance.G and instance.D == instance.J


def test_DelimitedFileLoader():
    delimited_contents = ("A, B, C, D\n"
                          "T, 1, 1.5, a\n"
                          "F, 2, 2.5, b\n"
                          "TRUE, 3, 3.5, c\n"
                          "FALSE, 4, 4.5, d\n")
    delimited_file = cStringIO.StringIO(delimited_contents)
    loader1 = file_.DelimitedFileLoader(delimited_file,
                                        instance_name="Instance",
                                        primary_keys="B")
    instances = list(loader1.connector.session.query(loader1.Instance))
    # Test that all rows have been converted to instances, all types have been
    # properly identified and correct values have been assigned in each case.
    assert len(instances) == 4
    assert instances[0].A == True
    assert instances[1].A == False
    assert instances[2].A == True
    assert instances[3].A == False
    assert instances[0].B == 1
    assert instances[1].B == 2
    assert instances[2].B == 3
    assert instances[3].B == 4
    assert instances[0].C == 1.5
    assert instances[1].C == 2.5
    assert instances[2].C == 3.5
    assert instances[3].C == 4.5
    assert instances[0].D == "a"
    assert instances[1].D == "b"
    assert instances[2].D == "c"
    assert instances[3].D == "d"


def test_XmlMultiLoader_single_table():
    loader_ = file_.XmlMultiLoader("data/menu.xml", table_prefix="menu")
    assert len(loader_.properties) == 1
    property_ = loader_.properties["Food"]
    session = property_.connector.session
    Instance = property_.Instance
    results = list(session.query(Instance))
    assert len(results) == 5
    for result in results:
        assert isinstance(result.price, basestring)
        assert isinstance(result.calories, int)
        assert isinstance(result.name, basestring)
        assert isinstance(result.description, basestring)
        assert isinstance(result.id, int)

       
def test_XmlMultiLoader_multiple_tables():
    loader_ = file_.XmlMultiLoader("data/sales_order.xml")
    property_ = loader_.properties["SalesOrder"]
    session = property_.connector.session
    Instance = property_.Instance
    results = list(session.query(Instance))
    assert len(results) == 1
    assert results[0].customer == "Gallagher Industries"
    assert results[0].date == datetime.date(2000, 10, 29)
    assert results[0].number == 1234
    assert len(results[0].lines) == 2
    assert results[0].lines[0].price == 10.95
    assert results[0].lines[1].price == 3.99
    assert results[0].lines[0].part == "A-10"
    assert results[0].lines[1].part == "B-43"
    assert results[0].lines[0].number == 1
    assert results[0].lines[1].number == 2
    assert results[0].lines[0].quantity == 12
    assert results[0].lines[1].quantity == 600


def test_XmlMultiLoader_many_to_many():
    primary_keys = {"Department":"DeptNum", "Employee":"Number"}
    loader_ = file_.XmlMultiLoader("data/department.xml",
                                  primary_keys=primary_keys)
    departments = loader_.properties["Department"]
    session = departments.connector.session
    Department = departments.Instance
    results = list(session.query(Department))
    assert results[0].deptnum == 123
    assert len(results[0].employees) == 3
    assert results[0].employees[0].number == 143
    assert results[0].employees[1].number == 687
    assert results[0].employees[2].number == 947
    assert results[1].deptnum == 456
    assert len(results[1].employees) == 3
    assert results[1].employees[0].number == 157
    assert results[1].employees[1].number == 687
    assert results[1].employees[2].number == 947


def test_DatabaseMultiLoader():
    loader1 = file_.XmlMultiLoader("data/sales_order.xml")
    connector = loader1.properties["SalesOrder"].connector
    names = {"SalesOrders":"SalesOrder", "Lines":"Line"}
    loader2 = loader.DatabaseMultiLoader("SalesOrders", connector, names,
                                         backref_by_default=True)
    property_ = loader2.properties["SalesOrders"]
    session = property_.connector.session
    Instance = property_.Instance
    results = list(session.query(Instance))
    assert results[0].customer == "Gallagher Industries"
    assert results[0].date == datetime.date(2000, 10, 29)
    assert results[0].number == 1234
    assert len(results[0].lines) == 2
    assert results[0].lines[0].price == 10.95
    assert results[0].lines[1].price == 3.99
    assert results[0].lines[0].part == "A-10"
    assert results[0].lines[1].part == "B-43"
    assert results[0].lines[0].number == 1
    assert results[0].lines[1].number == 2
    assert results[0].lines[0].quantity == 12
    assert results[0].lines[1].quantity == 600
    
def test_DatabaseMultiLoader_many_to_many():
    primary_keys = {"Department":"DeptNum", "Employee":"Number"}
    loader1 = file_.XmlMultiLoader("data/department.xml",
                                  primary_keys=primary_keys)
    connector = loader1.properties["Department"].connector
    names = {"Departments":"Department", "Employees":"Employee"}
    loader2 = loader.DatabaseMultiLoader("Departments", connector, names,
                                         backref_by_default=True)
    departments = loader2.properties["Departments"]
    session = departments.connector.session
    Department = departments.Instance
    results = list(session.query(Department))
    assert results[0].deptnum == 123
    assert len(results[0].employees) == 3
    assert results[0].employees[0].number == 143
    assert results[0].employees[1].number == 687
    assert results[0].employees[2].number == 947
    assert results[1].deptnum == 456
    assert len(results[1].employees) == 3
    assert results[1].employees[0].number == 157
    assert results[1].employees[1].number == 687
    assert results[1].employees[2].number == 947

if __name__ == "__main__":
    import sys
    args = sys.argv + ["-s", "-d"]
    nose.runmodule(argv=args)