#!/usr/bin/env python
# coding: utf-8
"""
    tests
    ~~~~~

    :copyright: 2010 by the INI Team, see AUTHORS for details.
    :license: MIT, see LICENSE for details.
"""
from StringIO import StringIO

from ini import OrderedDict, load, dump

def make_test_data():
    return zip(range(10), range(10))

def make_test_dict():
    return OrderedDict(make_test_data())

class TestOrderedDict(object):
    def test_clear(self):
        d = make_test_dict()
        assert d
        d.clear()
        assert not d

    def test_setitem(self):
        d = OrderedDict()
        data = make_test_data()
        for key, value in data:
            d[key] = value
        assert d.items() == data

    def test_delitem(self):
        data = make_test_data()
        d = OrderedDict(data)
        del data[2]
        del d[2]
        assert d.items() == data

    def test_reversed(self):
        data = make_test_data()
        d = OrderedDict(data)
        assert list(reversed(d)) == [item[0] for item in reversed(data)]

    def test_keys(self):
        data = make_test_data()
        d = OrderedDict(data)
        assert list(d) == d.keys() == list(d.iterkeys())
        assert list(d) == [item[0] for item in data]

    def test_values(self):
        data = make_test_data()
        d = OrderedDict(data)
        assert d.values() == list(d.itervalues()) == [d[k] for k in d]

    def test_equality(self):
        data = make_test_data()
        d1 = OrderedDict(data)
        d2 = OrderedDict(data)
        d3 = dict(data)
        assert d1 == d2 == d3

    def test_inequality(self):
        data = make_test_data()
        d1 = OrderedDict(data)
        d2 = OrderedDict(reversed(data))
        assert d1 != d2

    def test_popitem_last(self):
        data = make_test_data()
        d = OrderedDict(data)
        assert d.popitem() == data[-1]
        assert d.items() == data[:-1]

    def test_popitem_first(self):
        data = make_test_data()
        d = OrderedDict(data)
        assert d.popitem(last=False) == data[0]
        assert d.items() == data[1:]

    def test_pop_returns_correct_value(self):
        data = make_test_data()
        d = OrderedDict(data)
        for key, value in data:
            assert d.pop(key) == value

    def test_pop_raises_keyerror_if_dict_empty(self):
        d = OrderedDict()
        try:
            d.pop("some key")
        except KeyError as exc:
            assert isinstance(exc, KeyError)
        else:
            raise AssertionError("nothing raised")

    def test_pop_returns_default_if_empty(self):
        d = OrderedDict()
        assert d.pop("some key", "default value") == "default value"

    def test_pop_returns_default_if_key_doesnt_exist(self):
        d = make_test_dict()
        assert d.pop("some key", "default value") == "default value"

    def test_setdefault_returns_value(self):
        data = make_test_data()
        d = OrderedDict(data)
        for key, value in data:
            assert d.setdefault(key) == value

    def test_setdefault_sets_and_returns_default(self):
        d = make_test_dict()
        assert "some key" not in d
        assert d.setdefault("some key", "some value") == "some value"
        assert d["some key"] == "some value"

class TestLoad(object):
    def test_flat_file(self):
        ini_file = StringIO(
        "[spam]\n"
        "foo = bar\n"
        "spam = eggs\n"
        "[eggs]\n"
        "monty = python\n"
        )
        assert load(ini_file) == {
            "spam": {
                "foo": "bar",
                "spam": "eggs",
            },
            "eggs": {
                "monty": "python",
            },
        }

    def test_nested_file(self):
        ini_file = StringIO(
            "[spam]\n"
            "foo = bar\n"
            "[spam.eggs]\n"
            "monty = python\n"
            "[foo]\n"
            "bar = baz\n"
        )
        assert load(ini_file) == {
            "spam": {
                "foo": "bar",
                "eggs": {
                    "monty": "python",
                },
            },
            "foo": {
                "bar": "baz",
            },
        }

class TestDump(object):
    def test_flat(self):
        data = {
            "foo": {
                "bar": "baz",
            },
            "bar": {
                "spam": "eggs",
            },
        }
        expected = (
            "[foo]\n"
            "bar = baz\n"
            "[bar]\n"
            "spam = eggs\n"
        )
        test_file = StringIO()
        dump(data, test_file)
        assert test_file.getvalue() == expected

    def test_nested(self):
        data = {
            "foo": {
                "bar": {
                    "spam": "eggs",
                },
            },
            "bar": {
                "monty": "python",
            },
        }
        expected = (
            "[foo.bar]\n"
            "spam = eggs\n"
            "[bar]\n"
            "monty = python\n"
        )
        test_file = StringIO()
        dump(data, test_file)
        assert test_file.getvalue() == expected
