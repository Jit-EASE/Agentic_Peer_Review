import re

SECTION_PATTERNS = {
    "abstract": r"(abstract[\s\S]*?)(?=\n[a-z])",
    "introduction": r"(introduction[\s\S]*?)(?=\n[a-z])",
    "methods": r"(method[\s\S]*?)(?=\n[a-z])",
    "results": r"(results[\s\S]*?)(?=\n[a-z])",
    "discussion": r"(discussion[\s\S]*?)(?=\n[a-z])",
    "conclusion": r"(conclusion[\s\S]*?)$",
}

def segment_sections(text):
    sections = {}
    for key, pat in SECTION_PATTERNS.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            sections[key] = m.group(1)
    return sections
