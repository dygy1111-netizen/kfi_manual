import streamlit as st
import os, glob
from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

# ✅ 페이지 설정
st.set_page_config(page_title="위험물탱크 E-매뉴얼",
                   page_icon="📘",
                   layout="centered")   # ← wide 대신 centered

# ---------- 공통 CSS ---------- #
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}
.title-container { text-align: center; margin-top: 30px; margin-bottom: 20px; }
.main-title { font-size: 2.0rem; font-weight: 800; color: #222222; line-height: 1.4; }
.sub-title  { font-size: 2.0rem; font-weight: 800; color: #444444; line-height: 1.4; }
.guide-text { text-align: center; font-size: 1.1rem; margin-top: 10px; line-height: 1.6; color: #555555; }

.menu-box {
    border: 2px solid #d9e6f2;
    background-color: #f8fbff;
    border-radius: 12px;
    padding: 1.2em;
    margin-top: 1.2em;
}
.menu-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #003366;
    margin-bottom: 0.8em;
    display: flex;
    align-items: center;
}
.menu-title .emoji { margin-right: 0.4em; font-size: 1.4rem; }
.stButton button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac;
    color: white;
    border: none;
    padding: 0.7em;
    font-size: 1rem;
    font-weight: 600;
}
.stButton button:hover { background-color: #0072e0; }

.section-title { color:#003366; font-weight:700; margin-top:1.2em; font-size:1.1rem; }
table { width: 100%; border-collapse: collapse; margin-top: 0.5em; }
table th, table td { border: 1px solid #d0d7e2; padding: 8px; text-align: center; }
table th { background-color: #005bac; color: white; }
table tr:nth-child(even) { background-color: #f0f4f8; }

.back-btn button {
    background-color: #005bac;
    color: white;
    border-radius: 6px;
    padding: 0.6em 1em;
    border: none;
    font-weight: 600;
}
.back-btn button:hover { background-color: #0072e0; }
</style>
""", unsafe_allow_html=True)

# ---------- 이미지 탐색 함수 ---------- #
def find_image(name):
    exts = ['jpg','jpeg','png']
    for e in exts:
        path = f"images/{name}.{e}"
        if os.path.exists(path):
            return path
    for e in exts:
        g = glob.glob(f"images/{name}*.{e}")
        if g:
            return g[0]
    return None

# ---------- 목차 데이터 ---------- #
sections = {
    "1. 위험물탱크 위치, 구조 및 설비의 기준": [
        "1.1 안전거리",
        "1.2 보유공지",
        "1.3 표지 및 게시판",
        "1.4 외부구조 및 설비",
        "1.5 방유제",
        "1.6 옥외탱크저장소의 특례",
        "1.7 소화설비"
    ],
    "2. 안전성능검사": [
        "2.1 검사절차 및 확인사항",
        "2.2 검사방법",
        "2.3 참고사항"
    ],
    "3. 정기검사": [
        "3.1 검사절차 및 확인사항",
        "3.2 검사방법",
        "3.3 참고사항"
    ],
    "4. 부록": [
        "4.1 소방청 질의회신 및 협의사항",
        "4.2 검사관련 규격 및 기술지침",
        "4.3 검사 부적합 사례 및 실무 팁"
    ]
}

# ---------- PDF 생성 함수 ---------- #
def create_pdf(selected_items=None, with_images=False):
    """
    선택된 항목이 없으면 전체 출력.
    with_images=True → 이미지도 PDF에 추가(기본 False)
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    if selected_items:
        export_items = selected_items
    else:
        export_items = [sub for subs in sections.values() for sub in subs]

    for key in export_items:
        safe_name = key.replace(" ", "_").replace("/", "_")
        md_path = Path(f"contents/{safe_name}.md")
        img_path = find_image(safe_name)

        story.append(Paragraph(f"<b>{key}</b>", styles["Heading2"]))
        story.append(Spacer(1, 4*mm))

        if md_path.exists():
            with open(md_path, "r", encoding="utf-8") as f:
                text = f.read().replace("\n", "<br/>")
            story.append(Paragraph(text, styles["Normal"]))
        else:
            story.append(Paragraph("⚠️ 내용이 준비되지 않았습니다.", styles["Normal"]))

        # 🔹이미지를 PDF에 포함하려면 True로 설정
        if with_images and img_path:
            story.append(Spacer(1, 4*mm))
            story.append(RLImage(img_path, width=150*mm, preserveAspectRatio=True))

        story.append(Spacer(1, 10*mm))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------- 세션 상태 ---------- #
if "page" not in st.session_state:
    st.session_state.page = "목차"

def go_home(): st.session_state.page = "목차"
def go_page(p): st.session_state.page = p

# ---------- 인트로 페이지 ---------- #
if st.session_state.page == "인트로":
    st.markdown("""
    <div class="title-container">
        <div class="main-title">클릭하며 배우는</div>
        <div class="sub-title">위험물탱크 E-매뉴얼</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="guide-text">
    ☰ <b>왼쪽 상단 메뉴</b>를 클릭해 📘 <b>E-매뉴얼</b><br>
    또는 💡 <b>자주하는 질문(FAQ)</b> 페이지로 이동하세요.
    </div>
    """, unsafe_allow_html=True)

    cover_path = None
    for ext in ("jpg", "jpeg", "png"):
        p = Path(f"images/cover.{ext}")
        if p.exists(): cover_path = p; break
    if cover_path:
        st.markdown("---")
        st.image(str(cover_path), use_container_width=True, caption="E-매뉴얼 표지")
    else:
        st.info("💡 images 폴더에 cover.jpg/png/jpeg 파일을 넣으면 표지가 표시됩니다.")
    if st.button("📘 매뉴얼 바로가기", use_container_width=True):
        go_home()

# ---------- 목차 페이지 ---------- #
elif st.session_state.page == "목차":
    st.markdown('<div class="main-title">📘 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="big-card">', unsafe_allow_html=True)

        for main, subs in sections.items():
            st.markdown(f"<div class='chapter-title'>📂 {main}</div>", unsafe_allow_html=True)
            for sub in subs:
                st.button(sub, key=f"menu-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- PDF 출력 UI ----------
    st.markdown("### 📄 PDF 출력")
    all_items = [sub for subs in sections.values() for sub in subs]
    selected_items = st.multiselect(
        "출력할 항목을 선택하세요 (선택하지 않으면 전체 출력)",
        options=all_items
    )

    if st.button("📥 전체 PDF 다운로드"):
        pdf_buffer = create_pdf(selected_items, with_images=True)
        st.download_button(
            label="⬇️ 전체 PDF 저장",
            data=pdf_buffer,
            file_name="위험물탱크_E-매뉴얼_전체.pdf",
            mime="application/pdf"
        )

    if selected_items:
        if st.button("📥 선택 항목만 PDF 다운로드"):
            pdf_buffer = create_pdf(selected_items)
            st.download_button(
                label="⬇️ 선택 항목 PDF 저장",
                data=pdf_buffer,
                file_name="위험물탱크_E-매뉴얼_선택.pdf",
                mime="application/pdf"
            )

# ---------- 본문 ---------- #
else:
    current = st.session_state.page
    st.markdown(f'<div class="main-title">{current}</div>', unsafe_allow_html=True)

    def show_image_auto(key):
        safe_name = key.replace(" ", "_").replace("/", "_")
        img_path = find_image(safe_name)
        if img_path:
            st.image(img_path, use_container_width=True, caption=key)

    show_image_auto(current)

    def load_content(key):
        safe_name = key.replace(" ", "_").replace("/", "_")
        path = Path(f"contents/{safe_name}.md")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    content = load_content(current)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.warning("⚠️ 아직 준비된 내용이 없습니다.")

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기",
              use_container_width=True,
              key="btn-home",
              on_click=go_home)
