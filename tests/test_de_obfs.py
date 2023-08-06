import pytest

from cipherFinder.de_obfs import (
    do_regex,
    do_list_addition,
    grap,
    get_table_contents,
    TABLE_REGEX,
    REGEX,
)


@pytest.fixture
def table_fixture():
    return "local foo = {'foo', 'bar'} function (bazz, fooBar) end"


def test_grap():
    test_list = ["foo", "bar"]
    out = grap(test_list)

    assert out not in test_list
    assert len(test_list) == 1

    out2 = grap(test_list)

    assert out2 not in test_list
    assert len(test_list) != 1


def test_do_regex(table_fixture):  # pylint: disable=redefined-outer-name
    table_found = do_regex(table_fixture, TABLE_REGEX)
    variable_found = do_regex(table_fixture, REGEX[0])
    function_found = do_regex(table_fixture, REGEX[1])

    assert table_found == [("{'foo', 'bar'}", "'foo', 'bar'")]
    assert variable_found == [("local foo", "local foo", " ", "foo")]
    assert function_found == [
        ("function (bazz, fooBar)", "bazz, fooBar", "fooBar", ", ", " ")
    ]


def test_do_list_addition():
    test_list = [
        ("local foobar", "local foobar", " ", "foobar"),
        ("function (foo, bar)", "foo, bar", "bar", ", ", " "),
    ]
    out_list = []

    for i in do_list_addition(test_list):
        out_list.extend(i)

    assert out_list == ["foobar", "foo", "bar"]


def test_get_table_contents(
    table_fixture,
):  # pylint: disable=redefined-outer-name
    contents = get_table_contents(table_fixture)
    assert contents == ["'foo'", "'bar'"]
