# -*- coding: utf-8 -*-
# Copyright (C) 2010, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.

# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys

import pytest

from pyudev import _util


@pytest.mark.conversion
def test_ensure_byte_string():
    assert isinstance(_util.ensure_byte_string('hello world'), bytes)
    assert _util.ensure_byte_string('hello world') == b'hello world'
    hello = b'hello world'
    assert _util.ensure_byte_string(hello) is hello


@pytest.mark.conversion
def test_ensure_byte_string_none():
    with pytest.raises(AttributeError):
        _util.ensure_byte_string(None)


@pytest.mark.conversion
def test_ensure_unicode_string():
    assert pytest.is_unicode_string(
        _util.ensure_unicode_string(b'hello world'))
    assert _util.ensure_unicode_string(b'hello world') == 'hello world'
    hello = 'hello world'
    assert _util.ensure_unicode_string(hello) is hello


@pytest.mark.conversion
def test_ensure_unicode_string_none():
    with pytest.raises(AttributeError):
        _util.ensure_unicode_string(None)


@pytest.mark.conversion
def test_property_value_to_bytes_string():
    hello = 'hello world'.encode(sys.getfilesystemencoding())
    assert _util.property_value_to_bytes(hello) is hello
    assert isinstance(_util.property_value_to_bytes('hello world'), bytes)
    assert _util.property_value_to_bytes('hello world') == hello


@pytest.mark.conversion
def test_property_value_to_bytes_int():
    assert _util.property_value_to_bytes(10000) == b'10000'
    assert isinstance(_util.property_value_to_bytes(10000), bytes)


@pytest.mark.conversion
def test_property_value_to_bytes_bool():
    assert _util.property_value_to_bytes(True) == b'1'
    assert isinstance(_util.property_value_to_bytes(True), bytes)
    assert _util.property_value_to_bytes(False) == b'0'
    assert isinstance(_util.property_value_to_bytes(False), bytes)


@pytest.mark.conversion
def test_string_to_bool_true():
    assert isinstance(_util.string_to_bool('1'), bool)
    assert _util.string_to_bool('1')


@pytest.mark.conversion
def test_string_to_bool_false():
    assert isinstance(_util.string_to_bool('0'), bool)
    assert not _util.string_to_bool('0')


@pytest.mark.conversion
def test_string_to_bool_invalid_value():
    with pytest.raises(ValueError) as exc_info:
        _util.string_to_bool('foo')
    assert str(exc_info.value) == 'Not a boolean value: {0!r}'.format('foo')


def test_udev_list_iterate_no_entry():
    assert not list(_util.udev_list_iterate(None))


def test_udev_list_iterate_mock():
    test_list = iter(['spam', 'eggs', 'foo', 'bar'])

    def next_entry(entry):
        try:
            return next(test_list)
        except StopIteration:
            return None

    def name(entry):
        if entry:
            return entry
        else:
            pytest.fail('empty entry!')

    get_next = 'udev_list_entry_get_next'
    get_name = 'udev_list_entry_get_name'
    with pytest.nested(pytest.patch_libudev(get_name),
                       pytest.patch_libudev(get_next)) as (get_name, get_next):
        get_name.side_effect = name
        get_next.side_effect = next_entry
        items = list(_util.udev_list_iterate(next(test_list)))
        assert items == ['spam', 'eggs', 'foo', 'bar']
