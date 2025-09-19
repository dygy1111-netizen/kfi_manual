import streamlit as st
import json, re
from pathlib import Path

st.set_page_config(page_title="자주하는 질문", page_icon="💡", layout="wide")
st.title("💡 자주하는 질문 (FAQ)")

# ---------------- CSS: 깔끔한 접기/펼치기 스타일 ----------------
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
details.faq .answer {
  padding-top: 0.6rem;
  color: #333;
  line-height: 1.7;
}
mark { padding: 0 2px; }
</style>
""", unsafe_allow_html=True)

# ---------------- 1) FAQ 데이터 로딩 ----------------
faq_path = Path("faq.json")
if faq_path.exists():
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_list = json.load(f)
else:
    # 샘플 데이터
    faq_list = [
        {"q": "E-매뉴얼은 어떻게 이용하나요?",
         "a": "왼쪽 사이드바에서 E-매뉴얼을 클릭하면 목차와 내용을 볼 수 있습니다."},
        {"q": "모바일에서도 볼 수 있나요?",
         "a": "네, 모바일 브라우저에서도 화면 폭에 맞춰 자동으로 표시됩니다."},
        {"q": "이미지 확장자 제한이 있나요?",
         "a": "jpg, jpeg, png 등 일반적인 이미지 확장자를 모두 지원합니다."}
    ]

# ---------------- 2) 검색 입력 ----------------
keyword = st.text_input(
    "🔍 검색어를 입력하세요",
    placeholder="질문이나 답변의 키워드를 입력해 보세요."
).strip()

# ---------------- 3) 필터링 ----------------
if keyword:
    key_l = keyword.lower()
    results = [it for it in faq_list if key_l in it["q"].lower() or key_l in it["a"].lower()]
else:
    results = faq_list

# ---------------- 4) 하이라이트 함수 ----------------
def highlight(text: str, kw: str) -> str:
    if not kw:
        return text
    pattern = re.compile(re.escape(kw), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

# ---------------- 5) 렌더링 (질문 클릭 → 답변 펼침) ----------------
if results:
    for item in results:
        q_html = highlight(item["q"], keyword)
        a_html = highlight(item["a"], keyword)
        st.markdown(
            f"""
            <details class="faq">
              <summary>{q_html}</summary>
              <div class="answer">{a_html}</div>
            </details>
            """,
            unsafe_allow_html=True
        )
else:
    st.warning("검색 결과가 없습니다.")
