from typing import Optional
import re

def format_phone_number(text: str) -> Optional[str]:
    phone_regex = re.compile(r'^\+?[\d-]{1,15}$')
    
    if not phone_regex.match(text):
        return None

    tmp = text

    if text.startswith('+'):
        tmp = re.sub(r'(^\+\d{1,3}-)0', r'\g<1>', tmp)
    else:
        tmp = ('972' + tmp[1:]) if tmp.startswith('0') else tmp
    
    formatted_phone_number = re.sub(r'[^\d]', '', tmp)

    if formatted_phone_number == '':
        return None

    return formatted_phone_number