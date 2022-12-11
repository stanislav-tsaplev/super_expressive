from typing import Any
from dataclasses import dataclass, field


@dataclass
class _SubOptions:
    namespace: str = ""
    ignore_flags: bool = True
    ignore_start_and_end: bool = True


@dataclass
class _Token:
    type: str
    value: Any | None = None
    
    name: str = ""
    index: int = 0
    times: int = 0

    quantifier_requires_group: bool = False
    contains_children: bool = False
    contains_child: bool = False


@dataclass
class _StackFrame:
    token: _Token
    quantifier: _Token | None = None
    elements: list[_Token] = field(default_factory=list)


def _as_type(type: str, options = {}):
    def _inner(value) -> _Token:
        return _Token(type, value, **options)
    return _inner

def _deferred_type(type: str, options = {}) -> _Token:
    type_fn = _as_type(type, options)
    return type_fn(type_fn)


@dataclass
class _Tokens:
    root = _as_type("root") (None)
    noop = _as_type("noop") (None)
    start_of_string = _as_type("start_of_string") (None)
    end_of_string = _as_type("end_of_string") (None)
    start_of_input = _as_type("start_of_input") (None)
    end_of_input = _as_type("end_of_input") (None)
    any_char = _as_type("any_char") (None)
    whitespace_char = _as_type("whitespace_char") (None)
    non_whitespace_char = _as_type("non_whitespace_char") (None)
    digit = _as_type("digit") (None)
    non_digit = _as_type("non_digit") (None)
    word = _as_type("word") (None)
    non_word = _as_type("non_word") (None)
    word_boundary = _as_type("word_boundary") (None)
    non_word_boundary = _as_type("non_word_boundary") (None)
    new_line = _as_type("new_line") (None)
    carriage_return = _as_type("carriage_return") (None)
    tab = _as_type("tab") (None)
    null_byte = _as_type("null_byte") (None)
    any_of_chars = _as_type("any_of_chars")
    anything_but_string = _as_type("anything_but_string")
    anything_but_chars = _as_type("anything_but_chars")
    anything_but_range = _as_type("anything_but_range")
    char = _as_type("char")
    range = _as_type("range")
    string = _as_type("string", { "quantifier_requires_group": True })
    named_backreference = lambda name: _deferred_type("named_backreference", { "name": name })
    backreference = lambda index: _deferred_type("backreference", { "index": index })
    capture = _deferred_type('capture', { "contains_children": True })
    subexpression = _as_type('subexpression', { "contains_children": True, "quantifier_requires_group": True })
    named_capture = lambda name: _deferred_type("named_capture", { "name": name, "contains_children": True })
    group = _deferred_type('group', { "contains_children": True })
    any_of = _deferred_type('any_of', { "contains_children": True })
    assert_ahead = _deferred_type('assert_ahead', { "contains_children": True })
    assert_not_ahead = _deferred_type('assert_not_ahead', { "contains_children": True })
    assert_behind = _deferred_type('assert_behind', { "contains_children": True })
    assert_not_behind = _deferred_type('assert_not_behind', { "contains_children": True })
    exactly = lambda times: _deferred_type("exactly", { "times": times, "contains_child": True })
    at_least = lambda times: _deferred_type("at_least", { "times": times, "contains_child": True })
    between = lambda x, y: _deferred_type("between", { "times": [x, y], "contains_child": True })
    between_lazy = lambda x, y: _deferred_type("between_lazy", { "times": [x, y], "contains_child": True })
    zero_or_more = _deferred_type("zero_or_more", { "contains_child": True })
    zero_or_more_lazy = _deferred_type("zero_or_more_lazy", { "contains_child": True })
    one_or_more = _deferred_type("one_or_more", { "contains_child": True })
    one_or_more_lazy = _deferred_type("one_or_more_lazy", { "contains_child": True })
    optional = _deferred_type("optional", { "contains_child": True })
