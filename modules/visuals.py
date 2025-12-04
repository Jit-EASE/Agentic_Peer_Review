import tempfile
import matplotlib.pyplot as plt

def build_layer_score_chart(layer_analysis):
    layers = [k.upper() for k in layer_analysis]
    scores = [int(v["score"]) for v in layer_analysis.values()]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(layers, scores)
    ax.set_ylim(0, 100)
    ax.set_title("7-Layer Scores")
    ax.tick_params(axis="x", rotation=45)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.tight_layout()
    fig.savefig(tmp.name, dpi=150)
    plt.close(fig)
    return tmp.name

def build_section_length_chart(sections):
    names = list(sections.keys())
    lens = [len(v.split()) for v in sections.values()]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(names, lens)
    ax.set_title("Section Lengths")
    ax.tick_params(axis="x", rotation=45)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.tight_layout()
    fig.savefig(tmp.name, dpi=150)
    plt.close(fig)
    return tmp.name
