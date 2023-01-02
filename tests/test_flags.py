from ..src.super_expressive import SuperExpressive


def test_empty_regex():
    regex = r"(?:)"
    se = SuperExpressive()

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


# Since the lack of the 'g' regex flag in Python, 
# the corresponding test is omitted.


def test_multiline_flag():
    regex = r"(?m)(?:)"
    se = SuperExpressive()

    assert regex == se.line_by_line.to_regex_string()
    assert regex == se.line_by_line.to_regex().pattern

    assert regex == se.multiline.to_regex_string()
    assert regex == se.multiline.to_regex().pattern


def test_case_insensitive_flag():
    regex = r"(?i)(?:)"
    se = SuperExpressive()

    assert regex == se.case_insensitive.to_regex_string()
    assert regex == se.case_insensitive.to_regex().pattern

    assert regex == se.ignore_case.to_regex_string()
    assert regex == se.ignore_case.to_regex().pattern


# Since the lack of the 'y' regex flag in Python,
# the corresponding test is omitted


# Unicode mode is applied in Python 3 regexes by default,
# better use ASCII flag when needed
def test_unicode_flag():
    regex = r"(?u)(?:)"
    se = SuperExpressive()

    assert regex == se.unicode.to_regex_string()
    assert regex == se.unicode.to_regex().pattern


def test_ascii_flag():
    regex = r"(?a)(?:)"
    se = SuperExpressive()

    assert regex == se.ascii.to_regex_string()
    assert regex == se.ascii.to_regex().pattern


def test_singleline_flag():
    regex = r"(?s)(?:)"
    se = SuperExpressive()

    assert regex == se.single_line.to_regex_string()
    assert regex == se.single_line.to_regex().pattern

    assert regex == se.dotall.to_regex_string()
    assert regex == se.dotall.to_regex().pattern


def test_multiple_flags():
    regex = r"(?ais)(?:)"
    se = SuperExpressive().case_insensitive.ascii.single_line

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_stub_flags():
    regex = r"(?u)(?:)"
    se = SuperExpressive().allowMultipleMatches.unicode.sticky

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern