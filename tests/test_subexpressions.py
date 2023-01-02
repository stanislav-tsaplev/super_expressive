import pytest

from ..src.super_expressive import SuperExpressive, RegexError


def test_subexpression_must_be_a_super_expressive_instance():
    with pytest.raises(RegexError) as e:
        SuperExpressive().subexpression('nope')  # type: ignore
    assert str(e.value) == "expr must be a SuperExpressive instance"


simple_subexpression = (
    SuperExpressive()
        .string("hello")
        .any_char
        .string("world")
)


def test_simple():
    regex = r"^\d{3,}hello.world[0-9]$"
    se = (
        SuperExpressive()
            .start_of_input
            .at_least(3).digit
            .subexpression(simple_subexpression)
            .range('0', '9')
            .end_of_input
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_simple_quantified():
    regex = r"^\d{3,}(?:hello.world)+[0-9]$"
    se = (
        SuperExpressive()
            .start_of_input
            .at_least(3).digit
            .one_or_more.subexpression(simple_subexpression)
            .range('0', '9')
            .end_of_input
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


flags_subexpression = (
    SuperExpressive()
        .line_by_line
        .case_insensitive
        .string("hello")
        .any_char
        .string("world")
)


def test_ignoring_flags_false():
    regex = r"(?ims)^\d{3,}hello.world[0-9]$"
    se = (
        SuperExpressive()
            .single_line
            .start_of_input
            .at_least(3).digit
            .subexpression(flags_subexpression, ignore_flags=False)
            .range('0', '9')
            .end_of_input
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_ignoring_flags_true():
    regex = r"(?s)^\d{3,}hello.world[0-9]$"
    se = (
        SuperExpressive()
            .single_line
            .start_of_input
            .at_least(3).digit
            .subexpression(flags_subexpression)
            .range('0', '9')
            .end_of_input
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


start_end_subexpression = (
    SuperExpressive()
        .start_of_input
        .string("hello")
        .any_char
        .string("world")
        .end_of_input
)


def test_ignoring_start_end_false():
    regex = r"\d{3,}^hello.world$[0-9]"
    se = (
        SuperExpressive()
            .at_least(3).digit
            .subexpression(start_end_subexpression, ignore_start_and_end=False)
            .range('0', '9')
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_ignoring_start_end_true():
    regex = r"\d{3,}hello.world[0-9]"
    se = (
        SuperExpressive()
            .at_least(3).digit
            .subexpression(start_end_subexpression)
            .range('0', '9')
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_start_defined_in_subexpression_and_main_expression():
    with pytest.raises(RegexError) as e:
        (
            SuperExpressive()
                .start_of_input
                .at_least(3).digit
                .subexpression(start_end_subexpression, ignore_start_and_end=False)
                .range('0', '9')
        )
    assert str(e.value) == (
        "The parent regex already has a defined start of input. "
        "You can ignore a subexpressions start_of_input/end_of_input markers "
        "with the ignore_start_and_end option"
    )


def test_end_defined_in_main_expression_and_subexpression():
    with pytest.raises(RegexError) as e:
        (
            SuperExpressive()
                .end_of_input
                .subexpression(start_end_subexpression, ignore_start_and_end=False)
        )
    assert str(e.value) == (
        "The parent regex already has a defined end of input. "
        "You can ignore a subexpressions start_of_input/end_of_input markers "
        "with the ignore_start_and_end option"
    )


def test_end_defined_in_subexpression_and_main_expression():
    with pytest.raises(RegexError) as e:
        (
            SuperExpressive()
                .subexpression(start_end_subexpression, ignore_start_and_end=False)
                .end_of_input
        )
    assert str(e.value) == ("This regex already has a defined end of input")


named_capture_subexpression = (
    SuperExpressive()
        .named_capture("module")
            .exactly(2).any_char
        .end()
        .named_backreference("module")
)


# XXX: this test uses a different regex syntax (Python, not JS)
def test_no_namespacing():
    regex = r"\d{3,}(?P<module>.{2})(?P=module)[0-9]"
    se = (
        SuperExpressive()
            .at_least(3).digit
            .subexpression(named_capture_subexpression)
            .range('0', '9')
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


# XXX: this test uses a different regex syntax (Python, not JS)
def test_namespacing():
    regex = r"\d{3,}(?P<yolomodule>.{2})(?P=yolomodule)[0-9]"
    se = (
        SuperExpressive()
            .at_least(3).digit
            .subexpression(named_capture_subexpression, namespace="yolo")
            .range('0', '9')
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_group_name_collision_no_namespacing():
    with pytest.raises(RegexError) as e:
        (
            SuperExpressive()
                .named_capture("module")
                    .at_least(3).digit
                .end()
                .subexpression(named_capture_subexpression)
                .range('0', '9')
        )
    assert str(e.value) == "cannot use module again for a capture group"


def test_group_name_collision_after_namespacing():
    with pytest.raises(RegexError) as e:
        (
            SuperExpressive()
                .named_capture("yolomodule")
                    .at_least(3).digit
                .end()
                .subexpression(named_capture_subexpression, namespace="yolo")
                .range('0', '9')
        )
    assert str(e.value) == "cannot use yolomodule again for a capture group"


indexed_backreference_subexpression = (
    SuperExpressive()
        .capture
            .exactly(2).any_char
        .end()
        .backreference(1)
)


def test_indexed_backreferencing():
    regex = r"(\d{3,})(.{2})\2\1[0-9]"
    se = (
        SuperExpressive()
            .capture
                .at_least(3).digit
            .end()
            .subexpression(indexed_backreference_subexpression)
            .backreference(1)
            .range('0', '9')
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


nested_subexpression = SuperExpressive().exactly(2).any_char
first_layer_subexpression = (
    SuperExpressive()
        .string("outer begin")
        .named_capture("inner_subexpression")
            .optional.subexpression(nested_subexpression)
        .end()
        .string("outer end")
)


# XXX: this test uses a different regex syntax (Python, not JS)
def test_deeply_nested_subexpressions():
    regex = r"(\d{3,})outer begin(?P<inner_subexpression>(?:.{2})?)outer end\1[0-9]"
    se = (
        SuperExpressive()
            .capture
                .at_least(3).digit
            .end()
            .subexpression(first_layer_subexpression)
            .backreference(1)
            .range('0', '9')
    )

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern