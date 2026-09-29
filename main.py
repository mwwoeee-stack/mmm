import streamlit as st
import streamlit.components.v1 as components
import math

# 1. 스트림릿 와이드 모드 설정
st.set_page_config(
    page_title="Spider-Man Biomechanics Lab & 3D Web-Zip",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 기본 UI 여백 정리
st.markdown("""
<style>
    .block-container {
        padding: 1rem 1.5rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 2. 탭 구성
tab_game, tab_lab = st.tabs(["🎮 3D 시티 웹집 어드벤처", "🧪 첨단 생체재료 역학 연구소 (거미줄 제작)"])

# 세션 상태로 거미줄 물리 파라미터 보존
if "web_color" not in st.session_state:
    st.session_state.web_color = "#38bdf8"
if "web_speed" not in st.session_state:
    st.session_state.web_speed = 110.0
if "web_range" not in st.session_state:
    st.session_state.web_range = 190.0
if "web_thickness" not in st.session_state:
    st.session_state.web_thickness = 3

# ==================== [TAB 2: 거미줄 제작 & 물리역학 연구소] ====================
with tab_lab:
    st.header("🧪 첨단 생체고분자 복합소재 & 유체역학 조제실")
    st.caption("방사형 거미줄 단백질(Spidroin) 모방 합성 고분자의 미세 역학적 물성과 유체 노즐 분사 동역학 분석")
    st.markdown("---")

    col_ctrl, col_physics = st.columns([1.1, 1.2])

    with col_ctrl:
        st.subheader("⚙️ 고분자 나노구조 및 사출 공학 제어")

        fluid_base = st.selectbox(
            "기반 생체 복합 폴리머 기질 (Polymer Matrix)",
            [
                "재조합 스파이드로인 단백질 (Spidroin I/II Mimic)",
                "탄소나노튜브 복합 폴리아크릴로니트릴 (CNT-PAN Hybrid)",
                "점탄성 폴리우레탄-실리카 나노입자 (Viscoelastic PU-SiO2)",
                "자가치유 디설피드 가교 히드로겔 (Self-Healing Hydrogel)"
            ]
        )

        st.markdown("#### 1. 나노 네트워크 가교도 (Crosslinking Density)")
        crosslink_density = st.slider(
            "가교 밀도 ρ_x (10^4 mol/m³)",
            min_value=1.5,
            max_value=12.0,
            value=6.5,
            step=0.5,
            help="고분자 사슬 간 화학적 공유결합 밀도입니다. 고무 탄성 이론에 따라 탄성계수(Young's modulus)와 비행 견인 속도에 직접 비례합니다."
        )

        st.markdown("#### 2. 마이크로 노즐 사출 압력 (Chamber Pressure)")
        injection_pressure = st.slider(
            "노즐 압축 챔버 압력 ΔP (MPa)",
            min_value=8.0,
            max_value=35.0,
            value=22.0,
            step=1.0,
            help="웹슈터의 마이크로 플루이딕 노즐 내부 분사 압력입니다. 하겐-푸아죄유 법칙 및 베르누이 유체역학에 따라 거미줄의 최대 발사 사정거리를 결정합니다."
        )

        st.markdown("#### 3. 거미줄 광학 표면 물성")
        selected_color = st.color_picker("생체 형광 광학 색상 (Photoluminescence)", st.session_state.web_color)
        selected_thickness = st.slider("섬유 다발 가닥 수 / 직경 d (μm)", 1, 6, st.session_state.web_thickness)

    # ------------------ 물리 계산 공식 엔진 ------------------
    # 1. 고무 탄성 및 가교도에 기초한 영률(E) 계산: E ≈ 3 * rho_x * R * T
    R_gas = 8.314  # J/(mol*K)
    Temp = 298.15  # 상온 25도 (K)
    youngs_modulus_gpa = (3.0 * (crosslink_density * 1e4) * R_gas * Temp) / 1e9  # GPa 환산

    # 2. 거미줄 인장 속도 환산 (탄성파 전파 속도 c = sqrt(E / rho)): E가 높을수록 빠른 견인 속도 산출
    calculated_web_speed = round(80.0 + (youngs_modulus_gpa / 0.89) * 45.0, 1)
    calculated_web_speed = max(80.0, min(160.0, calculated_web_speed))

    # 3. 하겐-푸아죄유 & 사출 역학 기반 사정거리 계산: Range ∝ sqrt(2 * ΔP / rho_fluid)
    fluid_density = 1180.0  # kg/m3 (점성 고분자 용액 밀도)
    v_exit = math.sqrt((2.0 * (injection_pressure * 1e6)) / fluid_density)  # 초기 사출 유속 (m/s)
    calculated_web_range = round(95.0 + (v_exit / 245.0) * 110.0, 1)
    calculated_web_range = max(100.0, min(260.0, calculated_web_range))

    with col_physics:
        st.subheader("📐 유도된 물리·역학적 지표 및 수식 모델")

        st.latex(r"E \approx 3 \rho_x R T \quad \implies \quad v_{\text{zip}} \propto \sqrt{\frac{E}{\rho_{\text{fiber}}}}")
        st.caption("• **고무 탄성 이론(Affine Network Model)**: 가교 밀도($\\rho_x$)가 증가할수록 영률($E$)이 상승하여 거미줄이 하중을 받았을 때 신장 복원력이 커지며, 비행 견인 속도($v_{\\text{zip}}$)가 비례하여 증가합니다.")

        st.latex(r"Q = \frac{\pi r^4 \Delta P}{8 \mu L}, \quad v_0 = \sqrt{\frac{2 \Delta P}{\rho_{\text{fluid}}}} \quad \implies \quad R_{\max} \propto \frac{v_0^2}{g}")
        st.caption("• **하겐-푸아죄유(Hagen-Poiseuille) 유체역학**: 점성 유체($\\mu$)가 마이크로 방사 노즐을 통과할 때 형성되는 사출 압력차($\\Delta P$)가 초기 분사 속도($v_0$)를 결정하여 최대 사정거리($R_{\\max}$)를 도출합니다.")

        st.markdown("---")
        # 역학 지표 대시보드 카드
        m1, m2 = st.columns(2)
        m1.metric("계산된 영률 (Young's Modulus)", f"{youngs_modulus_gpa:.2f} GPa", delta=f"{crosslink_density} x10⁴ mol/m³")
        m2.metric("노즐 초기 사출 유속 (v₀)", f"{v_exit:.1f} m/s", delta=f"{injection_pressure} MPa")

        m3, m4 = st.columns(2)
        m3.metric("최종 웹집 추진력 (Speed)", f"{calculated_web_speed} km/h")
        m4.metric("최종 유효 사정거리 (Max Range)", f"{calculated_web_range} m")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 위 물리역학 파라미터를 3D 웹슈터에 주입하기", use_container_width=True, type="primary"):
            st.session_state.web_color = selected_color
            st.session_state.web_speed = calculated_web_speed
            st.session_state.web_range = calculated_web_range
            st.session_state.web_thickness = selected_thickness
            st.success(f"생체역학 파라미터가 장착되었습니다! (탄성 견인 속도: {calculated_web_speed} km/h, 사정거리: {calculated_web_range} m)")

# ==================== [TAB 1: 3D 게임 플레이 (기존 코드 100% 동일 유지)] ====================
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
        }}
        #canvas-container:active {{
            cursor: grabbing;
        }}
        
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
            font-size: 20px;
            font-weight: 900;
            color: #38bdf8;
        }}
        .hud-val span {{ font-size: 11px; color: #64748b; font-weight: 600; }}

        #stunt-alert {{
            position: absolute;
            top: 70px;
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

        #start-overlay {{
            position: absolute;
            inset: 0;
            background: rgba(11, 14, 20, 0.85);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #fff;
            z-index: 100;
            cursor: pointer;
            transition: opacity 0.3s ease;
        }}
        #start-overlay h1 {{ 
            font-size: 32px; 
            font-weight: 900; 
            margin-bottom: 8px; 
            color: #ef4444; 
            letter-spacing: 1px; 
        }}
        #start-overlay p {{ 
            font-size: 14px; 
            color: #cbd5e1; 
            background: rgba(255, 255, 255, 0.1); 
            padding: 8px 18px; 
            border-radius: 20px;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>

    <div id="hit-vignette"></div>

    <div id="start-overlay">
        <h1>🕷️ SPIDER-MAN 3D CITY</h1>
        <p>▶ 여기를 클릭해서 조작을 시작하세요</p>
    </div>

    <div id="hud">
        <div class="hud-card">
            <div class="hud-title">속도 (SPEED)</div>
            <div class="hud-val" id="speed-meter">0 <span>km/h</span></div>
        </div>
        <div class="hud-card">
            <div class="hud-title">골든 링 (RINGS)</div>
            <div class="hud-val" id="ring-score">0 <span>/ 10</span></div>
        </div>
        <div class="hud-card">
            <div class="hud-title">적용된 생체역학 고분자</div>
            <div class="hud-val" style="color: {st.session_state.web_color}; font-size: 15px;">BIO-POLYMER MATRIX</div>
        </div>
    </div>

    <div id="stunt-alert">✨ ACROBATIC FLIP! ✨</div>

    <div id="controls-guide">
        • <span class="key-badge">건물 클릭</span> 웹집 발사 (계산된 속도: {current_web_speed}km/h | 사거리: {current_web_range}m)<br>
        • <span class="key-badge">드래그</span> 시점/카메라 360도 회전<br>
        • <span class="key-badge">W</span> <span class="key-badge">A</span> <span class="key-badge">S</span> <span class="key-badge">D</span> 이동 및 <b>공중 방향 조절</b><br>
        • <span class="key-badge">Space</span> 점프 | <span class="key-badge">Space 더블탭</span> <b>360도 공중제비 슈퍼점프</b><br>
        • ⚠️ <b>건물 충돌 시스템 활성화 (벽 관통 불가)</b>
    </div>

    <div id="canvas-container"></div>

    <script>
        const WEB_COLOR = {current_web_color};
        const WEB_SPEED = {current_web_speed};
        const WEB_RANGE = {current_web_range};
        const WEB_THICKNESS = {current_web_thickness};

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

        const bldgMat = new THREE.MeshStandardMaterial({{
            map: winTexture,
            roughness: 0.35,
            metalness: 0.3
        }});

        const roofMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.8 }});
        const tankMat = new THREE.MeshStandardMaterial({{ color: 0x78350f, roughness: 0.6 }});

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
                    minX: posX - w/2 - 0.7,
                    maxX: posX + w/2 + 0.7,
                    minZ: posZ - d/2 - 0.7,
                    maxZ: posZ + d/2 + 0.7,
                    topY: h
                }});

                const decoType = Math.random();
                if (decoType > 0.6) {{
                    const tank = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 4, 12), tankMat);
                    tank.position.set(posX + (Math.random()-0.5)*w*0.4, h + 2, posZ + (Math.random()-0.5)*d*0.4);
                    scene.add(tank);
                }} else if (decoType > 0.3) {{
                    const duct = new THREE.Mesh(new THREE.BoxGeometry(3.5, 2.5, 3.5), roofMat);
                    duct.position.set(posX, h + 1.25, posZ);
                    scene.add(duct);
                }}
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

        const webMat = new THREE.LineBasicMaterial({{ 
            color: WEB_COLOR, 
            linewidth: WEB_THICKNESS 
        }});
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

        let yaw = 0;
        let pitch = 0.2;
        let isDragging = false;
        let startMouseX = 0;
        let startMouseY = 0;
        let clickStartX = 0;
        let clickStartY = 0;

        const overlay = document.getElementById('start-overlay');
        overlay.addEventListener('click', () => {{
            overlay.style.opacity = '0';
            setTimeout(() => {{ overlay.style.display = 'none'; }}, 300);
            window.focus();
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
                        player.vel.y = Math.max(player.vel.y, 25.0);
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
            if (moveDist < 6) {{
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
                        player.vel.x *= -0.2;
                        player.vel.z *= -0.2;
                        triggerHitEffect();
                    }}
                }}
            }}
        }}

        const clock = new THREE.Clock();
        const speedMeter = document.getElementById('speed-meter');
        const ringScore = document.getElementById('ring-score');

        function animate() {{
            requestAnimationFrame(animate);
            const delta = Math.min(clock.getDelta(), 0.05);

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

                if (dist < 4.5) {{
                    player.isWebZipping = false;
                    webLine.visible = false;
                    player.vel.add(toTarget.normalize().multiplyScalar(24));
                    player.vel.y = Math.max(player.vel.y, 22);
                }} else {{
                    player.vel.copy(toTarget.normalize().multiplyScalar(WEB_SPEED));

                    if (keys['KeyA']) player.vel.add(right.clone().multiplyScalar(-16));
                    if (keys['KeyD']) player.vel.add(right.clone().multiplyScalar(16));

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

            speedMeter.innerHTML = `${{Math.round(player.vel.length() * 3.6)}} <span>km/h</span>`;
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
