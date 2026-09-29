import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 와이드 모드 설정
st.set_page_config(
    page_title="Spider-Man Lab & 3D Web-Zip",
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

# 2. 탭 구성 (3D 시티 게임 vs 거미줄 화학 연구소)
tab_game, tab_lab = st.tabs(["🎮 3D 시티 웹집 어드벤처", "🧪 피터의 웹슈터 연구소 (거미줄 제작)"])

# 세션 상태로 거미줄 속성 보존
if "web_color" not in st.session_state:
    st.session_state.web_color = "#38bdf8"
if "web_speed" not in st.session_state:
    st.session_state.web_speed = 110
if "web_range" not in st.session_state:
    st.session_state.web_range = 190
if "web_thickness" not in st.session_state:
    st.session_state.web_thickness = 3

# ==================== [TAB 2: 거미줄 제작 페이지] ====================
with tab_lab:
    st.header("🧪 웹 플루이드(Web Fluid) 화학 조제실")
    st.write("나만의 특수 합성 폴리머 용액을 조합하여 3D 시티 게임에서 사용할 거미줄 스펙을 튜닝하세요.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("⚗️ 폴리머 화학 반응식 & 외형")
        selected_color = st.color_picker("거미줄 발광 색상 선택", st.session_state.web_color)
        selected_thickness = st.slider("거미줄 굵기 / 점도 (Line Thickness)", 1, 6, st.session_state.web_thickness)

        fluid_formula = st.selectbox(
            "합성 용액 포뮬러 종류",
            ["오리지널 나일론 실크 (표준형)", "스타크 테크 나노 웹 (초고속)", "심비오트 텐드릴 (고탄성/점착)", "일렉트로 쇼크 바운스 (특수형)"]
        )

    with col2:
        st.subheader("⚡ 비행 물리 파라미터")
        selected_speed = st.slider("웹집 인장 견인 속도 (Web-Zip Speed)", 80, 160, st.session_state.web_speed, help="건물로 발사되었을 때 끌어당기는 순간 가속도입니다.")
        selected_range = st.slider("최대 발사 사정거리 (Max Range, m)", 100, 260, st.session_state.web_range, help="레이더가 닿는 최대 도달 거리입니다.")

        st.info(f"**현재 세팅 요약**  \n• 거미줄 색상: `{selected_color}`  \n• 비행 최고 추진력: `{selected_speed} km/h`  \n• 사정거리: `{selected_range} m`")

        if st.button("🚀 조제 완료 & 웹슈터 장착하기", use_container_width=True, type="primary"):
            st.session_state.web_color = selected_color
            st.session_state.web_speed = selected_speed
            st.session_state.web_range = selected_range
            st.session_state.web_thickness = selected_thickness
            st.success("새로운 웹 플루이드 탄창이 장착되었습니다! '3D 시티 웹집 어드벤처' 탭으로 이동하세요.")

# ==================== [TAB 1: 3D 게임 플레이] ====================
with tab_game:
    # 튜닝된 파라미터 자바스크립트에 전달
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
        
        /* HUD 상단 */
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

        /* 플립/스턴트 알림 */
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

        /* 충돌 경고 */
        #hit-vignette {{
            position: absolute;
            inset: 0;
            box-shadow: inset 0 0 50px rgba(239, 68, 68, 0.7);
            opacity: 0;
            pointer-events: none;
            z-index: 25;
            transition: opacity 0.15s ease;
        }}
        
        /* 조작 가이드 안내 */
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

        /* 시작 오버레이 */
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
            <div class="hud-title">장착된 웹 용액</div>
            <div class="hud-val" style="color: {st.session_state.web_color}; font-size: 15px;">CUSTOM POLYMER</div>
        </div>
    </div>

    <div id="stunt-alert">✨ ACROBATIC FLIP! ✨</div>

    <div id="controls-guide">
        • <span class="key-badge">건물 클릭</span> 웹집 발사 (커스텀 속도: {current_web_speed}km/h)<br>
        • <span class="key-badge">드래그</span> 시점/카메라 360도 회전<br>
        • <span class="key-badge">W</span> <span class="key-badge">A</span> <span class="key-badge">S</span> <span class="key-badge">D</span> 이동 및 <b>공중 방향 조절</b><br>
        • <span class="key-badge">Space</span> 점프 | <span class="key-badge">Space 더블탭</span> <b>360도 공중제비 슈퍼점프</b><br>
        • ⚠️ <b>건물 충돌 시스템 활성화 (벽 관통 불가)</b>
    </div>

    <div id="canvas-container"></div>

    <script>
        // 연구소에서 넘겨받은 파라미터
        const WEB_COLOR = {current_web_color};
        const WEB_SPEED = {current_web_speed};
        const WEB_RANGE = {current_web_range};
        const WEB_THICKNESS = {current_web_thickness};

        // --- 1. Scene & Renderer ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a1128);
        scene.fog = new THREE.FogExp2(0x0a1128, 0.005);

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // --- 2. 조명 & 앰비언스 ---
        scene.add(new THREE.HemisphereLight(0xff7744, 0x111122, 0.7));
        const dirLight = new THREE.DirectionalLight(0xffaa44, 1.2);
        dirLight.position.set(100, 150, 70);
        scene.add(dirLight);

        // --- 3. 정밀한 빌딩 & 옥상 디테일 생성 ---
        const buildings = [];
        const buildingColliders = []; // 충돌 감지용 박스 경계 (AABB)

        // 건물 창문 캔버스 텍스처
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
        const tankMat = new THREE.MeshStandardMaterial({{ color: 0x78350f, roughness: 0.6 }}); // 나무/적갈색 물탱크

        const CITY_SIZE = 10;
        const SPACING = 42;

        for (let x = -CITY_SIZE/2; x < CITY_SIZE/2; x++) {{
            for (let z = -CITY_SIZE/2; z < CITY_SIZE/2; z++) {{
                if (Math.abs(x) < 2 && Math.abs(z) < 2) continue; // 중앙 비우기
                const h = 40 + Math.random() * 80;
                const w = 18 + Math.random() * 12;
                const d = 18 + Math.random() * 12;
                const posX = x * SPACING + (Math.random()-0.5)*8;
                const posZ = z * SPACING + (Math.random()-0.5)*8;

                // 1) 본체 빌딩
                const bldg = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), bldgMat);
                bldg.position.set(posX, h/2, posZ);
                scene.add(bldg);
                buildings.push(bldg);

                // 충돌체 AABB 데이터 저장 (플레이어 반지름 0.8 여유 포함)
                buildingColliders.push({{
                    minX: posX - w/2 - 0.7,
                    maxX: posX + w/2 + 0.7,
                    minZ: posZ - d/2 - 0.7,
                    maxZ: posZ + d/2 + 0.7,
                    topY: h
                }});

                // 2) 옥상 디테일 꾸미기 (물탱크 or 환기 덕트 or 헬리패드)
                const decoType = Math.random();
                if (decoType > 0.6) {{
                    // 옥상 원통 물탱크 (Water Tank)
                    const tank = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 4, 12), tankMat);
                    tank.position.set(posX + (Math.random()-0.5)*w*0.4, h + 2, posZ + (Math.random()-0.5)*d*0.4);
                    scene.add(tank);
                }} else if (decoType > 0.3) {{
                    // 환기구 덕트 박스
                    const duct = new THREE.Mesh(new THREE.BoxGeometry(3.5, 2.5, 3.5), roofMat);
                    duct.position.set(posX, h + 1.25, posZ);
                    scene.add(duct);
                }}
            }}
        }}

        // 도로 바닥
        const floor = new THREE.Mesh(
            new THREE.PlaneGeometry(800, 800),
            new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.9 }})
        );
        floor.rotation.x = -Math.PI / 2;
        scene.add(floor);

        // 골든 체크포인트 링
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

        // --- 4. 플레이어 & 거미줄 라인 (커스텀 색상 반영) ---
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

        // 사용자가 제작한 색상 & 굵기 적용 거미줄
        const webMat = new THREE.LineBasicMaterial({{ 
            color: WEB_COLOR, 
            linewidth: WEB_THICKNESS 
        }});
        const webGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
        const webLine = new THREE.Line(webGeo, webMat);
        webLine.visible = false;
        scene.add(webLine);

        // 플레이어 물리
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

        // --- 5. 조작 핸들러 ---
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
                        // 360도 공중제비 슈퍼 점프
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
                raycaster.far = WEB_RANGE; // 커스텀 사정거리
                const hits = raycaster.intersectObjects(buildings);

                if (hits.length > 0 && hits[0].point.y > 4) {{
                    player.isWebZipping = true;
                    player.zipTarget.copy(hits[0].point);
                    webLine.visible = true;
                    player.canDoubleJump = true;
                }}
            }}
        }});

        // --- 6. 정밀 충돌 판정 (AABB Collision) ---
        function resolveBuildingCollisions() {{
            const px = player.pos.x;
            const py = player.pos.y;
            const pz = player.pos.z;

            for (let b of buildingColliders) {{
                // 건물의 가로 세로 범위 안에 플레이어가 들어왔는가?
                if (px > b.minX && px < b.maxX && pz > b.minZ && pz < b.maxZ) {{
                    // 플레이어의 발이 건물 옥상보다 위에 있으면 옥상 착지
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
                    // 건물 벽체에 충돌했을 때 (관통 방지 밀어내기)
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

                        // 벽에 부딪히면 튕김 처리 및 웹집 해제
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

        // --- 7. 메인 루프 ---
        const clock = new THREE.Clock();
        const speedMeter = document.getElementById('speed-meter');
        const ringScore = document.getElementById('ring-score');

        function animate() {{
            requestAnimationFrame(animate);
            const delta = Math.min(clock.getDelta(), 0.05);

            const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
            const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw)).normalize();

            // W, A, S, D 이동
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
                    // 커스텀 웹 속도 반영
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

                player.vel.y -= 36.0 * delta; // 중력
                const damp = player.isGrounded ? 6.0 : 1.2;
                player.vel.x *= Math.max(0, 1 - damp * delta);
                player.vel.z *= Math.max(0, 1 - damp * delta);
            }}

            // 360도 공중제비 플립 애니메이션
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

            // 좌표 업데이트 & 충돌 판정 실행
            player.pos.addScaledVector(player.vel, delta);
            resolveBuildingCollisions();

            // 바닥 착지
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

            // 플레이어 메쉬 회전
            playerGroup.position.copy(player.pos);
            if (player.vel.lengthSq() > 1.0) {{
                playerGroup.rotation.y = Math.atan2(player.vel.x, player.vel.z);
            }}

            // 3인칭 숄더뷰 추적
            const camDist = 6.8;
            const camH = 2.6;
            camera.position.set(
                player.pos.x + Math.sin(yaw) * Math.cos(pitch) * camDist,
                player.pos.y + Math.sin(pitch) * camDist + camH,
                player.pos.z + Math.cos(yaw) * Math.cos(pitch) * camDist
            );
            camera.lookAt(player.pos.x, player.pos.y + 1.2, player.pos.z);

            // 링 수집 판정
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
