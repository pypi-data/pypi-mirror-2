'''
Created on Jun 4, 2010

@author: nathan
'''

import nose
import quantities as q
import struqtural.mixins.units as units


def test_scale_by_units():
    scale = units.rescale_by_units
    u1 = q.mile / q.hour
    u2 = q.foot / q.minute 
    u3 = q.inch / q.second
    mocks = [Mock(i) for i in range(1, 5)]
    velocities = range(1, 5) * u1
    scale(mocks, u1, u2, "a")
    for (mock, value) in zip(mocks, velocities.rescale(u2)):
        assert mock.a == float(value)
    scale(mocks, u2, u3, "a")
    for (mock, value) in zip(mocks, velocities.rescale(u3)):
        assert mock.a == float(value)


def test_scale():
    scale = units.rescale
    mock = Mock(100.0)
    scale(mock, 2, "a")
    assert mock.a == 200.0


def test_convert_unit_expression():
    convert = units.convert_unit_expression
    u1a = "meter / (second ** 2)"
    u2a = "mile / hour"
    u3a = "kg / m ** 3"
    u1b = q.meter / q.second ** 2
    u2b = q.mile / q.hour
    u3b = q.kg / q.m ** 3
    assert convert(u1a) == u1b
    assert convert(u2a) == u2b
    assert convert(u3a) == u3b
    

class Mock(object):
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c


if __name__ == "__main__":
    import sys
    args = sys.argv + ["-s", "-d"]
    nose.runmodule(argv=args)