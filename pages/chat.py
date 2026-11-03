import streamlit as st
from openai import OpenAI

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="피터 파커와의 대화 | Spider-Comms",
    page_icon="🕸️",
    layout="wide"
)

# 2. 스파이더맨 무전기 전용 사이버네틱 HUD 스타일 CSS
st.markdown("""
<style>
    /* 전체 배경 톤 다운 */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }

    /* 상단 무전기 하드웨어 프레임 */
    .radio-hud-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85));
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 24px;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.25), inset 0 0 15px rgba(56, 189, 248, 0.1);
        position: relative;
    }

    .radio-header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(239, 68, 68, 0.3);
        padding-bottom: 12px;
        margin-bottom: 12px;
    }

    .radio-title-text {
        font-size: 20px;
        font-weight: 900;
        color: #ef4444;
        letter-spacing: 1.5px;
        display: flex;
        align-items: center;
        gap: 10px;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }

    .freq-badge {
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid #38bdf8;
        color: #38bdf8;
        font-family: monospace;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 800;
        box-shadow: 0 0 8px rgba(56, 189, 248, 0.3);
    }

    .signal-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse-signal 1.2s infinite;
    }

    @keyframes pulse-signal {
        0% { transform: scale(0.9); opacity: 0.6; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.6; }
    }

    .status-row {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: #94a3b8;
    }

    /* Streamlit 채팅 말풍선 커스텀 */
    div[data-testid="stChatMessage"] {
        background-color: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        margin-bottom: 14px !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }

    /* 피터 파커(Assistant) 말풍선 */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]),
    div[data-testid="stChatMessage"]:has(span:contains("🕷️")) {
        border-left: 4px solid #ef4444 !important;
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.08), rgba(15, 23, 42, 0.85)) !important;
    }

    /* 사용자(User) 말풍선 */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]),
    div[data-testid="stChatMessage"]:has(span:contains("🧑")) {
        border-right: 4px solid #38bdf8 !important;
        background: linear-gradient(270deg, rgba(56, 189, 248, 0.08), rgba(15, 23, 42, 0.85)) !important;
    }

    /* 입력창(stChatInput) 스타일링 */
    div[data-testid="stChatInput"] {
        border-color: rgba(239, 68, 68, 0.5) !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #ef4444 !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 상단 무전기 HUD 대시보드
st.markdown("""
<div class="radio-hud-container">
    <div class="radio-header-top">
        <div class="radio-title-text">
            <span class="signal-dot"></span>
            STARK-COMMS // PROTOCOL : SPIDER-LINK
        </div>
        <div class="freq-badge">CH-1962.08 MHz [SECURE]</div>
    </div>
    <div class="status-row">
        <span>📡 <b>통신 채널:</b> 퀸즈-브루클린 암호화 링크 활성화</span>
        <span>⚡ <b>배터리/신호:</b> 98% ONLINE | 레이턴시: 12ms</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Streamlit secrets에서 API 키 가져오기
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("설정(.streamlit/secrets.toml)에 GEMINI_API_KEY를 먼저 등록해주세요.")
    st.stop()

# 5. OpenAI 호환 클라이언트로 Gemini 엔드포인트 연결
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 6. 시스템 프롬프트 정의 (무전 통신 몰입감 강화)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "너는 마블 시네마틱 유니버스(MCU)에서 배우 톰 홀랜드가 연기한 피터 파커(스파이더맨)야. "
        "지금 비밀 무전기(Comms Link)를 통해 상대방과 단독으로 통신하고 있어. "
        "말투는 밝고, 활기차며, 약간 횡설수설하면서도 호기심과 에너지가 넘쳐. "
        "무전 상황에 맞게 가끔 '치-익... 들려?', '아, 바람 소리 때문에 잠깐 끊겼다!', '오버!' 같은 자연스러운 무전 추임새를 적절히 섞어줘. "
        "과학과 테크놀로지, 물리/공학 이야기를 진심으로 좋아하고, '친절한 이웃'으로서 다정하고 예의 바르게 대답해. "
        "토니 스타크(스타크 씨), 메이 숙모, 친구 네드, MJ와의 일상이나 퀸즈 빌딩 숲 순찰, 웹슈터 점도/압력 개발 이야기를 자연스럽게 녹여내. "
        "항상 한국어로 대답하며, 상대방이 실제 피터 파커와 실시간 무전을 나누고 있다고 느낄 수 있도록 생동감 있게 대화해."
    )
}

# 7. 세션 상태 초기화
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "치-익... 아, 아! 마이크 테스트! 들려? 난 지금 퀸즈 쪽 고층 빌딩 옥상에 걸터앉아 있어. 오늘 연구랑 순찰은 어떻게 돼가고 있어?"}
    ]

# 8. 이전 대화 기록 렌더링
for msg in st.session_state.chat_messages:
    avatar = "🧑" if msg["role"] == "user" else "🕷️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 9. 사용자 입력 및 스트리밍 처리
user_input = st.chat_input("피터에게 무전을 전송하세요... (Enter)")

if user_input:
    # 사용자 입력 표시 및 저장
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)
    st.session_state.chat_messages.append({"role": "user", "content": user_input})

    # AI 응답 스트리밍 생성
    with st.chat_message("assistant", avatar="🕷️"):
        try:
            messages_payload = [SYSTEM_PROMPT] + st.session_state.chat_messages

            stream = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages_payload,
                stream=True
            )

            response_text = st.write_stream(stream)
            st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

        except Exception:
            st.warning("치-익... 치익... 웹슈터 통신 안테나가 잠시 불안정해요. 잠시 후 다시 연결해 주세요!")
