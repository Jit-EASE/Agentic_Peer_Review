import streamlit as st

def refinement_controls():
    return st.selectbox("Refinement Level", ["light", "medium", "heavy"])
