import streamlit as st
import os, glob, json
from pathlib import Path
from io import BytesIO

# ======================= 기본 설정 ======================= #
st.set_page_config(page_title="위험물탱크 E-매뉴얼",
                   page_icon="📘",
                   layout="centered")

DATA_FILE = "user_data.json"   # 사용자별 데이터 저장 파일

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
/* ===== 공통 레이아웃 ===== */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}

/* ===== 제목 영역 ===== */
.title-container {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 20px;
}
.main-title {
    font-size: 2.0rem;
    font-weight: 800;
    color: #222222;
    line-height: 1.4;
}
.sub-title {
    font-size: 2.0rem;
    font-weight: 800;
    color: #444444;
    line-height: 1.4;
}
.guide-text {
    text-align: center;
    font-size: 1.1rem;
    margin-top: 10px;
    line-height: 1.6;
    color: #555555;
}

/* ===== 메뉴 박스 ===== */
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
.menu-title .emoji {
    margin-right: 0.4em;
    font-size: 1.4rem;
}
.menu-btn {
    width: 100%;
    margin-bottom: 0.4em;
}

/* ===== 기본 버튼 ===== */
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
.stButton button:hover {
    background-color: #0072e0;
}

/* ===== 본문 섹션 ===== */
.section-title {
    color: #003366;
    font-weight: 700;
    margin-top: 1.2em;
    font-size: 1.1rem;
}

/* ===== 표 ===== */
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
table tr:nth-child(even) {
    background-color: #f0f4f8;
}

/* ===== 하단(목차로 돌아가기) 버튼 ===== */
.back-btn button {
    background-color: #005bac;
    color: white;
    border-radius: 6px;
    padding: 0.6em 1em;
    border: none;
    font-weight: 600;
    transition: background-color 0.2s ease;
}
.back-btn button:hover {
    background-color: #0072e0;
}
</style>
""", unsafe_allow_html=True)



# ======================= 데이터 ======================= #
sections = {
    "1. 위험물탱크 위치, 구조 및 설비의 기준": [
        "1.1 안전거리","1.2 보유공지","1.3 표지 및 게시판",
        "1.4-1 탱크 내부 압력 해소 구조","1.4-2 탱크 부식방지 설비","1.4-3 통기관","1.4-4 자동계량식 유량계",
        "1.4-5 주입구","1.4-6 펌프설비","1.4-7 배관 및 밸브","1.4-8 부상지붕탱크의 설비",
        "1.4-9 전기설비","1.4-10 부속설비","1.5 방유제","1.6 옥외탱크저장소의 특례","1.7 소화설비","1.8 경보설비"
    ],
    "2. 안전성능검사": ["2.1 검사절차 및 확인사항","2.2 검사방법","2.3 참고사항"],
    "3. 정기검사": ["3.1 검사절차 및 확인사항","3.2 검사방법","3.3 참고사항"],
    "4. 부록": [item["title"] for item in appendix_list]
}

# ======================= 검색 인덱스 (제목 + 본문) ======================= #
search_index = []  # [(표시이름, key, 상위메뉴, 본문텍스트)]
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
    exts = ['jpg', 'jpeg', 'png']
    results = []
    for e in exts:
        for path in sorted(glob.glob(f"images/{name}*.{e}")):
            base = os.path.splitext(os.path.basename(path))[0]
            desc = ""
            if base.startswith(name + "_"):
                desc = base[len(name) + 1 :]
            results.append((path, desc))
    return results

def load_content(key):
    safe = key.replace(" ", "_").replace("/", "_")
    p = Path(f"contents/{safe}.md")
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return None

# ======================= 세션 상태 초기화 ======================= #
if "page" not in st.session_state: st.session_state.page = "목차"
if "search" not in st.session_state: st.session_state.search = ""
if "favorites" not in st.session_state: st.session_state.favorites = set()
if "history" not in st.session_state: st.session_state.history = []

# ======================= 사용자 로그인(사번) ======================= #
st.sidebar.header("🔑 로그인")
user_id = st.sidebar.text_input("사번을 입력하세요", value=st.session_state.get("user_id",""))
if user_id:
    st.session_state.user_id = user_id
    all_users = load_all_users()
    if user_id not in all_users:
        all_users[user_id] = {"favorites": [], "history": []}
        save_all_users(all_users)
    if not st.session_state.favorites and not st.session_state.history:
        st.session_state.favorites = set(all_users[user_id]["favorites"])
        st.session_state.history = all_users[user_id]["history"]

def save_user_data():
    if "user_id" in st.session_state:
        all_users = load_all_users()
        all_users[st.session_state.user_id] = {
            "favorites": list(st.session_state.favorites),
            "history": st.session_state.history
        }
        save_all_users(all_users)

# ======================= 공통 함수 ======================= #
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

def go_back():
    hist = st.session_state.history
    if len(hist) > 1:
        # 현재 페이지 제거 후 직전 페이지로 이동
        hist.pop(0)
        st.session_state.page = hist[0]
    else:
        st.session_state.page = "목차"
    save_user_data()


# ======================= (중요) 쿼리 파라미터 액션 처리 ======================= #
# HTML 버튼으로 전달된 액션을 가장 먼저 처리(한 번 클릭에 동작)
action = st.query_params.get("action", None)
if action:
    if action == "back":
        go_back()
    elif action == "home":
        go_home()
    # action 파라미터 제거(다음 렌더에서 잔류 방지)
    try:
        q = dict(st.query_params)
        if "action" in q:
            del q["action"]
        st.query_params = q
    except Exception:
        pass

# ======================= 사이드바 ======================= #
if st.session_state.favorites:
    st.sidebar.markdown("⭐ **즐겨찾기**")
    for i,f in enumerate(st.session_state.favorites):
        st.sidebar.button(f, key=f"fav-{i}-{f}", on_click=go_page, args=(f,))
if st.session_state.history:
    st.sidebar.markdown("🕘 **최근 열람**")
    for i,h in enumerate(reversed(st.session_state.history[-5:])):
        st.sidebar.button(h, key=f"hist-{i}-{h}", on_click=go_page, args=(h,))

# ======================= 페이지 ======================= #
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
    cover = None
    for ext in ("jpg","jpeg","png"):
        p = Path(f"images/cover.{ext}")
        if p.exists():
            cover = p
            break
    if cover:
        st.markdown("---")
        st.image(str(cover), use_container_width=True, caption="E-매뉴얼 표지")
    else:
        st.info("💡 images 폴더에 cover.jpg/png/jpeg 파일을 넣으면 표지가 표시됩니다.")
    if st.button("📘 매뉴얼 바로가기", use_container_width=True): go_home()

elif st.session_state.page == "목차":
    st.markdown('<div class="main-title">📘 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
    st.session_state.search = st.text_input("", value=st.session_state.search, placeholder="🔍")
    q = st.session_state.search.strip().lower()

    # --- 🔎 검색 결과 블록 ---
    if q:
        results = [
            (title, key, main)
            for title, key, main, body in search_index
            if q in title.lower() or q in body
        ]
        if results:
            st.markdown("<br><div style='font-weight:700; color:#005bac;'>🔎 검색 결과</div>", unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="big-card">', unsafe_allow_html=True)
                for title, key, main in results:
                    st.button(title,
                              key=f"search-{key}",
                              use_container_width=True,
                              on_click=go_page,
                              args=(key,))
                st.markdown("</div>", unsafe_allow_html=True)

    # --- 📚 전체 메뉴 블록 (항상 표시) ---
    st.markdown("<br><div style='font-weight:700; color:#1f2937;'>📚 전체 목차</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="big-card">', unsafe_allow_html=True)
        for main, subs in sections.items():
            st.markdown(f"<div class='chapter-title'>📂 {main}</div>", unsafe_allow_html=True)
            for sub in subs:
                st.button(sub, key=f"menu-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # ===== 설명 페이지 =====
    current = st.session_state.page
    st.markdown(f'<div class="main-title">{current}</div>', unsafe_allow_html=True)

    # ⭐ 즐겨찾기 토글
    fav_icon = "⭐ 즐겨찾기 해제" if current in st.session_state.favorites else "☆ 즐겨찾기 추가"
    st.button(fav_icon, key="fav-toggle", on_click=toggle_favorite, args=(current,))

    # ✅ 이미지 + 본문 출력
    safe_name = current.replace(" ", "_").replace("/", "_")
    img_files = find_images(safe_name)
    for img_path, desc in img_files:
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

    # 🔹 목차로 돌아가기 버튼 (하단)
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기", use_container_width=True, key="btn-home", on_click=go_home)
