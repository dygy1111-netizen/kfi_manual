import streamlit as st
from pathlib import Path

# ------------------ 페이지 기본 설정 ------------------ #
st.set_page_config(
    page_title="1.1 안전거리",
    page_icon="📘",
    layout="wide"
)

# ------------------ 스타일 ------------------ #
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    color: #003366;
    margin-bottom: 1.2em;
}
.section-title {
    color: #003366;
    font-weight: 700;
    margin-top: 1.2em;
    font-size: 1.1rem;
}
table {width: 100%; border-collapse: collapse; margin-top: 0.5em;}
table th, table td {border: 1px solid #d0d7e2; padding: 8px; text-align: center;}
table th {background-color: #005bac; color: white;}
table tr:nth-child(even){background-color:#f0f4f8;}
</style>
""", unsafe_allow_html=True)

# ------------------ 절대 경로로 Markdown 불러오기 ------------------ #
# 현재 파일(pages/1_안전거리.py)의 상위 폴더(kfi_manual)까지 이동
BASE_DIR = Path(__file__).parent.parent
file_path = BASE_DIR / "data" / "안전거리.md"    # ⚠️ 실제 파일명과 일치해야 함

# 디버그용 출력 (필요 없으면 삭제 가능)
st.write("🔍 찾는 경로:", file_path)
st.write("🔍 존재 여부:", file_path.exists())

# ------------------ 페이지 제목 ------------------ #
st.markdown('<div class="title">1.1 안전거리</div>', unsafe_allow_html=True)

# ------------------ 내용 출력 ------------------ #
if file_path.exists():
    # Markdown 파일 내용 표시
    st.markdown(file_path.read_text(encoding="utf-8"), unsafe_allow_html=False)
else:
    st.error("❗ '안전거리.md' 파일을 찾을 수 없습니다.\n"
             "data 폴더와 파일 이름을 다시 확인해주세요.")
