import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="위험물탱크 매뉴얼",
    page_icon="📘",
    layout="wide"
)

st.title("📘 위험물탱크 매뉴얼")
st.markdown("모바일/PC 모두에서 쉽게 볼 수 있는 이미지+본문 매뉴얼입니다.")

# 목차 메뉴
menu = st.sidebar.radio(
    "📑 목차",
    ["개요", "설비 기준", "보유공지"],
    index=0
)

if menu == "개요":
    st.header("개요")
    st.image("images/overview.png", use_container_width=True)
    st.markdown("""
    **위험물탱크의 기본 개요**  
    - 위험물탱크의 구조 및 역할
    - 안전 관리 필요성
    - 주요 법령 및 규제 개요
    """)

elif menu == "설비 기준":
    st.header("설비 기준")
    st.image("images/facility.png", use_container_width=True)
    st.markdown("""
    **옥외탱크저장소 설비 기준**  
    - 탱크 재질 및 설계 요건  
    - 배관·밸브·펌프 설치 기준  
    - 소방 및 방재 설비 요구사항  
    """)

elif menu == "보유공지":
    st.header("보유공지")
    st.image("images/notice.png", use_container_width=True)
    st.markdown("""
    **저장량에 따른 보유공지 기준**  
    - 저장량별 보유공지 너비 계산식  
    - 위험물안전관리법 시행규칙 제30조 참고  
    - 현장 설치 사례 및 사진 예시  
    """)

st.markdown("---")
st.caption("ⓒ 2025 KFI 위험물검사부 · Streamlit 기반 매뉴얼")
