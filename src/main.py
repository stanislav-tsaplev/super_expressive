import re
from copy import deepcopy

from .base import _StackFrame, _Token, _Tokens, _SubOptions


class RegexError(ValueError):
    pass


_special_chars = r"\.^$|?*+()[]{}-"
def _escape_special(s: str):
    return "".join(
        ('\\' if char in _special_chars else '') + char
        for char in s
    )

_named_group_regex = re.compile(r"(?i)^[a-z]+\w*$")
_quantifier_table = {
  "one_or_more": "+",
  "one_or_more_lazy": "+?",
  "zero_or_more": "*",
  "zero_or_more_lazy": "*?",
  "optional": "?",
  "exactly": lambda times: f"{{{times}}}",
  "at_least": lambda times: f"{{{times},}}",
  "between": lambda times: f"{{{times[0]},{times[1]}}}",
  "between_lazy": lambda times: f"{{{times[0]},{times[1]}}}?",
}


class SuperExpressive:
    def __init__(self) -> None:
        self.has_defined_start = False
        self.has_defined_end = False
        
        self.flags: dict[str, bool] = { ch: False for ch in "aimsu" }

        self.stack: list[_StackFrame] = [_StackFrame(_Tokens.root)]
        self.named_groups: list[str] = []
        self.total_capture_groups = 0

    @property
    def ascii(self):
        """Assumes ascii 'locale'. \n
        Uses the `a` flag on the regular expression, which indicates 
        that it should use only ascii characters matching.
        """
        next = deepcopy(self)
        next.flags['a'] = True
        return next

    @property
    def case_insensitive(self) -> "SuperExpressive":
        """Ignores case. \n
        Uses the `i` flag on the regular expression, which indicates 
        that it should treat ignore the uppercase/lowercase distinction when matching.
        """
        next = deepcopy(self)
        next.flags['i'] = True
        return next

    @property
    def line_by_line(self) -> "SuperExpressive":
        """Makes anchors look for newline. \n
        Uses the `m` flag on the regular expression, which indicates 
        that it should treat the `.start_of_input` and `.end_of_input` markers 
        as the start and end of lines.
        """
        next = deepcopy(self)
        next.flags['m'] = True
        return next

    @property
    def single_line(self) -> "SuperExpressive":
        """Makes dot match newline. \n
        Uses the `s` flag on the regular expression, which indicates 
        that the input should be treated as a single line, 
        where the `.start_of_input` and `.end_of_input` markers explicitly mark 
        the start and end of input, and `.any_char` also matches newlines.
        """
        next = deepcopy(self)
        next.flags['s'] = True
        return next

    @property
    def unicode(self) -> "SuperExpressive":
        """Assumes unicode 'locale'. \n
        Uses the `u` flag on the regular expression, which indicates 
        that it should use full unicode matching. 
        Since unicode mode is the default in Python 3, there is need to use this flag
        (but you can use `.ascii` instead when necessary).
        """
        next = deepcopy(self)
        next.flags['u'] = True
        return next

    @property
    def any_char(self) -> "SuperExpressive":
        """Matches any single character. \n
        When combined with `.single_line` (`.dotall`), it also matches newlines.
        """
        return self.__match_element(_Tokens.any_char)

    @property
    def whitespace_char(self) -> "SuperExpressive":
        """Matches any whitespace character, \n
        including the special whitespace characters: `\\r`, `\\n`, `\\t`, `\\f`, `\\v`.
        """
        return self.__match_element(_Tokens.whitespace_char)

    @property
    def non_whitespace_char(self) -> "SuperExpressive":
        """Matches any non-whitespace character, \n
        excluding also the special whitespace characters: `\\r`, `\\n`, `\\t`, `\\f`, `\\v`.
        """
        return self.__match_element(_Tokens.non_whitespace_char)

    @property
    def digit(self) -> "SuperExpressive":
        """Matches any digit from `0-9`"""
        return self.__match_element(_Tokens.digit)

    @property
    def non_digit(self) -> "SuperExpressive":
        """Matches any non-digit"""
        return self.__match_element(_Tokens.non_digit)

    @property
    def word(self) -> "SuperExpressive":
        """Matches any alpha-numeric (`a-z`, `A-Z`, `0-9`) characters, as well as `_`.
        """
        return self.__match_element(_Tokens.word)

    @property
    def non_word(self) -> "SuperExpressive":
        """Matches any non alpha-numeric (`a-z`, `A-Z`, `0-9`) characters, excluding `_` as well.
        """
        return self.__match_element(_Tokens.non_word)

    @property
    def word_boundary(self) -> "SuperExpressive":
        """Matches (without consuming any characters) 
        immediately between a character matched by `.word` 
        and a character not matched by `.word` (in either order).
        """
        return self.__match_element(_Tokens.word_boundary)

    @property
    def non_word_boundary(self) -> "SuperExpressive":
        """Matches (without consuming any characters) 
        at the position between two characters matched by `.word`.
        """
        return self.__match_element(_Tokens.non_word_boundary)

    @property
    def new_line(self) -> "SuperExpressive":
        """Matches a `\\n` character"""
        return self.__match_element(_Tokens.new_line)

    @property
    def carriage_return(self) -> "SuperExpressive":
        """Matches a `\\r` character"""
        return self.__match_element(_Tokens.carriage_return)

    @property
    def tab(self) -> "SuperExpressive":
        """Matches a `\\t` character"""
        return self.__match_element(_Tokens.tab)

    @property
    def null_byte(self) -> "SuperExpressive":
        """Matches a `\\u0000` character (ASCII 0)"""
        return self.__match_element(_Tokens.null_byte)

    def char(self, c: str) -> "SuperExpressive":
        """Matches the exact (single) character `c`."""

        if not isinstance(c, str):
            raise RegexError(f"c must be a string (got {c})")
        if len(c) != 1:
            raise RegexError(f"char() can only be called with a single character (got {c})")

        next = deepcopy(self)
        current_frame = next.stack[-1]
        current_frame.elements.append(
            next.__apply_quantifier(_Tokens.char(_escape_special(c)))
        )

        return next

    def string(self, s: str) -> "SuperExpressive":
        """Matches the exact string (the sequential characters) `s`."""

        if not isinstance(s, str):
            raise RegexError(f"s must be a string (got {s})")
        if len(s) == 0:
            raise RegexError("s cannot be an empty string")

        next = deepcopy(self)
        element_value = (
            _Tokens.string(_escape_special(s))
            if len(s) > 1
            else _Tokens.char(_escape_special(s))
        )
        current_frame = next.stack[-1]
        current_frame.elements.append(
            next.__apply_quantifier(element_value)
        )

        return next

    def range(self, a: str|int, b: str|int) -> "SuperExpressive":
        """Matches any character that falls between `a` and `b`. \n
        Ordering is defined by a characters ASCII or unicode value."""

        a, b = str(a), str(b)

        if len(a) != 1:
            raise RegexError(f"a must be a single character or number (got {a})")
        if len(b) != 1:
            raise RegexError(f"a must be a single character or number (got {b})")
        if a[0] >= b[0]:
            raise RegexError(
                f"a must have a smaller character value than b "
                f"(a = {a[0]}, b = {b[0]})"
            )

        next = deepcopy(self)
        element_value = _Tokens.range(value=(a, b))
        current_frame = next.stack[-1]
        
        current_frame.elements.append(
            next.__apply_quantifier(element_value)
        )

        return next

    @property
    def assert_ahead(self) -> "SuperExpressive":
        """Assert that the proceeding elements are found without consuming them. \n
        Needs to be finalised with `.end()` or `.over`.
        """
        return self.__frame_creating_element(_Tokens.assert_ahead)

    @property
    def assert_behind(self) -> "SuperExpressive":
        """Assert that the elements contained within are found 
        immediately before this point in the string. \n
        Needs to be finalised with `.end()` or `.over`.
        """
        return self.__frame_creating_element(_Tokens.assert_behind)

    @property
    def assert_not_ahead(self) -> "SuperExpressive":
        """Assert that the proceeding elements are not found without consuming them. \n
        Needs to be finalised with `.end()` or `.over`.
        """
        return self.__frame_creating_element(_Tokens.assert_not_ahead)

    @property
    def assert_not_behind(self) -> "SuperExpressive":
        """Assert that the elements contained within are not found 
        immediately before this point in the string. \n
        Needs to be finalised with `.end()` or `.over`.
        """
        return self.__frame_creating_element(_Tokens.assert_not_behind)

    @property
    def group(self) -> "SuperExpressive":
        """Creates a non-capturing group of the proceeding elements. \n
        Needs to be finalised with `.end()` or `.over`.
        """
        return self.__frame_creating_element(_Tokens.group)

    @property
    def any_of(self) -> "SuperExpressive":
        """Matches a choice between specified elements. \n
        Needs to be finalised with `.end()` or `.over`.
        """
        return self.__frame_creating_element(_Tokens.any_of)

    def any_of_chars(self, chars: str) -> "SuperExpressive":
        """Matches any of the characters in the provided string `chars`."""

        if not isinstance(chars, str):
            raise RegexError(f"chars must be a string (got {chars})")
        if len(chars) <= 0:
            raise RegexError("chars must have at least one character")

        next = deepcopy(self)

        element_value = _Tokens.any_of_chars(_escape_special(chars))
        current_frame = next.stack[-1]

        current_frame.elements.append(
            next.__apply_quantifier(element_value)
        )
        return next

    def anything_but_chars(self, chars: str) -> "SuperExpressive":
        """Matches any character, except any of those in the provided string `chars`."""
        
        if not isinstance(chars, str):
            raise RegexError(f"chars must be a string (got {chars})")
        if len(chars) <= 0:
            raise RegexError("chars must have at least one character")

        next = deepcopy(self)

        element_value = _Tokens.anything_but_chars(_escape_special(chars))
        current_frame = next.stack[-1]

        current_frame.elements.append(
            next.__apply_quantifier(element_value)
        )
        return next

    def anything_but_range(self, a: str, b: str) -> "SuperExpressive":
        """Matches any character, except those that would be captured 
        by the range specified by `a` and `b`.
        """

        a, b = str(a), str(b)

        if len(a) != 1:
            raise RegexError(f"a must be a single character or number (got {a})")
        if len(b) != 1:
            raise RegexError(f"b must be a single character or number (got {b})")
        if a[0] >= b[0]:
            raise RegexError(
                f"a must have a smaller character value than b "
                f"(a = ${a[0]}, b = ${b[0]})"
            )

        next = deepcopy(self)

        element_value = _Tokens.anything_but_range(value=(a, b))
        current_frame = next.stack[-1]

        current_frame.elements.append(
            next.__apply_quantifier(element_value)
        )
        return next

    def anything_but_string(self, s: str) -> "SuperExpressive":
        """Matches any string the same length as `s`, 
        except the `s` itself (the characters sequentially defined in `s`).
        """

        if not isinstance(s, str):
            raise RegexError(f"s must be a string (got {s})")
        if len(s) <= 0:
            raise RegexError("s must have least one character")

        next = deepcopy(self)

        # crooked solution: _escape_special() invokation 
        # moved from here to anything_but_string() method 
        # due to the need to get the length of an unescaped string

        # element_value = _Tokens.anything_but_string(_escape_special(s))
        element_value = _Tokens.anything_but_string(s)
        current_frame = next.stack[-1]

        current_frame.elements.append(
            next.__apply_quantifier(element_value)
        )
        return next

    @property
    def capture(self) -> "SuperExpressive":
        """Creates a capture group for the proceeding elements. \n
        Needs to be finalised with `.end()` or `.over`. \n
        Can be later referenced with `.backreference(index)`.
        """
        next = deepcopy(self)

        new_frame = _StackFrame(_Tokens.capture)
        next.stack.append(new_frame)
        next.total_capture_groups += 1

        return next

    def backreference(self, index: int) -> "SuperExpressive":
        """Matches exactly what was previously matched by a `.capture` or `.named_capture` 
        using a positional index. \n
        Note that regex indices start at 1, so the first capture group has index 1.
        """
        if not isinstance(index, int):
            raise RegexError("index must be a number")
        if not 0 < index <= self.total_capture_groups:
            raise RegexError(
                f"invalid index {index}. "
                f"There are {self.total_capture_groups} capture groups on this SuperExpression"
            )
        return self.__match_element(_Tokens.backreference(index))

    def named_capture(self, name: str) -> "SuperExpressive":
        """Creates a named capture group for the proceeding elements. \n
        Needs to be finalised with `.end()` or `.over`. \n
        Can be later referenced with `.named_backreference(name)` or `.backreference(index)`.
        """
        next = deepcopy(self)
        new_frame = _StackFrame(_Tokens.named_capture(name))

        next.__track_named_group(name)
        next.stack.append(new_frame)
        next.total_capture_groups += 1

        return next

    def named_backreference(self, name: str) -> "SuperExpressive":
        """Matches exactly what was previously matched by a `.named_capture`."""
        if name not in self.named_groups:
            raise RegexError(f"no capture group called '{name}' exists (create one with .named_capture())")
        return self.__match_element(_Tokens.named_backreference(name))

    @property
    def optional(self) -> "SuperExpressive":
        """Assert that the proceeding element may or may not be matched."""
        return self.__quantifier_element("optional")

    @property
    def zero_or_more(self) -> "SuperExpressive":
        """Assert that the proceeding element may not be matched, or may be matched multiple times."""
        return self.__quantifier_element("zero_or_more")

    @property
    def zero_or_more_lazy(self) -> "SuperExpressive":
        """Assert that the proceeding element may not be matched, or may be matched multiple times, 
        but as few times as possible.
        """
        return self.__quantifier_element("zero_or_more_lazy")

    @property
    def one_or_more(self) -> "SuperExpressive":
        """Assert that the proceeding element may be matched once, or may be matched multiple times."""
        return self.__quantifier_element("one_or_more")

    @property
    def one_or_more_lazy(self) -> "SuperExpressive":
        """Assert that the proceeding element may be matched once, or may be matched multiple times, 
        but as few times as possible.
        """
        return self.__quantifier_element("one_or_more_lazy")

    def exactly(self, n: int) -> "SuperExpressive":
        """Assert that the proceeding element will be matched exactly `n` times."""

        if not isinstance(n, int) or n <= 0:
            raise RegexError(f"n must be a positive integer (got {n})")

        next = deepcopy(self)
        current_frame = next.stack[-1]
        if current_frame.quantifier:
            raise RegexError(
                f"cannot quantify regular expression with 'exactly' "
                f"because it's already being quantified with '{current_frame.quantifier.type}'"
            )
        current_frame.quantifier = _Tokens.exactly(n)
        return next

    def at_least(self, n: int) -> "SuperExpressive":
        """Assert that the proceeding element will be matched at least `n` times."""

        if not isinstance(n, int) or n <= 0:
            raise RegexError(f"n must be a positive integer (got {n})")

        next = deepcopy(self)
        current_frame = next.stack[-1]
        if current_frame.quantifier:
            raise RegexError(
                f"cannot quantify regular expression with 'at_least' "
                f"because it's already being quantified with '{current_frame.quantifier.type}'"
            )
        current_frame.quantifier = _Tokens.at_least(n)
        return next

    def between(self, x: int, y: int) -> "SuperExpressive":
        """Assert that the proceeding element will be matched somewhere between `x` and `y` times."""

        if not isinstance(x, int) or x < 0:
            raise RegexError(f"x must be an integer (got {x})")
        if not isinstance(y, int) or y <= 0:
            raise RegexError(f"y must be an integer greater than 0 (got {y})")
        if x >= y:
            raise RegexError(f"x must be less than y (x = {x}, y = {y})")

        next = deepcopy(self)
        current_frame = next.stack[-1]
        if current_frame.quantifier:
            raise RegexError(
                f"cannot quantify regular expression with 'between' "
                f"because it's already being quantified with '{current_frame.quantifier.type}'"
            )
        current_frame.quantifier = _Tokens.between(x, y)
        return next

    def between_lazy(self, x: int, y: int) -> "SuperExpressive":
        """Assert that the proceeding element will be matched somewhere between `x` and `y` times, 
        but as few times as possible.
        """
        if not isinstance(x, int) or x < 0:
            raise RegexError(f"x must be an integer (got {x})")
        if not isinstance(y, int) or y <= 0:
            raise RegexError(f"y must be an integer greater than 0 (got {y})")
        if x >= y:
            raise RegexError(f"x must be less than y (x = {x}, y = {y})")

        next = deepcopy(self)
        current_frame = next.stack[-1]
        if current_frame.quantifier:
            raise RegexError(
                f"cannot quantify regular expression with 'between_lazy' "
                f"because it's already being quantified with '{current_frame.quantifier.type}'"
            )
        current_frame.quantifier = _Tokens.between_lazy(x, y)
        return next
        
    @property
    def start_of_string(self) -> "SuperExpressive":
        """Always assert the start of input string, regardless of using multiline mode (`.line_by_line`)."""

        next = deepcopy(self)
        next.stack[-1].elements.append(_Tokens.start_of_string)
        return next

    @property
    def end_of_string(self) -> "SuperExpressive":
        """Always assert the end of input string, regardless of using multiline mode (`.line_by_line`)."""

        next = deepcopy(self)
        next.stack[-1].elements.append(_Tokens.end_of_string)
        return next

    @property
    def start_of_input(self) -> "SuperExpressive":
        """Assert the start of input string, or the start of a line 
        when multiline mode (`.line_by_line`) is used.
        """

        if self.has_defined_start:
            raise RegexError("This regex already has a defined start of input")
        if self.has_defined_end:
            raise RegexError("Cannot define the start of input after the end of input")

        next = deepcopy(self)
        next.has_defined_start = True
        next.stack[-1].elements.append(_Tokens.start_of_input)
        return next

    @property
    def end_of_input(self) -> "SuperExpressive":
        """Assert the end of input string, or the end of a line 
        when multiline mode (`.line_by_line`) is used.
        """

        if self.has_defined_end:
            raise RegexError("This regex already has a defined end of input")

        next = deepcopy(self)
        next.has_defined_end = True
        next.stack[-1].elements.append(_Tokens.end_of_input)
        return next

    def end(self) -> "SuperExpressive":
        """Closes the context of `.any_of`, `.group`, `.capture`, or `.assert_*`.\n
        Requires parentheses when invoked (see also `.over`).
        """
        if len(self.stack) <= 1:
            raise RegexError("Cannot call end while building the root expression")

        next = deepcopy(self)

        old_frame = next.stack.pop()
        assert old_frame.token.value

        current_frame = next.stack[-1]
        current_frame.elements.append(
            next.__apply_quantifier(old_frame.token.value(old_frame.elements))
        )
        return next

    def subexpression(self, 
        expr: "SuperExpressive",
        *,
        namespace: str = "",
        ignore_flags: bool = True,
        ignore_start_and_end: bool = True
    ) -> "SuperExpressive":
        """Matches another SuperExpressive instance inline. 
        Can be used to create libraries, or to modularise you code. \n
        By default, flags and start/end of input markers are ignored, 
        but can be explicitly turned on in the keyword parameters. \n

        `namespace`: A string namespace to use on all named capture groups in the subexpression, 
        to avoid naming collisions with your own named groups (default is ''). \n
        `ignore_flags`: If set to true, any flags this subexpression specifies 
        should be disregarded (default is True). \n
        `ignore_start_and_end`: If set to true, any `.start_of_input`/`.end_of_input` 
        asserted in this subexpression specifies should be disregarded (default is True).
        """
        if not isinstance(expr, SuperExpressive):
            raise RegexError("expr must be a SuperExpressive instance")
        if len(expr.stack) != 1:
            raise RegexError(
                "Cannot call subexpression with a not yet fully specified regex object.\n"
                f"(Try adding a .end() call to match the '{expr.stack[-1].token.type}' "
                "on the subexpression)"
            )

        options = _SubOptions(
            namespace=namespace,
            ignore_flags=ignore_flags,
            ignore_start_and_end=ignore_start_and_end
        )

        sub_next = deepcopy(expr)
        next = deepcopy(self)

        additional_capture_groups = { "count": 0 }
            
        sub_frame = sub_next.stack[-1]
        sub_frame.elements = [
            SuperExpressive.__merge_subexpression(
                element, options, next, additional_capture_groups
            )
            for element in sub_frame.elements
        ]

        next.total_capture_groups += additional_capture_groups["count"]

        if not options.ignore_flags:
            for flag, enabled in sub_next.flags.items():
                next.flags[flag] = next.flags[flag] or enabled

        current_frame = next.stack[-1]
        current_frame.elements.append(
            next.__apply_quantifier(_Tokens.subexpression(sub_frame.elements))
        )
               
        return next

    def to_regex(self) -> re.Pattern:
        """Outputs the regular expression pattern that this SuperExpression models."""

        pattern = self.__get_regex_pattern()
        flags = self.__get_regex_flags()
        if flags:
            pattern = f"(?{flags}){pattern}"
        return re.compile(pattern)

    def to_regex_string(self) -> str:
        """Outputs a string representation of the regular expression that this SuperExpression models."""

        pattern = self.__get_regex_pattern()
        flags = self.__get_regex_flags()
        if flags:
            return f"(?{flags}){pattern}"
        else:
            return pattern

    def __apply_quantifier(self, element: _Token) -> _Token:
        current_frame = self.stack[-1]
        if current_frame.quantifier:
            assert current_frame.quantifier.value

            wrapped = current_frame.quantifier.value(element)
            current_frame.quantifier = None
            return wrapped
        return element

    def __frame_creating_element(self, type_fn) -> "SuperExpressive":
        next = deepcopy(self)
        new_frame = _StackFrame(type_fn)
        next.stack.append(new_frame)
        return next

    def __match_element(self, type_fn) -> "SuperExpressive":
        next = deepcopy(self)
        current_frame = next.stack[-1]
        current_frame.elements.append(
            next.__apply_quantifier(type_fn)
        )
        return next

    def __quantifier_element(self, type_fn_name: str) -> "SuperExpressive":
        next = deepcopy(self)
        current_frame = next.stack[-1]

        if current_frame.quantifier:
            raise RegexError(
                f"cannot quantify regular expression with '{type_fn_name}' "
                f"because it's already being quantified with '{current_frame.quantifier.type}'"
            )
        current_frame.quantifier = _Tokens.__dict__[type_fn_name]
        return next

    def __track_named_group(self, name: str) -> None:
        if not isinstance(name, str):
            raise RegexError(f"name must be a string (got {name})")
        if len(name) == 0:
            raise RegexError("name must be at least one character")
        if name in self.named_groups:
            raise RegexError(f"cannot use {name} again for a capture group")
        if not _named_group_regex.match(name):
            raise RegexError(f"name '{name}' is not valid (only letters, numbers, and underscores)")
        
        self.named_groups.append(name)

    @staticmethod
    def _is_fusable(element: _Token) -> bool:
        return element.type in ("range", "char", "any_of_chars")

    @staticmethod
    def _fuse_elements(elements: list[_Token]) -> tuple[str, list[_Token]]:
        def _get_value(element: _Token):
            if element.type in ("char", "any_of_chars"):
                assert isinstance(element.value, str)
                return element.value
            else:
                assert element.value
                return f"{element.value[0]}-{element.value[1]}"

        fusables = [element for element in elements if SuperExpressive._is_fusable(element)]
        rest = [element for element in elements if not SuperExpressive._is_fusable(element)]

        fused = "".join(_get_value(element) for element in fusables)
        return fused, rest

    @staticmethod
    def __merge_subexpression(
        element: _Token,
        options: _SubOptions,
        parent: "SuperExpressive",
        capture_groups_counter: dict[str, int]
    ) -> _Token:
        next_element = deepcopy(element)
        
        if next_element.contains_child:
            assert next_element.value
            next_element.value = SuperExpressive.__merge_subexpression(
                next_element.value, options, parent, capture_groups_counter
            )
        elif next_element.contains_children:
            assert next_element.value
            next_element.value = [
                SuperExpressive.__merge_subexpression(
                    element, options, parent, capture_groups_counter
                )
                for element in next_element.value
            ]

        match next_element.type:
            case "backreference":
                next_element.index += parent.total_capture_groups

            case "capture":
                capture_groups_counter["count"] += 1
            
            case "named_capture":
                group_name = (
                    f"{options.namespace}{next_element.name}"
                    if options.namespace
                    else next_element.name
                )

                parent.__track_named_group(group_name)
                next_element.name = group_name

            case "named_backreference":
                next_element.name = (
                    f"{options.namespace}{next_element.name}"
                    if options.namespace
                    else next_element.name
                )

            case 'start_of_input':
                if options.ignore_start_and_end:
                    return _Tokens.noop

                if parent.has_defined_start:
                    raise RegexError(
                        "The parent regex already has a defined start of input. "
                        "You can ignore a subexpressions start_of_input/end_of_input markers "
                        "with the ignore_start_and_end option"
                    )

                if parent.has_defined_end:
                    raise RegexError(
                        "The parent regex already has a defined end of input. "
                        "You can ignore a subexpressions start_of_input/end_of_input markers "
                        "with the ignore_start_and_end option"
                    )

                parent.has_defined_start = True

            case "end_of_input":
                if options.ignore_start_and_end:
                    return _Tokens.noop

                if parent.has_defined_end:
                    raise RegexError(
                        "The parent regex already has a defined end of input. "
                        "You can ignore a subexpressions start_of_input/end_of_input markers "
                        "with the ignore_start_and_end option"
                    )
                
                parent.has_defined_end = True

        return next_element

    @staticmethod
    def __evaluate(element: _Token) -> str:
        match element.type:
            case "noop": return ""

            case "any_char": return "."
            case "whitespace_char": return "\\s"
            case "non_whitespace_char": return "\\S"
            case "digit": return "\\d"
            case "non_digit": return "\\D"
            case "word": return "\\w"
            case "non_word": return "\\W"
            case "word_boundary": return "\\b"
            case "non_word_boundary": return "\\B"
            case "new_line": return "\\n"
            case "carriage_return": return "\\r"
            case "tab": return "\\t"
            case "null_byte": return "\\0"

            case "start_of_string": return "\\A"
            case "end_of_string": return "\\Z"
            case "start_of_input": return "^"
            case "end_of_input": return "$"

            case "string": 
                assert isinstance(element.value, str)
                return element.value

            case "char": 
                assert isinstance(element.value, str)
                return element.value

            case "range": 
                assert element.value
                return f"[{element.value[0]}-{element.value[1]}]"

            case "anything_but_range": 
                assert element.value
                return f"[^{element.value[0]}-{element.value[1]}]"

            case "any_of_chars": 
                return f"[{element.value}]"

            case "anything_but_chars": 
                return f"[^{element.value}]"

            case "anything_but_string":
                assert element.value
                s = element.value
                # crooked solution: _escape_special() invokation 
                # moved here from anything_but_string() method 
                # due to the need to get the length of an unescaped string
                return f"(?:(?!{_escape_special(s)}).{{{len(s)}}})"

            case "backreference": 
                return f"\\{element.index}"

            case "named_backreference": 
                return f"(?P={element.name})"

            case ("optional" | "zero_or_more" | "zero_or_more_lazy" | 
                                "one_or_more" | "one_or_more_lazy"):
                assert element.value
                inner = SuperExpressive.__evaluate(element.value)
                with_group = (
                    f"(?:{inner})"
                    if element.value.quantifier_requires_group
                    else inner
                )
                symbol = _quantifier_table[element.type]
                return f"{with_group}{symbol}"

            case "between_lazy" | "between" | "at_least" | "exactly":
                assert element.value
                inner = SuperExpressive.__evaluate(element.value)
                with_group = (
                    f"(?:{inner})"
                    if element.value.quantifier_requires_group
                    else inner
                )
                return f"{with_group}{_quantifier_table[element.type](element.times)}"

            case "capture":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return f"({''.join(evaluated)})"

            case "named_capture":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return f"(?P<{element.name}>{''.join(evaluated)})"

            case "assert_ahead":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return f"(?={''.join(evaluated)})"

            case "assert_behind":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return f"(?<={''.join(evaluated)})"

            case "assert_not_ahead":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return f"(?!{''.join(evaluated)})"

            case "assert_not_behind":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return f"(?<!{''.join(evaluated)})"

            case "any_of":
                assert element.value
                fused, rest = SuperExpressive._fuse_elements(element.value)
                if not rest:
                    return f"[{fused}]"

                evaluated_rest = [SuperExpressive.__evaluate(element) for element in rest]
                separator = '|' if evaluated_rest and fused else ""
                return (
                    f"(?:{'|'.join(evaluated_rest)}{separator}"
                    f"{f'[{fused}]' if fused else ''})"
                )

            case "group":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return f"(?:{''.join(evaluated)})"

            case "subexpression":
                assert element.value
                evaluated = [SuperExpressive.__evaluate(child) for child in element.value]
                return ''.join(evaluated)

            case _: 
                raise RegexError(f"Can'_Tokens process unsupported element type: {element.type}")


    def __get_regex_pattern(self) -> str:
        if len(self.stack) != 1:
            current_frame = self.stack[-1]
            raise RegexError(
            "Cannot compute the value of a not yet fully specified regex object.\n"
            f"(Try adding a .end() call to match the '{current_frame.token.type}')"
        )
        
        current_frame = self.stack[-1]
        evaluated = [SuperExpressive.__evaluate(element) for element in current_frame.elements]
        pattern = "".join(evaluated)

        return pattern if pattern != "" else "(?:)"

    def __get_regex_flags(self) -> str:
        flags = [
            name if is_on else ""
            for name, is_on in self.flags.items()
        ]

        return "".join(sorted(flags))

    # aliases and stubs

    ignoreCase = ignore_case = caseInsensitive = case_insensitive
    multiline = lineByLine = line_by_line
    dotall = singleLine = single_line

    anyChar = any_char
    whitespace = whitespaceChar = whitespace_char
    nonWhitespace = non_whitespace = nonWhitespaceChar = non_whitespace_char
    nonDigit = non_digit
    wordChar = word_char = word
    nonWordChar = non_word_char = nonWord = non_word
    wordBoundary = word_boundary
    nonWordBoundary = non_word_boundary
    newLine = new_line
    carriageReturn = carriage_return
    nullByte = null_byte

    assertAhead = assert_ahead
    assertBehind = assert_behind
    assertNotAhead = assert_not_ahead
    assertNotBehind = assert_not_behind

    backref = backreference
    namedCapture = named_capture
    namedBackref = named_backref = namedBackreference = named_backreference

    anyOf = any_of
    anyOfChars = any_of_chars
    anythingButChars = anything_but_chars
    anythingButRange = anything_but_range
    anythingButString = anything_but_string

    zeroOrMore = zero_or_more
    zeroOrMoreLazy = zero_or_more_lazy
    oneOrMore = one_or_more
    oneOrMoreLazy = one_or_more_lazy
    atLeast = at_least
    betweenLazy = between_lazy

    startOfString = start_of_string
    endOfString = end_of_string
    startOfInput = start_of_input
    endOfInput = end_of_input

    sub = subexpression

    toRegex = to_regex
    toString = to_string = toRegexString = to_regex_string

    @property
    def over(self) -> "SuperExpressive":
        """Closes the context of `.any_of`, `.group`, `.capture` or `.assert_*`.\n
        Alias for `.end()`, but doesn't require parentheses.
        """
        return self.end()

    @property
    def allowMultipleMatches(self) -> "SuperExpressive":
        """API compatibility stub. \n
        Has been intended to use the `g` flag on the regular expression, which indicates that 
        it should match multiple values when run on a string. \n
        Python does not have a `g` flag, it implements this behavior at the pattern object method level.
        """
        return self

    @property
    def sticky(self) -> "SuperExpressive":
        """API compatibility stub. \n
        Has been intended to use the y flag on the regular expression, which indicates that 
        it should create a stateful regular expression that can be resumed from the last match.
        Python does not have a `y` flag.
        """
        return self
