import re

def clean_strings(raw_string):
    str_clean =  raw_string.text.replace('\n', '')
    return re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', str_clean)

