import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 페이지 설정 (전체 화면 와이드 모드)
st.set_page_config(
    page_title="Spider-Man 3D Web-Zip & Air Glide",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 스트림릿 기본 여백 및 패딩 최소화
st.markdown("""
<style>
    .main > div {
        padding: 0rem;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    body {
        margin: 0;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# 2. 3D 게임 임베디드 HTML/JS
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    html, body { width: 100%; height: 100vh; overflow: hidden; background: #0b0e14; font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif; }
    #canvas-container { width: 100%; height: 100%; position: absolute; top: 0; left: 0; }
    
    /* HUD 오버레이 */
    #hud {
        position: absolute;
        top: 20px;
        left: 20px;
        color: #fff;
        z-index: 10;
        pointer-events: none;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .hud-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 12px 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    }
    .hud-title {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #94a3b8;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .hud-val {
        font-size: 26px;
        font-weight: 900;
        color: #38bdf8;
        display: flex;
        align-items: baseline;
        gap: 4px;
    }
    .hud-val span { font-size: 13px; color: #64748b; font-weight: 600; }
    
    /* 조작 안내 */
    #controls-guide {
        position: absolute;
        bottom: 20px;
        left: 20px;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 14px 18px;
        color: #e2e8f0;
        font-size: 13px;
        line-height: 1.6;
        z-index: 10;
        pointer-events: none;
    }
    .key-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 2px 7px;
        border-radius: 6px;
        font-weight: 700;
        color: #f8fafc;
        margin: 0 2px;
        border-bottom: 2px solid rgba(0,0,0,0.3);
    }

    /* 조준점 (Reticle) */
    #crosshair {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 32px;
        height: 32px;
        transform: translate(-50%, -50%);
        pointer-events: none;
        z-index: 20;
        transition: transform 0.1s ease, border-color 0.2s ease;
    }
    #crosshair::before, #crosshair::after {
        content: '';
        position: absolute;
        background: #ef4444;
        transition: background 0.2s ease, transform 0.2s ease;
    }
    #crosshair::before { top: 15px; left: 0; width: 32px; height: 2px; }
    #crosshair::after { top: 0; left: 15px; width: 2px; height: 32px; }
    #crosshair.locked::before, #crosshair.locked::after {
        background: #22c55e;
        box-shadow: 0 0 10px #22c55e;
    }
    #crosshair.locked {
        transform: translate(-50%, -50%) scale(1.25) rotate(45deg);
    }
    #lock-dist {
        position: absolute;
        top: 38px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 11px;
        font-weight: 700;
        color: #22c55e;
        letter-spacing: 1px;
        white-space: nowrap;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }

    /* 화면 클릭 유도 오버레이 */
    #start-overlay {
        position: absolute;
        inset: 0;
        background: rgba(0,0,0,0.65);
        backdrop-filter: blur(6px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #fff;
        z-index: 100;
        cursor: pointer;
    }
    #start-overlay h1 { font-size: 38px; font-weight: 900; margin-bottom: 12px; color: #ef4444; letter-spacing: 2px; text-shadow: 0 0 20px rgba(239,68,68,0.5); }
    #start-overlay p { font-size: 16px; color: #cbd5e1; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="start-overlay">
    <h1>SPIDER-MAN 3D CITY</h1>
    <p>화면을 클릭하여 컨트롤을 시작하세요</p>
</div>

<div id="hud">
    <div class="hud-card">
        <div class="hud-title">속도 (SPEED)</div>
        <div class="hud-val" id="speed-meter">0 <span>km/h</span></div>
    </div>
    <div class="hud-card">
        <div class="hud-title">수집한 링 (RINGS)</div>
        <div class="hud-val" id="ring-score">0 <span>/ 10</span></div>
    </div>
</div>

<div id="controls-guide">
    <span class="key-badge">클릭</span> 마우스 잠금 & 해제<br>
    <span class="key-badge">마우스 이동</span> 시야 회전 및 조준<br>
    <span class="key-badge">좌클릭</span> 초록색 조준점 건물로 고속 웹집(Web-Zip)<br>
    <span class="key-badge">W</span> <span class="key-badge">A</span> <span class="key-badge">S</span> <span class="key-badge">D</span> 지상 이동 및 <b>공중 체공/점프 중 방향 조정</b><br>
    <span class="key-badge">Space</span> 높이 도약 점프 / 웹줄 분리
</div>

<div id="crosshair">
    <div id="lock-dist"></div>
</div>

<div id="canvas-container"></div>

<script>
    // --- 1. 기본 Scene, Camera, Renderer ---
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a1128);
    scene.fog = new THREE.FogExp2(0x0a1128, 0.005);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // --- 2. 조명 (일몰 노을 & 도시 반사광) ---
    const hemiLight = new THREE.HemisphereLight(0xff7744, 0x111122, 0.6);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xffaa44, 1.2);
    dirLight.position.set(100, 150, 50);
    scene.add(dirLight);

    // --- 3. 도시 빌딩 생성 & 바닥 ---
    const buildings = [];
    const buildingGeo = new THREE.BoxGeometry(1, 1, 1);
    
    // 창문 텍스처 시뮬레이션용 캔버스 패턴
    const canvasTex = document.createElement('canvas');
    canvasTex.width = 128;
    canvasTex.height = 128;
    const ctx = canvasTex.getContext('2d');
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0,0,128,128);
    ctx.fillStyle = '#fde047';
    for(let i=10; i<128; i+=25){
        for(let j=10; j<128; j+=25){
            if(Math.random() > 0.4) ctx.fillRect(i, j, 12, 16);
        }
    }
    const bldgTex = new THREE.CanvasTexture(canvasTex);
    bldgTex.wrapS = THREE.RepeatWrapping;
    bldgTex.wrapT = THREE.RepeatWrapping;

    const bldgMat = new THREE.MeshStandardMaterial({
        map: bldgTex,
        roughness: 0.3,
        metalness: 0.4
    });

    const CITY_SIZE = 12;
    const SPACING = 45;
    for(let x = -CITY_SIZE/2; x < CITY_SIZE/2; x++){
        for(let z = -CITY_SIZE/2; z < CITY_SIZE/2; z++){
            if(Math.abs(x) < 2 && Math.abs(z) < 2) continue; // 중앙 광장 확보
            const h = 40 + Math.random() * 90;
            const w = 20 + Math.random() * 15;
            const d = 20 + Math.random() * 15;
            
            const bldg = new THREE.Mesh(buildingGeo, bldgMat);
            bldg.scale.set(w, h, d);
            bldg.position.set(x * SPACING + (Math.random()-0.5)*10, h/2, z * SPACING + (Math.random()-0.5)*10);
            scene.add(bldg);
            buildings.push(bldg);
        }
    }

    // 바닥 (도로)
    const floorGeo = new THREE.PlaneGeometry(800, 800);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    // --- 4. 공중 체크포인트 링 (Ring Targets) ---
    const rings = [];
    const ringGeo = new THREE.TorusGeometry(3.5, 0.4, 12, 24);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xfacc15, wireframe: true });
    for(let i=0; i<10; i++){
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.position.set((Math.random()-0.5)*260, 25 + Math.random()*50, (Math.random()-0.5)*260);
        scene.add(ring);
        rings.push(ring);
    }
    let collectedRings = 0;

    // --- 5. 플레이어 (스파이더맨 아바타 & 파티클) ---
    const playerGroup = new THREE.Group();
    scene.add(playerGroup);

    // 스파이더맨 바디 메쉬 (빨강 & 파랑 콤비)
    const torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.2, 0.5), new THREE.MeshStandardMaterial({ color: 0xdc2626 }));
    torso.position.y = 0.9;
    playerGroup.add(torso);

    const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), new THREE.MeshStandardMaterial({ color: 0xdc2626 }));
    head.position.y = 1.75;
    playerGroup.add(head);

    const legs = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.9, 0.45), new THREE.MeshStandardMaterial({ color: 0x2563eb }));
    legs.position.y = 0.35;
    playerGroup.add(legs);

    // 거미줄 렌더러 (Line)
    const webLineMat = new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 });
    const webLineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    const webLine = new THREE.Line(webLineGeo, webLineMat);
    webLine.visible = false;
    scene.add(webLine);

    // --- 6. 물리 및 이동 컨트롤러 ---
    const player = {
        pos: new THREE.Vector3(0, 15, 0),
        vel: new THREE.Vector3(),
        isGrounded: false,
        isWebZipping: false,
        zipTarget: new THREE.Vector3(),
        zipDistance: 0
    };

    const keys = {};
    window.addEventListener('keydown', (e) => { keys[e.code] = true; });
    window.addEventListener('keyup', (e) => { keys[e.code] = false; });

    // 1인칭/3인칭 카메라 마우스 룩 (Pointer Lock)
    let pitch = 0;
    let yaw = 0;
    const overlay = document.getElementById('start-overlay');
    
    overlay.addEventListener('click', () => {
        document.body.requestPointerLock();
    });

    document.addEventListener('pointerlockchange', () => {
        if (document.pointerLockElement === document.body) {
            overlay.style.display = 'none';
        } else {
            overlay.style.display = 'flex';
        }
    });

    document.addEventListener('mousemove', (e) => {
        if (document.pointerLockElement !== document.body) return;
        const sensitivity = 0.0022;
        yaw -= e.movementX * sensitivity;
        pitch -= e.movementY * sensitivity;
        pitch = Math.max(-Math.PI / 2.3, Math.min(Math.PI / 2.3, pitch));
    });

    // 레이캐스터 (조준 및 건물 탐색)
    const raycaster = new THREE.Raycaster();
    const crosshair = document.getElementById('crosshair');
    const lockDistText = document.getElementById('lock-dist');
    let lockedPoint = null;

    // 마우스 좌클릭: 웹집 (Web-Zip) 발사
    window.addEventListener('mousedown', (e) => {
        if (document.pointerLockElement !== document.body) return;
        if (e.button === 0 && lockedPoint) {
            // 웹집 시작
            player.isWebZipping = true;
            player.zipTarget.copy(lockedPoint);
            player.zipDistance = player.pos.distanceTo(lockedPoint);
            webLine.visible = true;
        }
    });

    // --- 7. 메인 루프 (업데이트 로직) ---
    const clock = new THREE.Clock();
    const speedMeter = document.getElementById('speed-meter');
    const ringScore = document.getElementById('ring-score');

    function update() {
        const delta = Math.min(clock.getDelta(), 0.05);

        // 1. 카메라 방향 벡터 계산
        const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw)).normalize();
        const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw)).normalize();

        // 2. 조준점 락온 탐색 (화면 중앙 기준)
        const aimDir = new THREE.Vector3(
            -Math.sin(yaw) * Math.cos(pitch),
            Math.sin(pitch),
            -Math.cos(yaw) * Math.cos(pitch)
        ).normalize();

        raycaster.set(camera.position, aimDir);
        raycaster.far = 175; // 거미줄 최대 사거리
        const intersects = raycaster.intersectObjects(buildings);

        if (intersects.length > 0 && intersects[0].point.y > 5) {
            lockedPoint = intersects[0].point;
            crosshair.classList.add('locked');
            const d = Math.round(camera.position.distanceTo(lockedPoint));
            lockDistText.innerText = `${d}m (WEB-ZIP)`;
        } else {
            lockedPoint = null;
            crosshair.classList.remove('locked');
            lockDistText.innerText = '';
        }

        // 3. 이동 및 공중 기동 (W, A, S, D 키 입력)
        const moveInput = new THREE.Vector3();
        if (keys['KeyW']) moveInput.add(forward);
        if (keys['KeyS']) moveInput.sub(forward);
        if (keys['KeyD']) moveInput.add(right);
        if (keys['KeyA']) moveInput.sub(right);
        if (moveInput.lengthSq() > 0) moveInput.normalize();

        if (player.isWebZipping) {
            // [웹집 모드]: 타겟 지점으로 고속 질주
            const toTarget = new THREE.Vector3().subVectors(player.zipTarget, player.pos);
            const dist = toTarget.length();

            if (dist < 4.0 || keys['Space']) {
                // 도착 직전이거나 스페이스바로 캔슬 점프 시 탄력 도약
                player.isWebZipping = false;
                webLine.visible = false;
                player.vel.add(toTarget.normalize().multiplyScalar(28));
                player.vel.y = Math.max(player.vel.y, 22); // 도약 고도 상승
            } else {
                // 목표 지점으로 급가속
                const zipSpeed = 110.0;
                player.vel.copy(toTarget.normalize().multiplyScalar(zipSpeed));

                // 웹집 도중에도 A, D 키로 좌우 궤적 미세 커브 제어 가능
                if (keys['KeyA']) player.vel.add(right.clone().multiplyScalar(-20));
                if (keys['KeyD']) player.vel.add(right.clone().multiplyScalar(20));

                // 웹 라인 연결
                const posArr = new Float32Array([
                    player.pos.x, player.pos.y + 0.8, player.pos.z,
                    player.zipTarget.x, player.zipTarget.y, player.zipTarget.z
                ]);
                webLine.geometry.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
            }
        } else {
            // [자유 비행 / 점프 / 지상 모드]: 공중에서도 W, A, S, D로 방향 조작
            const airControl = player.isGrounded ? 55.0 : 42.0; // 공중에서도 높은 조타력 제공
            player.vel.x += moveInput.x * airControl * delta;
            player.vel.z += moveInput.z * airControl * delta;

            // 중력 적용
            player.vel.y -= 38.0 * delta;

            // 공기 저항 (공중 글라이딩 감속)
            const damping = player.isGrounded ? 6.0 : 1.2;
            player.vel.x *= Math.max(0, 1 - damping * delta);
            player.vel.z *= Math.max(0, 1 - damping * delta);

            // 점프 (지상에서 Space 누를 때)
            if (keys['Space'] && player.isGrounded) {
                player.vel.y = 20.0;
                player.isGrounded = false;
            }
        }

        // 위치 갱신
        player.pos.addScaledVector(player.vel, delta);

        // 지면 충돌
        if (player.pos.y <= 0.6) {
            player.pos.y = 0.6;
            player.vel.y = 0;
            player.isGrounded = true;
            if (player.isWebZipping) {
                player.isWebZipping = false;
                webLine.visible = false;
            }
        } else {
            player.isGrounded = false;
        }

        // 플레이어 메쉬 갱신 및 회전
        playerGroup.position.copy(player.pos);
        if (player.vel.lengthSq() > 1.0) {
            const lookAngle = Math.atan2(player.vel.x, player.vel.z);
            playerGroup.rotation.y = lookAngle;
            // 비행 시 앞쪽으로 몸체 틸트
            const horizontalSpeed = Math.sqrt(player.vel.x * player.vel.x + player.vel.z * player.vel.z);
            playerGroup.rotation.x = Math.min(Math.PI / 4, horizontalSpeed * 0.015);
        }

        // 4. 카메라 트래킹 (스파이더맨 3인칭 숄더뷰)
        const camDist = 6.5;
        const camHeight = 2.4;
        const camOffset = new THREE.Vector3(
            Math.sin(yaw) * Math.cos(pitch) * camDist,
            Math.sin(pitch) * camDist + camHeight,
            Math.cos(yaw) * Math.cos(pitch) * camDist
        );
        camera.position.copy(player.pos).add(camOffset);
        camera.lookAt(player.pos.x, player.pos.y + 1.2, player.pos.z);

        // 5. 링 수집 판정 & 애니메이션
        rings.forEach(ring => {
            ring.rotation.y += 0.02;
            ring.rotation.x += 0.01;
            if (ring.visible && player.pos.distanceTo(ring.position) < 5.0) {
                ring.visible = false;
                collectedRings++;
                ringScore.innerHTML = `${collectedRings} <span>/ 10</span>`;
                // 링 통과 보너스 가속
                player.vel.y = Math.max(player.vel.y, 15);
                player.vel.add(forward.clone().multiplyScalar(20));
            }
        });

        // 6. HUD 속도계 업데이트 (km/h 환산)
        const currentSpeedKmh = Math.round(player.vel.length() * 3.6);
        speedMeter.innerHTML = `${currentSpeedKmh} <span>km/h</span>`;

        renderer.render(scene, camera);
        requestAnimationFrame(update);
    }

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    update();
</script>
</body>
</html>
"""

# 3. Streamlit 컴포넌트로 렌더링 (화면 높이 880px 확보)
components.html(game_html, height=880, scrolling=False)
