from main import SuperExpressive


def test_optional():
    regex = r"\w?"
    se = SuperExpressive().optional.word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_zero_or_more():
    regex = r"\w*"
    se = SuperExpressive().zero_or_more.word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_zero_or_more_lazy():
    regex = r"\w*?"
    se = SuperExpressive().zero_or_more_lazy.word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_one_or_more():
    regex = r"\w+"
    se = SuperExpressive().one_or_more.word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_one_or_more_lazy():
    regex = r"\w+?"
    se = SuperExpressive().one_or_more_lazy.word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_exactly():
    regex = r"\w{4}"
    se = SuperExpressive().exactly(4).word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_at_least():
    regex = r"\w{4,}"
    se = SuperExpressive().at_least(4).word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_between():
    regex = r"\w{4,7}"
    se = SuperExpressive().between(4, 7).word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern


def test_between_lazy():
    regex = r"\w{4,7}?"
    se = SuperExpressive().between_lazy(4, 7).word

    assert regex == se.to_regex_string()
    assert regex == se.to_regex().pattern
