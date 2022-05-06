from typing import Optional
import re

phone_regex = re.compile(r'^\+?[()\d -]{1,18}$')

def format_phone_number(text: str) -> Optional[str]:
    def trim_junk_before_and_after_phone_number(s: str) -> str:
        tmp = s
        junk_before_phone_number_regex = r'^[^\d]*?((?:\+|\()?\d)'
        tmp = re.sub(junk_before_phone_number_regex, r'\g<1>', tmp)
        junk_after_phone_number_regex = r'[^\d]+$'
        tmp = re.sub(junk_after_phone_number_regex, '', tmp)

        return tmp

    tmp = trim_junk_before_and_after_phone_number(text)

    if not phone_regex.match(tmp):
        return None

    # Local american phone numbers ((213) 123-4567) are not supported
    if tmp.startswith('('):
        return None

    # Remove zero from +XXX-0XXXXXXXXX
    if tmp.startswith('+'):
        tmp = re.sub(r'(^\+\d{1,3}-)0', r'\g<1>', tmp)

    if tmp.startswith('00'):
        tmp = tmp[2:]
    elif tmp.startswith('0'):
        tmp = '972' + tmp[1:]
    
    formatted_phone_number = re.sub(r'[^\d]', '', tmp)

    if formatted_phone_number == '':
        return None

    return formatted_phone_number

def trim_with_message_if_too_long(text: str, max_size: int = 200) -> str:
    return text if len(text) <= max_size \
           else text[:max_size] + f'\n<Trimmed. Original length: {len(text)}>'