'''
Created on May 31, 2010

@author: nathan
'''


import nose
import struqtural.structures.eav as eav


def test_ArraySet():
    types_ = (int, str, bool)
    arrayset = eav.ArraySet(data=["name"], instance_name="Animal",
                            column_types=[str], primary_keys=["name"],
                            property_types=types_)
    Animal = arrayset.Instance
    stoat = Animal(name='stoat')
    stoat.append(4)
    stoat.append("very cute")
    stoat.append(True)
    marten = Animal('marten')
    marten.append(5)
    marten.append("somewhat cute")
    marten.append(False)
    marten.append(True)
    shrew = Animal('shrew')
    shrew.append(6)
    shrew.append("not cute")
    shrew.extend((True, True, "poisonous"))
    arrayset.add((stoat, marten, shrew), flush=True)
    results = list(arrayset.query())
    assert len(results) == 3
    (stoat, marten, shrew) = results
    assert len(stoat) == 3
    assert stoat[0] == 4
    assert stoat[1] == "very cute"
    assert stoat[2] == True
    assert len(marten) == 4
    assert marten[0] == 5
    assert marten[1] == "somewhat cute"
    assert marten[2] == False
    assert marten[3] == True
    assert len(shrew) == 5
    assert shrew[0] == 6
    assert shrew[1] == "not cute"
    assert shrew[2] == True
    assert shrew[3] == True
    assert shrew[4] == "poisonous"
    # Now test the methods that don't modify the data
    assert shrew.count("not cute") == 1
    assert shrew.index("not cute") == 1
    assert shrew.index(True) == 2
    assert shrew.count(True) == 2
    shrew[2] = False
    assert shrew[2] == False
    del shrew[3]
    assert len(shrew) == 4
    shrew.insert(0, "rodent")
    assert shrew[0] == "rodent"
    assert len(shrew) == 5
    assert "not cute" in shrew
    assert shrew.pop() == "poisonous"
    assert len(shrew) == 4
    shrew.remove("rodent")
    assert shrew[0] == 6
    assert len(shrew) == 3
    results = list(arrayset.query().has_value("not cute"))
    assert len(results) == 1
    assert results[0] == shrew
    results = list(arrayset.query().has_value(False))
    assert len(results) == 2
    assert results == [marten, shrew]
    results = list(arrayset.query().not_has_value(False))
    assert len(results) == 1
    assert results[0] == stoat


def test_DictionarySet():
    types_ = (int, str, bool)
    dictset = eav.DictionarySet(data=["name"], instance_name="Animal",
                                primary_keys=["name"], column_types=[str],
                                property_types=types_)
    Animal = dictset.Instance
    Fact = dictset.Property
    stoat = Animal('stoat')
    marten = Animal('marten')
    shrew = Animal('shrew')
    dictset.add((stoat, marten, shrew), flush=True)
    stoat['color'] = 'red'
    stoat['cuteness'] = "very cute"
    stoat['weasel-like'] = True
    marten['cuteness'] = 5
    marten['weasel-like'] = True
    marten['poisonous'] = False
    shrew['cuteness'] = 6
    shrew['weasel-like'] = False
    shrew['poisonous'] = True  
    # If you are querying on the primary Instance of a structure you don't have
    # to specify it. 
    results = list(dictset.query().eq('weasel-like', True))
    assert len(results) == 2
    assert results[0].name == "stoat"
    assert results[1].name == "marten"
    results = list(dictset.query().eq('poisonous', False))
    assert len(results) == 1
    assert results[0].name == "marten"
    results = list(dictset.query().not_has_key('poisonous'))
    assert len(results) == 1
    assert results[0].name == "stoat"
    results = list(dictset.query().has_key('poisonous'))
    assert len(results) == 2
    assert results[0].name == "marten"
    assert results[1].name == "shrew"
    results = list(dictset.query().gt('cuteness', 5))
    assert len(results) == 1
    assert results[0].name == "shrew"
    # Since we're not querying on Animal here we need to specify explicitly
    results = list(dictset.query(Fact).eq('cuteness', 'very cute'))
    assert len(results) == 1
    assert results[0].key == 'cuteness'
    assert results[0].value == 'very cute'
    assert results[0].type == 'str'


if __name__ == "__main__":
    nose.runmodule()