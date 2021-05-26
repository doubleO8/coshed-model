#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pendulum


class SlotsEmptyError(ValueError):
    pass


class Slots(set):
    def __init__(self, *args):
        if len(args) == 1:
            for item in iter(args[0]):
                val = Slots.int_timestamp(item)
                self |= val

    @classmethod
    def int_timestamp(cls, in_value):
        if isinstance(in_value, pendulum.DateTime):
            val = in_value.in_tz(pendulum.UTC).int_timestamp
        elif isinstance(in_value, int):
            val = pendulum.from_timestamp(in_value).in_tz(pendulum.UTC).int_timestamp
        else:
            # raise ValueError(type(in_value))
            dt = pendulum.parse(in_value)
            val = dt.in_tz(pendulum.UTC).int_timestamp

        return val

    def __ior__(self, other):
        return super().__ior__(set([Slots.int_timestamp(other)]))

    def __iadd__(self, other):
        return NotImplemented

    def __isub__(self, other):
        return NotImplemented

    def json(self, **kwargs):
        r_sorted = list(reversed(sorted(self)))

        if len(r_sorted) == 0 and not kwargs.get("allow_empty", False):
            raise SlotsEmptyError()

        if kwargs.get("limit"):
            r_sorted = r_sorted[: kwargs.get("limit")]

        return r_sorted
