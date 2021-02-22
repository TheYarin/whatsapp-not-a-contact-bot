import re

from src.helpers import trim_with_message_if_too_long

too_long_regex = re.compile(r'\n<Trimmed. Original length: \d+>$', flags=re.RegexFlag.IGNORECASE)

def test_sanity():
    assert trim_with_message_if_too_long(txt := '+972-50-123456789') == txt

def test_too_long():
    assert too_long_regex.search(trim_with_message_if_too_long('@' * ((limit := 200) + 1), limit))

def test_text_exactly_on_limit():
    assert trim_with_message_if_too_long(txt := '@' * (limit := 200), limit) == txt

def test_slightly_less_than_limit():
    assert trim_with_message_if_too_long(txt := '@' * ((limit := 200) - 1), limit) == txt