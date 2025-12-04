from openai import OpenAI
client = OpenAI()

def refine_text(text, level="medium"):
    prompt = f"""
Rewrite this academic text with {level} refinement.
Preserve meaning, improve clarity, and enhance flow.

{text}
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.25,
    )
    return r.choices[0].message.content

def refine_document(text, level="medium"):
    return refine_text(text, level)
