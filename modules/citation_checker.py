import re
from openai import OpenAI
client = OpenAI()

def extract_intext(text):
    apa = re.findall(r"\(([A-Z][A-Za-z]+.*?\d{4})\)", text)
    num = re.findall(r"\[(\d+.*?)\]", text)
    return {"apa": apa, "numeric": num}

def check_citation_integrity(text, refs):
    stats = extract_intext(text)
    prompt = f"""
Evaluate citation integrity.

In-text citations:
{stats}

Reference list:
{refs}

Analyse:
1. Missing citations
2. Under/over citation
3. Style consistency
4. Improvements
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=900
    )
    return r.choices[0].message.content
