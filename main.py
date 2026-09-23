import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(
    page_title="Spider-Man 3D Web-Zip",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 여백 정리
st.markdown("""
<style>
    .block-container {
        padding: 0.5rem 1rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. 3D 게임 HTML/JS
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    html, body { 
        width: 100%; 
        height: 100vh; 
        overflow: hidden; 
        background: #0b0e14; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
    }
    #canvas-container { 
        width: 100%; 
        height: 100%; 
        position: absolute; 
        top: 0; 
        left: 0; 
        cursor: grab;
    }
    #canvas-container:active {
        cursor: grabbing;
    }
    
    /* HUD 상단 */
    #hud {
        position: absolute;
        top: 15px;
        left: 15px;
        color: #fff;
        z-index: 10;
        pointer-events: none;
        display: flex;
        gap: 10px;
    }
    .hud-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 10px 14px;
        backdrop-filter: blur(4px);
    }
    .hud-title {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        font-weight: 700;
    }
    .hud-val {
        font-size: 22px;
        font-weight: 900;
        color: #38bdf8;
    }
    .hud-val span { font-size: 12px; color: #64748b; font-weight: 600; }

    /* 플립/스턴트 알림 텍스트 */
    #stunt-alert {
        position: absolute;
        top: 80px;
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
    }
    #stunt-alert.show {
        opacity: 1;
        transform: translateX(-50%) scale(1.15);
    }
    
    /* 조작 가이드 안내 */
    #controls-guide {
        position: absolute;
        bottom: 15px;
        left: 15px;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 12px 16px;
        color: #e2e8f0;
        font-size: 12px;
        line-height: 1.6;
        z-index: 10;
        pointer-events: none;
    }
    .key-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 1px 6px;
        border-radius: 4px;
        font-weight: 700;
        color: #38bdf8;
    }

    /* 시작 오버레이 */
    #start-overlay {
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
    }
    #start-overlay h1 { 
        font-size: 34px; 
        font-weight: 900; 
        margin-bottom: 8px; 
        color: #ef4444; 
        letter-spacing: 1px; 
    }
    #start-overlay p { 
        font-size: 15px; 
        color: #cbd5e1; 
        background: rgba(255, 255, 255, 0.1); 
        padding: 8px 18px; 
        border-radius: 20px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="start-overlay">
    <h1>🕷️ SPIDER-MAN 3D CITY</h1>
    <p>▶ 여기를 클릭해서 바로 시작하세요</p>
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
</div>

<div id="stunt-alert">✨ ACROBATIC FLIP! ✨</div>

<div id="controls-guide">
    • <span class="key-badge">건물 클릭</span> 조준한 건물로 고속 웹집(Web-Zip) 비행<br>
    • <span class="key-badge">드래그</span> 시점/카메라 360도 회전<br>
    • <span class="key-badge">W</span> <span class="key-badge">A</span> <span class="key-badge">S</span> <span class="key-badge">D</span> 지상 이동 및 <b>점프/체공 중 방향 조절</b><br>
    • <span class="key-badge">Space</span> 일반 점프<br>
    • <span class="key-badge">Space 더블 탭</span> <b>공중 360도 회전 & 슈퍼 하이 점프!</b>
</div>

<div id="canvas-container"></div>

<script>
    // --- 1. Scene & Camera & Renderer ---
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a1128);
    scene.fog = new THREE.FogExp2(0x0a1128, 0.006);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // --- 2. 조명 ---
    scene.add(new THREE.HemisphereLight(0xff7744, 0x111122, 0.7));
    const dirLight = new THREE.DirectionalLight(0xffaa44, 1.2);
    dirLight.position.set(80, 140, 60);
    scene.add(dirLight);

    // --- 3. 빌딩 숲 생성 ---
    const buildings = [];
    const bldgMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 });
    const CITY_SIZE = 10;
    const SPACING = 40;

    for (let x = -CITY_SIZE/2; x < CITY_SIZE/2; x++) {
        for (let z = -CITY_SIZE/2; z < CITY_SIZE/2; z++) {
            if (Math.abs(x) < 2 && Math.abs(z) < 2) continue;
            const h = 35 + Math.random() * 85;
            const w = 18 + Math.random() * 12;
            const d = 18 + Math.random() * 12;
            const bldg = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), bldgMat);
            bldg.position.set(x * SPACING + (Math.random()-0.5)*8, h/2, z * SPACING + (Math.random()-0.5)*8);
            scene.add(bldg);
            buildings.push(bldg);
        }
    }

    // 바닥
    const floor = new THREE.Mesh(
        new THREE.PlaneGeometry(800, 800),
        new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 })
    );
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    // 골든 체크포인트 링
    const rings = [];
    const ringGeo = new THREE.TorusGeometry(3.5, 0.4, 10, 20);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xfacc15, wireframe: true });
    for (let i = 0; i < 10; i++) {
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.position.set((Math.random() - 0.5) * 220, 20 + Math.random() * 45, (Math.random() - 0.5) * 220);
        scene.add(ring);
        rings.push(ring);
    }
    let ringCount = 0;

    // --- 4. 플레이어 & 시각 메쉬 그룹 ---
    const playerGroup = new THREE.Group();
    scene.add(playerGroup);

    // 공중제비 전용 회전 서브그룹
    const flipMeshGroup = new THREE.Group();
    playerGroup.add(flipMeshGroup);

    const torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.2, 0.5), new THREE.MeshStandardMaterial({ color: 0xdc2626 }));
    torso.position.y = 0.9;
    flipMeshGroup.add(torso);

    const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), new THREE.MeshStandardMaterial({ color: 0xdc2626 }));
    head.position.y = 1.75;
    flipMeshGroup.add(head);

    const legs = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.9, 0.45), new THREE.MeshStandardMaterial({ color: 0x2563eb }));
    legs.position.y = 0.35;
    flipMeshGroup.add(legs);

    // 거미줄 라인
    const webMat = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 });
    const webGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    const webLine = new THREE.Line(webGeo, webMat);
    webLine.visible = false;
    scene.add(webLine);

    // 플레이어 물리 & 공중제비 상태
    const player = {
        pos: new THREE.Vector3(0, 15, 0),
        vel: new THREE.Vector3(),
        isGrounded: false,
        isWebZipping: false,
        zipTarget: new THREE.Vector3(),
        canDoubleJump: true,
        isFlipping: false,
        flipProgress: 0
    };

    // --- 5. 조작 및 더블 스페이스 감지 ---
    let yaw = 0;
    let pitch = 0.2;
    let isDragging = false;
    let startMouseX = 0;
    let startMouseY = 0;
    let clickStartX = 0;
    let clickStartY = 0;

    const overlay = document.getElementById('start-overlay');
    overlay.addEventListener('click', () => {
        overlay.style.opacity = '0';
        setTimeout(() => { overlay.style.display = 'none'; }, 300);
        window.focus();
    });

    const keys = {};
    let lastSpaceTime = 0;
    const stuntAlert = document.getElementById('stunt-alert');
    let alertTimeout = null;

    function triggerStuntAlert() {
        stuntAlert.classList.add('show');
        if (alertTimeout) clearTimeout(alertTimeout);
        alertTimeout = setTimeout(() => {
            stuntAlert.classList.remove('show');
        }, 800);
    }

    window.addEventListener('keydown', (e) => {
        keys[e.code] = true;

        // 스페이스바 더블 탭 로직 (더블 클릭)
        if (e.code === 'Space') {
            const now = performance.now();
            const timeDiff = now - lastSpaceTime;

            if (player.isGrounded) {
                // 바닥에서의 1차 점프
                player.vel.y = 20.0;
                player.isGrounded = false;
                player.canDoubleJump = true;
            } else {
                // 공중 상태
                if (player.isWebZipping) {
                    // 웹집 중에 스페이스 누르면 탄력 도약
                    player.isWebZipping = false;
                    webLine.visible = false;
                    player.vel.y = Math.max(player.vel.y, 24.0);
                    player.canDoubleJump = true;
                } else if (timeDiff < 350 && player.canDoubleJump) {
                    // 공중에서 더블 탭 성공 -> 360도 공중제비 & 슈퍼 점프!
                    player.vel.y = 28.0; // 높은 도약
                    
                    // 전방으로도 탄력 가속 추가
                    const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
                    player.vel.add(forward.multiplyScalar(15.0));

                    player.canDoubleJump = false;
                    player.isFlipping = true;
                    player.flipProgress = 0;
                    triggerStuntAlert();
                }
            }
            lastSpaceTime = now;
        }
    });

    window.addEventListener('keyup', (e) => { keys[e.code] = false; });

    container.addEventListener('mousedown', (e) => {
        isDragging = true;
        startMouseX = e.clientX;
        startMouseY = e.clientY;
        clickStartX = e.clientX;
        clickStartY = e.clientY;
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const dx = e.clientX - startMouseX;
        const dy = e.clientY - startMouseY;
        startMouseX = e.clientX;
        startMouseY = e.clientY;

        yaw -= dx * 0.005;
        pitch = Math.max(-0.4, Math.min(1.2, pitch + dy * 0.005));
    });

    // 건물 클릭 시 웹집
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    window.addEventListener('mouseup', (e) => {
        if (!isDragging) return;
        isDragging = false;

        const moveDist = Math.hypot(e.clientX - clickStartX, e.clientY - clickStartY);
        if (moveDist < 6) {
            const rect = renderer.domElement.getBoundingClientRect();
            mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            raycaster.far = 180;
            const hits = raycaster.intersectObjects(buildings);

            if (hits.length > 0 && hits[0].point.y > 4) {
                player.isWebZipping = true;
                player.zipTarget.copy(hits[0].point);
                webLine.visible = true;
                player.canDoubleJump = true; // 웹집 탑승 시 더블점프 리셋
            }
        }
    });

    // --- 6. 메인 업데이트 루프 ---
    const clock = new THREE.Clock();
    const speedMeter = document.getElementById('speed-meter');
    const ringScore = document.getElementById('ring-score');

    function animate() {
        requestAnimationFrame(animate);
        const delta = Math.min(clock.getDelta(), 0.05);

        // 시선 방향
        const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
        const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw)).normalize();

        // W, A, S, D 키 입력
        const move = new THREE.Vector3();
        if (keys['KeyW'] || keys['ArrowUp']) move.add(forward);
        if (keys['KeyS'] || keys['ArrowDown']) move.sub(forward);
        if (keys['KeyD'] || keys['ArrowRight']) move.add(right);
        if (keys['KeyA'] || keys['ArrowLeft']) move.sub(right);
        if (move.lengthSq() > 0) move.normalize();

        if (player.isWebZipping) {
            // [웹집 모드]
            const toTarget = new THREE.Vector3().subVectors(player.zipTarget, player.pos);
            const dist = toTarget.length();

            if (dist < 4.5) {
                player.isWebZipping = false;
                webLine.visible = false;
                player.vel.add(toTarget.normalize().multiplyScalar(24));
                player.vel.y = Math.max(player.vel.y, 22);
            } else {
                const zipSpeed = 105.0;
                player.vel.copy(toTarget.normalize().multiplyScalar(zipSpeed));

                if (keys['KeyA']) player.vel.add(right.clone().multiplyScalar(-15));
                if (keys['KeyD']) player.vel.add(right.clone().multiplyScalar(15));

                const pts = new Float32Array([
                    player.pos.x, player.pos.y + 0.8, player.pos.z,
                    player.zipTarget.x, player.zipTarget.y, player.zipTarget.z
                ]);
                webLine.geometry.setAttribute('position', new THREE.BufferAttribute(pts, 3));
            }
        } else {
            // [자유 비행 & 점프 방향 제어]
            const controlPower = player.isGrounded ? 55.0 : 42.0;
            player.vel.x += move.x * controlPower * delta;
            player.vel.z += move.z * controlPower * delta;

            // 중력
            player.vel.y -= 36.0 * delta;

            // 공기 저항
            const damp = player.isGrounded ? 6.0 : 1.2;
            player.vel.x *= Math.max(0, 1 - damp * delta);
            player.vel.z *= Math.max(0, 1 - damp * delta);
        }

        // 공중제비 360도 회전 애니메이션 처리
        if (player.isFlipping) {
            player.flipProgress += delta * 12.0; // 회전 속도
            flipMeshGroup.rotation.x = player.flipProgress;
            if (player.flipProgress >= Math.PI * 2) {
                player.flipProgress = 0;
                flipMeshGroup.rotation.x = 0;
                player.isFlipping = false;
            }
        } else {
            flipMeshGroup.rotation.x = 0;
        }

        // 위치 적용
        player.pos.addScaledVector(player.vel, delta);

        // 바닥 충돌
        if (player.pos.y <= 0.6) {
            player.pos.y = 0.6;
            player.vel.y = 0;
            player.isGrounded = true;
            player.canDoubleJump = true; // 바닥 착지 시 더블점프 쿨타임 복원
            player.isFlipping = false;
            flipMeshGroup.rotation.x = 0;
            if (player.isWebZipping) {
                player.isWebZipping = false;
                webLine.visible = false;
            }
        } else {
            player.isGrounded = false;
        }

        // 캐릭터 진행 방향 회전
        playerGroup.position.copy(player.pos);
        if (player.vel.lengthSq() > 1.0) {
            playerGroup.rotation.y = Math.atan2(player.vel.x, player.vel.z);
        }

        // 3인칭 카메라 추적
        const camDist = 6.5;
        const camH = 2.5;
        camera.position.set(
            player.pos.x + Math.sin(yaw) * Math.cos(pitch) * camDist,
            player.pos.y + Math.sin(pitch) * camDist + camH,
            player.pos.z + Math.cos(yaw) * Math.cos(pitch) * camDist
        );
        camera.lookAt(player.pos.x, player.pos.y + 1.2, player.pos.z);

        // 링 수집
        rings.forEach(ring => {
            ring.rotation.y += 0.02;
            if (ring.visible && player.pos.distanceTo(ring.position) < 5.0) {
                ring.visible = false;
                ringCount++;
                ringScore.innerHTML = `${ringCount} <span>/ 10</span>`;
                player.vel.y = Math.max(player.vel.y, 18);
                player.vel.add(forward.clone().multiplyScalar(22));
                player.canDoubleJump = true; // 링 통과 시에도 추가 점프 활성화
            }
        });

        // 속도계 업데이트
        speedMeter.innerHTML = `${Math.round(player.vel.length() * 3.6)} <span>km/h</span>`;

        renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    animate();
</script>
</body>
</html>
"""

# 4. 렌더링 (높이 840px)
components.html(game_html, height=840, scrolling=False)
