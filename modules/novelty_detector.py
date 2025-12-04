from openai import OpenAI
client = OpenAI()

def assess_novelty(abstract, intro):
    prompt = f"""
Assess novelty using abstract + intro.

Evaluate:
- Contribution type
- Originality
- Positioning
- Gap clarity
- Risks
- Strengthening suggestions

Abstract:
{abstract}

Introduction:
{intro}
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1200
    )
    return r.choices[0].message.content
