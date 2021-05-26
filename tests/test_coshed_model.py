import pendulum

from coshed_model import __version__
from coshed_model.datetime_slots import Slots


def test_slots():
    s = Slots()
    assert len(s) == 0
    dt = pendulum.datetime(2021, 5, 25, tz="Europe/Berlin")
    s |= dt
    assert len(s) == 1
    s |= dt.to_rfc3339_string()
    assert len(s) == 1
    assert s.json() == [1621893600]


def test_slots_initialising():
    s = Slots([1, 1, 1])
    assert len(s) == 1

    s2 = Slots({1, 1, 1})
    assert len(s2) == 1

    s3 = Slots({1, 2, 3})
    s3 |= 1
    assert len(s3) == 3


def test_slots_json_output():
    s = Slots([1, 1, 1])
    assert s.json() == [1]

    s2 = Slots([17, 1, 1, -1])
    assert s2.json() == [17, 1, -1]

    s3 = Slots([17, 1, 1, -1, 2, 3, 4, 5, 6])
    assert s3.json(limit=3) == [17, 6, 5]
