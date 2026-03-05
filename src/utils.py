import re

# String cleaning
def clean_strings(raw_string, type=''):
    str_clean =  raw_string.text.replace('\n', '')
    if type == 'age':
        return str_clean
    else:
        return re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', str_clean)

def remove_leading_chars(orig_str, remove_char):
    text = orig_str.lower()
    new_text = text.lstrip(remove_char)
    return new_text.strip()
