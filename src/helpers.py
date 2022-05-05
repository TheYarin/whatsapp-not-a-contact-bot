from typing import Optional
import re

phone_regex = re.compile(r'^\+?[\d-]{1,15}$')

def format_phone_number(text: str) -> Optional[str]:
    tmp = text.replace(' ', '')
    ALLOWED_CHARS_REGEX = r'+\d'
    tmp = re.sub(f'^[^{ALLOWED_CHARS_REGEX}]+', '', tmp)
    tmp = re.sub(f'[^{ALLOWED_CHARS_REGEX}]+$', '', tmp)

    if not phone_regex.match(tmp):
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