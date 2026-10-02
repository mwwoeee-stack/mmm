import streamlit as st
import streamlit.components.v1 as components
import math

# 1. 스트림릿 와이드 모드 설정
st.set_page_config(
    page_title="Spider-Man Biomechanics Lab & Boss Battle Evolution",
    page_icon="🕷️️",
    st.set_page_config(
    page_title="Spider-Man Biomechanics Lab & Boss Battle Evolution",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded",  # <-- 항상 열어두기로 변경!
)
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 기본 UI 여백 정리
st.markdown("""
<style>
    .block-container {
        padding: 0.8rem 1.2rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
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

    # [피터 파커의 추천 프리셋 데이터 정의]
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
        "⚖️️ [피터의 추천 4] 데일리 순찰 밸런스형 (Standard Daily)": {
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

    # 피터 파커의 퀵 가이드 및 추천 프리셋 선택창
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

    # 물리 역학 계산식
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
            background: #0b0e14; 
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

            const camDist = 6.8;
            const camH = 2.6;
            camera.position.set(
                player.pos.x + Math.sin(yaw) * Math.cos(pitch) * camDist,
                player.pos.y + Math.sin(pitch) * camDist + camH,
                player.pos.z + Math.cos(yaw) * Math.cos(pitch) * camDist
            );
            camera.lookAt(player.pos.x, player.pos.y + 1.2, player.pos.z);

            rings.forEach(ring => {{
                ring.rotation.y += 0.02;
                if (ring.visible && player.pos.distanceTo(ring.position) < 5.0) {{
                    ring.visible = false;
                    ringCount++;
                    ringScore.innerHTML = `${{ringCount}} <span>/ 10</span>`;
                    player.vel.y = Math.max(player.vel.y, 18);
                    player.vel.add(forward.clone().multiplyScalar(22));
                    player.canDoubleJump = true;
                }}
            }});

            const currentSpeed = player.vel.length();
            const currentMomentum = PLAYER_MASS * currentSpeed;
            const currentKE = 0.5 * PLAYER_MASS * currentSpeed * currentSpeed;

            if (currentSpeed > physicsLogger.maxSpeed) {{
                physicsLogger.maxSpeed = currentSpeed;
                physicsLogger.maxMomentum = currentMomentum;
                physicsLogger.maxKineticEnergy = currentKE;
            }}

            speedMeter.innerHTML = `${{Math.round(currentSpeed * 3.6)}} <span>km/h</span>`;
            hudMomentum.innerHTML = `${{Math.round(currentMomentum)}} <span>kg·m/s</span>`;

            renderer.render(scene, camera);
        }}

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        animate();
    </script>
    </body>
    </html>
    """

    components.html(game_html, height=840, scrolling=False)

# ==================== [TAB 3: 보스전 (빌런 진화 + 능력 업그레이드 시스템)] ====================
with tab_boss:
    boss_web_color = int(st.session_state.web_color.replace("#", "0x"), 16)
    boss_web_speed = float(st.session_state.web_speed)

    boss_html = f"""
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
            background: #060814; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        }}
        #boss-canvas {{ 
            width: 100%; 
            height: 100%; 
            position: absolute; 
            top: 0; 
            left: 0; 
            cursor: crosshair; 
            outline: none;
        }}
        #boss-ui {{ 
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            width: min(700px, 92vw);
            z-index: 10;
            display: flex;
            flex-direction: column;
            gap: 6px;
            pointer-events: none;
            background: rgba(15, 23, 42, 0.88);
            padding: 12px 18px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        }}
        .boss-header {{
            display: flex;
            justify-content: space-between;
            color: #ef4444;
            font-weight: 900;
            letter-spacing: 1.5px;
            font-size: 15px;
        }}
        .boss-hp-bg {{
            width: 100%;
            height: 16px;
            background: #1e293b;
            border-radius: 8px;
            overflow: hidden;
        }}
        #boss-hp-bar {{
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, #dc2626, #f97316);
            transition: width 0.15s ease-out;
        }}
        .bind-header {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            font-weight: 800;
            color: #38bdf8;
            margin-top: 2px;
        }}
        .boss-bind-bg {{
            width: 100%;
            height: 14px;
            background: #0f172a;
            border-radius: 7px;
            overflow: hidden;
            border: 1px solid #0284c7;
        }}
        #boss-bind-bar {{
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, #38bdf8, #ffffff);
            box-shadow: 0 0 10px #38bdf8;
            transition: width 0.15s ease;
        }}
        #player-ui {{
            position: absolute;
            top: 15px;
            left: 15px;
            z-index: 10;
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 12px 16px;
            color: #fff;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .bar-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; display: flex; justify-content: space-between; }}
        .bar-bg {{ width: 170px; height: 11px; background: #1e293b; border-radius: 5px; overflow: hidden; }}
        #player-hp-bar {{ width: 100%; height: 100%; background: #22c55e; transition: width 0.2s ease; }}
        #ult-bar {{ width: 0%; height: 100%; background: linear-gradient(90deg, #06b6d4, #facc15); transition: width 0.15s ease; }}
        #ult-ready-tag {{
            font-size: 11px;
            color: #facc15;
            font-weight: 900;
            display: none;
            animation: blink 0.8s infinite;
        }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}

        .stat-badge {{
            font-size: 11px;
            color: #38bdf8;
            font-weight: 700;
            background: rgba(56, 189, 248, 0.15);
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}

        #action-banner {{
            position: absolute;
            top: 130px;
            left: 50%;
            transform: translateX(-50%) scale(0.85);
            font-size: 26px;
            font-weight: 900;
            letter-spacing: 2px;
            opacity: 0;
            pointer-events: none;
            z-index: 20;
            text-align: center;
            transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-shadow: 0 0 20px rgba(0,0,0,0.8);
        }}
        #action-banner.show {{
            opacity: 1;
            transform: translateX(-50%) scale(1.1);
        }}

        #boss-guide {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 12px 18px;
            color: #e2e8f0;
            font-size: 12px;
            line-height: 1.6;
            z-index: 10;
            pointer-events: none;
        }}
        .badge {{
            background: rgba(255, 255, 255, 0.2);
            padding: 1px 6px;
            border-radius: 4px;
            color: #38bdf8;
            font-weight: 700;
        }}
        .ult-badge {{
            background: rgba(245, 158, 11, 0.3);
            border: 1px solid #f59e0b;
            color: #fbbf24;
            padding: 1px 6px;
            border-radius: 4px;
            font-weight: 900;
        }}

        #hit-overlay {{
            position: absolute;
            inset: 0;
            box-shadow: inset 0 0 60px rgba(239, 68, 68, 0.8);
            opacity: 0;
            pointer-events: none;
            z-index: 30;
            transition: opacity 0.15s ease;
        }}

        /* 모달 화면 공통 */
        .full-overlay {{
            position: absolute;
            inset: 0;
            background: rgba(6, 8, 20, 0.94);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #fff;
            z-index: 100;
        }}

        /* 레벨업 선택 모달 */
        #upgrade-modal {{
            background: rgba(15, 23, 42, 0.96);
            border: 2px solid #facc15;
            border-radius: 18px;
            padding: 28px 36px;
            width: min(680px, 92vw);
            text-align: center;
            box-shadow: 0 0 50px rgba(250, 204, 21, 0.3);
        }}
        .upgrade-card-box {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin: 22px 0 10px 0;
        }}
        .upgrade-card {{
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 16px 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .upgrade-card:hover {{
            transform: translateY(-5px);
            border-color: #38bdf8;
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4);
            background: rgba(30, 58, 138, 0.6);
        }}
        .card-icon {{ font-size: 32px; margin-bottom: 8px; }}
        .card-title {{ font-size: 14px; font-weight: 800; color: #f8fafc; margin-bottom: 6px; }}
        .card-desc {{ font-size: 11px; color: #94a3b8; line-height: 1.4; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>

    <div id="hit-overlay"></div>
    <div id="action-banner"></div>

    <!-- 시작 및 패배/엔딩 모달 -->
    <div id="modal-screen" class="full-overlay" style="cursor: pointer;">
        <h1 id="modal-title" style="font-size: 34px; color: #38bdf8; letter-spacing: 2px; margin-bottom: 12px;">⚔️ SPIDER-MAN BOSS RAID</h1>
        <p id="modal-desc" style="font-size: 15px; color: #cbd5e1; background: rgba(255, 255, 255, 0.1); padding: 10px 22px; border-radius: 20px;">▶ 화면을 클릭하여 Stage 1 [그린 고블린] 레이드 시작!</p>
    </div>

    <!-- 레벨업 스킬 선택 모달 -->
    <div id="upgrade-overlay" class="full-overlay" style="display: none;">
        <div id="upgrade-modal">
            <h2 style="font-size: 28px; font-weight: 900; color: #facc15; letter-spacing: 1px;">🎉 LEVEL UP & 능력 강화!</h2>
            <p id="level-reward-desc" style="font-size: 14px; color: #cbd5e1; margin-top: 6px;">빌런을 물리치고 다음 단계로 진화합니다. 강화할 역학 능력을 선택하세요!</p>
            
            <div class="upgrade-card-box">
                <div class="upgrade-card" onclick="chooseUpgrade('dmg')">
                    <div class="card-icon">💥</div>
                    <div class="card-title">고분자 인장 강화</div>
                    <div class="card-desc">거미줄 타격 위력 대폭 증가 (+15 Damage)</div>
                </div>
                <div class="upgrade-card" onclick="chooseUpgrade('gauge')">
                    <div class="card-icon">⚡</div>
                    <div class="card-title">슈퍼 나노 반응로</div>
                    <div class="card-desc">명중 시 궁극기 게이지 충전량 2배 (+40% 차지)</div>
                </div>
                <div class="upgrade-card" onclick="chooseUpgrade('heal')">
                    <div class="card-icon">🛡️</div>
                    <div class="card-title">생체 탄성 슈트</div>
                    <div class="card-desc">체력 100% 완전 회복 & 이동 기동력 25% 상승</div>
                </div>
            </div>
        </div>
    </div>

    <div id="player-ui">
        <div>
            <div class="bar-label"><span>SPIDER HP</span><span id="player-hp-text">100%</span></div>
            <div class="bar-bg"><div id="player-hp-bar"></div></div>
        </div>
        <div>
            <div class="bar-label">
                <span>ULTIMATE WEB BLOSSOM</span>
                <span id="ult-ready-tag">READY [Q]!</span>
            </div>
            <div class="bar-bg"><div id="ult-bar"></div></div>
        </div>
        <div style="display: flex; gap: 6px; margin-top: 4px;">
            <span class="stat-badge" id="player-lvl-tag">LV 1 스파이더맨</span>
            <span class="stat-badge" id="player-dmg-tag">웹 위력 10</span>
        </div>
    </div>

    <!-- 보스 UI -->
    <div id="boss-ui">
        <div class="boss-header">
            <span id="boss-name-tag">😈 [STAGE 1] GREEN GOBLIN</span>
            <span id="boss-hp-text">HP 100%</span>
        </div>
        <div class="boss-hp-bg"><div id="boss-hp-bar"></div></div>
        
        <div class="bind-header">
            <span>🕸️ 거미줄 포박 진행도 (WEB BINDING)</span>
            <span id="boss-bind-text">0%</span>
        </div>
        <div class="boss-bind-bg"><div id="boss-bind-bar"></div></div>
    </div>

    <div id="boss-guide">
        • <span class="badge">좌클릭</span> 마우스 방향 정확 조준 발사 (포박 시 바닥 추락 & 기절!)<br>
        • <span class="ult-badge">Q / 우클릭</span> 궁극기 [웹 블라섬] 발동 | <span class="badge">벽면 W</span> 수직 벽타기<br>
        • 적 격파 시 <b>레벨업 & 상위 빌런(일렉트로, 베놈)</b> 순차 소환!
    </div>

    <div id="boss-canvas" tabindex="0"></div>

    <script>
        const container = document.getElementById('boss-canvas');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x060814);
        scene.fog = new THREE.FogExp2(0x060814, 0.007);

        const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 900);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        scene.add(new THREE.HemisphereLight(0x38bdf8, 0x1e1b4b, 0.8));
        const dirLight = new THREE.DirectionalLight(0xffeedd, 1.2);
        dirLight.position.set(50, 120, 60);
        scene.add(dirLight);

        // 아레나 바닥
        const arena = new THREE.Mesh(
            new THREE.BoxGeometry(140, 4, 140),
            new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.6 }})
        );
        arena.position.y = -2;
        scene.add(arena);

        // 등반 타워
        const climbBuildings = [];
        const towerGeo = new THREE.BoxGeometry(18, 55, 18);
        const towerMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.4 }});
        const towerPositions = [
            [-35, 27.5, -35], [35, 27.5, -35],
            [-35, 27.5, 35],  [35, 27.5, 35]
        ];
        towerPositions.forEach(pos => {{
            const tower = new THREE.Mesh(towerGeo, towerMat);
            tower.position.set(pos[0], pos[1], pos[2]);
            scene.add(tower);
            climbBuildings.push({{
                minX: pos[0] - 9.5, maxX: pos[0] + 9.5,
                minZ: pos[2] - 9.5, maxZ: pos[2] + 9.5,
                topY: 55
            }});
        }});

        // 플레이어 모델
        const playerGroup = new THREE.Group();
        scene.add(playerGroup);

        const torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.2, 0.5), new THREE.MeshStandardMaterial({{ color: 0xdc2626 }}));
        torso.position.y = 0.9;
        playerGroup.add(torso);

        const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), new THREE.MeshStandardMaterial({{ color: 0xdc2626 }}));
        head.position.y = 1.75;
        playerGroup.add(head);

        const legs = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.9, 0.45), new THREE.MeshStandardMaterial({{ color: 0x2563eb }}));
        legs.position.y = 0.35;
        playerGroup.add(legs);

        // 플레이어 스탯 & RPG 데이터
        const player = {{
            pos: new THREE.Vector3(0, 0, 30),
            vel: new THREE.Vector3(),
            hp: 100,
            maxHp: 100,
            level: 1,
            damage: 10,
            ultPerHit: 20,
            speedMulti: 1.0,
            ultGauge: 0,
            isGrounded: true,
            isWallClimbing: false,
            invulnerableTime: 2.0
        }};

        // 보스 데이터 정의 (3단계 진화)
        let currentStage = 1;
        const STAGE_CONFIG = {{
            1: {{
                name: "😈 [STAGE 1] GREEN GOBLIN",
                color: 0x16a34a,
                accentColor: 0x22c55e,
                speed: 0.45,
                attackInterval: 3.0,
                bombColor: 0xea580c,
                bindPerHit: 25,
                desc: "호박 폭탄을 투척하는 공중 글라이더 보스"
            }},
            2: {{
                name: "⚡ [STAGE 2] ELECTRO",
                color: 0x0284c7,
                accentColor: 0x38bdf8,
                speed: 0.85,
                attackInterval: 1.8,
                bombColor: 0x06b6d4,
                bindPerHit: 18,
                desc: "고속 회피 기동과 고전압 플라즈마를 난사하는 번개 보스"
            }},
            3: {{
                name: "🕷️ [STAGE 3] SYMBIOTE VENOM",
                color: 0x0f172a,
                accentColor: 0x475569,
                speed: 0.65,
                attackInterval: 1.2,
                bombColor: 0x881337,
                bindPerHit: 12,
                desc: "거대한 덩치와 무시무시한 심비오트 유도 탄환을 뿜어내는 최종 보스"
            }}
        }};

        // 보스 3D 메쉬 그룹
        const bossGroup = new THREE.Group();
        scene.add(bossGroup);

        const gliderMesh = new THREE.Mesh(
            new THREE.ConeGeometry(3.5, 6.5, 3),
            new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.8, roughness: 0.2 }})
        );
        gliderMesh.rotation.x = Math.PI / 2;
        gliderMesh.scale.set(1.5, 0.4, 0.8);
        bossGroup.add(gliderMesh);

        const bossBodyMat = new THREE.MeshStandardMaterial({{ color: 0x16a34a }});
        const bossBody = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 1.5, 12), bossBodyMat);
        bossBody.position.y = 1.0;
        bossGroup.add(bossBody);

        const bossHeadMat = new THREE.MeshStandardMaterial({{ color: 0x22c55e }});
        const bossHead = new THREE.Mesh(new THREE.SphereGeometry(0.45, 12, 12), bossHeadMat);
        bossHead.position.y = 2.0;
        bossGroup.add(bossHead);

        // 포박 와이어
        const webTrapGroup = new THREE.Group();
        const webLineMat = new THREE.LineBasicMaterial({{ color: 0xffffff, linewidth: 3 }});
        for (let i = 0; i < 14; i++) {{
            const p1 = new THREE.Vector3((Math.random()-0.5)*3.2, (Math.random()-0.5)*3.2 + 1, (Math.random()-0.5)*3.2);
            const p2 = new THREE.Vector3((Math.random()-0.5)*3.2, (Math.random()-0.5)*3.2 + 1, (Math.random()-0.5)*3.2);
            const lineGeo = new THREE.BufferGeometry().setFromPoints([p1, p2]);
            webTrapGroup.add(new THREE.Line(lineGeo, webLineMat));
        }}
        webTrapGroup.visible = false;
        bossGroup.add(webTrapGroup);

        const boss = {{
            pos: new THREE.Vector3(0, 12, -18),
            hp: 100,
            bindMeter: 0,
            stunTimer: 0,
            angle: 0,
            attackTimer: 0
        }};

        // 투사체
        const webBullets = [];
        const webBulletGeo = new THREE.SphereGeometry(0.65, 12, 12);
        const webBulletMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});

        const bossProjectiles = [];
        const projGeo = new THREE.SphereGeometry(0.65, 12, 12);

        // 조작 & UI 상태
        let isStarted = false;
        let isGameOver = false;
        let isUpgrading = false;
        let yaw = 0, pitch = 0.15;
        let isRightDragging = false;
        let startX = 0, startY = 0;
        const keys = {{}};

        const modalScreen = document.getElementById('modal-screen');
        const modalTitle = document.getElementById('modal-title');
        const modalDesc = document.getElementById('modal-desc');
        const upgradeOverlay = document.getElementById('upgrade-overlay');
        const bossNameTag = document.getElementById('boss-name-tag');
        const bossHpBar = document.getElementById('boss-hp-bar');
        const bossHpText = document.getElementById('boss-hp-text');
        const bossBindBar = document.getElementById('boss-bind-bar');
        const bossBindText = document.getElementById('boss-bind-text');
        const playerHpBar = document.getElementById('player-hp-bar');
        const playerHpText = document.getElementById('player-hp-text');
        const ultBar = document.getElementById('ult-bar');
        const ultReadyTag = document.getElementById('ult-ready-tag');
        const hitOverlay = document.getElementById('hit-overlay');
        const actionBanner = document.getElementById('action-banner');

        function showBanner(text, color) {{
            actionBanner.innerText = text;
            actionBanner.style.color = color;
            actionBanner.classList.add('show');
            setTimeout(() => {{ actionBanner.classList.remove('show'); }}, 1200);
        }}

        function setupBossStage(stage) {{
            const cfg = STAGE_CONFIG[stage];
            bossNameTag.innerText = cfg.name;
            bossBodyMat.color.setHex(cfg.color);
            bossHeadMat.color.setHex(cfg.accentColor);

            if (stage === 3) {{
                bossGroup.scale.set(1.5, 1.5, 1.5);
            }} else {{
                bossGroup.scale.set(1.0, 1.0, 1.0);
            }}

            boss.hp = 100;
            boss.bindMeter = 0;
            boss.stunTimer = 0;
            boss.pos.set(0, 12, -18);
            bossGroup.position.copy(boss.pos);
            webTrapGroup.visible = false;

            bossHpBar.style.width = '100%';
            bossHpText.innerText = 'HP 100%';
            bossBindBar.style.width = '0%';
            bossBindText.innerText = '0%';
        }}

        modalScreen.addEventListener('click', () => {{
            if (isGameOver) {{
                currentStage = 1;
                player.level = 1;
                player.damage = 10;
                player.ultPerHit = 20;
                player.speedMulti = 1.0;
                document.getElementById('player-lvl-tag').innerText = 'LV 1 스파이더맨';
                document.getElementById('player-dmg-tag').innerText = '웹 위력 10';
            }}
            setupBossStage(currentStage);

            player.hp = 100;
            player.ultGauge = 0;
            player.pos.set(0, 0, 30);
            player.vel.set(0, 0, 0);
            player.invulnerableTime = 2.0;

            webBullets.forEach(b => scene.remove(b.mesh));
            bossProjectiles.forEach(b => scene.remove(b.mesh));
            webBullets.length = 0;
            bossProjectiles.length = 0;

            playerHpBar.style.width = '100%';
            playerHpText.innerText = '100%';
            ultBar.style.width = '0%';
            ultReadyTag.style.display = 'none';

            modalScreen.style.display = 'none';
            isGameOver = false;
            isStarted = true;
            container.focus();
        }});

        window.chooseUpgrade = function(type) {{
            player.level++;
            document.getElementById('player-lvl-tag').innerText = `LV ${{player.level}} 스파이더맨`;

            if (type === 'dmg') {{
                player.damage += 15;
                document.getElementById('player-dmg-tag').innerText = `웹 위력 ${{player.damage}}`;
                showBanner("🔥 공격력 대폭 강화! (+15 DMG)", "#38bdf8");
            }} else if (type === 'gauge') {{
                player.ultPerHit += 20;
                showBanner("⚡ 궁극기 고속 충전 장착!", "#facc15");
            }} else if (type === 'heal') {{
                player.hp = 100;
                player.speedMulti += 0.25;
                playerHpBar.style.width = '100%';
                playerHpText.innerText = '100%';
                showBanner("🛡️ HP 100% 회복 & 기동력 상승!", "#22c55e");
            }}

            upgradeOverlay.style.display = 'none';
            isUpgrading = false;

            currentStage++;
            setupBossStage(currentStage);
            showBanner(`⚔️ ${{STAGE_CONFIG[currentStage].name}} 출현!`, "#ef4444");
            container.focus();
        }};

        window.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
            if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) e.preventDefault();
            if (e.code === 'KeyQ') fireUltimate();
        }});
        window.addEventListener('keyup', (e) => {{ keys[e.code] = false; }});

        container.addEventListener('mousedown', (e) => {{
            container.focus();
            if (e.button === 0) {{
                if (isStarted && !isGameOver && !isUpgrading) shootWebBullet();
            }} else if (e.button === 2) {{
                fireUltimate();
            }}
            isRightDragging = true;
            startX = e.clientX;
            startY = e.clientY;
        }});

        window.addEventListener('contextmenu', (e) => e.preventDefault());

        window.addEventListener('mousemove', (e) => {{
            if (!isRightDragging) return;
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            startX = e.clientX;
            startY = e.clientY;
            yaw -= dx * 0.005;
            pitch = Math.max(-0.4, Math.min(0.9, pitch + dy * 0.005));
        }});

        window.addEventListener('mouseup', () => {{ isRightDragging = false; }});

        function shootWebBullet() {{
            const shootDir = new THREE.Vector3();
            camera.getWorldDirection(shootDir);

            const bullet = new THREE.Mesh(webBulletGeo, webBulletMat);
            bullet.position.set(player.pos.x, player.pos.y + 1.2, player.pos.z);
            scene.add(bullet);

            webBullets.push({{
                mesh: bullet,
                vel: shootDir.multiplyScalar(140.0),
                life: 2.5
            }});
        }}

        function fireUltimate() {{
            if (!isStarted || isGameOver || isUpgrading || player.ultGauge < 100) return;
            player.ultGauge = 0;
            ultBar.style.width = '0%';
            ultReadyTag.style.display = 'none';

            showBanner("💥 WEB BLOSSOM ULTIMATE! 💥", "#facc15");
            player.vel.y = 22.0;

            for (let i = 0; i < 28; i++) {{
                const angle = (i / 28) * Math.PI * 2;
                const dir = new THREE.Vector3(Math.cos(angle), (Math.random()-0.3)*0.8, Math.sin(angle)).normalize();
                const bullet = new THREE.Mesh(webBulletGeo, new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }}));
                bullet.position.set(player.pos.x, player.pos.y + 1.5, player.pos.z);
                scene.add(bullet);

                webBullets.push({{
                    mesh: bullet,
                    vel: dir.multiplyScalar(110.0),
                    life: 3.5,
                    isUlt: true
                }});
            }}
        }}

        function triggerPlayerHit() {{
            hitOverlay.style.opacity = '1';
            setTimeout(() => {{ hitOverlay.style.opacity = '0'; }}, 180);
        }}

        function checkWallClimb() {{
            player.isWallClimbing = false;
            for (let t of climbBuildings) {{
                const isNearX = (player.pos.x >= t.minX - 1.8 && player.pos.x <= t.maxX + 1.8);
                const isNearZ = (player.pos.z >= t.minZ - 1.8 && player.pos.z <= t.maxZ + 1.8);
                if (isNearX && isNearZ && player.pos.y < t.topY) {{
                    if (keys['KeyW'] || keys['Space'] || keys['ArrowUp']) {{
                        player.isWallClimbing = true;
                        player.vel.y = 34.0;
                        player.vel.x *= 0.3;
                        player.vel.z *= 0.3;
                        return;
                    }}
                }}
            }}
        }}

        const clock = new THREE.Clock();

        function battleLoop() {{
            requestAnimationFrame(battleLoop);
            const delta = Math.min(clock.getDelta(), 0.05);

            if (!isStarted || isGameOver || isUpgrading) {{
                renderer.render(scene, camera);
                return;
            }}

            if (player.invulnerableTime > 0) player.invulnerableTime -= delta;

            const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
            const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw)).normalize();

            const move = new THREE.Vector3();
            if (keys['KeyW'] || keys['ArrowUp']) move.add(forward);
            if (keys['KeyS'] || keys['ArrowDown']) move.sub(forward);
            if (keys['KeyD'] || keys['ArrowRight']) move.add(right);
            if (keys['KeyA'] || keys['ArrowLeft']) move.sub(right);

            if (move.lengthSq() > 0) {{
                move.normalize();
                const spd = 95.0 * player.speedMulti;
                player.vel.x += move.x * spd * delta;
                player.vel.z += move.z * spd * delta;
            }}

            checkWallClimb();

            if (!player.isWallClimbing) player.vel.y -= 38.0 * delta;

            const damp = player.isGrounded ? 7.0 : 2.0;
            player.vel.x *= Math.max(0, 1 - damp * delta);
            player.vel.z *= Math.max(0, 1 - damp * delta);

            if (keys['Space'] && player.isGrounded) {{
                player.vel.y = 22.0;
                player.isGrounded = false;
            }}

            player.pos.addScaledVector(player.vel, delta);

            if (player.pos.y <= 0) {{
                player.pos.y = 0;
                player.vel.y = 0;
                player.isGrounded = true;
            }}
            player.pos.x = Math.max(-62, Math.min(62, player.pos.x));
            player.pos.z = Math.max(-62, Math.min(62, player.pos.z));
            playerGroup.position.copy(player.pos);

            const cfg = STAGE_CONFIG[currentStage];
            if (boss.stunTimer > 0) {{
                boss.stunTimer -= delta;
                boss.pos.y = Math.max(1.0, boss.pos.y - 20.0 * delta);
                webTrapGroup.visible = true;
                bossGroup.position.copy(boss.pos);

                if (boss.stunTimer <= 0) {{
                    webTrapGroup.visible = false;
                    boss.bindMeter = 0;
                    bossBindBar.style.width = '0%';
                    bossBindText.innerText = '0%';
                }}
            }} else {{
                boss.angle += delta * cfg.speed;
                boss.pos.x = Math.sin(boss.angle) * (currentStage === 2 ? 32 : 26);
                boss.pos.z = Math.cos(boss.angle) * 22 - 6;
                boss.pos.y = 11 + Math.sin(boss.angle * 1.8) * 3.0;
                bossGroup.position.copy(boss.pos);
                bossGroup.lookAt(player.pos.x, player.pos.y + 1.2, player.pos.z);

                boss.attackTimer += delta;
                if (boss.attackTimer > cfg.attackInterval) {{
                    boss.attackTimer = 0;
                    const pMat = new THREE.MeshStandardMaterial({{ color: cfg.bombColor, emissive: cfg.bombColor, emissiveIntensity: 0.8 }});
                    const bomb = new THREE.Mesh(projGeo, pMat);
                    bomb.position.copy(boss.pos);
                    scene.add(bomb);

                    const toPlayer = new THREE.Vector3().subVectors(player.pos, boss.pos).normalize();
                    bossProjectiles.push({{
                        mesh: bomb,
                        vel: toPlayer.multiplyScalar(currentStage === 2 ? 28.0 : 22.0),
                        life: 6.0
                    }});
                }}
            }}

            for (let i = webBullets.length - 1; i >= 0; i--) {{
                const b = webBullets[i];
                b.mesh.position.addScaledVector(b.vel, delta);
                b.life -= delta;

                const hitRange = currentStage === 3 ? 5.2 : 3.8;
                if (b.mesh.position.distanceTo(boss.pos) < hitRange) {{
                    const dmg = b.isUlt ? (player.damage * 2.5) : player.damage;
                    boss.hp = Math.max(0, boss.hp - dmg);
                    bossHpBar.style.width = boss.hp + '%';
                    bossHpText.innerText = 'HP ' + Math.round(boss.hp) + '%';

                    boss.bindMeter = Math.min(100, boss.bindMeter + (b.isUlt ? 60 : cfg.bindPerHit));
                    bossBindBar.style.width = boss.bindMeter + '%';
                    bossBindText.innerText = boss.bindMeter + '%';

                    if (boss.bindMeter >= 100 && boss.stunTimer <= 0) {{
                        boss.stunTimer = 5.0;
                        showBanner("🕸️ 보스 완전 포박! 5초간 기절! 🕸️", "#38bdf8");
                    }}

                    player.ultGauge = Math.min(100, player.ultGauge + player.ultPerHit);
                    ultBar.style.width = player.ultGauge + '%';
                    if (player.ultGauge >= 100) ultReadyTag.style.display = 'inline';

                    scene.remove(b.mesh);
                    webBullets.splice(i, 1);

                    if (boss.hp <= 0) {{
                        if (currentStage < 3) {{
                            isUpgrading = true;
                            upgradeOverlay.style.display = 'flex';
                            document.getElementById('level-reward-desc').innerText = `${{cfg.name}} 처치 완료! 다음 보스전을 위해 능력을 업그레이드하세요.`;
                        }} else {{
                            isGameOver = true;
                            modalTitle.innerText = "🏆 ALL BOSSES DEFEATED!";
                            modalTitle.style.color = "#22c55e";
                            modalDesc.innerText = "그린 고블린, 일렉트로, 베놈까지 뉴욕시의 모든 빌런을 소탕했습니다! 다시 도전하려면 클릭하세요.";
                            modalScreen.style.display = 'flex';
                        }}
                    }}
                    continue;
                }}

                if (b.life <= 0) {{
                    scene.remove(b.mesh);
                    webBullets.splice(i, 1);
                }}
            }}

            for (let i = bossProjectiles.length - 1; i >= 0; i--) {{
                const pb = bossProjectiles[i];
                pb.mesh.position.addScaledVector(pb.vel, delta);
                pb.life -= delta;

                if (pb.mesh.position.distanceTo(player.pos) < 2.0) {{
                    if (player.invulnerableTime <= 0) {{
                        const hitDmg = currentStage === 3 ? 20 : 14;
                        player.hp = Math.max(0, player.hp - hitDmg);
                        playerHpBar.style.width = player.hp + '%';
                        playerHpText.innerText = Math.round(player.hp) + '%';
                        triggerPlayerHit();

                        if (player.hp <= 0) {{
                            isGameOver = true;
                            modalTitle.innerText = "💀 MISSION FAILED";
                            modalTitle.style.color = "#ef4444";
                            modalDesc.innerText = `${{cfg.name}}에게 쓰러졌습니다. 다시 도전하려면 클릭하세요!`;
                            modalScreen.style.display = 'flex';
                        }}
                    }}
                    scene.remove(pb.mesh);
                    bossProjectiles.splice(i, 1);
                    continue;
                }}

                if (pb.life <= 0) {{
                    scene.remove(pb.mesh);
                    bossProjectiles.splice(i, 1);
                }}
            }}

            const camDist = 7.5;
            const camH = 3.0;
            camera.position.set(
                player.pos.x + Math.sin(yaw) * Math.cos(pitch) * camDist,
                player.pos.y + Math.sin(pitch) * camDist + camH,
                player.pos.z + Math.cos(yaw) * Math.cos(pitch) * camDist
            );
            camera.lookAt(player.pos.x, player.pos.y + 1.2, player.pos.z);

            renderer.render(scene, camera);
        }}

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        battleLoop();
    </script>
    </body>
    </html>
    """

    components.html(boss_html, height=840, scrolling=False)
