import streamlit as st
from orchestrator import Orchestrator
import base64

from components.refine_components import refinement_controls
from components.layer_panels import show_layer
from components.timeline import render_timeline


st.set_page_config(page_title="Agentic Peer Review System", layout="wide")

st.title("Agentic Peer Review System (Spectre Edition)")
st.caption("Refine.ink + Agentic Peer Review + Editorial AI + PDF Intelligence")

if "orch" not in st.session_state:
    st.session_state["orch"] = Orchestrator()

orch = st.session_state["orch"]

uploaded = st.file_uploader("Upload Manuscript PDF", type=["pdf"])

if uploaded:
    bdata = uploaded.read()
    b64 = "data:application/pdf;base64," + base64.b64encode(bdata).decode()

    text = orch.load_pdf(b64)
    st.success("PDF Loaded Successfully")
    st.text_area("Extracted Text Preview", text[:1500] + " ...", height=200)

    # ----- SEGMENT -----
    if st.button("Segment Manuscript"):
        sections = orch.segment()
        st.subheader("Detected Sections")
        st.json(sections)

    # ----- 7-LAYER ANALYSIS -----
    if st.button("Run 7-Layer Analysis"):
        analysis = orch.run_analysis()
        st.subheader("Layer Analysis Output")
        for layer, metrics in analysis.items():
            show_layer(layer, metrics)
        render_timeline(7)

    st.markdown("---")
    col1, col2 = st.columns(2)

    # ----- REFINE MODE -----
    with col1:
        st.header("Refine.ink Mode")
        level = refinement_controls()

        opts = ["full"]
        if orch.sections:
            opts += list(orch.sections.keys())

        sec_choice = st.selectbox("Select Section (optional)", opts)

        if st.button("Refine Text"):
            refined = orch.run_refinement(level, None if sec_choice == "full" else sec_choice)
            st.subheader("Refined Output")
            st.text_area("Refined Text", refined, height=300)

    # ----- SECTION REVIEW -----
    with col2:
        st.header("Section-by-Section Review")
        if orch.sections:
            tar = st.selectbox("Select Section for Review", list(orch.sections.keys()))
            if st.button("Generate Section Review"):
                out = orch.review_specific_section(tar)
                st.subheader("Section Review")
                st.write(out)
        else:
            st.info("Segment manuscript first.")

    st.markdown("---")
    col3, col4 = st.columns(2)

    # ----- CITATION INTEGRITY -----
    with col3:
        st.header("Citation Integrity Checker")
        reftext = st.text_area("Optional: Paste References Section", height=120)
        scope = st.selectbox("Check Scope", ["Full Manuscript"] + list(orch.sections or {}))

        if st.button("Run Citation Check"):
            sec = None if scope == "Full Manuscript" else scope
            report = orch.citation_review(section_name=sec, references_text=reftext)
            st.subheader("Citation Integrity Report")
            st.write(report)

    # ----- ARGUMENT MAP -----
    with col4:
        st.header("Argument Mapping")
        if orch.sections:
            tar = st.selectbox("Map Logic for Section", list(orch.sections.keys()))
            if st.button("Generate Argument Map"):
                amap = orch.argument_map(tar)
                st.subheader("Argument Map")
                st.write(amap)
        else:
            st.info("Segment manuscript first.")

    st.markdown("---")
    col5, col6 = st.columns(2)

    # ----- NOVELTY -----
    with col5:
        st.header("Novelty Assessment")
        if st.button("Assess Novelty"):
            nov = orch.novelty_assessment()
            st.subheader("Novelty Assessment")
            st.write(nov)

    # ----- PERSONA REVIEW -----
    with col6:
        st.header("Reviewer Personas")
        if orch.sections:
            sec = st.selectbox("Select Section for Persona Review", list(orch.sections.keys()))
            persona = st.selectbox("Choose Persona", [
                "strict",
                "friendly",
                "editor_in_chief",
                "methodologist",
                "policy_maker",
            ])
            if st.button("Run Persona Review"):
                hyp = orch.persona_section_review(sec, persona)
                st.subheader(f"Persona ({persona}) Review")
                st.write(hyp)

    st.markdown("---")

    # ----- PANEL REVIEW -----
    st.header("Reviewer Panel (Layer 6)")
    if st.button("Generate Reviewer Panel"):
        p = orch.reviewer_panel()
        st.write(p)

    # ----- EDITOR PACKET -----
    st.header("Editor Packet (Layer 7)")
    if st.button("Generate Editorial Bundle"):
        ed = orch.editor_bundle()
        st.json(ed)

    # ----- PDF PACKET -----
    st.markdown("---")
    st.header("Download Full Review Packet (PDF)")

    if st.button("Generate Review Packet PDF"):
        try:
            personas = ["strict", "friendly", "editor_in_chief"]
            pdf_path = orch.build_full_review_packet(
                manuscript_title="Manuscript",
                personas_selected=personas
            )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Review Packet PDF",
                    data=f,
                    file_name="review_packet.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"PDF Generation Error: {e}")

else:
    st.info("Upload a PDF to begin.")
