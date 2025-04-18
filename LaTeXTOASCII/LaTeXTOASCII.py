import re
from pylatexenc.latex2text import LatexNodes2Text

# Map of Unicode math symbols to ASCII equivalents
unicode_to_ascii = {
    '≤': '<=',
    '≥': '>=',
    '≠': '!=',
    '≈': '~=',
    '→': '->',
    '∞': 'infinity',
    'π': 'pi',
    '∑': 'sum',
    '−': '-',   # minus (U+2212) to hyphen-minus
    '×': '*',
    '÷': '/',
    '°': ' deg',
    '∫': 'int',
    '√': 'sqrt',
    '≃': '~=',
}

# Function to convert Unicode to ASCII equivalents
def replace_unicode_with_ascii(text):
    for uni, ascii_val in unicode_to_ascii.items():
        text = text.replace(uni, ascii_val)
    return text

# Function to remove extra spaces but keep LaTeX commands intact
def remove_extra_spaces(text):
    # This regex will match spaces that are not part of LaTeX control sequences like \left, \right, etc.
    text = re.sub(r'(?<!\\)(\s+)', ' ', text)  # Replace any consecutive spaces with a single space
    text = re.sub(r'(?<=\\)(\s+)', '', text)  # Remove spaces after a backslash
    return text

f = open("expressions.txt", "r")
out = open("output.txt", "w")

for x in f:
    x = x.strip()
    if not x:
        continue
    print("LaTeX Equation: ", x)
    text = LatexNodes2Text().latex_to_text(x)
    text = replace_unicode_with_ascii(text)
    text = remove_extra_spaces(text).strip()  # Stripping unnecessary spaces here
    print("ASCII Equation: ", text)
    out.write(text + "\n")
    
print("OUTPUT SAVED TO: OUTPUT.TXT")
f.close()
out.close()