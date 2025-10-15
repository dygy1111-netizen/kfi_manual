import streamlit as st
import json, re, os
from pathlib import Path

st.set_page_config(
    page_title="자주하는 질문",
    page_icon="💡",
    layout="centered",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# ---------------- 세션 기본 ----------------
if "auth_user" not in st.session_state: st.session_state.auth_user = None
if "favorites" not in st.session_state: st.session_state.favorites = set()
if "history" not in st.session_state: st.session_state.history = []

DATA_FILE = "user_data.json"
ENV_PASSWORD = os.environ.get("APP_LOGIN_PASSWORD", "changeme")

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
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; background:#fff; line-height:1.7;}
.main-title { font-size: 2.0rem; font-weight: 800; color: #222; text-align:center;}
.stButton button { width:100%; border-radius:8px; background:#005bac; color:#fff; border:none;
  padding:0.9em; font-size:1.05rem; font-weight:600;}
.stButton button:hover { background:#0072e0; }
details.faq { border:2px solid #d0d7e2; border-radius:10px; padding:0.7rem 1rem; margin:0.8rem 0; background:#f8fbff;}
details.faq summary { list-style:none; cursor:pointer; font-weight:700; font-size:1.05rem; color:#003366; padding:0.3rem 0;}
details.faq summary::-webkit-details-marker { display:none;}
details.faq summary:after { content:"▾"; float:right; color:#005bac;}
details.faq[open] summary:after { transform: rotate(180deg); }
mark { padding:0 2px; background:#fff59d; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ---------------- 목차(사이드바용) + 로그인(선택) ----------------
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
    "4. 부록": [
        "물분무설비 설치기준","부상지붕탱크 구조",
        "내부부상지붕탱크 구조","전기방식설비",
        "위험물제조소등 접지저항기준(소방청 협의사항)"
    ]
}

def jump_to_section(target: str):
    st.session_state["jump_to"] = target
    st.switch_page("pages/1_E_매뉴얼.py")

with st.sidebar:
    st.header("🔐 로그인 (선택)")
    if st.session_state.auth_user:
        st.success(f"로그인: {st.session_state.auth_user}")
        if st.button("로그아웃", key="faq-logout"):
            save_user_data(st.session_state.auth_user, st.session_state.favorites, st.session_state.history)
            st.session_state.auth_user = None
            st.toast("로그아웃 완료")
            st.rerun()
    else:
        u = st.text_input("아이디", key="faq-username")
        p = st.text_input("비밀번호", type="password", key="faq-password")
        if st.button("로그인", key="faq-login"):
            if not u or not p:
                st.error("아이디/비밀번호를 입력하세요.")
            elif p != ENV_PASSWORD:
                st.error("비밀번호가 올바르지 않습니다.")
            else:
                st.session_state.auth_user = u
                ud = load_user_data(u)
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

# ---------------- FAQ 데이터 ----------------
faq_path = Path("faq.json")
if faq_path.exists():
    try:
        faq_list = json.loads(faq_path.read_text(encoding="utf-8"))
    except:
        faq_list = [{"q": "샘플 질문", "a": "샘플 답변입니다.\n\n![](faq_images/sample.jpg)"}]
else:
    faq_list = [{"q": "샘플 질문", "a": "샘플 답변입니다.\n\n![](faq_images/sample.jpg)"}]

# ---------------- 렌더 ----------------
st.markdown('<div class="main-title">💡 자주하는 질문 (FAQ)</div>', unsafe_allow_html=True)
keyword = st.text_input("🔍 검색어를 입력하세요", placeholder="질문 또는 답변 키워드").strip()

def highlight(text, kw):
    if not kw: return text
    pattern = re.compile(re.escape(kw), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

results = []
if keyword:
    key_l = keyword.lower()
    results = [it for it in faq_list if key_l in it.get("q","").lower() or key_l in it.get("a","").lower()]
else:
    results = faq_list

if results:
    for item in results:
        q_html = highlight(item.get("q",""), keyword)
        a_html = highlight(item.get("a",""), keyword)
        st.markdown(
            f"<details class='faq'><summary>{q_html}</summary><div>{a_html}</div></details>",
            unsafe_allow_html=True
        )
else:
    st.warning("검색 결과가 없습니다.")
