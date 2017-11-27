# -*- coding: utf-8 -*-
import unittest

from type_play import optional


class TestOptional(unittest.TestCase):
    def test_get(self) -> None:
        obj = object()
        maybe_obj = optional.Optional(obj)
        self.assertIs(obj, maybe_obj.get())

    def test_get_empty(self) -> None:
        with self.assertRaises(optional.EmptyOptionalError):
            empty = optional.Optional()
            val = empty.get()
            print(val)

    def test_is(self) -> None:
        self.assertIs(optional.Optional(), optional.Optional())

    def test_map(self) -> None:
        value = 3.5

        def _func(x: float) -> str:
            return str(2 * x)

        maybe_value = optional.Optional(value)
        mapped = maybe_value.map(_func)
        self.assertEqual(maybe_value, optional.Optional(value))
        self.assertEqual(_func(value), mapped.get())
