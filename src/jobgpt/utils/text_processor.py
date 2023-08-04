import re
import string
import html

def process_text_for_html(text):
    text = re.sub(f'[^{re.escape(string.printable)}]', '', text)
    text = html.escape(text).encode('unicode_escape').decode()
    return text