import streamlit as st
import streamlit.components.v1 as components
import math

# 1. 스트림릿 와이드 모드 설정
st.set_page_config(
    page_title="Spider-Man Biomechanics Lab & Boss Battle Evolution",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 상단 흰색 여백 제거 및 불필요한 Streamlit 헤더 정리
st.markdown("""
<style>
    /* 상단 헤더 높이 최소화 */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 1.5rem !important;
        z-index: 1 !important;
    }
    
    /* 최상단 여백(padding-top) 0으로 설정 */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }

    /* 탭 헤더 및 내부 여백 밀착 */
    div[data-testid="stTabs"] {
        margin-top: -0.5rem !important;
    }
    div[data-baseweb="tab-list"] {
        gap: 8px;
    }
    div[data-baseweb="tab-panel"] {
        padding-top: 0.2rem !important;
    }

    /* components.html iframe 테두리 및 여백 제거 */
    iframe {
        border: none !important;
        display: block !important;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 2. 탭 구성
tab_game, tab_lab, tab_boss = st.tabs([
    "🎮 3D 시티 웹스윙 & 물리 데이터 로거", 
    "🧪 첨단 생체재료 역학 연구소 (거미줄 제작)", 
    "⚔️ 빌런 보스 레이드 & 레벨업 배틀"
])

# 세션 상태 보존
if "web_color" not in st.session_state:
    st.session_state.web_color = "#38bdf8"
if "web_speed" not in st.session_state:
    st.session_state.web_speed = 110.0
if "web_range" not in st.session_state:
    st.session_state.web_range = 190.0
if "web_thickness" not in st.session_state:
    st.session_state.web_thickness = 3

# UI 슬라이더 제어용 세션 상태
if "slider_matrix" not in st.session_state:
    st.session_state.slider_matrix = "재조합 스파이드로인 단백질 (Spidroin I/II Mimic)"
if "slider_rho_x" not in st.session_state:
    st.session_state.slider_rho_x = 6.5
if "slider_delta_p" not in st.session_state:
    st.session_state.slider_delta_p = 22.0
if "slider_thickness" not in st.session_state:
    st.session_state.slider_thickness = 3
if "slider_color" not in st.session_state:
    st.session_state.slider_color = "#38bdf8"

# ==================== [TAB 2: 거미줄 제작 & 물리역학 연구소] ====================
with tab_lab:
    st.header("🧪 첨단 생체고분자 복합소재 & 유체역학 조제실")
    st.caption("방사형 거미줄 단백질(Spidroin) 모방 합성 고분자의 미세 역학적 물성과 유체 노즐 분사 동역학 분석")
    st.markdown("---")

    PRESETS = {
        "⚙️ 커스텀 조제 (직접 수치 조정)": {
            "desc": "물리화학 파라미터를 원하는 대로 미세 튜닝하는 기본 모드입니다."
        },
        "🏙️ [피터의 추천 1] 도심 고속 비행용 (Speed Booster)": {
            "matrix": "탄소나노튜브 복합 폴리아크릴로니트릴 (CNT-PAN Hybrid)",
            "rho_x": 9.5,
            "delta_p": 25.0,
            "color": "#38bdf8",
            "thickness": 3,
            "desc": "높은 가교 밀도로 고탄성(High Young's Modulus)을 구현하여 강력한 인장력으로 시티 스윙 속도를 극대화합니다."
        },
        "🎯 [피터의 추천 2] 원거리 저격 & 랜드마크 타격용 (Long Range)": {
            "matrix": "재조합 스파이드로인 단백질 (Spidroin I/II Mimic)",
            "rho_x": 5.5,
            "delta_p": 34.0,
            "color": "#facc15",
            "thickness": 2,
            "desc": "노즐 챔버 압력을 최대치로 끌어올려 베르누이 유속(v₀)과 유효 사정거리를 최대로 확보한 세팅입니다."
        },
        "🛡️ [피터의 추천 3] 빌런 제압 & 안전 포박용 (Heavy Duty)": {
            "matrix": "자가치유 디설피드 가교 히드로겔 (Self-Healing Hydrogel)",
            "rho_x": 4.0,
            "delta_p": 16.0,
            "color": "#ef4444",
            "thickness": 5,
            "desc": "굵은 섬유 다발과 유연한 충격 흡수력을 통해 안정적인 제동과 보스 포박에 적합한 묵직한 세팅입니다."
        },
        "⚖️ [피터의 추천 4] 데일리 순찰 밸런스형 (Standard Daily)": {
            "matrix": "재조합 스파이드로인 단백질 (Spidroin I/II Mimic)",
            "rho_x": 6.5,
            "delta_p": 22.0,
            "color": "#06b6d4",
            "thickness": 3,
            "desc": "비행 견인 속도(110 km/h)와 사정거리(190 m)의 황금 밸런스를 맞춘 피터 파커의 시그니처 세팅입니다."
        }
    }

    def on_preset_change():
        selected = st.session_state.selected_preset_key
        if selected != "⚙️ 커스텀 조제 (직접 수치 조정)":
            cfg = PRESETS[selected]
            st.session_state.slider_matrix = cfg["matrix"]
            st.session_state.slider_rho_x = cfg["rho_x"]
            st.session_state.slider_delta_p = cfg["delta_p"]
            st.session_state.slider_color = cfg["color"]
            st.session_state.slider_thickness = cfg["thickness"]

    st.markdown("#### 🕷️ 피터 파커의 웹슈터 조제 어시스턴트")
    c_preset, c_desc = st.columns([1, 1.4])
    with c_preset:
        preset_choice = st.selectbox(
            "상황별 권장 세팅 선택 (Preset)",
            list(PRESETS.keys()),
            index=0,
            key="selected_preset_key",
            on_change=on_preset_change
        )
    with c_desc:
        st.info(f"💡 **프리셋 특징**: {PRESETS[preset_choice]['desc']}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_ctrl, col_physics = st.columns([1.1, 1.2])

    with col_ctrl:
        st.subheader("⚙ 고분자 나노구조 및 사출 공학 제어")

        matrix_options = [
            "재조합 스파이드로인 단백질 (Spidroin I/II Mimic)",
            "탄소나노튜브 복합 폴리아크릴로니트릴 (CNT-PAN Hybrid)",
            "점탄성 폴리우레탄-실리카 나노입자 (Viscoelastic PU-SiO2)",
            "자가
