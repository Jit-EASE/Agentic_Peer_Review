import streamlit as st

def render_timeline(stage):
    st.markdown("### Review Timeline")
    for i in range(1, 8):
        if stage == i:
            st.markdown(f"**➡️ Stage {i} (Active)**")
        else:
            st.markdown(f"Stage {i}")
