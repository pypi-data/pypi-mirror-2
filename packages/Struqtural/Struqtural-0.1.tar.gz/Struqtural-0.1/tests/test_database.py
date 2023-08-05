'''
Created on Apr 19, 2010

@author: nathan
'''

import struqtural.database as db
import struqtural.instances as instance
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.engine.base as base
import nose

from collections import namedtuple


def instantiate(data, name, primary, connector):
    table = db.infer_schema(data, name, primary, connector)
    Instance = instance.create([c.name for c in table.columns])
    db.map_(Instance, table)
    return Instance


def get_data():
    item = namedtuple("Item", ["A", "B", "C", "D"])
    data = [item("T", "1", "1.5", "a"),
            item("F", "2", "2.5", "b"),
            item("TRUE", "3", "3.5", "c"),
            item("FALSE", "4", "4.5", "d")]
    return data


def test_sql_format():
    ts = ["A correct string",
          "An almost correct string.",
          "An (almost) almost correct string ",
          " A #very# incorr/ect, %string@!! ('  "]
    rs = ["A_correct_string",
          "An_almost_correct_string_",
          "An_almost_almost_correct_string",
          "A_very_incorrect_string"]
    assert db.sql_format(ts[0]) == "A_correct_string"
    assert db.sql_format(ts[1]) == "An_almost_correct_string_"
    assert db.sql_format(ts[2]) == "An_almost_almost_correct_string"
    assert db.sql_format(ts[3]) == "A_very_incorrect_string"
    assert db.sql_format([ts[0]]) == ["A_correct_string"]
    assert db.sql_format(ts) == rs


def test_generate_table_types():
    item = namedtuple("Item", "A B C D")
    data = [item(True, 1, 1.0, "1")]
    types = db.generate_column_types(data)
    assert issubclass(types[0], sa.Boolean)
    assert issubclass(types[1], sa.Integer)
    assert issubclass(types[2], sa.Float)
    assert issubclass(types[3], sa.String)


def test_instantiate_table():
    data = get_data()
    item = namedtuple("Item", ["A", "B", "C", "D"])
    results = [item(True, 1, 1.5, "a"),
               item(False, 2, 2.5, "b"),
               item(True, 3, 3.5, "c"),
               item(False, 4, 4.5, "d")]
    connector = db.DatabaseConnector()
    session = connector.connect()
    Instance = instantiate(data, "test", "B", connector)
    instances = list(session.query(Instance))
    assert len(instances) == 4
    values = lambda i: item._make(getattr(instances[i], a) for a in
                                  instances[i].__attributes__)
    assert values(0) == results[0]
    assert values(1) == results[1]
    assert values(2) == results[2]
    assert values(3) == results[3]


def test_introspect_table():
    introspect = db.introspect_table
    data = get_data()
    connector = db.DatabaseConnector()
    session = connector.connect()
    Instance = instantiate(data, "test", "B", connector)
    instances1 = [i for i in session.query(Instance)]
    orm.clear_mappers()
    table = introspect("test", connector)
    Instance = db.instance_from_table(table)
    instances2 = [i for i in session.query(Instance)]
    for (i1, i2) in zip(instances1, instances2):
        assert i1 == i2
    assert db.primary_key_names(Instance) == ["B"]


def test_verified_type():
    # First, let's verify that everything works correctly when passed
    # sqlalchemy types.
    verified_string = repr(db.configure_alchemy_type(sa.String))
    verified_unicode = repr(db.configure_alchemy_type(sa.Unicode))
    assert verified_string == repr(sa.String(db.MAX_STRING_LENGTH))
    assert verified_unicode == repr(sa.Unicode(db.MAX_STRING_LENGTH))
    assert repr(db.configure_alchemy_type(sa.Integer)) == repr(sa.Integer())
    assert repr(db.configure_alchemy_type(sa.Float)) == repr(sa.Float())
    assert repr(db.configure_alchemy_type(sa.Boolean)) == repr(sa.Boolean())
    # Next, let's make sure that things work if we get passed Python types for
    # whatever reason.
    assert verified_string == repr(db.configure_alchemy_type(str))
    assert verified_unicode == repr(db.configure_alchemy_type(unicode))
    assert repr(db.configure_alchemy_type(int)) == repr(sa.Integer())
    assert repr(db.configure_alchemy_type(float)) == repr(sa.Float())
    assert repr(db.configure_alchemy_type(bool)) == repr(sa.Boolean())


def test_infer_schema_no_types():
    data = get_data()
    name = "test"
    primary_keys = ["B"]
    connector = db.DatabaseConnector()
    table = db.infer_schema(data, name, primary_keys, connector)
    assert table.name == "test"
    assert len(table.columns) == 4
    assert isinstance(table.columns["A"].type, sa.Boolean)
    assert isinstance(table.columns["B"].type, sa.Integer)
    assert isinstance(table.columns["C"].type, sa.Float)
    assert isinstance(table.columns["D"].type, sa.String)
    assert len(table.primary_key) == 1
    assert "B" in table.primary_key

   
def test_infer_schema_no_primary_key():
    data = get_data()
    name = "test"
    connector = db.DatabaseConnector()
    table = db.infer_schema(data, name, None, connector)
    assert len(table.columns) == 5
    assert len(table.primary_key) == 1
    assert "id" in table.primary_key


def test_infer_schema_no_data():
    item = type(get_data()[0])
    name = "test"
    primary_keys = ["B"]
    connector = db.DatabaseConnector()
    table = db.infer_schema(item, name, primary_keys, connector,
                            types=[bool, int, float, str])
    # Without data
    assert len(table.columns) == 4
    assert isinstance(table.columns["A"].type, sa.Boolean)
    assert isinstance(table.columns["B"].type, sa.Integer)
    assert isinstance(table.columns["C"].type, sa.Float)
    assert isinstance(table.columns["D"].type, sa.String)


def test_record_tuple():
    record = db.record_tuple
    data = get_data()
    connector = db.DatabaseConnector()
    connector.connect()
    table = db.infer_schema(data, "test", "B", connector)
    records = dict(record(col) for col in table.columns)
    assert records["A"] == "b"
    assert records["B"] == "i4"
    assert records["C"] == "f8"
    assert records["D"] == "S64"


def test_join_instances():
    join = db.join_sequence
    item1 = namedtuple("Item1", ["A", "B", "C", "D", "F"])
    item2 = namedtuple("Item2", ["B", "E"])
    item3 = namedtuple("Item3", ["A", "F", "G"])
    item4 = namedtuple("Item4", ["X", "Y", "Z"])
    data1 = [item1("T", "1", "1.5", "a", "F"),
             item1("F", "2", "2.5", "b", "T"),
             item1("TRUE", "3", "3.5", "c", "T"),
             item1("FALSE", "4", "4.5", "d", "F")]
    data2 = [item2("1", "w"),
             item2("2", "x"),
             item2("3", "y"),
             item2("4", "z")]
    data3 = [item3("F", "F", "AA"),
             item3("F", "T", "BB"),
             item3("T", "F", "CC"),
             item3("T", "T", "DD")]
    data4 = [item4("F", "F", "AA"),
             item4("F", "T", "BB"),
             item4("T", "F", "CC"),
             item4("T", "T", "DD")]
    connector = db.DatabaseConnector()
    session = connector.connect()
    Instance1 = instantiate(data1, "test1", "B", connector)
    Instance2 = instantiate(data2, "test2", "B", connector)
    Instance3 = instantiate(data3, "test3", ["A", "F"], connector)
    Instance4 = instantiate(data3, "test4", ["A", "F"], connector)
    Instance5 = instantiate(data4, "test5", ["X", "Y"], connector)
    Instance6 = instantiate(data4, "test6", ["X", "Y"], connector)
    Instance7 = join(Instance1, (Instance2, {"B":"B"}), factory=instance.create)
    instances1 = list(session.query(Instance7))
    # Test join with a single identical left and right key
    assert instances1[0].E == "w"
    assert instances1[1].E == "x"
    assert instances1[2].E == "y"
    assert instances1[3].E == "z"
    Instance8 = join(Instance1, (Instance3, {"A":"A", "F":"F"}), 
                     factory=instance.create)
    instances2 = list(session.query(Instance8))
    # Test join multiple identical left and right keys
    assert instances2[0].G == "CC"
    assert instances2[1].G == "BB"
    assert instances2[2].G == "DD"
    assert instances2[3].G == "AA"
    Instance9 = join(Instance1, (Instance5, {"A":"X", "F":"Y"}),
                     factory=instance.create)
    instances3 = list(session.query(Instance9))
    # Test join with multiple different left and right keys
    assert instances3[0].Z == "CC"
    assert instances3[1].Z == "BB"
    assert instances3[2].Z == "DD"
    assert instances3[3].Z == "AA"
    joins = [(Instance4, {"A":"A", "F":"F"}), (Instance6, {"A":"X", "F":"Y"})]
    Instance10 = join(Instance1, joins, factory=instance.create)
    instances4 = list(session.query(Instance10))
    # Test compound join with both identical and different sets of keys
    assert instances4[0].G == "CC"
    assert instances4[1].G == "BB"
    assert instances4[2].G == "DD"
    assert instances4[3].G == "AA"
    assert instances4[0].Z == "CC"
    assert instances4[1].Z == "BB"
    assert instances4[2].Z == "DD"
    assert instances4[3].Z == "AA"


def test_create_relationship():
    data1 = get_data()
    item = namedtuple("Item", ["E", "F", "G"])
    data2 = [item("a", "w", "0.25"),
             item("b", "x", "0.50"),
             item("c", "y", "0.75"),
             item("d", "z", "1.00")] 
    connector = db.DatabaseConnector()
    session = connector.connect()
    Instance1 = instantiate(data1, "test1", "B", connector)
    Instance2 = instantiate(data2, "test2", "E", connector)
    db.relationship(Instance2, Instance1, "instance2", "E", "D")
    instances2 = list(i.instance2 for i in session.query(Instance1))
    assert instances2[0].E == "a"
    assert instances2[0].F == "w"
    assert instances2[0].G == 0.25
    assert instances2[1].E == "b"
    assert instances2[1].F == "x"
    assert instances2[1].G == 0.50
    assert instances2[2].E == "c"
    assert instances2[2].F == "y"
    assert instances2[2].G == 0.75
    assert instances2[3].E == "d"
    assert instances2[3].F == "z"
    assert instances2[3].G == 1.0


def test_DatabaseConnector():
    connector = db.DatabaseConnector()
    session = connector.connect()
    assert isinstance(session.connection(), base.Connection)
    assert connector.metadata.is_bound()


def alchemy_data():
    metadata = sa.MetaData()
    columns1 = (sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("name", sa.String(32)),
                sa.Column("age", sa.Integer()))
    columns2 = (sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("number", sa.Integer()),
                sa.Column("street", sa.String(32)),
                sa.Column("zip", sa.String(9)))
    columns3 = (sa.Column("person_id", sa.Integer()),
                sa.Column("address_id", sa.Integer()))
    table1 = sa.Table("people", metadata, *columns1)
    table2 = sa.Table("addresses", metadata, *columns2)
    table3 = sa.Table("person_address_association", metadata, *columns3)
    return (table1, table2, table3)


def alchemy_data_with_fks():
    (table1, table2, table3) = alchemy_data()
    table3.columns["person_id"].append_foreign_key(sa.ForeignKey("people.id"))
    table3.columns["address_id"].append_foreign_key \
        (sa.ForeignKey("addresses.id"))
    return (table1, table2, table3)


def test__get_fk():
    (table1, table2, table3) = alchemy_data_with_fks()
    person_foreign_key = list(table3.columns["person_id"].foreign_keys)
    address_foreign_key = list(table3.columns["address_id"].foreign_keys)
    assert db.get_fk(table1, table3) == person_foreign_key
    assert db.get_fk(table2, table3) == address_foreign_key


def test_columns_from_join_table():
    (table1, table2, table3) = alchemy_data_with_fks()
    results = db.columns_from_join_table(table1, table2, table3)
    assert results[0] == [table1.columns["id"]]
    assert results[1] == [table2.columns["id"]]
    assert results[2] == [table3.columns["person_id"]]
    assert results[3] == [table3.columns["address_id"]]


def test_columns_from_tables():
    (table1, table2, table3) = alchemy_data_with_fks()
    (c1, c3a) = db.columns_from_tables(table1, table3)
    (c2, c3b) = db.columns_from_tables(table2, table3)
    assert c1 == [table1.columns["id"]]
    assert c2 == [table2.columns["id"]]
    assert c3a == [table3.columns["person_id"]]
    assert c3b == [table3.columns["address_id"]]


def test_columns_from_foreign_keys():
    (table1, table2, table3) = alchemy_data_with_fks()
    t3_t1_ref = db.columns_from_foreign_keys(table1.columns["id"], table3)
    t3_t2_ref = db.columns_from_foreign_keys(table2.columns["id"], table3)
    assert t3_t1_ref == [table3.columns["person_id"]]
    assert t3_t2_ref == [table3.columns["address_id"]]


def test_referenced_by_name():
    (table1, table2, table3) = alchemy_data_with_fks()
    t1_t3_ref = db.referenced_by_name \
        (table3.columns["person_id"], table1)
    t2_t3_ref = db.referenced_by_name \
        (table3.columns["address_id"], table2)
    assert t1_t3_ref == [table1.columns["id"]]
    assert t2_t3_ref == [table2.columns["id"]]

    
def test_referencing_by_name():
    (table1, table2, table3) = alchemy_data_with_fks()
    t3_t1_ref = db.referencing_by_name(table1.columns["id"], table3)
    t3_t2_ref = db.referencing_by_name(table2.columns["id"], table3)
    assert t3_t1_ref == [table3.columns["person_id"]]
    assert t3_t2_ref == [table3.columns["address_id"]]


def test_get_many_to_many_join_columns():
    (table1, table2, table3) = alchemy_data_with_fks()
    results = db.get_many_to_many_join_columns(table1, table2, table3)
    assert results[0] == [table1.columns["id"]]
    assert results[1] == [table2.columns["id"]]
    assert results[2] == [table3.columns["person_id"]]
    assert results[3] == [table3.columns["address_id"]]


def test_many_to_many_relationship():
    (table1, table2, table3) = alchemy_data_with_fks()
    class Person(object):
        def __init__(self, name, age):
            self.name = name
            self.age = age           
    class Address(object):
        def __init__(self, number, street, zip):
            self.number = number
            self.street = street
            self.zip = zip
    connector = db.DatabaseConnector(metadata=table1.metadata)
    session = connector.session
    connector.metadata.create_all()
    orm.mapper(Person, table1)
    orm.mapper(Address, table2)
    db.relationship(Person, Address, intermediate_table=table3)
    john = Person("john", 30)
    jane = Person("jane", 30)
    home = Address(123, "street", "12345")
    work = Address(234, "road", "23456")
    school = Address(345, "avenue", "34567")
    session.add_all((john, jane, home, work, school))
    session.flush()
    john.addresses.extend((home, work, school))
    jane.addresses.extend((home, work))
    assert session.query(Address).filter(Address.people.contains(john)).count() == 3
    assert session.query(Address).filter(Address.people.contains(jane)).count() == 2


if __name__ == "__main__":
    import sys
    args = sys.argv + ["-s", "-d"]
    nose.runmodule(argv=args)