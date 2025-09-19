import streamlit as st
import json, re
from pathlib import Path

st.set_page_config(page_title="자주하는 질문", page_icon="💡", layout="wide")
st.title("💡 자주하는 질문 (FAQ)")

# --------------------------------------------------
# 1️⃣ FAQ 데이터 로딩
# --------------------------------------------------
faq_path = Path("faq.json")
if faq_path.exists():
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_list = json.load(f)
else:
    faq_list = [
        {"q": "E-매뉴얼은 어떻게 이용하나요?",
         "a": "왼쪽 사이드바에서 E-매뉴얼을 클릭하면 목차와 내용을 볼 수 있습니다."},
        {"q": "모바일에서도 볼 수 있나요?",
         "a": "네, 모바일 브라우저에서도 화면 폭에 맞춰 자동으로 표시됩니다."},
        {"q": "이미지 확장자 제한이 있나요?",
         "a": "jpg, jpeg, png 등 일반적인 이미지 확장자는 모두 지원합니다."}
    ]

# --------------------------------------------------
# 2️⃣ 검색 입력창
# --------------------------------------------------
keyword = st.text_input(
    "🔍 검색어를 입력하세요",
    placeholder="질문이나 답변의 키워드를 입력해 보세요."
)

# --------------------------------------------------
# 3️⃣ 검색 필터링
# --------------------------------------------------
if keyword:
    results = [
        item for item in faq_list
        if keyword.lower() in item["q"].lower() or keyword.lower() in item["a"].lower()
    ]
else:
    results = faq_list

# --------------------------------------------------
# 4️⃣ 키워드 하이라이트 함수
# --------------------------------------------------
def highlight(text, kw):
    # 검색어를 HTML <mark> 태그로 감싸 강조
    pattern = re.compile(re.escape(kw), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

# --------------------------------------------------
# 5️⃣ 검색 결과 출력
# --------------------------------------------------
if results:
    for item in results:
        q_text = highlight(item["q"], keyword) if keyword else item["q"]
        a_text = highlight(item["a"], keyword) if keyword else item["a"]

        st.markdown(f"**Q. {q_text}**", unsafe_allow_html=True)
        st.markdown(a_text, unsafe_allow_html=True)
        st.markdown("---")
else:
    st.warning("검색 결과가 없습니다.")
