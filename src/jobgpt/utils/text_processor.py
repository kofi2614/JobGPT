import re
import string
def process_text_for_html(text):
    text = re.sub(f'[^{re.escape(string.printable)}]', '', text)
    return text