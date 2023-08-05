import re
import string
import html

def process_text(text):
    text = re.sub(r"(['`′‘’]{2})", "", text)
    text = re.sub("([{}])".format("".join(["̀", "́", "̃", "̣", "̧"])), "", text)
    uncommon = r"([˜¿ð½¡²\x89\x93\xad\x8d◊�\x81\x7f¦\ufeffþ©…¯±°¹²³])"
    text = re.sub(uncommon, "", text)
    text = re.sub(r'([«»"„“”″\uee52])', "", text)
    text = re.sub(r"([`′‘’])", "", text)
    text = re.sub(r"([–—−])", "-", text)
    text = re.sub(r"([·…•․])", "", text)
    text = re.sub(r"([\u2002\u2003\u2005])", "", text)
    text = re.sub(r"([\ue484])", "", text)
    text = re.sub(r"([\uf230])", "", text)
    text = re.sub(r"([◆●⌑◼☐★⋅])", "", text)    
    text = re.sub(f'[^{re.escape(string.printable)}]', '', text)
    text = re.sub(r' {4,}', '\n', text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = text.replace("\n", "\\n")
    # text = html.escape(text).encode('unicode_escape').decode()
    return text