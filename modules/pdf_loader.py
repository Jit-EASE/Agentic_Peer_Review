import base64
import io
from PyPDF2 import PdfReader

def extract_pdf_text(contents):
    header, encoded = contents.split(",")
    decoded = base64.b64decode(encoded)
    reader = PdfReader(io.BytesIO(decoded))

    text = ""
    for p in reader.pages:
        text += (p.extract_text() or "") + "\n"
    return text.strip()
