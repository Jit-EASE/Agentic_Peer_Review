# modules/analysis_engine.py
import re

def clamp(v, low=0, high=100): return max(low, min(high, v))

def keyword_score(text, keywords):
    hits = sum(1 for kw in keywords if kw.lower() in text)
    return clamp(int(100 * hits / len(keywords)))

def analyze_layers(text):
    lower = text.lower()
    tokens = re.findall(r"\b\w+\b", lower)
    word_count = len(tokens)

    analysis = {}

    # ------- LAYER 1 -------
    structure_kw = ["abstract","introduction","method","results","conclusion"]
    structural_hits = sum(1 for kw in structure_kw if kw in lower)
    score1 = clamp(int(word_count/40) + structural_hits*10, 10, 100)
    analysis["layer1"] = {
        "score": score1,
        "summary": f"Word count {word_count}. Section hits={structural_hits}/5."
    }

    # ------- LAYER 2 -------
    integrity_kw = ["sample size","random","robustness","bias","outlier"]
    score2 = keyword_score(lower, integrity_kw)
    analysis["layer2"] = {
        "score": score2,
        "summary": f"Integrity score {score2}/100."
    }

    # ------- LAYER 3 -------
    methods_kw = ["ols","fixed effects","panel","did","heteroskedasticity"]
    score3 = keyword_score(lower, methods_kw)
    analysis["layer3"] = {
        "score": score3,
        "summary": f"Method score {score3}/100."
    }

    # ------- LAYER 4 -------
    sentences = re.split(r"[.!?]+", text)
    lens = [len(re.findall(r"\b\w+\b", s)) for s in sentences if s.strip()]
    avg_len = sum(lens)/len(lens) if lens else 0
    score4 = clamp(int(100 - abs(avg_len-22) * 2), 20, 100)
    analysis["layer4"] = {
        "score": score4,
        "summary": f"Avg sentence length {avg_len:.1f} words."
    }

    # ------- LAYER 5 -------
    gov_kw = ["ethics","gdpr","data protection","consent","privacy"]
    score5 = keyword_score(lower, gov_kw)
    analysis["layer5"] = {
        "score": score5,
        "summary": f"Governance score {score5}/100."
    }

    # ------- LAYER 6 -------
    panel_score = clamp((score1 + score2 + score3 + score4 + score5)//5)
    analysis["layer6"] = {
        "score": panel_score,
        "summary": f"Panel aggregated score {panel_score}."
    }

    # ------- LAYER 7 -------
    verdict = (
        "Accept with minor revisions" if panel_score > 80 else
        "Major revisions required" if panel_score > 60 else
        "Reject"
    )

    analysis["layer7"] = {
        "score": panel_score,
        "summary": f"Editorial verdict: {verdict}."
    }

    return analysis
