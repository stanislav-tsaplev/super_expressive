from main import SuperExpressive


def test_any_char():
    regex = r"."
    se = SuperExpressive()

    assert regex == se.any_char.to_regex_string()
    assert regex == se.any_char.to_regex().pattern


def test_whitespace_char():
    regex = r"\s"
    se = SuperExpressive()

    assert regex == se.whitespace_char.to_regex_string()
    assert regex == se.whitespace_char.to_regex().pattern


def test_non_whitespace_char():
    regex = r"\S"
    se = SuperExpressive()

    assert regex == se.non_whitespace_char.to_regex_string()
    assert regex == se.non_whitespace_char.to_regex().pattern


def test_digit():
    regex = r"\d"
    se = SuperExpressive()

    assert regex == se.digit.to_regex_string()
    assert regex == se.digit.to_regex().pattern


def test_non_digit():
    regex = r"\D"
    se = SuperExpressive()

    assert regex == se.non_digit.to_regex_string()
    assert regex == se.non_digit.to_regex().pattern


def test_word():
    regex = r"\w"
    se = SuperExpressive()

    assert regex == se.word.to_regex_string()
    assert regex == se.word.to_regex().pattern


def test_non_word():
    regex = r"\W"
    se = SuperExpressive()

    assert regex == se.non_word.to_regex_string()
    assert regex == se.non_word.to_regex().pattern


def test_word_boundary():
    regex = r"\b"
    se = SuperExpressive()

    assert regex == se.word_boundary.to_regex_string()
    assert regex == se.word_boundary.to_regex().pattern


def test_non_word_boundary():
    regex = r"\B"
    se = SuperExpressive()

    assert regex == se.non_word_boundary.to_regex_string()
    assert regex == se.non_word_boundary.to_regex().pattern


def test_new_line():
    regex = r"\n"
    se = SuperExpressive()

    assert regex == se.new_line.to_regex_string()
    assert regex == se.new_line.to_regex().pattern


def test_carriage_return():
    regex = r"\r"
    se = SuperExpressive()

    assert regex == se.carriage_return.to_regex_string()
    assert regex == se.carriage_return.to_regex().pattern


def test_tab():
    regex = r"\t"
    se = SuperExpressive()

    assert regex == se.tab.to_regex_string()
    assert regex == se.tab.to_regex().pattern


def test_null_byte():
    regex = r"\0"
    se = SuperExpressive()

    assert regex == se.null_byte.to_regex_string()
    assert regex == se.null_byte.to_regex().pattern
