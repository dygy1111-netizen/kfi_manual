import streamlit as st
import os, glob, json, re
from pathlib import Path

st.set_page_config(
    page_title="위험물탱크 E-매뉴얼",
    page_icon="📘",
    layout="centered",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# ---------------- 세션 기본 ----------------
if "auth_user" not in st.session_state: st.session_state.auth_user = None
if "page" not in st.session_state: st.session_state.page = "목차"
if "search" not in st.session_state: st.session_state.search = ""
if "favorites" not in st.session_state: st.session_state.favorites = set()
if "history" not in st.session_state: st.session_state.history = []

DATA_FILE = "user_data.json"

def _load_all_users():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def _save_all_users(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_user_data(username: str):
    return _load_all_users().get(username, {"favorites": [], "history": []})

def save_user_data(username: str, favorites, history):
    data = _load_all_users()
    data[username] = {"favorites": list(favorites), "history": history[:5]}
    _save_all_users(data)

# ---------------- 스타일 ----------------
st.markdown("""
<style>
:root { --content-max: 980px; --img-max: 1000px; }
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background:#fff; line-height:1.7;}
@media (min-width: 1200px){
  .block-container { max-width: var(--content-max); }
}
.main-title { font-size: 2.0rem; font-weight: 800; color: #222; text-align:center;}
.stButton button { width:100%; border-radius:8px; background:#005bac; color:#fff; border:none;
  padding:0.9em; font-size:1.05rem; font-weight:600;}
.stButton button:hover { background:#0072e0; }
.back-btn button { background:#005bac; color:#fff; border-radius:6px; padding:0.6em 1em; border:none; font-weight:600;}

/* ✅ 마크다운 표 스타일 복원 */
table { width: 100%; border-collapse: collapse; margin: 0.5em 0 1.2em; }
table th, table td { border: 1px solid #d0d7e2; padding: 8px; text-align: center; }
table th { background-color: #005bac; color: #fff; }
table tr:nth-child(even) { background-color: #f0f4f8; }
</style>
""", unsafe_allow_html=True)


# ---------------- 데이터 ----------------
appendix_list = [
    {"title": "물분무설비 설치기준", "key": "물분무설비 설치기준"},
    {"title": "부상지붕탱크 구조", "key": "부상지붕탱크 구조"},
    {"title": "내부부상지붕탱크 구조", "key": "내부부상지붕탱크 구조"},
    {"title": "전기방식설비", "key": "전기방식설비"},
    {"title": "위험물제조소등 접지저항기준(소방청 협의사항)", "key": "위험물제조소등 접지저항기준(소방청 협의사항)"}
]
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

# ---------------- 검색 인덱스 ----------------
search_index = []
for main, subs in sections.items():
    for sub in subs:
        key = sub
        safe = key.replace(" ", "_").replace("/", "_")
        p = Path(f"contents/{safe}.md")
        body = ""
        if p.exists():
            try:
                body = p.read_text(encoding="utf-8").lower()
            except:
                body = ""
        search_index.append((sub, key, main, body))

# ---------------- 유틸 ----------------
def find_images(name):
    exts = ['jpg','jpeg','png','webp']
    results = []
    for e in exts:
        for path in sorted(glob.glob(f"images/{name}*.{e}")):
            base = os.path.splitext(os.path.basename(path))[0]
            desc = base[len(name)+1:] if base.startswith(name + "_") else ""
            results.append((path, desc))
    return results

def load_content(key):
    safe = key.replace(" ", "_").replace("/", "_")
    p = Path(f"contents/{safe}.md")
    return p.read_text(encoding="utf-8") if p.exists() else None

def persist_user_state():
    if st.session_state.auth_user:
        save_user_data(st.session_state.auth_user, st.session_state.favorites, st.session_state.history)

def go_home():
    st.session_state.page = "목차"
    st.session_state.search = ""
    persist_user_state()
    st.rerun()

def go_page(p):
    st.session_state.page = p
    if p in st.session_state.history:
        st.session_state.history.remove(p)
    st.session_state.history.insert(0, p)
    st.session_state.history = st.session_state.history[:5]
    persist_user_state()

def toggle_favorite(item):
    if item in st.session_state.favorites:
        st.session_state.favorites.remove(item)
    else:
        st.session_state.favorites.add(item)
    persist_user_state()

def jump_to_section(target: str):
    st.session_state["jump_to"] = target
    st.switch_page("pages/1_E_매뉴얼.py")

# ---- 외부에서 jump_to로 넘어온 경우 처리
if "jump_to" in st.session_state and st.session_state["jump_to"]:
    st.session_state.page = st.session_state.pop("jump_to")

# ---------------- 사이드바: 로그인(선택) + 빠른메뉴 ----------------
with st.sidebar:
    st.header("👤 사용자 로그인 (선택)")
    if st.session_state.auth_user:
        st.success(f"현재 사용자: {st.session_state.auth_user}")
        if st.button("로그아웃", key="sb-logout"):
            save_user_data(st.session_state.auth_user, st.session_state.favorites, st.session_state.history)
            st.session_state.auth_user = None
            st.toast("로그아웃 완료")
            st.rerun()
    else:
        u = st.text_input("아이디", key="sb_username")
        if st.button("로그인", key="sb-login"):
            if not u.strip():
                st.error("아이디를 입력하세요.")
            else:
                st.session_state.auth_user = u.strip()
                ud = load_user_data(st.session_state.auth_user)
                st.session_state.favorites |= set(ud.get("favorites", []))
                merged_hist = st.session_state.history + [h for h in ud.get("history", []) if h not in st.session_state.history]
                st.session_state.history = merged_hist[:5]
                st.toast("로그인 성공! 데이터가 복원되었습니다.")
                st.rerun()

    st.caption("로그인 안 해도 열람 가능(세션 임시 저장). 로그인하면 사용자별 저장·복원됩니다.")

    st.markdown("---")
    st.header("📂 빠른 메뉴")
    for main, subs in sections.items():
        with st.expander(f"📂 {main}", expanded=False):
            for sub in subs:
                if st.button(sub, key=f"side-{sub}", use_container_width=True):
                    st.session_state["jump_to"] = sub
                    st.switch_page("pages/1_E_매뉴얼.py")

    if st.session_state.get("favorites"):
        st.markdown("---"); st.markdown("⭐ **즐겨찾기**")
        for i, f in enumerate(st.session_state.favorites):
            st.button(f, key=f"fav-{i}-{f}", on_click=jump_to_section, args=(f,))
    if st.session_state.get("history"):
        st.markdown("---"); st.markdown("🕘 **최근 열람**")
        for i, h in enumerate(reversed(st.session_state.history[-5:])):
            st.button(h, key=f"hist-{i}-{h}", on_click=jump_to_section, args=(h,))

# ---------------- 메인 ----------------
if st.session_state.page == "목차":
    st.markdown('<div class="main-title">📚 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)

    st.session_state.search = st.text_input("🔍 검색", value=st.session_state.search)
    q = st.session_state.search.strip().lower()
    tokens = [t for t in q.split() if t]

    if tokens:
        def matches(title, body):
            return all(t in title.lower() or t in body for t in tokens)
        results = [(title, key, main) for title, key, main, body in search_index if matches(title, body)]
        if results:
            st.markdown("### 🔎 검색 결과")
            for title, key, main in results:
                st.caption(main)
                st.button(title, use_container_width=True, on_click=go_page, args=(key,))
        else:
            st.info("검색 결과가 없습니다.")

    st.markdown("### 📂 전체 목차")
    for main, subs in sections.items():
        st.markdown(f"**{main}**")
        for sub in subs:
            st.button(sub, key=f"menu-{sub}", use_container_width=True, on_click=go_page, args=(sub,))

else:
    current = st.session_state.page
    st.markdown(f'<div class="main-title">{current}</div>', unsafe_allow_html=True)
    fav_icon = "⭐ 즐겨찾기 해제" if current in st.session_state.favorites else "☆ 즐겨찾기 추가"
    st.button(fav_icon, key="fav-toggle", on_click=toggle_favorite, args=(current,))

    safe_name = current.replace(" ", "_").replace("/", "_")
    imgs = find_images(safe_name)
    if imgs:
      if st.session_state.get("large_images"):  # ✅ 큰 이미지 모드: 1열
        for (img_path, desc) in imgs:
            caption = f"{current} ({desc})" if desc else current
            st.image(img_path, use_container_width=True, caption=caption)
      else:  # 기존 2열
        for i in range(0, len(imgs), 2):
            cols = st.columns(2)
            for c, (img_path, desc) in zip(cols, imgs[i:i+2]):
                caption = f"{current} ({desc})" if desc else current
                c.image(img_path, use_container_width=True, caption=caption)

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
