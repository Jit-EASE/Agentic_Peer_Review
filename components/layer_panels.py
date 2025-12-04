import streamlit as st

def show_layer(layer, metrics):
    st.markdown(f"### **{layer.upper()}**")
    st.write("Score:", metrics["score"])
    st.write(metrics["summary"])
