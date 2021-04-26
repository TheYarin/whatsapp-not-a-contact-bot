from typing import Optional
import re

phone_regex = re.compile(r'^\+?[\d-]{1,15}$')

def format_phone_number(text: str) -> Optional[str]:
    tmp = text.replace(' ', '')

    if not phone_regex.match(tmp):
        return None

    if text.startswith('+'):
        tmp = re.sub(r'(^\+\d{1,3}-)0', r'\g<1>', tmp)
    else:
        tmp = ('972' + tmp[1:]) if tmp.startswith('0') else tmp
    
    formatted_phone_number = re.sub(r'[^\d]', '', tmp)

    if formatted_phone_number == '':
        return None

    return formatted_phone_number

def trim_with_message_if_too_long(text: str, max_size: int = 200) -> str:
    return text if len(text) <= max_size \
           else text[:max_size] + f'\n<Trimmed. Original length: {len(text)}>'