import streamlit as st
import os, json

st.set_page_config(
    page_title="위험물탱크 E-매뉴얼",
    page_icon="📘",
    layout="centered",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# ---------------- 공통 세션 상태 ----------------
if "auth_user" not in st.session_state: st.session_state.auth_user = None
if "page" not in st.session_state: st.session_state.page = "목차"
if "search" not in st.session_state: st.session_state.search = ""
if "favorites" not in st.session_state: st.session_state.favorites = set()
if "history" not in st.session_state: st.session_state.history = []

DATA_FILE = "user_data.json"
ENV_PASSWORD = os.environ.get("APP_LOGIN_PASSWORD", "changeme")  # 배포 시 꼭 변경!

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
.sub-title  { font-size: 2.0rem; font-weight: 800; color: #444; text-align:center;}
.guide-text { text-align: center; font-size: 1.1rem; margin-top: 10px; color: #555; }
.stButton button {
    width: 100%; border-radius: 8px; background-color: #005bac; color: white; border: none;
    padding: 0.9em; font-size: 1.05rem; font-weight: 600;
}
.stButton button:hover { background-color: #0072e0; }
</style>
""", unsafe_allow_html=True)

# ---------------- 사이드바: 간단 로그인(선택) ----------------
with st.sidebar:
    st.header("🔐 로그인 (선택)")

    if st.session_state.auth_user:
        st.success(f"로그인: {st.session_state.auth_user}")
        if st.button("로그아웃"):
            # 로그인 사용자면 저장 후 로그아웃
            save_user_data(st.session_state.auth_user, st.session_state.favorites, st.session_state.history)
            st.session_state.auth_user = None
            st.toast("로그아웃 완료")
            st.rerun()
    else:
        username = st.text_input("아이디", key="sb_username")
        password = st.text_input("비밀번호", type="password", key="sb_password")
        if st.button("로그인"):
            if not username or not password:
                st.error("아이디/비밀번호를 입력하세요.")
            elif password != ENV_PASSWORD:
                st.error("비밀번호가 올바르지 않습니다.")
            else:
                st.session_state.auth_user = username
                # 사용자 저장 데이터 불러와 현재 세션과 머지
                ud = load_user_data(username)
                # 즐겨찾기는 합집합, 최근열람은 기존 유지 + 저장분 선호(중복 제거)
                st.session_state.favorites |= set(ud.get("favorites", []))
                merged_hist = st.session_state.history + [h for h in ud.get("history", []) if h not in st.session_state.history]
                st.session_state.history = merged_hist[:5]
                st.toast("로그인 성공! 데이터가 복원되었습니다.")
                st.rerun()

    st.caption("로그인 안 해도 열람 가능(임시 세션 저장). 로그인하면 사용자별로 저장·복원됩니다.")

# ---------------- 메인 ----------------
st.markdown('<div class="sub-title">위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
st.markdown("**매뉴얼 또는 FAQ를 선택하세요.**")

col1, col2 = st.columns(2)
with col1:
    if st.button("📘 매뉴얼 시작하기", use_container_width=True):
        st.switch_page("pages/1_E_매뉴얼.py")
with col2:
    if st.button("💡 자주하는 질문(FAQ)", use_container_width=True):
        st.switch_page("pages/2_자주하는질문.py")
