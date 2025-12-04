from openai import OpenAI
client = OpenAI()

def map_argument_structure(name, text):
    prompt = f"""
Map argument structure for section '{name}'.

Include:
- Claims
- Evidence
- Assumptions
- Logical flow
- Gaps
- Reorganisation suggestions

Text:
{text}
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    return r.choices[0].message.content
