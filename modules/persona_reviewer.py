from openai import OpenAI
client = OpenAI()

PERSONAS = {
    "strict": "You are a strict reviewer at a top-tier journal.",
    "friendly": "You are supportive, constructive, positive.",
    "editor_in_chief": "You are the Editor-in-Chief evaluating strategic fit.",
    "methodologist": "You evaluate methods, identification, econometrics.",
    "policy_maker": "You evaluate real-world policy relevance.",
}

def persona_review(section, text, persona):
    intro = PERSONAS.get(persona, PERSONAS["strict"])
    prompt = f"""
{intro}

Review section '{section}'.

Include:
- Overview
- Strengths
- Weaknesses
- Detailed comments
- Recommendation

Text:
{text}
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1400
    )
    return r.choices[0].message.content
