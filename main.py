<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>스파이더맨 3D 웹 슬링거 (Spider Web Zip 3D)</title>
    <!-- Tailwind CSS for sleek overlay UI -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Three.js (3D engine) & Tone.js (Procedural audio) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Noto+Sans+KR:wght@400;600;800&display=swap');
        
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
        }

        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: 'Noto Sans KR', sans-serif;
            background-color: #050508;
            color: #ffffff;
        }

        #canvas-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        .hud-font {
            font-family: 'Orbitron', sans-serif;
        }

        /* Spider Reticle Cursor */
        .reticle {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 44px;
            height: 44px;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 20;
            transition: transform 0.15s ease-out, border-color 0.2s;
        }

        .reticle-corner {
            position: absolute;
            width: 10px;
            height: 10px;
            border: 2px solid rgba(255, 255, 255, 0.7);
        }

        .reticle.can-hook .reticle-corner {
            border-color: #00ffaa;
            filter: drop-shadow(0 0 6px rgba(0, 255, 170, 0.9));
        }

        .reticle.cannot-hook .reticle-corner {
            border-color: #ff3344;
            filter: drop-shadow(0 0 4px rgba(255, 51, 68, 0.5));
        }

        .reticle.hooked .reticle-corner {
            border-color: #00d9ff;
            filter: drop-shadow(0 0 10px rgba(0, 217, 255, 1));
            transform: scale(1.2);
        }

        /* Speed lines visual effect */
        #speed-vignette {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 10;
            opacity: 0;
            background: radial-gradient(circle, transparent 45%, rgba(0, 162, 255, 0.25) 85%, rgba(220, 20, 60, 0.4) 100%);
            transition: opacity 0.2s ease-out;
        }

        /* Glassmorphism panels */
        .spider-panel {
            background: rgba(12, 16, 28, 0.75);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        }
    </style>
</head>
<body class="relative overflow-hidden">
    <!-- 3D Canvas Viewport -->
    <div id="canvas-container"></div>

    <!-- Speed Lines Vignette -->
    <div id="speed-vignette"></div>

    <!-- Spider Reticle / Aim Cursor -->
    <div id="reticle" class="reticle cannot-hook">
        <div class="reticle-corner top-0 left-0 border-r-0 border-b-0"></div>
        <div class="reticle-corner top-0 right-0 border-l-0 border-b-0"></div>
        <div class="reticle-corner bottom-0 left-0 border-r-0 border-t-0"></div>
        <div class="reticle-corner bottom-0 right-0 border-l-0 border-t-0"></div>
        <div id="reticle-dot" class="w-1.5 h-1.5 bg-white rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
        <div id="distance-badge" class="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] hud-font font-bold px-1.5 py-0.5 rounded bg-black/60 text-emerald-300">-- m</div>
    </div>

    <!-- Upper HUD: Title, Score, Checkpoint Rings -->
    <div class="absolute top-4 left-4 right-4 flex justify-between items-start pointer-events-none z-30">
        <!-- Spider Stat Card -->
        <div class="spider-panel rounded-2xl p-4 flex items-center space-x-4 pointer-events-auto">
            <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-red-600 to-rose-400 flex items-center justify-center shadow-lg shadow-red-600/40">
                <svg class="w-7 h-7 text-white" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
            </div>
            <div>
                <div class="text-xs uppercase font-extrabold tracking-widest text-red-400">SPIDER WEB-ZIPPER</div>
                <div class="flex items-baseline space-x-2">
                    <span id="score-text" class="text-3xl font-black hud-font text-white">0</span>
                    <span class="text-xs text-gray-400 font-medium">PTS</span>
                </div>
            </div>
        </div>

        <!-- Combo & Ring Tracker -->
        <div class="flex flex-col items-end space-y-2">
            <div class="spider-panel rounded-2xl px-5 py-2.5 flex items-center space-x-3 pointer-events-auto">
                <div class="text-right">
                    <div class="text-[10px] text-yellow-400 font-bold tracking-wider">CHECKPOINT RINGS</div>
                    <div id="ring-count" class="hud-font font-bold text-xl text-yellow-300">0 / 12</div>
                </div>
                <div class="text-2xl">⚡</div>
            </div>
            <div id="combo-badge" class="spider-panel rounded-xl px-4 py-1.5 opacity-0 transition-opacity duration-300">
                <span class="text-xs text-cyan-400 font-black hud-font" id="combo-text">PERFECT ZIP x1</span>
            </div>
        </div>
    </div>

    <!-- Bottom HUD: Velocity, Web Fluid & Control Hints -->
    <div class="absolute bottom-5 left-5 right-5 flex justify-between items-end pointer-events-none z-30">
        <!-- Speedometer -->
        <div class="spider-panel rounded-2xl p-4 w-48 pointer-events-auto">
            <div class="flex justify-between items-baseline mb-1">
                <span class="text-xs font-bold text-gray-400">VELOCITY</span>
                <span class="hud-font text-xs text-cyan-400 font-semibold">ZIP SPEED</span>
            </div>
            <div class="flex items-baseline space-x-1.5">
                <span id="speed-display" class="hud-font text-4xl font-black text-cyan-400">0</span>
                <span class="hud-font text-xs font-bold text-gray-300">KM/H</span>
            </div>
            <!-- Dynamic Speed Bar -->
            <div class="w-full bg-gray-800/80 rounded-full h-1.5 mt-2 overflow-hidden">
                <div id="speed-meter" class="bg-gradient-to-r from-cyan-400 via-blue-500 to-rose-500 h-full w-0 transition-all duration-75"></div>
            </div>
        </div>

        <!-- Web Fluid Gauge & Center Action Indicator -->
        <div class="flex flex-col items-center">
            <div id="status-hint" class="spider-panel rounded-full px-5 py-2 mb-3 text-xs font-bold text-white tracking-wide border-red-500/30 flex items-center space-x-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span id="action-hint-text">건물 표면을 조준하고 좌클릭으로 거미줄을 발사하세요!</span>
            </div>

            <!-- Web Fluid Bar -->
            <div class="spider-panel rounded-2xl px-4 py-2 flex items-center space-x-3 pointer-events-auto">
                <span class="text-xs font-bold text-red-400">WEB FLUID</span>
                <div class="w-32 bg-gray-900 rounded-full h-2.5 p-0.5 border border-red-500/30">
                    <div id="fluid-bar" class="h-full bg-gradient-to-r from-red-600 to-rose-400 rounded-full w-full transition-all duration-100"></div>
                </div>
                <span id="fluid-percent" class="hud-font text-xs font-bold text-white">100%</span>
            </div>
        </div>

        <!-- Guide & Controls Button -->
        <div class="flex space-x-2 pointer-events-auto">
            <button id="btn-sound" class="spider-panel hover:bg-slate-800/80 text-white rounded-2xl p-3.5 transition flex items-center justify-center">
                <svg id="icon-sound" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                </svg>
            </button>
            <button id="btn-help" class="spider-panel hover:bg-slate-800/80 text-white rounded-2xl px-4 py-3 text-xs font-bold tracking-wider transition">
                조작 설명서 [H]
            </button>
            <button id="btn-reset" class="spider-panel bg-red-600/80 hover:bg-red-500 text-white rounded-2xl px-4 py-3 text-xs font-bold tracking-wider transition shadow-lg shadow-red-900/50">
                위치 리셋 [R]
            </button>
        </div>
    </div>

    <!-- Help Modal Overlay -->
    <div id="help-modal" class="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50 transition-opacity duration-200">
        <div class="spider-panel rounded-3xl max-w-lg w-full p-7 mx-4 border border-rose-500/40 relative">
            <div class="flex justify-between items-center pb-4 border-b border-white/10 mb-4">
                <div class="flex items-center space-x-3">
                    <div class="w-3 h-3 rounded-full bg-rose-500 animate-ping"></div>
                    <h2 class="text-xl font-black tracking-wide text-white">SPIDER-MAN 웹 조작 가이드</h2>
                </div>
                <button id="btn-close-help" class="text-gray-400 hover:text-white text-2xl font-bold leading-none">&times;</button>
            </div>
            
            <div class="space-y-4 text-sm text-gray-300">
                <div class="flex items-start space-x-3 bg-white/5 p-3 rounded-xl">
                    <span class="px-2 py-1 bg-red-600 rounded text-xs font-bold text-white whitespace-nowrap">마우스 이동</span>
                    <p class="text-xs text-gray-200">화면을 드래그하거나 움직여 건물을 조준합니다. 사정거리(180m) 안의 건물에 닿으면 조준선이 <strong class="text-emerald-400">초록색</strong>으로 변경됩니다.</p>
                </div>
                <div class="flex items-start space-x-3 bg-white/5 p-3 rounded-xl">
                    <span class="px-2 py-1 bg-cyan-600 rounded text-xs font-bold text-white whitespace-nowrap">좌클릭 / 터치</span>
                    <p class="text-xs text-gray-200"><strong>웹 발사 & 고속 웹집(Web-Zip)</strong>: 탄성 높은 거미줄을 발사하여 목표 지점으로 번개처럼 급가속해 날아갑니다.</p>
                </div>
                <div class="flex items-start space-x-3 bg-white/5 p-3 rounded-xl">
                    <span class="px-2 py-1 bg-amber-600 rounded text-xs font-bold text-white whitespace-nowrap">Space / 우클릭</span>
                    <p class="text-xs text-gray-200"><strong>거미줄 분리 & 공중 부스트 점프</strong>: 비행 도중 거미줄을 끊고 전방 상공으로 시원하게 탄력 도약합니다.</p>
                </div>
                <div class="flex items-start space-x-3 bg-white/5 p-3 rounded-xl">
                    <span class="px-2 py-1 bg-purple-600 rounded text-xs font-bold text-white whitespace-nowrap">W, A, S, D</span>
                    <p class="text-xs text-gray-200">공중 자세 제어 및 이동. 높은 빌딩 사이를 날아다니며 황금 링(체크포인트)을 통과해 최고 점수를 기록해보세요!</p>
                </div>
            </div>

            <div class="mt-6 flex justify-end">
                <button id="btn-start-game" class="w-full py-3.5 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-extrabold text-sm tracking-widest uppercase shadow-lg shadow-red-600/40 transition">
                    도시 속으로 출동 (게임 시작)
                </button>
            </div>
        </div>
    </div>

    <script>
        /* ==========================================================
           AUDIO SYSTEM (Tone.js Synthesizers for Spider-Man sounds)
           ========================================================== */
        let audioActive = false;
        let webShootSynth, whooshSynth, dingSynth;

        function initAudio() {
            if (audioActive) return;
            try {
                Tone.start();
                // Sharp web shooter whip 'Thwip'
                webShootSynth = new Tone.NoiseSynth({
                    noise: { type: 'white' },
                    envelope: { attack: 0.002, decay: 0.12, sustain: 0, release: 0.05 }
                }).toDestination();
                webShootSynth.volume.value = -4;

                // High speed whoosh synth (FM tone)
                whooshSynth = new Tone.Synth({
                    oscillator: { type: 'triangle' },
                    envelope: { attack: 0.05, decay: 0.4, sustain: 0.1, release: 0.5 }
                }).toDestination();
                whooshSynth.volume.value = -12;

                // Ring checkpoint chime
                dingSynth = new Tone.PolySynth(Tone.Synth, {
                    oscillator: { type: 'sine' },
                    envelope: { attack: 0.01, decay: 0.3, sustain: 0, release: 0.8 }
                }).toDestination();
                dingSynth.volume.value = -8;

                audioActive = true;
            } catch (e) {
                console.warn("Audio init failed:", e);
            }
        }

        function playWebSound() {
            if (!audioActive) return;
            try {
                webShootSynth.triggerAttackRelease("16n");
                whooshSynth.triggerAttackRelease("C3", "8n");
            } catch (e) {}
        }

        function playRingSound() {
            if (!audioActive) return;
            try {
                dingSynth.triggerAttackRelease(["E5", "G#5", "B5"], "8n");
            } catch (e) {}
        }

        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0e1c);
        scene.fog = new THREE.FogExp2(0x0d1224, 0.0035);

        const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.5, 900);
        const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.1;
        container.appendChild(renderer.domElement);

        /* Lights: Dusk Sunset Skyline Atmosphere */
        const ambientLight = new THREE.AmbientLight(0x283250, 1.2);
        scene.add(ambientLight);

        const sunLight = new THREE.DirectionalLight(0xff7744, 2.0);
        sunLight.position.set(120, 200, -80);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 2048;
        sunLight.shadow.mapSize.height = 2048;
        sunLight.shadow.camera.near = 10;
        sunLight.shadow.camera.far = 600;
        const d = 180;
        sunLight.shadow.camera.left = -d;
        sunLight.shadow.camera.right = d;
        sunLight.shadow.camera.top = d;
        sunLight.shadow.camera.bottom = -d;
        scene.add(sunLight);

        const skyFill = new THREE.HemisphereLight(0x3a4f78, 0x11131a, 0.8);
        scene.add(skyFill);

        const buildings = [];
        const buildingMeshes = [];
        const CITY_SIZE = 12; // 12x12 blocks
        const BLOCK_SPACING = 38;

        // Ground Road Grid
        const groundGeo = new THREE.PlaneGeometry(1600, 1600, 32, 32);
        const groundMat = new THREE.MeshStandardMaterial({
            color: 0x090c14,
            roughness: 0.85,
            metalness: 0.2
        });
        const ground = new THREE.Mesh(groundGeo, groundMat);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        scene.add(ground);

        // Ground grid glow lines (streets)
        const gridHelper = new THREE.GridHelper(1600, 80, 0x00a2ff, 0x162038);
        gridHelper.position.y = 0.3;
        scene.add(gridHelper);

        // Procedural Window Canvas Texture
        function createBuildingTexture(baseColHex, litWindowChance) {
            const canvas = document.createElement('canvas');
            canvas.width = 128;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = baseColHex;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            const rows = 16;
            const cols = 8;
            const padX = 4;
            const padY = 5;
            const w = (canvas.width - padX * (cols + 1)) / cols;
            const h = (canvas.height - padY * (rows + 1)) / rows;

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    if (Math.random() < litWindowChance) {
                        const isGold = Math.random() > 0.4;
                        ctx.fillStyle = isGold ? '#ffe79a' : '#5ce1e6';
                    } else {
                        ctx.fillStyle = '#080d1a';
                    }
                    ctx.fillRect(padX + c * (w + padX), padY + r * (h + padY), w, h);
                }
            }
            const texture = new THREE.CanvasTexture(canvas);
            texture.wrapS = THREE.RepeatWrapping;
            texture.wrapT = THREE.RepeatWrapping;
            return texture;
        }

        const bldTex1 = createBuildingTexture('#141c2e', 0.45);
        const bldTex2 = createBuildingTexture('#0f1624', 0.3);
        const bldTex3 = createBuildingTexture('#181f33', 0.6);

        const buildingMaterials = [
            new THREE.MeshStandardMaterial({ map: bldTex1, roughness: 0.4, metalness: 0.6 }),
            new THREE.MeshStandardMaterial({ map: bldTex2, roughness: 0.5, metalness: 0.4 }),
            new THREE.MeshStandardMaterial({ map: bldTex3, roughness: 0.3, metalness: 0.7 })
        ];

        // Generate City Skyscrapers
        const bldGeoBase = new THREE.BoxGeometry(1, 1, 1);
        const halfSize = (CITY_SIZE * BLOCK_SPACING) / 2;

        for (let x = -CITY_SIZE / 2; x < CITY_SIZE / 2; x++) {
            for (let z = -CITY_SIZE / 2; z < CITY_SIZE / 2; z++) {
                // leave occasional plaza / central canyon open
                if (Math.abs(x) < 1 && Math.abs(z) < 1) continue;

                const posX = x * BLOCK_SPACING + (Math.random() * 8 - 4);
                const posZ = z * BLOCK_SPACING + (Math.random() * 8 - 4);
                const width = 16 + Math.random() * 14;
                const depth = 16 + Math.random() * 14;
                const height = 50 + Math.random() * 130 + (Math.abs(x) < 3 ? 40 : 0);

                const mat = buildingMaterials[Math.floor(Math.random() * buildingMaterials.length)];
                const building = new THREE.Mesh(bldGeoBase, mat);
                building.scale.set(width, height, depth);
                building.position.set(posX, height / 2, posZ);
                building.castShadow = true;
                building.receiveShadow = true;

                // Configure texture scale for building height
                building.material.map.repeat.set(1, Math.floor(height / 20));

                scene.add(building);
                buildings.push({
                    mesh: building,
                    minX: posX - width / 2,
                    maxX: posX + width / 2,
                    minZ: posZ - depth / 2,
                    maxZ: posZ + depth / 2,
                    topY: height
                });
                buildingMeshes.push(building);

                // Add rooftop neon edge/spire
                if (Math.random() > 0.6) {
                    const spireGeo = new THREE.CylinderGeometry(0.3, 0.8, 14, 8);
                    const spireMat = new THREE.MeshBasicMaterial({ color: 0xff3b5c });
                    const spire = new THREE.Mesh(spireGeo, spireMat);
                    spire.position.set(posX, height + 7, posZ);
                    scene.add(spire);
                }
            }
        }

        const rings = [];
        const ringGeo = new THREE.TorusGeometry(4.2, 0.45, 12, 32);
        const ringMat = new THREE.MeshStandardMaterial({
            color: 0xffb703,
            emissive: 0xff9900,
            emissiveIntensity: 0.8,
            roughness: 0.2,
            metalness: 0.9
        });

        function spawnSkyRings() {
            for (let i = 0; i < 14; i++) {
                const ring = new THREE.Mesh(ringGeo, ringMat.clone());
                const angle = (i / 14) * Math.PI * 2;
                const rad = 60 + Math.random() * 80;
                ring.position.set(
                    Math.cos(angle) * rad + (Math.random() * 20 - 10),
                    35 + Math.random() * 60,
                    Math.sin(angle) * rad + (Math.random() * 20 - 10)
                );
                ring.rotation.y = Math.random() * Math.PI;
                ring.rotation.x = Math.random() * 0.4;
                scene.add(ring);
                rings.push({ mesh: ring, collected: false });
            }
        }
        spawnSkyRings();

        // Spider-Man avatar representation (Stylized Over-The-Shoulder / Third-Person)
        const heroGroup = new THREE.Group();
        const heroSuitMat = new THREE.MeshStandardMaterial({ color: 0xcc1122, roughness: 0.35, metalness: 0.3 });
        const heroBlueMat = new THREE.MeshStandardMaterial({ color: 0x0033aa, roughness: 0.4, metalness: 0.4 });
        const eyeMat = new THREE.MeshBasicMaterial({ color: 0xffffff });

        // Torso
        const torso = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.6, 0.8), heroSuitMat);
        torso.position.y = 0;
        heroGroup.add(torso);

        // Head
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.55, 16, 16), heroSuitMat);
        head.position.y = 1.25;
        heroGroup.add(head);

        // White Spider Eyes
        const leftEye = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.16, 0.1), eyeMat);
        leftEye.position.set(-0.22, 1.3, 0.52);
        leftEye.rotation.z = 0.2;
        const rightEye = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.16, 0.1), eyeMat);
        rightEye.position.set(0.22, 1.3, 0.52);
        rightEye.rotation.z = -0.2;
        heroGroup.add(leftEye);
        heroGroup.add(rightEye);

        // Limbs for dynamic pose
        const leftArm = new THREE.Mesh(new THREE.BoxGeometry(0.35, 1.3, 0.35), heroBlueMat);
        leftArm.position.set(-0.9, 0.1, 0);
        heroGroup.add(leftArm);

        const rightArm = new THREE.Mesh(new THREE.BoxGeometry(0.35, 1.3, 0.35), heroSuitMat);
        rightArm.position.set(0.9, 0.1, 0);
        heroGroup.add(rightArm);

        const legs = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.6, 0.5), heroBlueMat);
        legs.position.y = -1.4;
        heroGroup.add(legs);

        heroGroup.castShadow = true;
        scene.add(heroGroup);

        // Web Line Visual
        const webLineMat = new THREE.LineBasicMaterial({
            color: 0xffffff,
            linewidth: 3,
            transparent: true,
            opacity: 0.95
        });
        const webLineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
        const webLineMesh = new THREE.Line(webLineGeo, webLineMat);
        webLineMesh.visible = false;
        scene.add(webLineMesh);

        // Web Impact Particles
        const impactParticleGeo = new THREE.BufferGeometry();
        const pCount = 30;
        const pPositions = new Float32Array(pCount * 3);
        const pVelocities = [];
        for (let i = 0; i < pCount; i++) {
            pPositions[i * 3] = 0;
            pPositions[i * 3 + 1] = 0;
            pPositions[i * 3 + 2] = 0;
            pVelocities.push(new THREE.Vector3(
                (Math.random() - 0.5) * 12,
                (Math.random() - 0.5) * 12,
                (Math.random() - 0.5) * 12
            ));
        }
        impactParticleGeo.setAttribute('position', new THREE.BufferAttribute(pPositions, 3));
        const impactMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.6, transparent: true, opacity: 0 });
        const impactParticles = new THREE.Points(impactParticleGeo, impactMat);
        scene.add(impactParticles);
        let impactLife = 0;

        const player = {
            pos: new THREE.Vector3(0, 35, 80),
            vel: new THREE.Vector3(0, 0, 0),
            yaw: 0,
            pitch: 0,
            isGrounded: false,
            webActive: false,
            webTarget: new THREE.Vector3(),
            webDistance: 0,
            webPullSpeed: 82, // High speed exhilarating web-zip
            fluid: 100
        };

        const keys = { w: false, a: false, s: false, d: false, space: false };
        let score = 0;
        let collectedRingsCount = 0;
        let comboCounter = 1;
        let lastZipTime = 0;

        // Aim Raycasting
        const raycaster = new THREE.Raycaster();
        const centerScreen = new THREE.Vector2(0, 0); // Always aim towards center crosshair
        const MAX_WEB_RANGE = 185;
        let aimHitPoint = null;
        let canHook = false;

        // UI references
        const reticleEl = document.getElementById('reticle');
        const distBadgeEl = document.getElementById('distance-badge');
        const speedDisplayEl = document.getElementById('speed-display');
        const speedMeterEl = document.getElementById('speed-meter');
        const speedVignetteEl = document.getElementById('speed-vignette');
        const fluidBarEl = document.getElementById('fluid-bar');
        const fluidPercentEl = document.getElementById('fluid-percent');
        const scoreTextEl = document.getElementById('score-text');
        const ringCountEl = document.getElementById('ring-count');
        const comboBadgeEl = document.getElementById('combo-badge');
        const comboTextEl = document.getElementById('combo-text');
        const actionHintEl = document.getElementById('action-hint-text');

        let isPointerLocked = false;
        let isDragging = false;
        let previousMouseX = 0;
        let previousMouseY = 0;

        // Pointer Lock / Mouse rotation
        function setupControls() {
            window.addEventListener('keydown', (e) => {
                const k = e.key.toLowerCase();
                if (k === 'w' || e.key === 'ArrowUp') keys.w = true;
                if (k === 'a' || e.key === 'ArrowLeft') keys.a = true;
                if (k === 's' || e.key === 'ArrowDown') keys.s = true;
                if (k === 'd' || e.key === 'ArrowRight') keys.d = true;
                if (e.code === 'Space') {
                    keys.space = true;
                    releaseWeb(true); // Jump release boost
                }
                if (k === 'r') resetPlayer();
                if (k === 'h') toggleHelpModal();
            });

            window.addEventListener('keyup', (e) => {
                const k = e.key.toLowerCase();
                if (k === 'w' || e.key === 'ArrowUp') keys.w = false;
                if (k === 'a' || e.key === 'ArrowLeft') keys.a = false;
                if (k === 's' || e.key === 'ArrowDown') keys.s = false;
                if (k === 'd' || e.key === 'ArrowRight') keys.d = false;
                if (e.code === 'Space') keys.space = false;
            });

            // Mouse Look Drag & Shoot
            window.addEventListener('mousedown', (e) => {
                // If clicked on HUD interactive buttons, don't trigger game action
                if (e.target.closest('button') || e.target.closest('#help-modal')) return;
                initAudio();

                if (e.button === 0) { // Left Click: Fire Web Zip
                    shootWeb();
                } else if (e.button === 2) { // Right Click: Boost Release
                    releaseWeb(true);
                }
                isDragging = true;
                previousMouseX = e.clientX;
                previousMouseY = e.clientY;
            });

            window.addEventListener('mouseup', () => {
                isDragging = false;
            });

            window.addEventListener('contextmenu', (e) => e.preventDefault());

            window.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    player.yaw -= e.movementX * 0.0024;
                    player.pitch -= e.movementY * 0.0022;
                } else if (isDragging) {
                    const deltaX = e.clientX - previousMouseX;
                    const deltaY = e.clientY - previousMouseY;
                    player.yaw -= deltaX * 0.003;
                    player.pitch -= deltaY * 0.003;
                    previousMouseX = e.clientX;
                    previousMouseY = e.clientY;
                }
                // Clamp pitch so camera doesn't flip
                player.pitch = Math.max(-Math.PI / 2.3, Math.min(Math.PI / 2.3, player.pitch));
            });

            // Touch Screen Support
            let touchStartX = 0;
            let touchStartY = 0;
            let hasTouchMoved = false;

            window.addEventListener('touchstart', (e) => {
                if (e.target.closest('button') || e.target.closest('#help-modal')) return;
                initAudio();
                const touch = e.touches[0];
                touchStartX = touch.clientX;
                touchStartY = touch.clientY;
                hasTouchMoved = false;
            }, { passive: false });

            window.addEventListener('touchmove', (e) => {
                const touch = e.touches[0];
                const deltaX = touch.clientX - touchStartX;
                const deltaY = touch.clientY - touchStartY;
                if (Math.hypot(deltaX, deltaY) > 8) hasTouchMoved = true;

                player.yaw -= deltaX * 0.004;
                player.pitch -= deltaY * 0.0035;
                player.pitch = Math.max(-Math.PI / 2.3, Math.min(Math.PI / 2.3, player.pitch));

                touchStartX = touch.clientX;
                touchStartY = touch.clientY;
            }, { passive: false });

            window.addEventListener('touchend', () => {
                if (!hasTouchMoved) {
                    // Tap = Shoot web
                    shootWeb();
                }
            });
        }
        setupControls();

        function shootWeb() {
            if (player.fluid < 10) {
                actionHintEl.textContent = "거미줄 용액(Web Fluid) 충전 대기 중!";
                return;
            }

            if (canHook && aimHitPoint) {
                player.webActive = true;
                player.webTarget.copy(aimHitPoint);
                player.fluid = Math.max(0, player.fluid - 15);
                playWebSound();

                // Trigger Web Particle Burst
                spawnImpactSparks(aimHitPoint);

                // Right Arm shooting animation pose
                rightArm.rotation.x = -Math.PI / 2;
                rightArm.position.z = 0.6;

                // Combo calculation
                const now = performance.now();
                if (now - lastZipTime < 2400) {
                    comboCounter = Math.min(8, comboCounter + 1);
                    showComboUI();
                } else {
                    comboCounter = 1;
                }
                lastZipTime = now;

                actionHintEl.textContent = "웹집(Web-Zip) 고속 가속 중! Space로 분리 점프!";
            } else {
                actionHintEl.textContent = "조준 거리가 너무 멀거나 건물이 아닙니다!";
            }
        }

        function releaseWeb(applyJumpBoost = false) {
            if (!player.webActive) return;
            player.webActive = false;
            webLineMesh.visible = false;

            // Reset arm pose
            rightArm.rotation.x = 0;
            rightArm.position.z = 0;

            if (applyJumpBoost) {
                // Catapult jump forward & upward with velocity boost
                const forward = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), player.yaw);
                player.vel.add(forward.multiplyScalar(22));
                player.vel.y += 18;
                score += 30 * comboCounter;
                updateScoreUI();
                actionHintEl.textContent = "웹 부스트 점프 발동!";
            }
        }

        function spawnImpactSparks(pos) {
            impactParticles.position.copy(pos);
            const posAttr = impactParticleGeo.attributes.position;
            for (let i = 0; i < pCount; i++) {
                posAttr.setXYZ(i, 0, 0, 0);
            }
            posAttr.needsUpdate = true;
            impactMat.opacity = 1.0;
            impactLife = 1.0;
        }

        function resetPlayer() {
            player.pos.set(0, 45, 80);
            player.vel.set(0, 0, 0);
            player.yaw = 0;
            player.pitch = 0;
            player.webActive = false;
            webLineMesh.visible = false;
            actionHintEl.textContent = "스파이더맨 위치가 중심가 상공으로 리셋되었습니다.";
        }

        function showComboUI() {
            comboTextEl.textContent = `PERFECT ZIP x${comboCounter}`;
            comboBadgeEl.style.opacity = '1';
            setTimeout(() => {
                comboBadgeEl.style.opacity = '0';
            }, 1800);
        }

        function updateScoreUI() {
            scoreTextEl.textContent = score.toLocaleString();
            ringCountEl.textContent = `${collectedRingsCount} / ${rings.length}`;
        }

        function updateAim() {
            // Camera forwards vector
            raycaster.setFromCamera(centerScreen, camera);
            const intersects = raycaster.intersectObjects(buildingMeshes, false);

            if (intersects.length > 0 && intersects[0].distance <= MAX_WEB_RANGE) {
                aimHitPoint = intersects[0].point;
                canHook = true;
                const distMeters = Math.round(intersects[0].distance);
                distBadgeEl.textContent = `${distMeters} m`;
                distBadgeEl.classList.replace('text-rose-400', 'text-emerald-300');

                if (player.webActive) {
                    reticleEl.className = 'reticle hooked';
                } else {
                    reticleEl.className = 'reticle can-hook';
                }
            } else {
                aimHitPoint = null;
                canHook = false;
                distBadgeEl.textContent = "사정거리 밖";
                distBadgeEl.classList.replace('text-emerald-300', 'text-rose-400');
                reticleEl.className = 'reticle cannot-hook';
            }
        }

        const clock = new THREE.Clock();
        const GRAVITY = -36;

        function animate() {
            requestAnimationFrame(animate);
            const dt = Math.min(clock.getDelta(), 0.1);

            // 1. Aim Raycast
            updateAim();

            // 2. Web Fluid Regeneration
            if (!player.webActive && player.fluid < 100) {
                player.fluid = Math.min(100, player.fluid + dt * 22);
            }
            fluidBarEl.style.width = `${Math.round(player.fluid)}%`;
            fluidPercentEl.textContent = `${Math.round(player.fluid)}%`;

            // 3. Spider Kinematics / Web-Zip
            if (player.webActive) {
                // Calculate pull vector to anchor
                const pullDir = new THREE.Vector3().subVectors(player.webTarget, player.pos);
                const dist = pullDir.length();

                if (dist < 4.0) {
                    // Reached anchor surface: auto-release with wall bounce
                    releaseWeb(true);
                } else {
                    pullDir.normalize();
                    // Accelerate rapidly towards target (Web Zip thrill)
                    const zipForce = pullDir.multiplyScalar(player.webPullSpeed * dt * 2.5);
                    player.vel.add(zipForce);

                    // Add slight upward lift during pull
                    player.vel.y += 12 * dt;

                    // Web Line Render
                    const handPos = heroGroup.position.clone().add(new THREE.Vector3(0.5, 0.5, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), player.yaw));
                    const points = [handPos, player.webTarget];
                    webLineGeo.setFromPoints(points);
                    webLineMesh.visible = true;
                }
            } else {
                webLineMesh.visible = false;
                // Standard Air / Gravity Physics
                player.vel.y += GRAVITY * dt;

                // Air WASD Steering
                const forward = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), player.yaw);
                const right = new THREE.Vector3(1, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), player.yaw);
                const moveForce = new THREE.Vector3();

                if (keys.w) moveForce.add(forward);
                if (keys.s) moveForce.sub(forward);
                if (keys.d) moveForce.add(right);
                if (keys.a) moveForce.sub(right);

                if (moveForce.lengthSq() > 0) {
                    moveForce.normalize().multiplyScalar(40 * dt);
                    player.vel.add(moveForce);
                }

                // Air Drag Friction
                player.vel.x *= Math.pow(0.96, dt * 60);
                player.vel.z *= Math.pow(0.96, dt * 60);
                player.vel.y *= Math.pow(0.99, dt * 60);
            }

            // Apply Velocity to Position
            player.pos.addScaledVector(player.vel, dt);

            // Ground Floor Collision
            if (player.pos.y < 2.5) {
                player.pos.y = 2.5;
                player.vel.y = Math.max(0, player.vel.y);
                player.vel.x *= 0.85;
                player.vel.z *= 0.85;
                if (player.webActive) releaseWeb(false);
            }

            // High Building Collision check (prevent clipping inside buildings)
            for (let b of buildings) {
                if (player.pos.x > b.minX - 1.5 && player.pos.x < b.maxX + 1.5 &&
                    player.pos.z > b.minZ - 1.5 && player.pos.z < b.maxZ + 1.5) {
                    if (player.pos.y < b.topY) {
                        // Push player away from nearest face
                        const dx1 = Math.abs(player.pos.x - b.minX);
                        const dx2 = Math.abs(player.pos.x - b.maxX);
                        const dz1 = Math.abs(player.pos.z - b.minZ);
                        const dz2 = Math.abs(player.pos.z - b.maxZ);
                        const minPen = Math.min(dx1, dx2, dz1, dz2);

                        if (minPen === dx1) player.pos.x = b.minX - 1.5;
                        else if (minPen === dx2) player.pos.x = b.maxX + 1.5;
                        else if (minPen === dz1) player.pos.z = b.minZ - 1.5;
                        else player.pos.z = b.maxZ + 1.5;

                        // Wall hit damping
                        player.vel.x *= -0.2;
                        player.vel.z *= -0.2;
                        if (player.webActive) releaseWeb(false);
                    } else if (player.pos.y < b.topY + 2.0 && player.vel.y < 0) {
                        // Landing on rooftop
                        player.pos.y = b.topY + 2.0;
                        player.vel.y = 0;
                    }
                }
            }

            // 4. Collect Sky Checkpoint Rings
            for (let r of rings) {
                if (!r.collected) {
                    r.mesh.rotation.y += dt * 1.5;
                    const d = player.pos.distanceTo(r.mesh.position);
                    if (d < 5.5) {
                        r.collected = true;
                        collectedRingsCount++;
                        score += 200 * comboCounter;
                        updateScoreUI();
                        playRingSound();

                        // Ring collect pop effect
                        r.mesh.scale.set(1.8, 1.8, 1.8);
                        r.mesh.material.emissive.setHex(0x00ffff);
                        setTimeout(() => {
                            r.mesh.visible = false;
                        }, 250);
                    }
                }
            }

            // 5. Update Impact Particles
            if (impactLife > 0) {
                impactLife -= dt * 2.5;
                impactMat.opacity = Math.max(0, impactLife);
                const posAttr = impactParticleGeo.attributes.position;
                for (let i = 0; i < pCount; i++) {
                    const vx = pVelocities[i].x * dt;
                    const vy = pVelocities[i].y * dt;
                    const vz = pVelocities[i].z * dt;
                    posAttr.setXYZ(i, posAttr.getX(i) + vx, posAttr.getY(i) + vy, posAttr.getZ(i) + vz);
                }
                posAttr.needsUpdate = true;
            }

            // 6. Avatar Update & Dynamic In-Flight Tilt
            heroGroup.position.copy(player.pos);
            heroGroup.rotation.y = player.yaw;

            // Bank angle while turning or zipping
            const horizontalSpeed = Math.hypot(player.vel.x, player.vel.z);
            const totalSpeedKmh = Math.round(player.vel.length() * 3.6);
            speedDisplayEl.textContent = totalSpeedKmh;
            speedMeterEl.style.width = `${Math.min(100, (totalSpeedKmh / 160) * 100)}%`;

            // Speed Lines & Dynamic FOV Warping
            if (totalSpeedKmh > 65) {
                speedVignetteEl.style.opacity = Math.min(0.85, (totalSpeedKmh - 65) / 80).toString();
                camera.fov = THREE.MathUtils.lerp(camera.fov, 82, dt * 6);
            } else {
                speedVignetteEl.style.opacity = '0';
                camera.fov = THREE.MathUtils.lerp(camera.fov, 70, dt * 6);
            }
            camera.updateProjectionMatrix();

            // Avatar acrobatics pose during speed flight
            if (player.webActive || totalSpeedKmh > 40) {
                torso.rotation.x = THREE.MathUtils.lerp(torso.rotation.x, 0.7, dt * 10);
                legs.rotation.x = THREE.MathUtils.lerp(legs.rotation.x, -0.6, dt * 10);
            } else {
                torso.rotation.x = THREE.MathUtils.lerp(torso.rotation.x, 0, dt * 8);
                legs.rotation.x = THREE.MathUtils.lerp(legs.rotation.x, 0, dt * 8);
            }

            // 7. Smooth Over-The-Shoulder Camera Positioning
            const camOffset = new THREE.Vector3(0.9, 1.8, 4.4); // slightly over right shoulder
            camOffset.applyAxisAngle(new THREE.Vector3(1, 0, 0), player.pitch);
            camOffset.applyAxisAngle(new THREE.Vector3(0, 1, 0), player.yaw);

            const targetCamPos = player.pos.clone().add(camOffset);
            camera.position.lerp(targetCamPos, 0.4);

            const lookTarget = player.pos.clone().add(
                new THREE.Vector3(0, 0.8, -18)
                    .applyAxisAngle(new THREE.Vector3(1, 0, 0), player.pitch)
                    .applyAxisAngle(new THREE.Vector3(0, 1, 0), player.yaw)
            );
            camera.lookAt(lookTarget);

            // Render 3D Frame
            renderer.render(scene, camera);
        }

        function toggleHelpModal() {
            const modal = document.getElementById('help-modal');
            modal.classList.toggle('hidden');
        }

        document.getElementById('btn-help').addEventListener('click', toggleHelpModal);
        document.getElementById('btn-close-help').addEventListener('click', toggleHelpModal);
        document.getElementById('btn-start-game').addEventListener('click', () => {
            initAudio();
            toggleHelpModal();
        });
        document.getElementById('btn-reset').addEventListener('click', resetPlayer);

        let soundEnabled = true;
        document.getElementById('btn-sound').addEventListener('click', () => {
            initAudio();
            soundEnabled = !soundEnabled;
            Tone.Destination.mute = !soundEnabled;
            document.getElementById('btn-sound').classList.toggle('opacity-50', !soundEnabled);
        });

        // Window Responsive Resize
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // Start game loop when window loads
        window.onload = function () {
            animate();
        };
    </script>
</body>
</html>
