import pendulum

from coshed_model import __version__
from coshed_model.datetime_slots import TimestampSlot
from coshed_model.datetime_slots import SlotsDocument


def test_timestamp_slot():
    s = TimestampSlot()
    assert len(s) == 0

    dt = pendulum.datetime(2021, 5, 25, tz="Europe/Berlin")
    s |= dt
    assert len(s) == 1

    s |= dt.to_rfc3339_string()
    assert len(s) == 1
    assert s.json() == [1621893600]


def test_timestamp_slot_initialising():
    s = TimestampSlot([1, 1, 1])
    assert len(s) == 1

    s2 = TimestampSlot({1, 1, 1})
    assert len(s2) == 1

    s3 = TimestampSlot({1, 2, 3})
    s3 |= 1
    assert len(s3) == 3


def test_timestamp_slot_json_output():
    s = TimestampSlot([1, 1, 1])
    assert s.json() == [1]

    s2 = TimestampSlot([17, 1, 1, -1])
    assert s2.json() == [17, 1, -1]

    s3 = TimestampSlot([17, 1, 1, -1, 2, 3, 4, 5, 6])
    assert s3.json(limit=3) == [17, 6, 5]


def test_slots_document():
    d = SlotsDocument()
    assert len(d) == 0
    assert len(d.keys()) == 0

    d2 = SlotsDocument({"110": 3})
    d2.add("110", pendulum.datetime(2021, 5, 25, tz="Europe/Berlin"))
    d2.add("110", pendulum.datetime(2021, 5, 25, tz="Europe/Berlin"))
    assert len(d2) == 1
    assert "110" in d2.keys()
    assert len(d2.json()["data"]["110"]) == 1
