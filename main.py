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

# 상단 흰색 여백, 로딩바, 헤더 툴바 및 내부 컨테이너 패딩 강제 제거
st.markdown("""
<style>
    /* 1. 상단 Streamlit 헤더 및 툴바 완전 제거 */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 2. 최상단 컨테이너 패딩 및 마진 강제 0 */
    .stAppViewContainer, .main, .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* 3. 탭 바를 상단 맨 끝으로 밀착 */
    div[data-testid="stTabs"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    div[data-baseweb="tab-list"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-baseweb="tab-panel"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* 4. iframe 래퍼의 상단 빈 공간 강제 삭제 */
    div[data-testid="stCustomComponentV1"] {
        margin-top: -10px !important;
        padding: 0 !important;
    }

    iframe {
        border: none !important;
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
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
            "자가치유 디설피드 가교 히드로겔 (Self-Healing Hydrogel)"
        ]
        curr_idx = matrix_options.index(st.session_state.slider_matrix) if st.session_state.slider_matrix in matrix_options else 0

        fluid_base = st.selectbox(
            "기반 생체 복합 폴리머 기질 (Polymer Matrix)",
            matrix_options,
            index=curr_idx,
            key="slider_matrix"
        )

        st.markdown("#### 1. 나노 네트워크 가교도 (Crosslinking Density)")
        crosslink_density = st.slider(
            "가교 밀도 ρ_x (10^4 mol/m³)",
            min_value=1.5,
            max_value=12.0,
            value=float(st.session_state.slider_rho_x),
            step=0.5,
            key="slider_rho_x",
            help="고분자 사슬 간 화학적 공유결합 밀도입니다. 높을수록 거미줄이 팽팽해져 '비행 속도'가 빨라집니다."
        )

        st.markdown("#### 2. 마이크로 노즐 사출 압력 (Chamber Pressure)")
        injection_pressure = st.slider(
            "노즐 압축 챔버 압력 ΔP (MPa)",
            min_value=8.0,
            max_value=35.0,
            value=float(st.session_state.slider_delta_p),
            step=1.0,
            key="slider_delta_p",
            help="웹슈터 노즐 내부의 유체 분사 압력입니다. 높을수록 거미줄의 '유효 사정거리'가 대폭 길어집니다."
        )

        st.markdown("#### 3. 거미줄 광학 표면 물성")
        selected_color = st.color_picker(
            "생체 형광 광학 색상 (Photoluminescence)",
            value=st.session_state.slider_color,
            key="slider_color"
        )
        selected_thickness = st.slider(
            "섬유 다발 가닥 수 / 직경 d (μm)",
            1, 6,
            value=int(st.session_state.slider_thickness),
            key="slider_thickness",
            help="줄의 굵기입니다. 3D 화면 속 거미줄 라인의 시각적 두께에 반영됩니다."
        )

    R_gas = 8.314
    Temp = 298.15
    youngs_modulus_gpa = (3.0 * (crosslink_density * 1e4) * R_gas * Temp) / 1e9

    calculated_web_speed = round(80.0 + (youngs_modulus_gpa / 0.89) * 45.0, 1)
    calculated_web_speed = max(80.0, min(160.0, calculated_web_speed))

    fluid_density = 1180.0
    v_exit = math.sqrt((2.0 * (injection_pressure * 1e6)) / fluid_density)
    calculated_web_range = round(95.0 + (v_exit / 245.0) * 110.0, 1)
    calculated_web_range = max(100.0, min(260.0, calculated_web_range))

    with col_physics:
        st.subheader("📐 유도된 물리·역학적 지표 및 수식 모델")

        st.latex(r"E \approx 3 \rho_x R T \quad \implies \quad v_{\text{zip}} \propto \sqrt{\frac{E}{\rho_{\text{fiber}}}}")
        st.caption("• **고무 탄성 이론**: 가교 밀도(ρ_x)가 증가하면 탄성 영률(E)이 올라 비행 추진 속도가 증가합니다.")

        st.latex(r"Q = \frac{\pi r^4 \Delta P}{8 \mu L}, \quad v_0 = \sqrt{\frac{2 \Delta P}{\rho_{\text{fluid}}}} \quad \implies \quad R_{\max} \propto \frac{v_0^2}{g}")
        st.caption("• **베르누이 및 사출 동역학**: 노즐 챔버 압력(ΔP)이 강할수록 분사 속도(v₀)와 최대 사정거리(R_max)가 증가합니다.")

        st.markdown("---")
        m1, m2 = st.columns(2)
        m1.metric("계산된 영률 (Young's Modulus)", f"{youngs_modulus_gpa:.2f} GPa", delta=f"{crosslink_density} x10⁴ mol/m³")
        m2.metric("노즐 초기 사출 유속 (v₀)", f"{v_exit:.1f} m/s", delta=f"{injection_pressure} MPa")

        m3, m4 = st.columns(2)
        m3.metric("최종 웹 추진 속도 (Speed)", f"{calculated_web_speed} km/h")
        m4.metric("최종 유효 사정거리 (Max Range)", f"{calculated_web_range} m")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 위 물리역학 파라미터를 3D 웹슈터에 주입하기", use_container_width=True, type="primary"):
            st.session_state.web_color = selected_color
            st.session_state.web_speed = calculated_web_speed
            st.session_state.web_range = calculated_web_range
            st.session_state.web_thickness = selected_thickness
            st.success(f"생체역학 파라미터가 장착되었습니다! (탄성 견인 속도: {calculated_web_speed} km/h, 사정거리: {calculated_web_range} m)")

# ==================== [TAB 1: 3D 시티 게임 (물리 리포트 기능 탑재)] ====================
with tab_game:
    current_web_color = int(st.session_state.web_color.replace("#", "0x"), 16)
    current_web_speed = float(st.session_state.web_speed)
    current_web_range = float(st.session_state.web_range)
    current_web_thickness = int(st.session_state.web_thickness)

    game_html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
    <meta charset="utf-8">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
        html, body {{ 
            width: 100%; 
            height: 100vh; 
            overflow: hidden; 
            background: #0a1128; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        }}
        #canvas-container {{ 
            width: 100%; 
            height: 100%; 
            position: absolute; 
            top: 0; 
            left: 0; 
            cursor: grab; 
            outline: none;
        }}
        #canvas-container:active {{ cursor: grabbing; }}
        
        #hud {{
            position: absolute;
            top: 15px;
            left: 15px;
            color: #fff;
            z-index: 10;
            pointer-events: none;
            display: flex;
            gap: 10px;
        }}
        .hud-card {{
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 8px 14px;
            backdrop-filter: blur(4px);
        }}
        .hud-title {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94a3b8;
            font-weight: 700;
        }}
        .hud-val {{
            font-size: 18px;
            font-weight: 900;
            color: #38bdf8;
        }}
        .hud-val span {{ font-size: 11px; color: #64748b; font-weight: 600; }}

        #end-game-btn {{
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 20;
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: 800;
            font-size: 13px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
            transition: transform 0.15s ease;
        }}
        #end-game-btn:hover {{ transform: scale(1.05); }}

        #stunt-alert {{
            position: absolute;
            top: 75px;
            left: 50%;
            transform: translateX(-50%) scale(0.8);
            color: #facc15;
            font-size: 22px;
            font-weight: 900;
            letter-spacing: 2px;
            text-shadow: 0 0 15px rgba(250, 204, 21, 0.8);
            opacity: 0;
            pointer-events: none;
            z-index: 15;
            transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        #stunt-alert.show {{
            opacity: 1;
            transform: translateX(-50%) scale(1.15);
        }}

        #hit-vignette {{
            position: absolute;
            inset: 0;
            box-shadow: inset 0 0 50px rgba(239, 68, 68, 0.7);
            opacity: 0;
            pointer-events: none;
            z-index: 25;
            transition: opacity 0.15s ease;
        }}
        
        #controls-guide {{
            position: absolute;
            bottom: 15px;
            left: 15px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 10px 14px;
            color: #e2e8f0;
            font-size: 12px;
            line-height: 1.5;
            z-index: 10;
            pointer-events: none;
        }}
        .key-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 1px 5px;
            border-radius: 4px;
            font-weight: 700;
            color: #38bdf8;
        }}

        .overlay-screen {{
            position: absolute;
            inset: 0;
            background: rgba(11, 14, 20, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #fff;
            z-index: 100;
            transition: opacity 0.3s ease;
        }}
        
        #report-modal {{
            background: rgba(15, 23, 42, 0.95);
            border: 2px solid #38bdf8;
            border-radius: 16px;
            padding: 24px 32px;
            width: min(640px, 92vw);
            box-shadow: 0 10px 40px rgba(56, 189, 248, 0.3);
            text-align: center;
        }}
        .report-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
            margin: 20px 0;
            text-align: left;
        }}
        .report-card {{
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 12px 16px;
        }}
        .report-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; margin-bottom: 4px; }}
        .report-value {{ font-size: 20px; font-weight: 900; color: #38bdf8; }}
        .report-formula {{ font-size: 10px; color: #64748b; margin-top: 2px; }}
        .restart-btn {{
            background: #0284c7;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>

    <div id="hit-vignette"></div>

    <div id="start-overlay" class="overlay-screen" style="cursor: pointer;">
        <h1 style="font-size: 32px; font-weight: 900; margin-bottom: 8px; color: #ef4444; letter-spacing: 1px;">🕷️ SPIDER-MAN 3D CITY</h1>
        <p style="font-size: 14px; color: #cbd5e1; background: rgba(255, 255, 255, 0.1); padding: 8px 18px; border-radius: 20px;">▶ 클릭하여 비행 시작 (종료 시 물리 분석 리포트 제공)</p>
    </div>

    <div id="report-overlay" class="overlay-screen" style="display: none;">
        <div id="report-modal">
            <h2 style="font-size: 24px; font-weight: 900; color: #f8fafc; letter-spacing: 1px;">📊 비행 역학 분석 리포트</h2>
            <p style="font-size: 12px; color: #94a3b8; margin-top: 4px;">기준 질량: 스파이더맨 m = 65.0 kg | 완충 지속 시간: Δt = 0.05 s</p>
            
            <div class="report-grid">
                <div class="report-card">
                    <div class="report-label">최대 속력 (Max Speed)</div>
                    <div class="report-value" id="rep-max-speed">0.0 km/h</div>
                    <div class="report-formula">v_max (SI: 0.0 m/s)</div>
                </div>
                <div class="report-card">
                    <div class="report-label">최대 운동량 (Max Momentum)</div>
                    <div class="report-value" id="rep-max-p">0.0 kg·m/s</div>
                    <div class="report-formula">p = m · v_max</div>
                </div>
                <div class="report-card">
                    <div class="report-label">최대 충격량 (Peak Impulse)</div>
                    <div class="report-value" id="rep-max-impulse">0.0 N·s</div>
                    <div class="report-formula">I = |Δp| = m · |Δv|</div>
                </div>
                <div class="report-card">
                    <div class="report-label">최대 충격력 (Peak Impact Force)</div>
                    <div class="report-value" id="rep-max-force">0.0 N</div>
                    <div class="report-formula">F_avg = I / Δt</div>
                </div>
                <div class="report-card" style="grid-column: span 2;">
                    <div class="report-label">최대 운동 에너지 (Max Kinetic Energy)</div>
                    <div class="report-value" id="rep-max-ke" style="color: #facc15;">0.0 J</div>
                    <div class="report-formula">E_k = 1/2 · m · v²</div>
                </div>
            </div>

            <button class="restart-btn" id="restart-btn">🔄 다시 비행하기</button>
        </div>
    </div>

    <button id="end-game-btn">🏁 비행 종료 & 역학 분석</button>

    <div id="hud">
        <div class="hud-card">
            <div class="hud-title">현재 속력</div>
            <div class="hud-val" id="speed-meter">0 <span>km/h</span></div>
        </div>
        <div class="hud-card">
            <div class="hud-title">순간 운동량 (p)</div>
            <div class="hud-val" id="hud-momentum">0 <span>kg·m/s</span></div>
        </div>
        <div class="hud-card">
            <div class="hud-title">골든 링</div>
            <div class="hud-val" id="ring-score">0 <span>/ 10</span></div>
        </div>
    </div>

    <div id="stunt-alert">✨ ACROBATIC FLIP! ✨</div>

    <div id="controls-guide">
        • <span class="key-badge">건물 클릭</span> 웹스윙 견인 | <span class="key-badge">W,A,S,D</span> 방향 조타<br>
        • <span class="key-badge">Space</span> 점프 | <span class="key-badge">더블 Space</span> <b>공중제비 슈퍼점프</b><br>
        • 우측 상단 <b>[비행 종료]</b> 클릭 시 역학 분석 리포트 팝업
    </div>

    <div id="canvas-container" tabindex="0"></div>

    <script>
        const WEB_COLOR = {current_web_color};
        const WEB_SPEED = {current_web_speed};
        const WEB_RANGE = {current_web_range};
        const WEB_THICKNESS = {current_web_thickness};
        const PLAYER_MASS = 65.0;
        const IMPACT_DT = 0.05;

        const physicsLogger = {{
            maxSpeed: 0.0,
            maxMomentum: 0.0,
            maxImpulse: 0.0,
            maxForce: 0.0,
            maxKineticEnergy: 0.0,
            reset: function() {{
                this.maxSpeed = 0.0;
                this.maxMomentum = 0.0;
                this.maxImpulse = 0.0;
                this.maxForce = 0.0;
                this.maxKineticEnergy = 0.0;
            }}
        }};

        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a1128);
        scene.fog = new THREE.FogExp2(0x0a1128, 0.005);

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        scene.add(new THREE.HemisphereLight(0xff7744, 0x111122, 0.7));
        const dirLight = new THREE.DirectionalLight(0xffaa44, 1.2);
        dirLight.position.set(100, 150, 70);
        scene.add(dirLight);

        const buildings = [];
        const buildingColliders = [];

        const winCanvas = document.createElement('canvas');
        winCanvas.width = 128;
        winCanvas.height = 128;
        const wCtx = winCanvas.getContext('2d');
        wCtx.fillStyle = '#1e2640';
        wCtx.fillRect(0,0,128,128);
        wCtx.fillStyle = '#fde047';
        for(let i=8; i<128; i+=22){{
            for(let j=8; j<128; j+=22){{
                if(Math.random() > 0.45) wCtx.fillRect(i, j, 12, 14);
            }}
        }}
        const winTexture = new THREE.CanvasTexture(winCanvas);
        winTexture.wrapS = THREE.RepeatWrapping;
        winTexture.wrapT = THREE.RepeatWrapping;

        const bldgMat = new THREE.MeshStandardMaterial({{ map: winTexture, roughness: 0.35, metalness: 0.3 }});
        const roofMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.8 }});

        const CITY_SIZE = 10;
        const SPACING = 42;

        for (let x = -CITY_SIZE/2; x < CITY_SIZE/2; x++) {{
            for (let z = -CITY_SIZE/2; z < CITY_SIZE/2; z++) {{
                if (Math.abs(x) < 2 && Math.abs(z) < 2) continue;
                const h = 40 + Math.random() * 80;
                const w = 18 + Math.random() * 12;
                const d = 18 + Math.random() * 12;
                const posX = x * SPACING + (Math.random()-0.5)*8;
                const posZ = z * SPACING + (Math.random()-0.5)*8;

                const bldg = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), bldgMat);
                bldg.position.set(posX, h/2, posZ);
                scene.add(bldg);
                buildings.push(bldg);

                buildingColliders.push({{
                    minX: posX - w/2 - 0.7, maxX: posX + w/2 + 0.7,
                    minZ: posZ - d/2 - 0.7, maxZ: posZ + d/2 + 0.7,
                    topY: h
                }});
            }}
        }}

        const floor = new THREE.Mesh(
            new THREE.PlaneGeometry(800, 800),
            new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.9 }})
        );
        floor.rotation.x = -Math.PI / 2;
        scene.add(floor);

        const rings = [];
        const ringGeo = new THREE.TorusGeometry(3.5, 0.4, 10, 20);
        const ringMat = new THREE.MeshBasicMaterial({{ color: 0xfacc15, wireframe: true }});
        for (let i = 0; i < 10; i++) {{
            const ring = new THREE.Mesh(ringGeo, ringMat);
            ring.position.set((Math.random() - 0.5) * 220, 25 + Math.random() * 45, (Math.random() - 0.5) * 220);
            scene.add(ring);
            rings.push(ring);
        }}
        let ringCount = 0;

        const playerGroup = new THREE.Group();
        scene.add(playerGroup);

        const flipMeshGroup = new THREE.Group();
        playerGroup.add(flipMeshGroup);

        const torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.2, 0.5), new THREE.MeshStandardMaterial({{ color: 0xdc2626 }}));
        torso.position.y = 0.9;
        flipMeshGroup.add(torso);

        const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), new THREE.MeshStandardMaterial({{ color: 0xdc2626 }}));
        head.position.y = 1.75;
        flipMeshGroup.add(head);

        const legs = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.9, 0.45), new THREE.MeshStandardMaterial({{ color: 0x2563eb }}));
        legs.position.y = 0.35;
        flipMeshGroup.add(legs);

        const webMat = new THREE.LineBasicMaterial({{ color: WEB_COLOR, linewidth: WEB_THICKNESS }});
        const webGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
        const webLine = new THREE.Line(webGeo, webMat);
        webLine.visible = false;
        scene.add(webLine);

        const player = {{
            pos: new THREE.Vector3(0, 25, 0),
            vel: new THREE.Vector3(),
            isGrounded: false,
            isWebZipping: false,
            zipTarget: new THREE.Vector3(),
            canDoubleJump: true,
            isFlipping: false,
            flipProgress: 0
        }};

        let yaw = 0, pitch = 0.2;
        let isDragging = false;
        let startMouseX = 0, startMouseY = 0;
        let clickStartX = 0, clickStartY = 0;
        let isSimRunning = false;

        const overlay = document.getElementById('start-overlay');
        const reportOverlay = document.getElementById('report-overlay');
        const endBtn = document.getElementById('end-game-btn');
        const restartBtn = document.getElementById('restart-btn');

        overlay.addEventListener('click', () => {{
            overlay.style.opacity = '0';
            setTimeout(() => {{ overlay.style.display = 'none'; }}, 300);
            isSimRunning = true;
            physicsLogger.reset();
            container.focus();
        }});

        endBtn.addEventListener('click', () => {{
            isSimRunning = false;
            player.vel.set(0, 0, 0);
            webLine.visible = false;

            document.getElementById('rep-max-speed').innerHTML = `${{(physicsLogger.maxSpeed * 3.6).toFixed(1)}} <span>km/h</span>`;
            document.querySelector('#rep-max-speed + .report-formula').innerText = `v_max (SI: ${{physicsLogger.maxSpeed.toFixed(2)}} m/s)`;
            document.getElementById('rep-max-p').innerHTML = `${{physicsLogger.maxMomentum.toFixed(1)}} <span>kg·m/s</span>`;
            document.getElementById('rep-max-impulse').innerHTML = `${{physicsLogger.maxImpulse.toFixed(1)}} <span>N·s</span>`;
            document.getElementById('rep-max-force').innerHTML = `${{physicsLogger.maxForce.toFixed(1)}} <span>N</span>`;
            document.getElementById('rep-max-ke').innerHTML = `${{physicsLogger.maxKineticEnergy.toFixed(1)}} <span>J</span>`;

            reportOverlay.style.display = 'flex';
        }});

        restartBtn.addEventListener('click', () => {{
            reportOverlay.style.display = 'none';
            player.pos.set(0, 25, 0);
            player.vel.set(0, 0, 0);
            ringCount = 0;
            document.getElementById('ring-score').innerHTML = `0 <span>/ 10</span>`;
            rings.forEach(r => r.visible = true);
            physicsLogger.reset();
            isSimRunning = true;
            container.focus();
        }});

        const keys = {{}};
        let lastSpaceTime = 0;
        const stuntAlert = document.getElementById('stunt-alert');
        const hitVignette = document.getElementById('hit-vignette');
        let alertTimeout = null;

        function triggerStuntAlert() {{
            stuntAlert.classList.add('show');
            if (alertTimeout) clearTimeout(alertTimeout);
            alertTimeout = setTimeout(() => {{ stuntAlert.classList.remove('show'); }}, 800);
        }}

        function triggerHitEffect() {{
            hitVignette.style.opacity = '1';
            setTimeout(() => {{ hitVignette.style.opacity = '0'; }}, 200);
        }}

        window.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
            if (e.code === 'Space') {{
                const now = performance.now();
                const diff = now - lastSpaceTime;

                if (player.isGrounded) {{
                    player.vel.y = 20.0;
                    player.isGrounded = false;
                    player.canDoubleJump = true;
                }} else {{
                    if (player.isWebZipping) {{
                        player.isWebZipping = false;
                        webLine.visible = false;
                        player.vel.y = Math.max(player.vel.y, 22.0);
                        player.canDoubleJump = true;
                    }} else if (diff < 350 && player.canDoubleJump) {{
                        player.vel.y = 28.0;
                        const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
                        player.vel.add(forward.multiplyScalar(16.0));
                        player.canDoubleJump = false;
                        player.isFlipping = true;
                        player.flipProgress = 0;
                        triggerStuntAlert();
                    }}
                }}
                lastSpaceTime = now;
            }}
        }});

        window.addEventListener('keyup', (e) => {{ keys[e.code] = false; }});

        container.addEventListener('mousedown', (e) => {{
            isDragging = true;
            startMouseX = e.clientX;
            startMouseY = e.clientY;
            clickStartX = e.clientX;
            clickStartY = e.clientY;
        }});

        window.addEventListener('mousemove', (e) => {{
            if (!isDragging) return;
            const dx = e.clientX - startMouseX;
            const dy = e.clientY - startMouseY;
            startMouseX = e.clientX;
            startMouseY = e.clientY;
            yaw -= dx * 0.005;
            pitch = Math.max(-0.4, Math.min(1.2, pitch + dy * 0.005));
        }});

        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        window.addEventListener('mouseup', (e) => {{
            if (!isDragging) return;
            isDragging = false;
            const moveDist = Math.hypot(e.clientX - clickStartX, e.clientY - clickStartY);
            if (moveDist < 6 && isSimRunning) {{
                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

                raycaster.setFromCamera(mouse, camera);
                raycaster.far = WEB_RANGE;
                const hits = raycaster.intersectObjects(buildings);

                if (hits.length > 0 && hits[0].point.y > 4) {{
                    player.isWebZipping = true;
                    player.zipTarget.copy(hits[0].point);
                    webLine.visible = true;
                    player.canDoubleJump = true;
                }}
            }}
        }});

        function resolveBuildingCollisions() {{
            const px = player.pos.x;
            const py = player.pos.y;
            const pz = player.pos.z;

            for (let b of buildingColliders) {{
                if (px > b.minX && px < b.maxX && pz > b.minZ && pz < b.maxZ) {{
                    if (py >= b.topY - 1.0 && player.vel.y <= 0) {{
                        player.pos.y = b.topY;
                        player.vel.y = 0;
                        player.isGrounded = true;
                        player.canDoubleJump = true;
                        if (player.isWebZipping) {{
                            player.isWebZipping = false;
                            webLine.visible = false;
                        }}
                        return;
                    }} 
                    else if (py < b.topY) {{
                        const pushLeft = px - b.minX;
                        const pushRight = b.maxX - px;
                        const pushFront = pz - b.minZ;
                        const pushBack = b.maxZ - pz;
                        const minOverlap = Math.min(pushLeft, pushRight, pushFront, pushBack);

                        if (minOverlap === pushLeft) player.pos.x = b.minX;
                        else if (minOverlap === pushRight) player.pos.x = b.maxX;
                        else if (minOverlap === pushFront) player.pos.z = b.minZ;
                        else if (minOverlap === pushBack) player.pos.z = b.maxZ;

                        if (player.isWebZipping) {{
                            player.isWebZipping = false;
                            webLine.visible = false;
                        }}

                        const preVx = player.vel.x;
                        const preVz = player.vel.z;
                        player.vel.x *= -0.2;
                        player.vel.z *= -0.2;

                        const deltaVx = player.vel.x - preVx;
                        const deltaVz = player.vel.z - preVz;
                        const deltaV = Math.hypot(deltaVx, deltaVz);

                        const impulse = PLAYER_MASS * deltaV;
                        const impactForce = impulse / IMPACT_DT;

                        if (impulse > physicsLogger.maxImpulse) {{
                            physicsLogger.maxImpulse = impulse;
                            physicsLogger.maxForce = impactForce;
                        }}
                        triggerHitEffect();
                    }}
                }}
            }}
        }}

        const clock = new THREE.Clock();
        const speedMeter = document.getElementById('speed-meter');
        const hudMomentum = document.getElementById('hud-momentum');
        const ringScore = document.getElementById('ring-score');

        function animate() {{
            requestAnimationFrame(animate);
            const delta = Math.min(clock.getDelta(), 0.05);

            if (!isSimRunning) {{
                renderer.render(scene, camera);
                return;
            }}

            const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
            const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw)).normalize();

            const move = new THREE.Vector3();
            if (keys['KeyW'] || keys['ArrowUp']) move.add(forward);
            if (keys['KeyS'] || keys['ArrowDown']) move.sub(forward);
            if (keys['KeyD'] || keys['ArrowRight']) move.add(right);
            if (keys['KeyA'] || keys['ArrowLeft']) move.sub(right);
            if (move.lengthSq() > 0) move.normalize();

            if (player.isWebZipping) {{
                const toTarget = new THREE.Vector3().subVectors(player.zipTarget, player.pos);
                const dist = toTarget.length();

                if (dist < 4.0) {{
                    player.isWebZipping = false;
                    webLine.visible = false;
                    player.vel.y = Math.max(player.vel.y, 20.0);
                }} else {{
                    const pullDir = toTarget.normalize();
                    const targetSpeed = Math.min(dist * 2.8, WEB_SPEED * 0.45);
                    player.vel.lerp(pullDir.multiplyScalar(targetSpeed), delta * 5.0);

                    if (keys['KeyA']) player.vel.add(right.clone().multiplyScalar(-10));
                    if (keys['KeyD']) player.vel.add(right.clone().multiplyScalar(10));

                    const pts = new Float32Array([
                        player.pos.x, player.pos.y + 0.8, player.pos.z,
                        player.zipTarget.x, player.zipTarget.y, player.zipTarget.z
                    ]);
                    webLine.geometry.setAttribute('position', new THREE.BufferAttribute(pts, 3));
                }}
            }} else {{
                const controlPower = player.isGrounded ? 55.0 : 42.0;
                player.vel.x += move.x * controlPower * delta;
                player.vel.z += move.z * controlPower * delta;

                player.vel.y -= 36.0 * delta;
                const damp = player.isGrounded ? 6.0 : 1.2;
                player.vel.x *= Math.max(0, 1 - damp * delta);
                player.vel.z *= Math.max(0, 1 - damp * delta);
            }}

            if (player.isFlipping) {{
                player.flipProgress += delta * 12.0;
                flipMeshGroup.rotation.x = player.flipProgress;
                if (player.flipProgress >= Math.PI * 2) {{
                    player.flipProgress = 0;
                    flipMeshGroup.rotation.x = 0;
                    player.isFlipping = false;
                }}
            }} else {{
                flipMeshGroup.rotation.x = 0;
            }}

            player.pos.addScaledVector(player.vel, delta);
            resolveBuildingCollisions();

            if (player.pos.y <= 0.6) {{
                player.pos.y = 0.6;
                player.vel.y = 0;
                player.isGrounded = true;
                player.canDoubleJump = true;
                if (player.isWebZipping) {{
                    player.isWebZipping = false;
                    webLine.visible = false;
                }}
            }}

            playerGroup.position.copy(player.pos);
            if (player.vel.lengthSq() > 1.0) {{
                playerGroup.rotation.y = Math.atan2(player.vel.x, player.vel.z);
            }}
