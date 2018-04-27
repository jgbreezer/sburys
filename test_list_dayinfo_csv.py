"""
Tests for list_dayinfo_csv

Yet to test:
- test multiple csv rows and matching number of items yielded from week_values()
- overlapping ranges/duplicate columns
"""
import io

import pytest

import dayinfo


def test_dayvalue_week_values_ranges():
    expect = [
        # TODO
        {'day': 'mon', 'description': 'ignored 4', 'square': 4, 'value': -2},
        {'day': 'tue', 'description': 'ignored 4', 'square': 4, 'value': -2},
        {'day': 'wed', 'description': 'ignored 4', 'square': 4, 'value': -2},
        {'day': 'thu', 'description': 'ignored -4', 'double': -4, 'value': -2},
        {'day': 'fri', 'description': 'ignored -4', 'double': -4, 'value': -2},
    ]

    for test_heading in (
        ("mon-tue","wed-thu","fri"),
        ("mon","tue-thu","fri"),
        ("mon-thu","fri"),
        ("mon-fri",),
        ):
        data_row = "ignored," + ",".join(("-2",)*len(test_heading))
        test_csv = "description,{}\n{}\n".format(",".join(test_heading), data_row)
        dv = dayinfo.DayValue(io.StringIO(test_csv))
        result = next(dv.week_values())
        assert result == expect


def test_dayvalue_week_values_days_individual():
    TEST_CSV = "mon,tue,wed,thu,fri,description\n" \
    "2,3,5,8,13,£ % text\n"
    expect = [
        # TODO
        {'day': 'mon', 'description': '£ % text 4', 'square': 4, 'value': 2},
        {'day': 'tue', 'description': '£ % text 9', 'square': 9, 'value': 3},
        {'day': 'wed', 'description': '£ % text 25', 'square': 25, 'value': 5},
        {'day': 'thu', 'description': '£ % text 16', 'double': 16, 'value': 8},
        {'day': 'fri', 'description': '£ % text 26', 'double': 26, 'value': 13},
    ]

    dv = dayinfo.DayValue(io.StringIO(TEST_CSV))
    result = next(dv.week_values())
    assert result == expect

def test_dayvalue_week_values_days_field_ordering():
    "Ordering of fields does not matter."
    TEST_CSV = "fri,tue,mon,wed,description,thu\n" \
    "5,2,1,3,testordering,4\n"
    expect = [
        {'day': 'mon', 'description': 'testordering 1', 'square': 1, 'value': 1},
        {'day': 'tue', 'description': 'testordering 4', 'square': 4, 'value': 2},
        {'day': 'wed', 'description': 'testordering 9', 'square': 9, 'value': 3},
        {'day': 'thu', 'description': 'testordering 8', 'double': 8, 'value': 4},
        {'day': 'fri', 'description': 'testordering 10', 'double': 10, 'value': 5},
    ]

    dv = dayinfo.DayValue(io.StringIO(TEST_CSV))
    result = next(dv.week_values())
    assert result == expect


def test_dayvalue_week_values_days_extra_fields_ignored():
    TEST_CSV = "mon-fri,an_extra_field,description,is_ignored,as-is-non-day-range-extra,this-too\n" \
    "-2,extrafield,ignored,ignored one,2,ignored-three\n"
    expect = [
        {'day': 'mon', 'description': 'ignored 4', 'square': 4, 'value': -2},
        {'day': 'tue', 'description': 'ignored 4', 'square': 4, 'value': -2},
        {'day': 'wed', 'description': 'ignored 4', 'square': 4, 'value': -2},
        {'day': 'thu', 'description': 'ignored -4', 'double': -4, 'value': -2},
        {'day': 'fri', 'description': 'ignored -4', 'double': -4, 'value': -2},
    ]

    dv = dayinfo.DayValue(io.StringIO(TEST_CSV))
    result = next(dv.week_values())
    assert result == expect
