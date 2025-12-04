from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import tempfile
import datetime

from modules.visuals import build_layer_score_chart, build_section_length_chart


def _section(story, title, content, styles):
    story.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(content.replace("\n", "<br/>"), styles["BodyText"]))
    story.append(Spacer(1, 0.3 * inch))


def generate_review_packet(
    title,
    layer_analysis,
    section_reviews,
    citation_report,
    argument_maps,
    novelty_report,
    persona_reviews,
    panel_review,
    editor_packet,
):
    styles = getSampleStyleSheet()
    story = []

    # Cover
    story.append(Paragraph("<b>Agentic Editorial Review Packet</b>", styles["Title"]))
    story.append(Paragraph(f"Manuscript: <b>{title}</b>", styles["Heading3"]))
    story.append(Paragraph(f"Generated: {datetime.datetime.now()}", styles["BodyText"]))
    story.append(PageBreak())

    # Visual charts
    chart1 = build_layer_score_chart(layer_analysis)
    chart2 = build_section_length_chart(section_reviews)

    story.append(Paragraph("<b>Visual Summary</b>", styles["Heading2"]))
    story.append(Image(chart1, width=400, height=200))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Image(chart2, width=400, height=200))
    story.append(PageBreak())

    # Layers
    _section(story, "7-Layer Analysis", str(layer_analysis), styles)

    for sec, rev in section_reviews.items():
        _section(story, f"Section Review — {sec}", rev, styles)
        story.append(PageBreak())

    _section(story, "Citation Integrity", citation_report, styles)
    story.append(PageBreak())

    for sec, amap in argument_maps.items():
        _section(story, f"Argument Map — {sec}", amap, styles)
        story.append(PageBreak())

    _section(story, "Novelty Assessment", novelty_report, styles)
    story.append(PageBreak())

    for persona, text in persona_reviews.items():
        _section(story, f"Persona Review: {persona}", text, styles)
        story.append(PageBreak())

    _section(story, "Reviewer Panel", panel_review, styles)
    _section(story, "Editorial Summary", str(editor_packet), styles)

    # Output
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp.name, pagesize=A4)
    doc.build(story)

    return tmp.name
