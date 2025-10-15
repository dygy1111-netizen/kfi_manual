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
    all_users = _load_all_users()
    return all_users.get(username, {"favorites": [], "history": []})

def save_user_data(username: str, favorites, history):
    all_users = _load_all_users()
    all_users[username] = {
        "favorites": list(favorites),
        "history": history[:5],
    }
    _save_all_users(all_users)

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

# ---------------- 로그인 전용(회원가입 없음) ----------------
ENV_PASSWORD = os.environ.get("APP_LOGIN_PASSWORD", "changeme")  # ← 반드시 배포 환경에서 바꾸세요!

def login_view():
    st.markdown('<div class="sub-title">로그인</div>', unsafe_allow_html=True)
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("로그인"):
            if not username or not password:
                st.error("아이디/비밀번호를 입력하세요.")
                return
            if password != ENV_PASSWORD:
                st.error("비밀번호가 올바르지 않습니다.")
                return
            # 로그인 성공
            st.session_state.auth_user = username
            # 사용자 데이터 복원
            ud = load_user_data(username)
            st.session_state.favorites = set(ud.get("favorites", []))
            st.session_state.history = ud.get("history", [])
            st.success(f"{username}님 환영합니다.")
            st.rerun()
    with col2:
        st.info("관리자: Render/환경변수 'APP_LOGIN_PASSWORD' 로 비밀번호 관리")

if st.session_state.auth_user is None:
    login_view()
    st.stop()

# ---------------- 로그인 이후 메인 ----------------
st.markdown('<div class="sub-title">위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
st.markdown(f"**안녕하세요, {st.session_state.auth_user}님.**")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("📘 매뉴얼 시작하기"):
        st.switch_page("pages/1_E_매뉴얼.py")
with col2:
    if st.button("💡 자주하는 질문(FAQ)"):
        st.switch_page("pages/2_자주하는질문.py")
with col3:
    if st.button("로그아웃"):
        # 저장 후 로그아웃
        save_user_data(st.session_state.auth_user, st.session_state.favorites, st.session_state.history)
        st.session_state.auth_user = None
        st.session_state.favorites = set()
        st.session_state.history = []
        st.success("로그아웃 되었습니다.")
        st.rerun()
