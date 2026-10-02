import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정 (제목, 아이콘, 와이드 모드)
st.set_page_config(
    page_title="피터 파커와의 대화 | Spider-Chat",
    page_icon="🕸️",
    layout="wide"
)

# 2. 페이지 상단 제목 및 설명 (시스템 프롬프트는 숨기고 친근한 UI 구성)
st.title("🕸️ 피터 파커와의 비밀 무전기")
st.caption("뉴욕 퀸즈의 다정한 이웃, 스파이더맨(피터 파커)과 자유롭게 대화를 나눠보세요!")

# 3. Streamlit secrets에서 API 키 가져오기
api_key = st.secrets.get("GEMINI_API_KEY")

# API 키가 등록되지 않았을 경우 안내 문구 출력
if not api_key:
    st.error("설정(.streamlit/secrets.toml)에 GEMINI_API_KEY를 먼저 등록해주세요.")
    st.stop()

# 4. OpenAI 호환 클라이언트로 Gemini 엔드포인트 연결
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 5. 시스템 프롬프트 정의 (화면에는 출력되지 않음)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "너는 마블 시네마틱 유니버스(MCU)에서 배우 톰 홀랜드가 연기한 피터 파커(스파이더맨)야. "
        "말투는 밝고, 활기차며, 약간 횡설수설하면서도 호기심과 에너지가 넘쳐. "
        "과학과 테크놀로지를 진심으로 좋아하고, '친절한 이웃'으로서 다정하고 예의 바르게 대답해 줘. "
        "토니 스타크(스타크 씨), 메이 숙모, 친구 네드, MJ와의 일상이나 퀸즈 골목 순찰, 웹슈터 개발 같은 이야기를 자연스럽게 녹여내. "
        "항상 한국어로 대답하며, 상대방이 진짜 피터 파커와 이야기하고 있다고 느낄 수 있도록 몰입감 있게 대화해."
    )
}

# 6. 이전 대화 기록을 세션 상태에 저장 및 초기화
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# 7. 화면에 이전 대화 기록 불러오기 (사용자와 AI의 말풍선만 표시)
for msg in st.session_state.chat_messages:
    avatar = "🧑" if msg["role"] == "user" else "🕷️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 8. 사용자 입력창 처리
user_input = st.chat_input("피터에게 물어보고 싶은 말을 입력하세요...")

if user_input:
    # 사용자 입력 화면에 표시 및 저장
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)
    st.session_state.chat_messages.append({"role": "user", "content": user_input})

    # AI 응답 생성
    with st.chat_message("assistant", avatar="🕷️"):
        try:
            # API 요청용 메시지 배열 생성 (시스템 프롬프트 + 이전 대화 기록 전체)
            messages_payload = [SYSTEM_PROMPT] + st.session_state.chat_messages

            # 실시간 텍스트 스트리밍 호출
            stream = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages_payload,
                stream=True
            )

            # 스트림을 화면에 한 글자씩 흘러나오게 표시
            response_text = st.write_stream(stream)

            # AI 응답도 세션 상태에 저장하여 다음 턴에 기억하도록 함
            st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

        except Exception:
            # 요청 실패 시 시스템 오류 대신 친절한 한국어 안내 문구 한 줄 표시
            st.warning("웹슈터 통신 연결이 잠시 불안정해요. 잠시 후 다시 시도해 주세요!")
