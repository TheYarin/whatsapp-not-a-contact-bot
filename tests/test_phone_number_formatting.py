from src.helpers import format_phone_number

# def test_invalid_phone_number_1(): # Removing this test for now because I'm not sure about how should the phone number's length be limited.
#     assert format_phone_number('+972-50-123456789') is None

def test_invalid_phone_number_2():
    assert format_phone_number("' and 1=1 --") is None

def test_invalid_phone_number_3():
    assert format_phone_number('') is None

def test_invalid_phone_number_4():
    assert format_phone_number('jibberish') is None

def test_invalid_phone_number_5():
    assert format_phone_number('+972-50-1234567 +972-50-1234567') is None

def test_invalid_phone_number_6():
    assert format_phone_number('+972-50+1234567') is None

def test_invalid_phone_number_7():
    assert format_phone_number('+---') is None

def test_invalid_phone_number_6_padding_supported():
    assert format_phone_number(' +972-50-1234567') == '972501234567'

def test_international_phone_number_1():
    assert format_phone_number('+972-50-1234567') == '972501234567'

def test_international_phone_number_2():
    assert format_phone_number('+972-050-1234567') == '972501234567'

def test_international_phone_number_3():
    assert format_phone_number('+1-50-1234567') == '1501234567'

def test_local_phone_number_no_dashes():
    assert format_phone_number('0501234567') == '972501234567'

def test_local_phone_number_with_all_dashes():
    assert format_phone_number('050-123-4567') == '972501234567'

def test_local_phone_number_with_some_dashes():
    assert format_phone_number('050-1234567') == '972501234567'

def test_international_number_with_no_dashes():
    assert format_phone_number('+972501234567') == '972501234567'

def test_already_formatted_number():
    assert format_phone_number('972501234567') == '972501234567'

def test_american_phone_number_1_unsupported():
    assert format_phone_number('(213) 123-4567') is None

def test_american_phone_number_2_supported():
    assert format_phone_number('+1 213 123 4567') == '12131234567'

def test_american_phone_number_3_unsupported():
    assert format_phone_number('(213) 123-42-53 ext. 1234') is None

def test_american_phone_number_4_supported():
    assert format_phone_number('+1 (123)-456-7890') == '11234567890'

def test_short_number():
    assert format_phone_number('166') == '166' # I am not happy with this one, but I'm mentioning this case here for completeness

def test_nozero_local_number():
    assert format_phone_number('50-123-4567') == '501234567' # I am not happy with this one, but I'm mentioning this case here for completeness

def test_international_number_containing_space():
    assert format_phone_number('972 52-123-4567') == '972521234567'

def test_international_number_with_zero_at_the_start_of_the_country_code():
    assert format_phone_number('+04912345678') == '04912345678' # Not sure this is the desired behavior, change if necessary

def test_weird_number_that_caught_me_by_surprise():
    assert format_phone_number('1800-123-456') == '1800123456'

def test_annoying_invisible_character(): # That little bitch showed up a few times.
    assert format_phone_number('\u200e0501234567') == '972501234567'

def test_annoying_invisible_character2(): # That little bitch showed up, too.
    assert format_phone_number('\u200f0501234567') == '972501234567'

def test_number_accompanied_by_junk():
    assert format_phone_number('hello hello +972 50-1234567 oops I forgot some text here') == '972501234567'

def test_number_accompanied_by_junk_2():
    assert format_phone_number('hello (not a number yet +) hello +1 50-1234567 oops I forgot some text here') == '1501234567'

def test_international_number_preceeded_by_two_pluses():
    assert format_phone_number('++1 50-1234567') == '1501234567'

def test_two_phone_numbers_accompanied_by_junk():
    assert format_phone_number("hello +1 50-1234567 oops I forgot some text here and also +04912345678 that's the second number") is None

def test_international_number_starting_with_two_zeros():
    assert format_phone_number('00357-12345678') == '35712345678'