import re

def clean_strings(raw_string):
    str_clean =  raw_string.text.replace('\n', '')
    return re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', str_clean)

def remove_leading_chars(orig_str, remove_char):
    text = orig_str.lower()
    new_text = text.lstrip(remove_char)
    return new_text.strip()