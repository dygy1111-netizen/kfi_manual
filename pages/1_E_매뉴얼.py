import streamlit as st
import os, glob, json
from pathlib import Path

# ======================= 기본 설정 ======================= #
# 🔹menu_items 옵션을 추가해 Streamlit 기본 메뉴(회색 글씨) 제거
st.set_page_config(
    page_title="위험물탱크 E-매뉴얼",
    page_icon="📘",
    layout="centered",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
)

DATA_FILE = "user_data.json"

def load_all_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_all_users(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ======================= 부록 리스트 ======================= #
appendix_list = [
    {"title": "물분무설비 설치기준", "key": "물분무설비 설치기준"},
    {"title": "부상지붕탱크 구조", "key": "부상지붕탱크 구조"},
    {"title": "내부부상지붕탱크 구조", "key": "내부부상지붕탱크 구조"},
    {"title": "전기방식설비", "key": "전기방식설비"},
    {"title": "위험물제조소등 접지저항기준(소방청 협의사항)", "key": "위험물제조소등 접지저항기준(소방청 협의사항)"}
]

# ======================= CSS ======================= #
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}
.main-title {
    font-size: 2.0rem;
    font-weight: 800;
    color: #222222;
    line-height: 1.4;
    text-align: center;
}
/* 공통 버튼 스타일 */
.stButton button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac;
    color: white;
    border: none;
    padding: 0.7em;
    font-size: 1rem;
    font-weight: 600;
    transition: background-color 0.2s ease;
}
.stButton button:hover { background-color: #0072e0; }

/* 사이드바 빠른 이동 버튼 */
.sidebar-btn button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac !important;
    color: white !important;
    border: none;
    padding: 0.6em;
    font-size: 1rem;
    font-weight: 600;
}
.sidebar-btn button:hover {
    background-color: #0072e0 !important;
}

.section-title {
    color:#003366; font-weight:700;
    margin-top:1.2em; font-size:1.1rem;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5em;
}
table th, table td {
    border: 1px solid #d0d7e2;
    padding: 8px;
    text-align: center;
}
table th {
    background-color: #005bac;
    color: white;
}
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

# ======================= 데이터 ======================= #
sections = {
    "1. 위험물탱크 위치, 구조 및 설비의 기준": [
        "1.1 안전거리","1.2 보유공지","1.3 표지 및 게시판",
        "1.4-1 탱크 내부 압력 해소 구조","1.4-2 탱크 부식방지 설비","1.4-3 통기관",
        "1.4-4 자동계량식 유량계","1.4-5 주입구","1.4-6 펌프설비",
        "1.4-7 배관 및 밸브","1.4-8 부상지붕탱크의 설비",
        "1.4-9 전기설비","1.4-10 부속설비",
        "1.5 방유제","1.6 옥외탱크저장소의 특례",
        "1.7 소화설비","1.8 경보설비"
    ],
    "2. 안전성능검사": ["2.1 검사절차 및 확인사항","2.2 검사방법","2.3 참고사항"],
    "3. 정기검사": ["3.1 검사절차 및 확인사항","3.2 검사방법","3.3 참고사항"],
    "4. 부록": [item["title"] for item in appendix_list]
}

# ======================= 검색 인덱스 ======================= #
search_index = []
for main, subs in sections.items():
    for sub in subs:
        key = sub if isinstance(sub, str) else sub["key"]
        safe = key.replace(" ", "_").replace("/", "_")
        p = Path(f"contents/{safe}.md")
        body = ""
        if p.exists():
            try:
                body = p.read_text(encoding="utf-8").lower()
            except:
                body = ""
        title = sub if isinstance(sub, str) else sub["title"]
        search_index.append((title, key, main, body))

# ======================= 유틸 함수 ======================= #
def find_images(name):
    exts = ['jpg','jpeg','png']
    results = []
    for e in exts:
        for path in sorted(glob.glob(f"images/{name}*.{e}")):
            base = os.path.splitext(os.path.basename(path))[0]
            desc = ""
            if base.startswith(name + "_"):
                desc = base[len(name)+1:]
            results.append((path, desc))
    return results

def load_content(key):
    safe = key.replace(" ", "_").replace("/", "_")
    p = Path(f"contents/{safe}.md")
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return None

# ======================= 세션 상태 ======================= #
if "page" not in st.session_state: st.session_state.page = "목차"
if "search" not in st.session_state: st.session_state.search = ""
if "favorites" not in st.session_state: st.session_state.favorites = set()
if "history" not in st.session_state: st.session_state.history = []

# --- 사이드바에서 특정 항목을 선택해 들어온 경우 바로 해당 페이지로 진입
if "jump_to" in st.session_state and st.session_state["jump_to"]:
    target = st.session_state.pop("jump_to")
    # 유효성 검사(선택지가 실제 sections 안에 있으면 바로 이동)
    if any(target in subs for subs in sections.values()):
        st.session_state.page = target
    else:
        # 혹시 부록 같은 독립 항목이면 그대로 설정
        st.session_state.page = target

def save_user_data():
    if "user_id" in st.session_state:
        all_users = load_all_users()
        all_users[st.session_state.user_id] = {
            "favorites": list(st.session_state.favorites),
            "history": st.session_state.history
        }
        save_all_users(all_users)

def go_home():
    st.session_state.page = "목차"

def go_page(p):
    st.session_state.page = p
    if p in st.session_state.history:
        st.session_state.history.remove(p)
    st.session_state.history.insert(0, p)
    st.session_state.history = st.session_state.history[:5]
    save_user_data()

def toggle_favorite(item):
    if item in st.session_state.favorites:
        st.session_state.favorites.remove(item)
    else:
        st.session_state.favorites.add(item)
    save_user_data()
# --- 사이드바에서 '하위항목' 클릭 시, 대상 섹션을 세션에 담고 매뉴얼 페이지로 이동
def jump_to_section(target: str):
    st.session_state["jump_to"] = target
    st.switch_page("pages/1_E_매뉴얼.py")

# ======================= 사이드바 ======================= #
with st.sidebar:
    # (필요시) 고정 링크들
    # st.page_link("home.py", label="🏠 Home")
    # st.page_link("pages/1_E_매뉴얼.py", label="📘 E 매뉴얼")
    # st.page_link("pages/2_자주하는질문.py", label="💡 자주하는 질문")

    # 대제목 → 하위 메뉴 펼침
    for main, subs in sections.items():
        with st.expander(f"📂 {main}", expanded=False):
            for sub in subs:
                st.button(
                    sub,
                    key=f"side-{sub}",
                    use_container_width=True,
                    on_click=jump_to_section,   # 🔴 여기!
                    args=(sub,)
                )

    # ⭐ 즐겨찾기
    if st.session_state.get("favorites"):
        st.markdown("---")
        st.markdown("⭐ **즐겨찾기**")
        for i, f in enumerate(st.session_state.favorites):
            st.button(
                f,
                key=f"fav-{i}-{f}",
                on_click=jump_to_section,      # 🔴 여기!
                args=(f,)
            )

    # 🕘 최근 열람
    if st.session_state.get("history"):
        st.markdown("---")
        st.markdown("🕘 **최근 열람**")
        for i, h in enumerate(reversed(st.session_state.history[-5:])):
            st.button(
                h,
                key=f"hist-{i}-{h}",
                on_click=jump_to_section,      # 🔴 여기!
                args=(h,)
            )

# ======================= 메인 컨텐츠 ======================= #
if st.session_state.page == "목차":
    st.markdown('<div class="main-title">📚 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
    st.session_state.search = st.text_input("🔍 검색", value=st.session_state.search)
    q = st.session_state.search.strip().lower()

    if q:
        results = [(title, key) for title, key, main, body in search_index
                   if q in title.lower() or q in body]
        if results:
            st.markdown("### 🔎 검색 결과")
            for title, key in results:
                st.button(title, use_container_width=True, on_click=go_page, args=(key,))

    st.markdown("### 📂 전체 목차")
    for main, subs in sections.items():
        st.markdown(f"**{main}**")
        cols = st.columns(2)
        for i, sub in enumerate(subs):
            with cols[i % 2]:
                st.button(sub, key=f"menu-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))

else:
    current = st.session_state.page
    st.markdown(f'<div class="main-title">{current}</div>', unsafe_allow_html=True)
    fav_icon = "⭐ 즐겨찾기 해제" if current in st.session_state.favorites else "☆ 즐겨찾기 추가"
    st.button(fav_icon, key="fav-toggle", on_click=toggle_favorite, args=(current,))

    safe_name = current.replace(" ", "_").replace("/", "_")
    for img_path, desc in find_images(safe_name):
        caption = f"{current} ({desc})" if desc else current
        st.image(img_path, use_container_width=True, caption=caption)

    content = load_content(current)
    if content:
        if "### 부록" in content:
            main_part, appendix_part = content.split("### 부록", 1)
            st.markdown(main_part, unsafe_allow_html=True)
            st.markdown("### 부록")
            for line in appendix_part.splitlines():
                line = line.strip()
                if line:
                    st.button(line, on_click=go_page, args=(line,))
        else:
            st.markdown(content, unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기", use_container_width=True, on_click=go_home)
