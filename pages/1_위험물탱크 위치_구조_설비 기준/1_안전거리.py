import streamlit as st
from pathlib import Path

st.set_page_config(page_title="1.1 안전거리", page_icon="📘", layout="wide")

st.markdown("## 1.1 안전거리")

file_path = Path("data/안전거리.md")
if file_path.exists():
    st.markdown(file_path.read_text(encoding="utf-8"), unsafe_allow_html=False)
else:
    st.error("❗ 안전거리.md 파일을 찾을 수 없습니다.")
