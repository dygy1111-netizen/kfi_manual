import streamlit as st
import os, glob
from pathlib import Path

# ✅ 페이지 설정
st.set_page_config(page_title="위험물탱크 E-매뉴얼",
                   page_icon="📘",
                   layout="centered")

# ---------- 공통 CSS (변수로 저장) ---------- #
custom_css = """
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}
.main-title {
    font-size: 2.0rem;
    font-weight: 800;
    color: #222222 !important;
    line-height: 1.4;
    text-align:center;
}
.chapter-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1f2937 !important;
    margin-top: 1.6rem;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #e5e7eb;
}
.stButton button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac !important;
    color: white !important;
    border: none;
    padding: 0.7em;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom:0.3em;
}
.stButton button:hover { background-color: #0072e0 !important; }
.back-btn button {
    background-color: #005bac !important;
    color: white !important;
    border-radius: 6px;
    padding: 0.6em 1em;
    border: none;
    font-weight: 600;
}
.back-btn button:hover { background-color: #0072e0 !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)  # ✅ 최초 적용

# ---------- 이미지 탐색 함수 ---------- #
def find_image(name):
    exts = ['jpg','jpeg','png']
    for e in exts:
        path = f"images/{name}.{e}"
        if os.path.exists(path):
            return path
    for e in exts:
        g = glob.glob(f"images/{name}*.{e}")
        if g: return g[0]
    return None

# ---------- 목차 데이터 ---------- #
sections = {
    "1. 위험물탱크 위치, 구조 및 설비의 기준": [
        "1.1 안전거리","1.2 보유공지","1.3 표지 및 게시판",
        "1.4 외부구조 및 설비","1.5 방유제",
        "1.6 옥외탱크저장소의 특례","1.7 소화설비"
    ],
    "2. 안전성능검사": [
        "2.1 검사절차 및 확인사항","2.2 검사방법","2.3 참고사항"
    ],
    "3. 정기검사": [
        "3.1 검사절차 및 확인사항","3.2 검사방법","3.3 참고사항"
    ],
    "4. 부록": [
        "4.1 소방청 질의회신 및 협의사항",
        "4.2 검사관련 규격 및 기술지침",
        "4.3 검사 부적합 사례 및 실무 팁"
    ]
}

# ---------- 세션 상태 ---------- #
if "page" not in st.session_state: st.session_state.page = "목차"
if "favorites" not in st.session_state: st.session_state.favorites = set()
if "history" not in st.session_state: st.session_state.history = []

def go_home(): st.session_state.page = "목차"
def go_page(p):
    st.session_state.page = p
    if p in st.session_state.history: st.session_state.history.remove(p)
    st.session_state.history.insert(0, p)
    st.session_state.history = st.session_state.history[:5]

def toggle_favorite(item):
    if item in st.session_state.favorites: st.session_state.favorites.remove(item)
    else: st.session_state.favorites.add(item)

def load_content(key):
    safe = key.replace(" ", "_").replace("/", "_")
    path = Path(f"contents/{safe}.md")
    if path.exists():
        with open(path,"r",encoding="utf-8") as f: return f.read()
    return None

# ---------- 페이지 로직 ---------- #
if st.session_state.page == "인트로":
    st.markdown('<div class="main-title">📘 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
    if st.button("📘 매뉴얼 바로가기", use_container_width=True): go_home()

elif st.session_state.page == "목차":
    st.markdown('<div class="main-title">📘 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)

    # 🔎 검색
    query = st.text_input("🔍 검색어 입력", "")
    results = []
    if query:
        for subs in sections.values():
            for sub in subs:
                txt = load_content(sub)
                if txt and query.lower() in txt.lower():
                    results.append(sub)
        if results:
            st.subheader("🔎 검색 결과")
            for r in results:
                st.button(r, key=f"search-{r}", on_click=go_page, args=(r,))
            st.markdown("---")
        else:
            st.info("검색 결과가 없습니다.")

    # ⭐ 즐겨찾기
    if st.session_state.favorites:
        st.subheader("⭐ 즐겨찾기")
        for f in st.session_state.favorites:
            cols = st.columns([6,1])
            with cols[0]: st.button(f, key=f"fav-{f}", on_click=go_page, args=(f,))
            with cols[1]: st.button("🗑️", key=f"del-{f}", on_click=toggle_favorite, args=(f,))
        st.markdown("---")

    # 🕓 최근 본 항목
    if st.session_state.history:
        st.subheader("🕓 최근 본 항목")
        for h in st.session_state.history:
            st.button(h, key=f"hist-{h}", on_click=go_page, args=(h,))
        st.markdown("---")

    # 📚 목차 출력
    for main, subs in sections.items():
        st.markdown(f"<div class='chapter-title'>📂 {main}</div>", unsafe_allow_html=True)
        for sub in subs:
            cols = st.columns([6,1])
            with cols[0]:
                st.button(sub, key=f"menu-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))
            with cols[1]:
                icon = "⭐" if sub in st.session_state.favorites else "☆"
                st.button(icon, key=f"favbtn-{sub}", on_click=toggle_favorite, args=(sub,))

else:
    current = st.session_state.page
    st.markdown(f'<div class="main-title">{current}</div>', unsafe_allow_html=True)

    img = find_image(current.replace(" ","_").replace("/","_"))
    if img: st.image(img, use_container_width=True, caption=current)

    txt = load_content(current)
    if txt: st.markdown(txt, unsafe_allow_html=True)
    else: st.warning("⚠️ 아직 준비된 내용이 없습니다.")

    icon = "⭐ 즐겨찾기 해제" if current in st.session_state.favorites else "☆ 즐겨찾기 추가"
    st.button(icon, key="fav-toggle", on_click=toggle_favorite, args=(current,))
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기", use_container_width=True, on_click=go_home)

# ✅ CSS를 마지막에 다시 적용 (색상 유지)
st.markdown(custom_css, unsafe_allow_html=True)
