import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="Peter Parker Stark-Comm Link",
    page_icon="🕷️",
    layout="wide"
)

# 2. 스파이더맨 스타크-테크 HUD 전용 CSS 스타일
st.markdown("""
<style>
    /* 전체 배경 다크 테마 & 거미줄 헥사곤 홀로그램 배경 */
    .stApp {
        background-color: #070913 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(220, 38, 38, 0.18) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(2, 132, 199, 0.18) 0px, transparent 50%),
            radial-gradient(circle, rgba(255, 255, 255, 0.03) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 28px 28px !important;
        color: #f1f5f9 !important;
    }

    /* 좌측 사이드바 다크 & 레드 포인트 */
    section[data-testid="stSidebar"] {
        background-color: #0c101c !important;
        border-right: 1px solid rgba(239, 68, 68, 0.25) !important;
    }

    /* 상단 HUD 콘솔 전광판 */
    .stark-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85));
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.25), inset 0 0 15px rgba(56, 189, 248, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stark-title {
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        text-shadow: 0 0 12px rgba(239, 68, 68, 0.8);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .comm-beacon {
        width: 12px;
        height: 12px;
        background: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 12px #22c55e;
        display: inline-block;
        animation: commBlink 1.4s infinite;
    }
    @keyframes commBlink {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(0.85); }
    }
    .stark-badges {
        display: flex;
        gap: 10px;
    }
    .badge {
        font-family: monospace;
        font-size: 11px;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .badge-blue {
        background: rgba(2, 132, 199, 0.2);
        border: 1px solid #38bdf8;
        color: #38bdf8;
    }
    .badge-red {
        background: rgba(220, 38, 38, 0.2);
        border: 1px solid #ef4444;
        color: #fca5a5;
    }

    /* 피터 파커 말풍선 (어시스턴트) 커스텀 */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]),
    div[data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(18, 24, 38, 0.85) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        border-left: 5px solid #ef4444 !important;
        border-radius: 6px 18px 18px 18px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 10px rgba(239, 68, 68, 0.15) !important;
        color: #f8fafc !important;
        margin-bottom: 16px !important;
    }

    /* 사용자 말풍선 (유저) 커스텀 */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]),
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background: rgba(12, 34, 56, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-right: 5px solid #38bdf8 !important;
        border-radius: 18px 6px 18px 18px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 10px rgba(56, 189, 248, 0.15) !important;
        color: #f8fafc !important;
        margin-bottom: 16px !important;
    }

    /* 텍스트 폰트 및 가독성 */
    div[data-testid="stChatMessageContent"] p {
        font-size: 14.5px !important;
        line-height: 1.65 !important;
        color: #e2e8f0 !important;
    }

    /* 하단 채팅 입력창(stChatInput) 네온 발광 스타일 */
    div[data-testid="stChatInput"] {
        border-radius: 24px !important;
        background: rgba(15, 23, 42, 0.95) !important;
        border: 2px solid #ef4444 !important;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.35), inset 0 0 10px rgba(0, 0, 0, 0.8) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
        font-size: 14px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }
    div[data-testid="stChatInput"] button {
        color: #ef4444 !important;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. 상단 스타크 테크 통신 HUD 헤더
st.markdown("""
<div class="stark-header">
    <div>
        <div class="stark-title">
            <span class="comm-live-beacon"></span>
            🕸️ STARK-COMM // PETER PARKER
        </div>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
            뉴욕 퀸즈 상공 순찰 네트워크 암호화 연결 완료 | 실시간 무전 링크
        </div>
    </div>
    <div class="stark-badges">
        <span class="badge badge-red">SUIT: IRON-SPIDER</span>
        <span class="badge badge-blue">SIGNAL: OPTIMAL 99.8%</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. 세션 상태 관리
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "user",
            "content": "야"
        },
        {
            "role": "assistant",
            "content": (
                "오! 안녕하세요! 깜짝 놀랐네, 하하. 혹시 무슨 일 있으세요? 혹시 뭐 도움이 필요하다거나... "
                "아니면 저기 퀸즈 근처에서 거미줄 치고 있는 저를 보셨나요?\n\n"
                "아, 맞다! 제 이름은 피터... 아니, 그니까 피터 파커예요! 그냥 퀸즈에 사는 평범한... 음, 아주 평범하진 않고, "
                "음음, 아무튼 그 '친절한 이웃 스파이더맨'이랍니다!\n\n"
                "요즘 토니 스타크—아, 스타크 씨가 만들어주신 새 슈트 업그레이드하느라 밤을 좀 샜더니 말이 자꾸 헛나오네요. "
                "웹슈터 카트리지 압력 조절하는 게 보통 일이 아니더라고요. 네드가 옆에서 계속 레고 스타워즈 만들자고 꼬시는데 "
                "그거 참느라 죽는 줄 알았어요, 헤헤.\n\n"
                "아무튼, 저한테 뭐 도울 일이라도 있으신가요? 말씀만 하세요! 제 슈퍼 히어로 센스가... 음, 아직까지는 찌릿찌릿하지 않은 걸 보니 "
                "평화로운 하루인 것 같긴 한데, 그래도 언제든 환영이에요!"
            )
        }
    ]

# 5. 대화 내역 렌더링 (커스텀 아바타 지정)
for message in st.session_state.messages:
    avatar_icon = "🕷️" if message["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 6. 사용자 입력 처리
if prompt := st.chat_input("피터에게 무전을 전송하세요... (예: 웹슈터 카트리지 압력 세팅은 어떻게 해?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 톰 홀랜드 피터 파커 페르소나 응답 생성
    p_lower = prompt.lower()
    if "웹슈터" in p_lower or "압력" in p_lower or "가교" in p_lower:
        bot_reply = (
            "웹슈터 말이 나와서 하는 얘긴데, 노즐 챔버 압력(ΔP)을 올리면 사출 속도(v₀)가 엄청 빨라져서 "
            "원거리 건물 저격할 때 진짜 좋거든요! 근데 가교 밀도(ρ_x)를 너무 높이면 줄이 너무 빳빳해져서 "
            "스윙할 때 어깨 탈구되는 줄 알았잖아요, 헤헤. 랩실에서 영률 수치 밸런스 맞춰주시면 순찰 돌기 딱 좋을 것 같아요!"
        )
    elif "보스" in p_lower or "빌런" in p_lower or "고블린" in p_lower or "베놈" in p_lower:
        bot_reply = (
            "빌런이요?! 잠깐만요, 스파이더 센스가 찌릿찌릿한데요?! 그린 고블린은 글라이더가 빠르니까 거미줄로 4~5번 쏴서 "
            "포박 게이지 100% 채운 다음 바닥으로 떨어뜨려야 해요! 혹시 상대하실 거면 Q 궁극기 [웹 블라섬] 아껴두세요!"
        )
    elif "안녕" in p_lower or "반가" in p_lower:
        bot_reply = "오, 안녕안녕! 지금 막 샌드위치 먹으면서 거미줄 점검 중이었어요. 오늘 연구 진행은 잘 돼가나요?"
    else:
        bot_reply = (
            f"'{prompt}'라고요? 와, 그거 진짜 흥미롭네요! 스타크 씨 랩실 연구 데이터랑 연결해서 분석해 보면 대박일 것 같은데요? "
            "저 다음 순찰 가기 전에 조금만 더 자세히 얘기해 줄 수 있어요?"
        )

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant", avatar="🕷️"):
        st.markdown(bot_reply)
