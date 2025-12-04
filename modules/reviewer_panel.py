from openai import OpenAI
client = OpenAI()

def generate_panel_review(analysis):
    prompt = f"""
Simulate a 3-reviewer panel using analysis:

{analysis}

Produce:
- Reviewer A notes
- Reviewer B notes
- Reviewer C notes
- Ensemble verdict
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return r.choices[0].message.content
