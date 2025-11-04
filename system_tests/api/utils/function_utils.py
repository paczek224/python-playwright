import json

from assertpy import assert_that


def negate(cond):
    return lambda x: not cond(x)


def all_match(data, cond):
    for el in data:
        assert_that(cond(el)).described_as(f"{json.dumps(el, indent=3)} dont meet the condition").is_true()


def any_match(data, cond):
    assert_that(list(filter(cond, data))).is_not_empty()


def none_match(data, cond):
    assert_that(list(filter(cond, data))).is_empty()
