from openai import OpenAI
client = OpenAI()

SECTION_GUIDANCE = {
    "abstract": "summarizes purpose, methods, results, and implications.",
    "introduction": "provides background, research gap, objectives.",
    "methods": "explains design, data, models, reproducibility.",
    "results": "presents findings objectively.",
    "discussion": "interprets findings, links to theory, implications.",
    "conclusion": "summarizes contributions and future work.",
}

def review_section(name, text):
    guideline = SECTION_GUIDANCE.get(name.lower(), "has academic purpose.")

    prompt = f"""
Review the '{name}' section.

1. Purpose
2. Strengths
3. Weaknesses
4. Suggestions
5. Paragraph critique
6. Optional rewritten version

This section typically {guideline}.

Text:
{text}
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1600,
        temperature=0.25
    )
    return r.choices[0].message.content
