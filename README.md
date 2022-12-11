# SuperExpressive

This package is the Python port of the following JavaScript library: https://github.com/francisrstokes/super-expressive
<br/>

## Installation
```
pip install super_expressive
```
<br/>

## Example

The following example recognises and captures the value of a 16-bit hexadecimal number like `0xC0D3`.

```py
from super_expressive import SuperExpressive


my_regex = (
    SuperExpressive()
        .start_of_input
        .optional.string('0x')
        .capture
            .exactly(4).any_of
                .range('a', 'f')
                .range('a', 'f')
                .range('0', '9')
            .end()
        .end()
        .end_of_input
    .to_regex()
)

// Produces the following regular expression:
re.compile('^(?:0x)?([A-Fa-f0-9]{4})$')
```
<br/>

## API
**Legend:**

    [–] original, not supported
    [=] original, supported
    [≈] original, supported (slightly different syntax)
    [+] new, added

---

[–] **`.allow_multiple_matches`**

API compatibility stub.

Has been intended to use the `g` flag on the regular expression, which indicates that it should match multiple values when run on a string.

Python does not have a `g` flag, it implements this behavior at the pattern object method level.

**Example:**
```py
pattern = (
    SuperExpressive()
        .allow_multiple_matches
        .string("hello")
    .to_regex_string()
)
# 'hello'
```

---

[–] **`.sticky`**

API compatibility stub.

Has been intended to use the y flag on the regular expression, which indicates that it should create a stateful regular expression that can be resumed from the last match.

Python does not have a `y` flag.

**Example:**
```py
pattern = (
    SuperExpressive()
        .sticky
        .string("hello")
    .to_regex_string()
)
# 'hello'
```

---

[+] **`.ascii`**

Assumes ascii 'locale'.

Uses the `a` flag on the regular expression, which indicates that it should use only ascii characters matching.

You could use this flag when necessary, considering the default mode in Python 3 is the unicode mode.

**Example:**
```py
pattern = (
    SuperExpressive()
        .ascii
        .string("hello")
    .to_regex_string()
)
# '(?a)hello'
```
---

[=] **`.case_insensitive`**
- `.caseInsensitive`
- `.ignore_case`
- `.ignoreCase`

Ignores case.

Uses the `i` flag on the regular expression, which indicates that it should treat ignore the uppercase/lowercase distinction when matching.

*Warning: this produces a different regex syntax than the original one (Python, not JS).*

**Example:**
```py
pattern = (
    SuperExpressive()
        .case_insensitive
        .string("hello")
    .to_regex_string()
)
# '(?i)hello'
```
---

[=] **`.line_by_line`**
- `.lineByLine`
- `.multiline`

Makes anchors look for newline.

Uses the `m` flag on the regular expression, which indicates that it should treat the `.start_of_input` and `.end_of_input` markers as the start and end of lines.

*Warning: this produces a different regex syntax than the original one (Python, not JS).*

**Example:**
```py
pattern = (
    SuperExpressive()
        .line_by_line
        .string("hello")
    .to_regex_string()
)
# '(?m)hello'
```
---

[=] **`.single_line`**
- `.singleLine`
- `.dotall`

Makes dot match newline.

Uses the `s` flag on the regular expression, which indicates 
that the input should be treated as a single line, where the `.start_of_input` and `.end_of_input` markers explicitly mark the start and end of input, and `.any_char` also matches newlines.

*Warning: this produces a different regex syntax than the original one (Python, not JS).*

**Example:**
```py
pattern = (
    SuperExpressive()
        .single_line
        .string("hello")
    .to_regex_string()
)
# '(?s)hello'
```
---

[=] **`.unicode`**

Assumes unicode 'locale'.

Uses the `u` flag on the regular expression, which indicates 
that it should use full unicode matching.

Since unicode mode is the default in Python 3, there is no need for using this flag
(but you can use `.ascii` instead when necessary).

*Warning: this produces a different regex syntax than the original one (Python, not JS).*

**Example:**
```py
pattern = (
    SuperExpressive()
        .unicode
        .string("hello")
    .to_regex_string()
)
# '(?u)hello'
```
---

[=] **`.any_char`**
- `.anyChar`

Matches any single character.

When combined with `.single_line` (aka `.dotall`), it also matches newlines.

**Example:**
```py
pattern = (
    SuperExpressive()
        .any_char
    .to_regex_string()
)
# '.'
```
---

[=] **`.whitespace_char`**
- `.whitespaceChar`
- `.whitespace`

Matches any whitespace character, including the special whitespace characters: `\r`, `\n`, `\t`, `\f`, `\v`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .whitespace_char
    .to_regex_string()
)
# '\\s'
```
---

[=] **`.non_whitespace_char`**
- `.nonWhitespaceChar`
- `.non_whitespace`
- `.nonWhitespace`

Matches any non-whitespace character, excluding also the special whitespace characters: `\r`, `\n`, `\t`, `\f`, `\v`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .non_whitespace_char
    .to_regex_string()
)
# '\\S'
```
---

[=] **`.digit`**

Matches any digit from `0-9`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .digit
    .to_regex_string()
)
# '\\d'
```
---

[=] **`.non_digit`**
- `.nonDigit`

Matches any non-digit.

**Example:**
```py
pattern = (
    SuperExpressive()
        .non_digit
    .to_regex_string()
)
# '\\D'
```
---

[=] **`.word`**
- `.word_char`
- `.wordChar`

Matches any alpha-numeric (`a-z`, `A-Z`, `0-9`) characters, as well as `_`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .word
    .to_regex_string()
)
# '\\w'
```
---

[=] **`.non_word`**
- `.nonWord`
- `.non_word_char`
- `.nonWordChar`

Matches any non alpha-numeric (`a-z`, `A-Z`, `0-9`) characters, excluding `_` as well.

**Example:**
```py
pattern = (
    SuperExpressive()
        .non_word
    .to_regex_string()
)
# '\\W'
```
---

[=] **`.word_boundary`**
- `.wordBoundary`

Matches (without consuming any characters) immediately between a character matched by `.word` and a character not matched by `.word` (in either order).

**Example:**
```py
pattern = (
    SuperExpressive()
        .word_boundary
    .to_regex_string()
)
# '\\b'
```
---

[=] **`.non_word_boundary`**
- `.nonWordBoundary`

Matches (without consuming any characters) at the position between two characters matched by `.word`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .non_word_boundary
    .to_regex_string()
)
# '\\B'
```
---

[=] **`.new_line`**
- `.newLine`

Matches a `\n` character.

**Example:**
```py
pattern = (
    SuperExpressive()
        .new_line
    .to_regex_string()
)
# '\\n'
```
---

[=] **`.carriage_return`**
- `.carriageReturn`

Matches a `\r` character.

**Example:**
```py
pattern = (
    SuperExpressive()
        .new_line
    .to_regex_string()
)
# '\\r'
```
---

[=] **`.tab`**

Matches a `\t` character.

**Example:**
```py
pattern = (
    SuperExpressive()
        .tab
    .to_regex_string()
)
# '\\t'
```
---

[=] **`.null_byte`**
- `.nullByte`

Matches a `\\u0000` character (ASCII 0).

**Example:**
```py
pattern = (
    SuperExpressive()
        .null_byte
    .to_regex_string()
)
# '\\0'
```
---

[=] **`.char(c: str)`**

Matches the exact (single) character `c`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .char('.')
    .to_regex_string()
)
# '\\.'
```
---

[=] **`.string(s: str)`**

Matches the exact string (the sequential characters) `s`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .string("1+1")
    .to_regex_string()
)
# '1\\+1'
```
---

[=] **`.range(a: str|int, b: str|int)`**

Matches any character that falls between `a` and `b`.

Ordering is defined by a characters ASCII or unicode value.

**Example:**
```py
pattern = (
    SuperExpressive()
        .range(0, 9)
        .range('a', 'f')
    .to_regex_string()
)
# '[0-9][a-f]'
```
---

[=] **`.any_of`**
- `.anyOf`

Matches a choice between specified elements.

Needs to be finalised with `.end()` or `.over`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .any_of
            .char('-')
            .range(0, 9)
            .string("no")
        .end()
    .to_regex_string()
)
# '(?:no|[\\-0-9])'
```
---

[=] **`.group`**

Creates a non-capturing group of the proceeding elements.

Needs to be finalised with `.end()` or `.over`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .optional.group
            .char('-')
            .range(0, 9)
            .string("no")
        .end()
    .to_regex_string()
)
# '(?:\\-[0-9]no)?'
```
---

[=] **`.assert_ahead`**
- `.assertAhead`

Assert that the proceeding elements are found without consuming them.

Needs to be finalised with `.end()` or `.over`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .assert_ahead
            .range('a', 'f')
        .end()
        .range('a', 'z')
    .to_regex_string()
)
# '(?=[a-f])[a-z]'
```
---

[=] **`.assert_behind`**
- `.assertBehind`

Assert that the elements contained within are found immediately before this point in the string.

Needs to be finalised with `.end()` or `.over`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .assert_behind
            .range('a', 'f')
        .end()
        .range('a', 'z')
    .to_regex_string()
)
# '(?<=[a-f])[a-z]'
```
---

[=] **`.assert_not_ahead`**
- `.assertNotAhead`

Assert that the proceeding elements are not found without consuming them. 

Needs to be finalised with `.end()` or `.over`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .assert_not_ahead
            .range('a', 'f')
        .end()
        .range('a', 'z')
    .to_regex_string()
)
# '(?![a-f])[a-z]'
```
---

[=] **`.assert_not_behind`**
- `.assertNotBehind`

Assert that the elements contained within are not found immediately before this point in the string.

Needs to be finalised with `.end()` or `.over`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .assert_not_behind
            .range('a', 'f')
        .end()
        .range('a', 'z')
    .to_regex_string()
)
# '(?<![a-f])[a-z]'
```
---

[=] **`.any_of_chars(chars: str)`**
- `.anyOfChars(chars: str)`

Matches any of the characters in the provided string `chars`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .any_of_chars("aeiou")
        .any_of_chars("+-*/=")
    .to_regex_string()
)
# '[aeiou][\\+\\-\\*/=]'
```
---

[=] **`.anything_but_chars(chars: str)`**
- `.anythingButChars(chars: str)`

Matches any character, except any of those in the provided string `chars`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .anything_but_chars("aeiou")
        .anything_but_chars("+-*/=")
    .to_regex_string()
)
# '[^aeiou][^\\+\\-\\*/=]'
```
---

[=] **`.anything_but_range(a: str, b: str)`**
- `.anythingButRange(a: str, b: str)`

Matches any character, except those that would be captured by the range specified by `a` and `b`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .anything_but_range(0, 9)
        .anything_but_range('a', 'f')
    .to_regex_string()
)
# '[^0-9][^a-f]'
```
---

[=] **`.anything_but_string(s: str)`**
- `.anythingButString(s: str)`

Matches any string the same length as `s`, except the `s` itself (the sequential characters in `s`).

**Example:**
```py
pattern = (
    SuperExpressive()
        .anything_but_string("aeiou")
        .anything_but_string("+-*/=")
    .to_regex_string()
)
# '(?:(?!aeiou).{5})(?:(?!\\+\\-\\*/=).{5})'
```
---

[=] **`.capture`**

Creates a capture group for the proceeding elements.

Needs to be finalised with `.end()` or `.over`.

Can be later referenced with `.backreference(index)`.

**Example:**
```py
pattern = (
    SuperExpressive()
        .capture
            .string("prefix:")
            .range(0, 9)
            .char("-")
            .range('a', 'f')
        .end()
    .to_regex_string()
)
# '(prefix:[0-9]\\-[a-f])'
```
---

[=] **`.named_capture(name: str)`**
- `.namedCapture(name: str)`

Creates a named capture group for the proceeding elements.

Needs to be finalised with `.end()` or `.over`.

Can be later referenced with `.named_backreference(name)` or `.backreference(index)`.

*Warning: this produces a different regex syntax than the original one (Python, not JS).*

**Example:**
```py
pattern = (
    SuperExpressive()
        .named_capture("some_stuff")
            .string("prefix:")
            .range(0, 9)
            .char("-")
            .range('a', 'f')
        .end()
    .to_regex_string()
)
# '(?P<some_stuff>prefix:[0-9]\\-[a-f])'
```
---

[=] **`.backreference(index: int)`**
- `.backref(index: int)`

Matches exactly what was previously matched by a `.capture` or `.named_capture` using a positional index.

Note that regex indices start at 1, so the first capture group has index 1.

*Warning: this produces a different regex syntax than the original one (Python, not JS).*

**Example:**
```py
pattern = (
    SuperExpressive()
        .capture
            .string("prefix:")
            .range(0, 9)
            .char("-")
            .range('a', 'f')
        .end()
        .string("something else")
        .backreference(1)
    .to_regex_string()
)
# '(prefix:[0-9]\\-[a-f])something else\\1'
```
---

[=] **`.named_backreference(name: str)`**
- `.namedBackreference(name: str)`
- `.named_backref(name: str)`
- `.namedBackref(name: str)`

Matches exactly what was previously matched by a `.named_capture`.

*Warning: this produces a different regex syntax than the original one (Python, not JS).*

**Example:**
```py
pattern = (
    SuperExpressive()
        .named_capture("some_stuff")
            .string("prefix:")
            .range(0, 9)
            .char("-")
            .range('a', 'f')
        .end()
        .string("something else")
        .named_backreference("some_stuff")
    .to_regex_string()
)
# '(?P<some_stuff>prefix:[0-9]\\-[a-f])something else(?P=some_stuff)'
```
---

[=] **`.optional`**

Assert that the proceeding element may or may not be matched.

**Example:**
```py
pattern = (
    SuperExpressive()
        .optional.digit
    .to_regex_string()
)
# '\d?'
```
---

[=] **`.zero_or_more`**
- `.zeroOrMore`

Assert that the proceeding element may not be matched, or may be matched multiple times.

**Example:**
```py
pattern = (
    SuperExpressive()
        .zero_or_more.digit
    .to_regex_string()
)
# '\d*'
```
---

[=] **`.zero_or_more_lazy`**
- `.zeroOrMoreLazy`

Assert that the proceeding element may not be matched, or may be matched multiple times, but as few times as possible.

**Example:**
```py
pattern = (
    SuperExpressive()
        .zero_or_more_lazy.digit
    .to_regex_string()
)
# '\d*?'
```        
---

[=] **`.one_or_more`**
- `.oneOrMore`

Assert that the proceeding element may be matched once, or may be matched multiple times.

**Example:**
```py
pattern = (
    SuperExpressive()
        .one_or_more.digit
    .to_regex_string()
)
# '\d+'
```
---

[=] **`.one_or_more_lazy`**
- `.oneOrMoreLazy`

Assert that the proceeding element may be matched once, or may be matched multiple times, but as few times as possible.

**Example:**
```py
pattern = (
    SuperExpressive()
        .one_or_more_lazy.digit
    .to_regex_string()
)
# '\d+?'
```
---

[=] **`.exactly(n: int)`**

Assert that the proceeding element will be matched exactly `n` times.

**Example:**
```py
pattern = (
    SuperExpressive()
        .exactly(5).digit
    .to_regex_string()
)
# '\d{5}'
```
---

[=] **`.at_least(n: int)`**
- `.atLeast(n: int)`

Assert that the proceeding element will be matched at least `n` times.

**Example:**
```py
pattern = (
    SuperExpressive()
        .at_least(5).digit
    .to_regex_string()
)
# '\d{5,}'
```
---

[=] **`.between(x: int, y: int)`**

Assert that the proceeding element will be matched somewhere between `x` and `y` times.

**Example:**
```py
pattern = (
    SuperExpressive()
        .between(3, 5).digit
    .to_regex_string()
)
# '\d{3,5}'
```
---

[=] **`.between_lazy(x: int, y: int)`**
- `.betweenLazy(x: int, y: int)`

Assert that the proceeding element will be matched somewhere between `x` and `y` times, but as few times as possible.

**Example:**
```py
pattern = (
    SuperExpressive()
        .between(3, 5).digit
    .to_regex_string()
)
# '\d{3,5}?'
```
---

[+] **`.start_of_string`**
- `.startOfString`

Always assert the start of input string, regardless of using multiline mode (aka `.line_by_line`).

**Example:**
```py
pattern = (
    SuperExpressive()
        .start_of_string
        .string("hello")
    .to_regex_string()
)
# '\Ahello'
```
---

[+] **`.end_of_string`**
- `.endOfString`

Always assert the end of input string, regardless of using multiline mode (aka `.line_by_line`).

**Example:**
```py
pattern = (
    SuperExpressive()
        .string("hello")
        .end_of_string
    .to_regex_string()
)
# 'hello\Z'
```
---

[=] **`.start_of_input`**
- `.startOfInput`

Assert the start of input string, or the start of a line when multiline mode ( aka `.line_by_line`) is used.

**Example:**
```py
pattern = (
    SuperExpressive()
        .start_of_input
        .string("hello")
    .to_regex_string()
)
# '^hello'
```
---

[=] **`.end_of_input`**
- `.endOfInput`

Assert the end of input string, or the end of a line when multiline mode (aka `.line_by_line`) is used.

**Example:**
```py
pattern = (
    SuperExpressive()
        .string("hello")
        .end_of_input
    .to_regex_string()
)
# 'hello$'
```
---

[=] **`.end()`**

Closes the context of `.any_of`, `.group`, `.capture`, or `.assert_*`.

Requires parentheses when invoked (see also `.over`).

**Example:**
```py
pattern = (
    SuperExpressive()
        .string("prefix:")
        .capture
            .anyOf
                .range(0, 9)
                .char("-")
                .range('a', 'f')
                .string("something else")
            .end()
        .end()
    .to_regex_string()
)
# 'prefix:((?:something else|[0-9\\-a-f]))'
```
---

[+] **`.over`**

Closes the context of `.any_of`, `.group`, `.capture` or `.assert_*`.

Alias for `.end()`, but doesn't require parentheses.

**Example:**
```py
pattern = (
    SuperExpressive()
        .string("prefix:")
        .capture
            .anyOf
                .range(0, 9)
                .char("-")
                .range('a', 'f')
                .string("something else")
            .over
        .over
    .to_regex_string()
)
# 'prefix:((?:something else|[0-9\\-a-f]))'
```
---

[≈] **`.subexpression(expr: SuperExpressive, *, namespace: str = "", ignore_flags: bool = True, ignore_start_and_end: bool = True)`**
- `.sub(expr, *, namespace="", ignore_flags=True, ignore_start_and_end=True)`

Matches another `SuperExpressive` instance inline. 

Can be used to create libraries, or to modularise you code.

**Example:**
```py
hex_number = SuperExpressive().one_or_more.any_of.range(0, 9).range('A', 'F').end()

pattern = (
    SuperExpressive()
        .subexpression(hex_number)
        .one_or_more.whitespace
        .optional.subexpression(hex_number)
    .to_regex_string()
)
# '[0-9A-F]+\\s+(?:[0-9A-F]+)?'
```

By default, flags and start/end of input markers are ignored, but can be explicitly turned on in the keyword parameters.
- `ignore_flags`: If set to true, any flags this subexpression specifies 
should be disregarded (default is `True`).

**Example:**
```py
hex_number = (
    SuperExpressive()
        .case_insensitive
        .one_or_more.any_of
            .range(0, 9)
            .range('A', 'F')
        .end()
)

pattern1 = (
    SuperExpressive()
        .subexpression(hex_number)
        .one_or_more.whitespace
        .optional.subexpression(hex_number)
    .to_regex_string()
)
# '[0-9A-F]+\\s+(?:[0-9A-F]+)?'

pattern2 = (
    SuperExpressive()
        .subexpression(hex_number, ignore_flags=False)
        .one_or_more.whitespace
        .optional.subexpression(hex_number)
    .to_regex_string()
)
# '(?i)[0-9A-F]+\\s+(?:[0-9A-F]+)?'
```

- `ignore_start_and_end`: If set to true, any `.start_of_input` / `.end_of_input` 
asserted in this subexpression specifies should be disregarded (default is `True`).

**Example:**
```py
hex_number = (
    SuperExpressive()
        .start_of_input
        .one_or_more.any_of
            .range(0, 9)
            .range('A', 'F')
        .end()
        .end_of_input
)

pattern1 = (
    SuperExpressive()
        .subexpression(hex_number)
        .one_or_more.whitespace
        .optional.subexpression(hex_number)
    .to_regex_string()
)
# '[0-9A-F]+\\s+(?:[0-9A-F]+)?'

pattern2 = (
    SuperExpressive()
        .subexpression(hex_number)
        .one_or_more.whitespace
        .optional.subexpression(hex_number, ignore_start_and_end=False)
    .to_regex_string()
)
# '[0-9A-F]+\\s+(?:^[0-9A-F]+$)?'
```

- `namespace`: A string namespace to use on all named capture groups in the subexpression, to avoid naming collisions with your own named groups (default is `""`).

**Example:**
```py
hex_number = (
    SuperExpressive()
        .named_capture("hex")
            .one_or_more.any_of
                .range(0, 9)
                .range('A', 'F')
            .end()
        .end()
        .named_backreference("hex")
)
#'(?P<hex>[0-9A-F]+)(?P=hex)'

pattern1 = (
    SuperExpressive()
        .subexpression(hex_number)
        .one_or_more.whitespace
        .optional.subexpression(hex_number, namespace="snd_")
    .to_regex_string()
)
# '(?P<hex>[0-9A-F]+)(?P=hex)\\s+(?:(?P<snd_hex>[0-9A-F]+)(?P=snd_hex))?'

pattern2 = (
    SuperExpressive()
        .named_capture("hex")
            .subexpression(hex_number, namespace="sub1_")
            .one_or_more.whitespace
            .optional.subexpression(hex_number, namespace="sub2_")
        .end()
        .named_backreference("hex")
    .to_regex_string()
)
# '(?P<hex>(?P<sub1_hex>[0-9A-F]+)(?P=sub1_hex)\\s+(?:(?P<sub2_hex>[0-9A-F]+)(?P=sub2_hex))?)(?P=hex)'

```
---

[=] **`.to_regex()`**
- `.toRegex()`

Outputs the regular expression pattern that this `SuperExpression` models.

---

[=] **`.to_regex_string()`**
- `.toRegexString()`
- `.to_string()`
- `.toString()`

Outputs a string representation of the regular expression that this `SuperExpression` models.
