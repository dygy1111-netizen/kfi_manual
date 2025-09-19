import streamlit as st
import json, re
from pathlib import Path

st.set_page_config(page_title="자주하는 질문", page_icon="💡", layout="wide")

# 🔹제목을 한 줄 작게
st.markdown(
    "<h3 style='font-size:1.3rem; font-weight:700; margin-bottom:0.8rem;'>💡 자주하는 질문 (FAQ)</h3>",
    unsafe_allow_html=True
)

# ---------------- CSS (하이라이트 + 접기/펼치기)
st.markdown("""
<style>
details.faq {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 0.6rem 0.9rem;
  margin: 0.6rem 0;
  background: #ffffff;
}
details.faq[open] {
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
details.faq summary {
  list-style: none;
  cursor: pointer;
  font-weight: 700;
  font-size: 1.05rem;
  outline: none;
}
details.faq summary::-webkit-details-marker { display: none; }
details.faq summary:after {
  content: "▾";
  float: right;
  transition: transform 0.2s ease;
  color: #666;
}
details.faq[open] summary:after {
  transform: rotate(180deg);
}
mark { padding: 0 2px; }
</style>
""", unsafe_allow_html=True)

# ---------------- 데이터 로딩
faq_path = Path("faq.json")
if faq_path.exists():
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_list = json.load(f)
else:
    faq_list = [
        {"q": "샘플 질문", "a": "샘플 답변입니다.\n\n![](faq_images/sample.jpg)"}
    ]

# ---------------- 검색 입력
keyword = st.text_input("🔍 검색어를 입력하세요", placeholder="질문이나 답변의 키워드를 입력해 보세요.").strip()

# ---------------- 검색 필터링
if keyword:
    key_l = keyword.lower()
    results = [it for it in faq_list if key_l in it["q"].lower() or key_l in it["a"].lower()]
else:
    results = faq_list

# ---------------- 하이라이트 함수
def highlight(text, kw):
    if not kw:
        return text
    pattern = re.compile(re.escape(kw), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

# ---------------- 렌더링 (st.expander + markdown)
if results:
    for item in results:
        q_html = highlight(item["q"], keyword)   # 질문 하이라이트
        a_html = highlight(item["a"], keyword)   # 답변 하이라이트 (마크다운 그대로)

        # 질문 클릭 → 답변 펼침
        with st.expander(q_html):
            # 답변은 마크다운으로 출력 → 이미지, 표, 링크 모두 지원
            st.markdown(a_html, unsafe_allow_html=True)
else:
    st.warning("검색 결과가 없습니다.")
