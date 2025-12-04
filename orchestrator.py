from modules.pdf_loader import extract_pdf_text
from modules.text_segmenter import segment_sections
from modules.analysis_engine import analyze_layers
from modules.refine_engine import refine_text, refine_document
from modules.section_reviewer import review_section
from modules.citation_checker import check_citation_integrity
from modules.argument_mapper import map_argument_structure
from modules.novelty_detector import assess_novelty
from modules.persona_reviewer import persona_review
from modules.reviewer_panel import generate_panel_review
from modules.editor_module import generate_editor_packet
from modules.pdf_builder import generate_review_packet


class Orchestrator:

    def __init__(self):
        self.manuscript_text = None
        self.sections = None
        self.analysis = None

    def load_pdf(self, base64_pdf):
        self.manuscript_text = extract_pdf_text(base64_pdf)
        return self.manuscript_text

    def segment(self):
        if not self.manuscript_text:
            raise ValueError("Load PDF first.")
        self.sections = segment_sections(self.manuscript_text)
        return self.sections

    def run_analysis(self):
        if not self.manuscript_text:
            raise ValueError("Load manuscript first.")
        self.analysis = analyze_layers(self.manuscript_text)
        return self.analysis

    def run_refinement(self, level="medium", section=None):
        if section and self.sections and section in self.sections:
            return refine_text(self.sections[section], level)
        return refine_document(self.manuscript_text, level)

    def review_specific_section(self, section_name):
        if not self.sections:
            raise ValueError("Segment manuscript first.")
        if section_name not in self.sections:
            return "Section not found."
        return review_section(section_name, self.sections[section_name])

    def citation_review(self, section_name=None, references_text=None):
        text = (
            self.sections[section_name]
            if section_name and self.sections
            else self.manuscript_text
        )
        return check_citation_integrity(text, references_text or "")

    def argument_map(self, section_name):
        if not self.sections:
            raise ValueError("Segment first.")
        return map_argument_structure(section_name, self.sections[section_name])

    def novelty_assessment(self):
        abstr = self.sections.get("abstract", "") if self.sections else ""
        intro = self.sections.get("introduction", "") if self.sections else ""
        base = abstr or intro or self.manuscript_text[:1500]
        return assess_novelty(base, intro)

    def persona_section_review(self, section_name, persona):
        return persona_review(section_name, self.sections[section_name], persona)

    def reviewer_panel(self):
        if not self.analysis:
            raise ValueError("Run analysis first.")
        return generate_panel_review(self.analysis)

    def editor_bundle(self):
        return generate_editor_packet(self.analysis)

    def build_full_review_packet(self, manuscript_title, personas_selected):
        # Section reviews
        sec_reviews = {
            sec: review_section(sec, txt) for sec, txt in self.sections.items()
        }

        # Argument maps
        arg_maps = {
            sec: map_argument_structure(sec, txt) for sec, txt in self.sections.items()
        }

        # Persona reviews
        persona_map = {
            f"{persona} — {sec}": persona_review(sec, txt, persona)
            for persona in personas_selected
            for sec, txt in self.sections.items()
        }

        # Citation & novelty
        citation_report = check_citation_integrity(self.manuscript_text)
        novelty_report = self.novelty_assessment()

        # Panel & editorial
        panel = self.reviewer_panel()
        editor = self.editor_bundle()

        return generate_review_packet(
            manuscript_title,
            self.analysis,
            sec_reviews,
            citation_report,
            arg_maps,
            novelty_report,
            persona_map,
            panel,
            editor,
        )
