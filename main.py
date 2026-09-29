import streamlit as st
import streamlit.components.v1 as components
import math

# 1. 스트림릿 와이드 모드 설정
st.set_page_config(
    page_title="Spider-Man Biomechanics Lab & Boss Battle",
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
tab_game, tab_lab, tab_boss = st.tabs([
    "🎮 3D 시티 웹집 어드벤처", 
    "🧪 첨단 생체재료 역학 연구소 (거미줄 제작)", 
    "⚔️ 빌런 보스전 (그린 고블린 배틀)"
])

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
        st.caption("• **고무 탄성 이론(Affine Network Model)**: 가교 밀도($\\rho_x$)가 증가할수록 영률($E$)이 상승하여 비행 견인 속도($v_{\\text{zip}}$)가 비례하여 증가합니다.")

        st.latex(r"Q = \frac{\pi r^4 \Delta P}{8 \mu L}, \quad v_0 = \sqrt{\frac{2 \Delta P}{\rho_{\text{fluid}}}} \quad \implies \quad R_{\max} \propto \frac{v_0^2}{g}")
        st.caption("• **하겐-푸아죄유(Hagen-Poiseuille) 유체역학**: 점성 유체($\\mu$)가 마이크로 방사 노즐을 통과할 때 형성되는 사출 압력차($\\Delta P$)가 초기 분사 속도($v_0$)를 결정하여 최대 사정거리($R_{\\max}$)를 도출합니다.")

        st.markdown("---")
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

# ==================== [TAB 3: 전면 개편된 보스전: 벽타기 & 거미줄 구속 & 웹블로섬 궁극기] ====================
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

        /* 보스 체력 & 구속 게이지 UI */
        #boss-ui {{
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: min(650px, 90vw);
            z-index: 10;
            display: flex;
            flex-direction: column;
            gap: 5px;
            pointer-events: none;
        }}
        .boss-header {{
            display: flex;
            justify-content: space-between;
            color: #ef4444;
            font-weight: 900;
            letter-spacing: 1.5px;
            font-size: 14px;
            text-shadow: 0 0 10px rgba(239, 68, 68, 0.7);
        }}
        .boss-hp-bg {{
            width: 100%;
            height: 18px;
            background: rgba(15, 23, 42, 0.9);
            border: 2px solid rgba(239, 68, 68, 0.6);
            border-radius: 9px;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
        }}
        #boss-hp-bar {{
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, #dc2626, #f97316);
            transition: width 0.15s ease-out;
        }}
        /* 거미줄 구속도 바 */
        .boss-bind-bg {{
            width: 100%;
            height: 8px;
            background: #1e293b;
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        #boss-bind-bar {{
            width: 0%;
            height: 100%;
            background: #38bdf8;
            transition: width 0.1s ease;
        }}

        /* 좌상단: 플레이어 체력 & 궁극기(ULTIMATE) 게이지 */
        #player-ui {{
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 10;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 12px 18px;
            color: #fff;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .bar-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; display: flex; justify-content: space-between; }}
        .bar-bg {{ width: 170px; height: 10px; background: #1e293b; border-radius: 5px; overflow: hidden; }}
        #player-hp-bar {{ width: 100%; height: 100%; background: #22c55e; transition: width 0.2s ease; }}
        #ult-bar {{ width: 0%; height: 100%; background: linear-gradient(90deg, #06b6d4, #f59e0b); transition: width 0.15s ease; }}
        #ult-ready-tag {{
            font-size: 11px;
            color: #facc15;
            font-weight: 900;
            display: none;
            animation: blink 0.8s infinite;
        }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}

        /* 중앙 알림 배너 (벽타기, 스턴, 궁극기) */
        #action-banner {{
            position: absolute;
            top: 85px;
            left: 50%;
            transform: translateX(-50%) scale(0.85);
            font-size: 24px;
            font-weight: 900;
            letter-spacing: 2px;
            opacity: 0;
            pointer-events: none;
            z-index: 20;
            transition: all 0.2s ease;
        }}
        #action-banner.show {{
            opacity: 1;
            transform: translateX(-50%) scale(1.1);
        }}

        /* 하단 조작 가이드 */
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

        /* 시작 모달 */
        #modal-screen {{
            position: absolute;
            inset: 0;
            background: rgba(6, 8, 20, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #fff;
            z-index: 100;
            cursor: pointer;
        }}
        #modal-screen h1 {{
            font-size: 36px;
            color: #38bdf8;
            letter-spacing: 2px;
            margin-bottom: 12px;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
        }}
        #modal-screen p {{
            font-size: 15px;
            color: #cbd5e1;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 22px;
            border-radius: 20px;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>

    <div id="hit-overlay"></div>

    <div id="action-banner"></div>

    <div id="modal-screen">
        <h1 id="modal-title">⚔️ SPIDER-MAN VS GOBLIN</h1>
        <p id="modal-desc">▶ 클릭하여 배틀 시작 (속도 대폭 강화 & 벽타기 & 궁극기 탑재)</p>
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
    </div>

    <div id="boss-ui">
        <div class="boss-header">
            <span>😈 GREEN GOBLIN</span>
            <span id="boss-hp-text">100%</span>
        </div>
        <div class="boss-hp-bg"><div id="boss-hp-bar"></div></div>
        <div class="boss-bind-bg"><div id="boss-bind-bar"></div></div>
    </div>

    <div id="boss-guide">
        • <span class="badge">좌클릭</span> <b>거미줄 발사</b> (적중 시 대미지 + <b>거미줄로 묶음 Stun</b>)<br>
        • <span class="ult-badge">Q 키 / 우클릭</span> <b>궁극기 [웹 블라섬]</b> 게이지 100% 시 360도 거미줄 난사 폭발!<br>
        • <span class="badge">벽면 근처 W</span> <b>벽 타기 질주 (Wall Run / Climb)</b>로 순식간에 빌딩 등반!<br>
        • <span class="badge">W</span> <span class="badge">A</span> <span class="badge">S</span> <span class="badge">D</span> 초고속 기동 | <span class="badge">Space</span> 회피 도약
    </div>

    <div id="boss-canvas" tabindex="0"></div>

    <script>
        const WEB_COLOR = {boss_web_color};
        const WEB_SPEED = {boss_web_speed};

        const container = document.getElementById('boss-canvas');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x060814);
        scene.fog = new THREE.FogExp2(0x060814, 0.007);

        const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 900);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        scene.add(new THREE.HemisphereLight(0x22c55e, 0x1e1b4b, 0.8));
        const dirLight = new THREE.DirectionalLight(0xffeedd, 1.2);
        dirLight.position.set(50, 120, 60);
        scene.add(dirLight);

        // --- 1. 아레나 & 벽타기 가능한 빌딩 기둥 배치 ---
        const arena = new THREE.Mesh(
            new THREE.BoxGeometry(130, 4, 130),
            new THREE.MeshStandardMaterial({{ color: 0x1e293b, roughness: 0.6 }})
        );
        arena.position.y = -2;
        scene.add(arena);

        const climbBuildings = [];
        const towerGeo = new THREE.BoxGeometry(18, 55, 18);
        const towerMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.4 }});

        // 경기장 사방에 4개의 거대한 등반용 타워 배치
        const towerPositions = [
            [-32, 27.5, -32], [32, 27.5, -32],
            [-32, 27.5, 32],  [32, 27.5, 32]
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

        // --- 2. 플레이어 (스파이더맨 아바타) ---
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

        const player = {{
            pos: new THREE.Vector3(0, 0, 30),
            vel: new THREE.Vector3(),
            hp: 100,
            ultGauge: 0, // 0 ~ 100
            isGrounded: true,
            isWallClimbing: false,
            invulnerableTime: 2.0
        }};

        // --- 3. 그린 고블린 & 글라이더 (거미줄 묶임 효과 포함) ---
        const goblinGroup = new THREE.Group();
        scene.add(goblinGroup);

        const glider = new THREE.Mesh(
            new THREE.ConeGeometry(3.5, 6.5, 3),
            new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.8, roughness: 0.2 }})
        );
        glider.rotation.x = Math.PI / 2;
        glider.scale.set(1.5, 0.4, 0.8);
        goblinGroup.add(glider);

        const gobBody = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 1.4, 12), new THREE.MeshStandardMaterial({{ color: 0x16a34a }}));
        gobBody.position.y = 1.0;
        goblinGroup.add(gobBody);

        const gobHead = new THREE.Mesh(new THREE.SphereGeometry(0.4, 12, 12), new THREE.MeshStandardMaterial({{ color: 0x22c55e }}));
        gobHead.position.y = 2.0;
        goblinGroup.add(gobHead);

        // 묶였을 때 나타나는 하얀 거미줄 고치 (Web Cocoon)
        const cocoonMat = new THREE.MeshBasicMaterial({{ color: 0xffffff, wireframe: true, transparent: true, opacity: 0 }});
        const cocoon = new THREE.Mesh(new THREE.SphereGeometry(2.8, 16, 16), cocoonMat);
        goblinGroup.add(cocoon);

        const boss = {{
            pos: new THREE.Vector3(0, 16, -20),
            hp: 100,
            bindMeter: 0,      // 0 ~ 100
            stunTimer: 0,      // 거미줄 묶임 상태 지속시간
            angle: 0,
            attackTimer: 0
        }};
        goblinGroup.position.copy(boss.pos);

        // 투사체 배열
        const webBullets = [];
        const webBulletGeo = new THREE.SphereGeometry(0.5, 8, 8);
        const webBulletMat = new THREE.MeshBasicMaterial({{ color: WEB_COLOR }});

        const pumpkinBombs = [];
        const bombGeo = new THREE.SphereGeometry(0.65, 12, 12);
        const bombMat = new THREE.MeshStandardMaterial({{ color: 0xea580c, emissive: 0xf97316, emissiveIntensity: 0.8 }});

        // 조작 & UI 제어
        let isStarted = false;
        let isGameOver = false;
        let yaw = 0;
        let pitch = 0.15;
        let isDragging = false;
        let startX = 0, startY = 0;
        const keys = {{}};

        const modalScreen = document.getElementById('modal-screen');
        const modalTitle = document.getElementById('modal-title');
        const modalDesc = document.getElementById('modal-desc');
        const bossHpBar = document.getElementById('boss-hp-bar');
        const bossHpText = document.getElementById('boss-hp-text');
        const bossBindBar = document.getElementById('boss-bind-bar');
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
            setTimeout(() => {{ actionBanner.classList.remove('show'); }}, 1000);
        }}

        function ensureFocus() {{
            container.focus();
            window.focus();
        }}

        modalScreen.addEventListener('click', () => {{
            boss.hp = 100;
            boss.bindMeter = 0;
            boss.stunTimer = 0;
            player.hp = 100;
            player.ultGauge = 0;
            player.pos.set(0, 0, 30);
            player.vel.set(0, 0, 0);
            player.invulnerableTime = 2.0;
            boss.pos.set(0, 16, -20);
            webBullets.forEach(b => scene.remove(b.mesh));
            pumpkinBombs.forEach(b => scene.remove(b.mesh));
            webBullets.length = 0;
            pumpkinBombs.length = 0;
            bossHpBar.style.width = '100%';
            bossHpText.innerText = '100%';
            bossBindBar.style.width = '0%';
            playerHpBar.style.width = '100%';
            playerHpText.innerText = '100%';
            ultBar.style.width = '0%';
            ultReadyTag.style.display = 'none';
            modalScreen.style.display = 'none';
            isGameOver = false;
            isStarted = true;
            ensureFocus();
        }});

        container.addEventListener('click', ensureFocus);

        // 키보드 & 마우스 이벤트
        window.addEventListener('keydown', (e) => {{
            keys[e.code] = true;
            if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {{
                e.preventDefault();
            }}
            // 궁극기 발사 키 (Q 키)
            if (e.code === 'KeyQ') {{
                fireUltimate();
            }}
        }});
        window.addEventListener('keyup', (e) => {{ keys[e.code] = false; }});

        container.addEventListener('mousedown', (e) => {{
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            ensureFocus();
            // 우클릭으로도 궁극기 발사 지원
            if (e.button === 2) {{
                fireUltimate();
            }}
        }});

        window.addEventListener('contextmenu', (e) => e.preventDefault());

        window.addEventListener('mousemove', (e) => {{
            if (!isDragging) return;
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            startX = e.clientX;
            startY = e.clientY;
            yaw -= dx * 0.005;
            pitch = Math.max(-0.4, Math.min(0.9, pitch + dy * 0.005));
        }});

        // 일반 거미줄 발사 (좌클릭)
        window.addEventListener('mouseup', (e) => {{
            if (!isDragging) return;
            isDragging = false;
            if (!isStarted || isGameOver || e.button !== 0) return;

            const shootDir = new THREE.Vector3(
                -Math.sin(yaw) * Math.cos(pitch),
                Math.sin(pitch),
                -Math.cos(yaw) * Math.cos(pitch)
            ).normalize();

            const bullet = new THREE.Mesh(webBulletGeo, webBulletMat);
            bullet.position.set(player.pos.x, player.pos.y + 1.2, player.pos.z);
            scene.add(bullet);

            webBullets.push({{
                mesh: bullet,
                vel: shootDir.multiplyScalar(WEB_SPEED * 1.1),
                life: 3.0
            }});
        }});

        // --- 궁극기: 360도 웹 블라섬 (Web Blossom) ---
        function fireUltimate() {{
            if (!isStarted || isGameOver || player.ultGauge < 100) return;
            player.ultGauge = 0;
            ultBar.style.width = '0%';
            ultReadyTag.style.display = 'none';

            showBanner("💥 WEB BLOSSOM ULTIMATE! 💥", "#facc15");

            // 공중으로 크게 솟구친 후 20발의 전방위 거미줄 폭풍 발사
            player.vel.y = 22.0;

            for (let i = 0; i < 20; i++) {{
                const angle = (i / 20) * Math.PI * 2;
                const dir = new THREE.Vector3(Math.cos(angle), (Math.random()-0.3)*0.8, Math.sin(angle)).normalize();
                const bullet = new THREE.Mesh(webBulletGeo, new THREE.MeshBasicMaterial({{ color: 0x38bdf8 }}));
                bullet.position.set(player.pos.x, player.pos.y + 1.5, player.pos.z);
                scene.add(bullet);

                webBullets.push({{
                    mesh: bullet,
                    vel: dir.multiplyScalar(95.0),
                    life: 3.5,
                    isUlt: true
                }});
            }}
        }}

        function triggerPlayerHit() {{
            hitOverlay.style.opacity = '1';
            setTimeout(() => {{ hitOverlay.style.opacity = '0'; }}, 180);
        }}

        // --- 벽타기 검사 로직 ---
        function checkWallClimb(moveVector, delta) {{
            player.isWallClimbing = false;
            for (let t of climbBuildings) {{
                // 건물 벽면 2m 이내에 근접해 있는가?
                const isNearX = (player.pos.x >= t.minX - 1.8 && player.pos.x <= t.maxX + 1.8);
                const isNearZ = (player.pos.z >= t.minZ - 1.8 && player.pos.z <= t.maxZ + 1.8);
                
                if (isNearX && isNearZ && player.pos.y < t.topY) {{
                    // 벽 쪽으로 W 키를 누르고 있거나 점프 중일 때 수직 벽타기 발동!
                    if (keys['KeyW'] || keys['Space'] || keys['ArrowUp']) {{
                        player.isWallClimbing = true;
                        player.vel.y = 32.0; // 빠른 속도로 벽을 수직 질주
                        player.vel.x *= 0.3;
                        player.vel.z *= 0.3;
                        showBanner("🧗 WALL RUN CLIMB!", "#38bdf8");
                        return;
                    }}
                }}
            }}
        }}

        const clock = new THREE.Clock();

        function battleLoop() {{
            requestAnimationFrame(battleLoop);
            const delta = Math.min(clock.getDelta(), 0.05);

            if (!isStarted || isGameOver) {{
                renderer.render(scene, camera);
                return;
            }}

            if (player.invulnerableTime > 0) player.invulnerableTime -= delta;

            const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
            const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw)).normalize();

            // 1) 플레이어 초고속 이동 (스피드 대폭 향상: 95.0)
            const move = new THREE.Vector3();
            if (keys['KeyW'] || keys['ArrowUp']) move.add(forward);
            if (keys['KeyS'] || keys['ArrowDown']) move.sub(forward);
            if (keys['KeyD'] || keys['ArrowRight']) move.add(right);
            if (keys['KeyA'] || keys['ArrowLeft']) move.sub(right);

            if (move.lengthSq() > 0) {{
                move.normalize();
                player.vel.x += move.x * 95.0 * delta;
                player.vel.z += move.z * 95.0 * delta;
            }}

            // 벽 타기 체크
            checkWallClimb(move, delta);

            // 벽 타는 중이 아닐 때만 일반 중력 적용
            if (!player.isWallClimbing) {{
                player.vel.y -= 38.0 * delta;
            }}

            const damp = player.isGrounded ? 7.0 : 2.0;
            player.vel.x *= Math.max(0, 1 - damp * delta);
            player.vel.z *= Math.max(0, 1 - damp * delta);

            // 점프
            if (keys['Space'] && player.isGrounded) {{
                player.vel.y = 22.0;
                player.isGrounded = false;
            }}

            player.pos.addScaledVector(player.vel, delta);

            // 바닥 착지
            if (player.pos.y <= 0) {{
                player.pos.y = 0;
                player.vel.y = 0;
                player.isGrounded = true;
            }}
            player.pos.x = Math.max(-58, Math.min(58, player.pos.x));
            player.pos.z = Math.max(-58, Math.min(58, player.pos.z));
            playerGroup.position.copy(player.pos);

            // 2) 고블린 보스 AI (거미줄 묶임 상태 판정)
            if (boss.stunTimer > 0) {{
                // [거미줄에 완전히 묶여서 스턴 상태]
                boss.stunTimer -= delta;
                cocoonMat.opacity = Math.min(0.8, boss.stunTimer / 1.5);
                // 스턴 중에는 움직이거나 폭탄을 쏘지 못하고 흔들리기만 함
                goblinGroup.rotation.z = Math.sin(clock.getElapsedTime() * 15) * 0.15;
            }} else {{
                // 정상 기동 상태
                cocoonMat.opacity = boss.bindMeter / 140.0;
                boss.angle += delta * 1.2;
                boss.pos.x = Math.sin(boss.angle) * 34;
                boss.pos.z = Math.cos(boss.angle * 0.7) * 28 - 6;
                boss.pos.y = 15 + Math.sin(boss.angle * 2.0) * 4.5;
                goblinGroup.position.copy(boss.pos);
                goblinGroup.lookAt(player.pos.x, player.pos.y + 1.2, player.pos.z);

                // 공격 폭탄 투척
                boss.attackTimer += delta;
                if (boss.attackTimer > 2.0) {{
                    boss.attackTimer = 0;
                    const bomb = new THREE.Mesh(bombGeo, bombMat);
                    bomb.position.copy(boss.pos);
                    scene.add(bomb);

                    const toPlayer = new THREE.Vector3().subVectors(player.pos, boss.pos).normalize();
                    pumpkinBombs.push({{
                        mesh: bomb,
                        vel: toPlayer.multiplyScalar(28.0),
                        life: 5.0
                    }});
                }}
            }}

            // 3) 거미줄 투사체 업데이트 & 보스 피격 / 구속 판정
            for (let i = webBullets.length - 1; i >= 0; i--) {{
                const b = webBullets[i];
                b.mesh.position.addScaledVector(b.vel, delta);
                b.life -= delta;

                if (b.mesh.position.distanceTo(boss.pos) < 3.5) {{
                    // 거미줄 명중!
                    const dmg = b.isUlt ? 35 : 8;
                    boss.hp = Math.max(0, boss.hp - dmg);
                    bossHpBar.style.width = boss.hp + '%';
                    bossHpText.innerText = boss.hp + '%';

                    // 거미줄 구속 수치 증가
                    boss.bindMeter += b.isUlt ? 60 : 25;
                    bossBindBar.style.width = Math.min(100, boss.bindMeter) + '%';

                    // 구속 게이지가 100에 도달하면 3.5초간 완전 스턴!
                    if (boss.bindMeter >= 100 && boss.stunTimer <= 0) {{
                        boss.stunTimer = 3.5;
                        boss.bindMeter = 0;
                        showBanner("🕸️ GOBLIN WEB-BOUND! (STUNNED) 🕸️", "#38bdf8");
                    }}

                    // 플레이어 궁극기 게이지 충전
                    player.ultGauge = Math.min(100, player.ultGauge + 15);
                    ultBar.style.width = player.ultGauge + '%';
                    if (player.ultGauge >= 100) ultReadyTag.style.display = 'inline';

                    scene.remove(b.mesh);
                    webBullets.splice(i, 1);

                    if (boss.hp <= 0) {{
                        isGameOver = true;
                        modalTitle.innerText = "🏆 VICTORY!";
                        modalTitle.style.color = "#22c55e";
                        modalDesc.innerText = "거미줄로 그린 고블린을 제압했습니다! 다시 도전하려면 클릭하세요.";
                        modalScreen.style.display = 'flex';
                    }}
                    continue;
                }}

                if (b.life <= 0) {{
                    scene.remove(b.mesh);
                    webBullets.splice(i, 1);
                }}
            }}

            // 4) 호박 폭탄 업데이트 & 플레이어 피격
            for (let i = pumpkinBombs.length - 1; i >= 0; i--) {{
                const pb = pumpkinBombs[i];
                pb.mesh.position.addScaledVector(pb.vel, delta);
                pb.life -= delta;

                if (pb.mesh.position.distanceTo(player.pos) < 2.0) {{
                    if (player.invulnerableTime <= 0) {{
                        player.hp = Math.max(0, player.hp - 20);
                        playerHpBar.style.width = player.hp + '%';
                        playerHpText.innerText = player.hp + '%';
                        triggerPlayerHit();

                        if (player.hp <= 0) {{
                            isGameOver = true;
                            modalTitle.innerText = "💀 MISSION FAILED";
                            modalTitle.style.color = "#ef4444";
                            modalDesc.innerText = "쓰러졌습니다. 다시 도전하려면 클릭하세요!";
                            modalScreen.style.display = 'flex';
                        }}
                    }}
                    scene.remove(pb.mesh);
                    pumpkinBombs.splice(i, 1);
                    continue;
                }}

                if (pb.life <= 0) {{
                    scene.remove(pb.mesh);
                    pumpkinBombs.splice(i, 1);
                }}
            }}

            // 5) 카메라 추적
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
