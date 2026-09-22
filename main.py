import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. Streamlit 페이지 레이아웃 및 스타일 설정
# ==============================================================================
st.set_page_config(
    page_title="스파이더맨 웹슈터 공학 랩 & 물리 스윙 게임",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 다크 테마 커스텀 CSS 스타일링
st.markdown("""
<style>
    .main { background-color: #0b0f19; }
    h1, h2, h3 { color: #f8fafc; font-family: 'Pretendard', sans-serif; }
    .stMetric { background-color: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

st.title("🕸️ 피터 파커의 고분자 웹슈터 공학 연구소 & 스윙 시뮬레이터")
st.caption("바이오 복합 탄성 고분자 역학과 진자 운동 역동성을 결합한 실시간 물리 액션 웹앱")

# ==============================================================================
# 2. 사이드바: 고분자 합성 공학 파라미터 (생체재료역학 계산)
# ==============================================================================
with st.sidebar:
    st.header("🧪 웹 플루이드 고분자 배합 (Lab)")
    st.markdown("거미 실크 단백질(스피드로인)의 유체역학 및 기계적 물성을 튜닝합니다.")
    
    # 1) 가교 밀도 (Crosslink Density, rho_xl) - 분자 간 결합 강도 결정
    crosslink = st.slider(
        "가교 밀도 (Crosslink Density, %)",
        min_value=10, max_value=100, value=75, step=5,
        help="단백질 사슬 간 결합 강도. 높을수록 파단 강도와 영률이 증가하지만 취성(깨짐)이 생깁니다."
    )
    
    # 2) 사출 노즐 구경 (Nozzle Gauge, d) - 거미줄 단면적 결정
    nozzle_diam = st.slider(
        "방사 노즐 구경 (Nozzle Diameter, mm)",
        min_value=0.5, max_value=3.0, value=1.2, step=0.1,
        help="거미줄의 굵기를 결정합니다. 단면적이 클수록 더 큰 장력을 버팁니다."
    )
    
    # 3) 파일럿 체중 (스파이더맨 질량, m)
    mass = st.number_input(
        "스윙 체중 (Pilot Mass, kg)",
        min_value=40, max_value=100, value=65, step=1
    )

    # --------------------------------------------------------------------------
    # 재료역학 수식 계산 (Structural Mechanics Calculation)
    # --------------------------------------------------------------------------
    # 단면적 A = pi * (d/2)^2 (단위: mm^2)
    radius_mm = nozzle_diam / 2.0
    area_mm2 = 3.141592 * (radius_mm ** 2)
    
    # 인장 강도(Tensile Strength, MPa): 방사 단백질 기본 강도에 가교 밀도 반영 (실제 거미줄 ~1000~1500 MPa)
    tensile_strength_mpa = 400.0 + (crosslink * 12.0)
    
    # 최대 파단 하중 F_break = Tensile Strength * Area (N)
    f_break_n = tensile_strength_mpa * area_mm2
    
    # 영률(Young's Modulus, GPa): 거미줄의 뻣뻣함 정도 (실제 ~10~20 GPa)
    youngs_modulus_gpa = 3.0 + (crosslink * 0.18)

    st.divider()
    st.subheader("📊 재료 분석 지표")
    st.metric("최대 허용 장력 (F_break)", f"{f_break_n:,.0f} N")
    st.metric("영률 (Young's Modulus)", f"{youngs_modulus_gpa:.1f} GPa")
    
    # 안전율 가이드 (정적 상태 1G 대비)
    static_load = mass * 9.81
    safety_margin = f_break_n / static_load
    st.metric("정적 안전율 (Safety Factor)", f"{safety_margin:.1f}x")

# 메인 상단: 공학 원리 안내
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**1. 원터치 스윙 (Swing Key)**")
    st.info("화면을 **마우스로 꾹 누르거나 [스페이스바]**를 누르면 가장 가까운 빌딩 루프탑에 거미줄을 걸어 진자 운동을 시작합니다.")
with col2:
    st.markdown("**2. 거미줄 파단 임계점 (Tensile Limit)**")
    st.warning(f"스윙 최저점 장력 $T = m(g\\cos\\theta + v^2/r)$이 **{f_break_n:,.0f} N**을 초과하면 거미줄이 폭음과 함께 끊어집니다!")
with col3:
    st.markdown("**3. 파일럿 블랙아웃 (Bio-G-Force)**")
    st.error("스윙 회전 원심가속도가 **7.5 G**를 초과하면 뇌 혈류 공급 저하로 시야가 차단(Blackout)되며 추락합니다.")

# ==============================================================================
# 3. HTML5 Canvas 기반 실시간 물리 엔진 (JavaScript Component)
# ==============================================================================
# Streamlit 파이썬 변수(f_break_n, mass 등)를 JavaScript 엔진으로 직접 주입
canvas_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        margin: 0;
        padding: 0;
        background: #020617;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        user-select: none;
        overflow: hidden;
    }}
    #game-container {{
        position: relative;
        width: 100%;
        max-width: 960px;
        margin: 0 auto;
    }}
    canvas {{
        display: block;
        background: linear-gradient(to bottom, #090d16 0%, #1e1b4b 70%, #311042 100%);
        border: 2px solid #334155;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    #hud {{
        position: absolute;
        top: 15px;
        left: 20px;
        pointer-events: none;
        display: flex;
        gap: 16px;
        font-size: 14px;
        font-weight: 600;
        text-shadow: 1px 1px 3px black;
    }}
    .hud-box {{
        background: rgba(15, 23, 42, 0.85);
        padding: 8px 14px;
        border-radius: 6px;
        border: 1px solid #475569;
    }}
    #blackout-overlay {{
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        background: radial-gradient(circle, transparent 40%, rgba(0,0,0,0.95) 90%);
        opacity: 0;
        transition: opacity 0.1s ease-out;
        border-radius: 12px;
    }}
    #game-over {{
        display: none;
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(15, 23, 42, 0.95);
        padding: 24px 36px;
        border-radius: 12px;
        border: 2px solid #ef4444;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(239, 68, 68, 0.3);
    }}
    button.retry-btn {{
        margin-top: 16px;
        background: #ef4444;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 15px;
        font-weight: 700;
        border-radius: 6px;
        cursor: pointer;
    }}
    button.retry-btn:hover {{
        background: #dc2626;
    }}
</style>
</head>
<body>

<div id="game-container">
    <canvas id="canvas" width="960" height="540"></canvas>
    
    <!-- 실시간 HUD 정보 계측창 -->
    <div id="hud">
        <div class="hud-box">거리: <span id="hud-dist" style="color:#38bdf8;">0 m</span></div>
        <div class="hud-box">속도: <span id="hud-speed" style="color:#4ade80;">0 km/h</span></div>
        <div class="hud-box">장력(Tension): <span id="hud-tension" style="color:#fbbf24;">0 N</span> / {f_break_n:,.0f} N</div>
        <div class="hud-box">G-Force: <span id="hud-gforce" style="color:#f87171;">1.0 G</span></div>
    </div>
    
    <!-- 급선회 원심력 초과 시 시야 차단 효과 (Blackout Vignette) -->
    <div id="blackout-overlay"></div>

    <!-- 게임오버 팝업 -->
    <div id="game-over">
        <h2 id="death-reason" style="color: #ef4444; margin:0 0 10px 0;">거미줄 파단!</h2>
        <p id="death-desc" style="color: #cbd5e1; font-size:14px; margin:0;">장력이 허용 한도를 초과하여 끊어졌습니다.</p>
        <p style="margin: 12px 0 0 0; font-size: 16px; font-weight: bold;">기록: <span id="final-dist">0</span> m</p>
        <button class="retry-btn" onclick="resetGame()">다시 도전</button>
    </div>
</div>

<script>
// =============================================================================
// 파이썬으로부터 주입받은 공학 물리 상수
// =============================================================================
const F_BREAK = {f_break_n};         // 거미줄 최대 파단 한도 (N)
const MASS = {mass};                 // 플레이어 질량 (kg)
const G = 9.81;                      // 중력가속도 (m/s^2)
const PIXELS_PER_METER = 20;         // 화면 스케일 (20px = 1m)
const MAX_SAFE_G = 7.5;              // 인체 블랙아웃 임계 G-Force

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const hudDist = document.getElementById("hud-dist");
const hudSpeed = document.getElementById("hud-speed");
const hudTension = document.getElementById("hud-tension");
const hudGforce = document.getElementById("hud-gforce");
const blackoutOverlay = document.getElementById("blackout-overlay");
const gameOverPanel = document.getElementById("game-over");
const deathReason = document.getElementById("death-reason");
const deathDesc = document.getElementById("death-desc");
const finalDist = document.getElementById("final-dist");

// =============================================================================
// 게임 상태 변수
// =============================================================================
let isAttached = false;     // 거미줄 부착 상태 여부
let anchor = {{ x: 0, y: 0 }}; // 고정된 건물 옥상 앵커 좌표
let ropeLength = 0;         // 거미줄 고유 길이
let isAlive = true;
let score = 0;
let cameraX = 0;

// 스파이더맨 물리 객체 상태
const player = {{
    x: 100,
    y: 300,
    vx: 12,                  // 초기 전진 수평속도 (m/s)
    vy: 0,                   // 초기 수직속도 (m/s)
    radius: 12
}};

// 건물 숲 절차적 생성 (Procedural City Generation)
let buildings = [];
let nextBuildingX = 0;

function initBuildings() {{
    buildings = [];
    nextBuildingX = 0;
    while (nextBuildingX < canvas.width * 2.5) {{
        spawnBuilding();
    }}
}}

function spawnBuilding() {{
    const width = 80 + Math.random() * 90;
    const height = 180 + Math.random() * 220; // 옥상 높이 다양화
    const gap = 40 + Math.random() * 60;
    buildings.push({{
        x: nextBuildingX,
        y: canvas.height - height,
        w: width,
        h: height,
        color: '#1e293b',
        windowColor: Math.random() > 0.4 ? '#fbbf24' : '#0f172a'
    }});
    nextBuildingX += width + gap;
}}

// =============================================================================
// 입력 제어 (스페이스바 및 마우스 클릭 이벤트)
// =============================================================================
let inputDown = false;

function onActionStart() {{
    if (!isAlive) return;
    inputDown = true;
    tryAttachWeb();
}}

function onActionEnd() {{
    inputDown = false;
    isAttached = false; // 줄을 놓으면 즉시 관성 탄도 비행(포물선)
}}

window.addEventListener("keydown", (e) => {{
    if (e.code === "Space" && !e.repeat) {{
        onActionStart();
        e.preventDefault();
    }}
}});
window.addEventListener("keyup", (e) => {{
    if (e.code === "Space") {{
        onActionEnd();
        e.preventDefault();
    }}
}});
canvas.addEventListener("mousedown", onActionStart);
window.addEventListener("mouseup", onActionEnd);

// 가장 가깝고 앞선 건물 옥상 모서리를 탐색해 거미줄 사출
function tryAttachWeb() {{
    if (isAttached) return;
    
    let bestAnchor = null;
    let minDistance = 9999;
    
    // 현재 플레이어 기준 전방 위쪽에 위치한 건물 모서리 탐색
    for (const b of buildings) {{
        const rooftopX = b.x + b.w * 0.5;
        const rooftopY = b.y;
        
        // 전방 20m ~ 40m 상공 범위 건물 모서리 필터링
        const dx = (rooftopX - player.x) / PIXELS_PER_METER;
        const dy = (rooftopY - player.y) / PIXELS_PER_METER;
        const dist = Math.sqrt(dx*dx + dy*dy);
        
        // 플레이어보다 앞서 있고(dx > 2m) 너무 멀지 않은 위치 선택
        if (dx > 2 && dist < 45 && dist < minDistance) {{
            minDistance = dist;
            bestAnchor = {{ x: rooftopX, y: rooftopY }};
        }}
    }}
    
    if (bestAnchor) {{
        anchor = bestAnchor;
        const dx = (player.x - anchor.x) / PIXELS_PER_METER;
        const dy = (player.y - anchor.y) / PIXELS_PER_METER;
        ropeLength = Math.sqrt(dx*dx + dy*dy);
        isAttached = true;
    }}
}}

// =============================================================================
// 핵심 물리 시뮬레이션 루프 (Runge-Kutta/Verlet 근사 적분)
// =============================================================================
function updatePhysics(dt) {{
    if (!isAlive) return;

    let tensionN = 0;
    let gForce = 1.0;

    // 1) 기본 중력 가속도 적용 (dv = g * dt)
    player.vy += G * dt;

    // 2) 거미줄에 연결된 경우: 진자 운동(Pendulum Dynamics) 제약 조건 계산
    if (isAttached) {{
        const dx = (player.x - anchor.x) / PIXELS_PER_METER;
        const dy = (player.y - anchor.y) / PIXELS_PER_METER;
        const currentDist = Math.sqrt(dx*dx + dy*dy);
        
        // 줄이 팽팽하게 펴진 순간
        if (currentDist >= ropeLength) {{
            // 줄 방향 단위 벡터 계산
            const nx = dx / currentDist;
            const ny = dy / currentDist;
            
            // 줄 방향 속도 성분 투영 (Radial Velocity: v_r = v · n)
            const vr = player.vx * nx + player.vy * ny;
            
            // 줄이 늘어나지 않도록 구심 방향으로 속도 보정
            if (vr > 0) {{
                player.vx -= vr * nx;
                player.vy -= vr * ny;
            }}
            
            // 위치 제약조건 복원
            player.x = anchor.x + nx * ropeLength * PIXELS_PER_METER;
            player.y = anchor.y + ny * ropeLength * PIXELS_PER_METER;
            
            // -------------------------------------------------------------
            // 장력 계산: T = m * (g * cos(theta) + v^2 / r)
            // -------------------------------------------------------------
            const speedSq = player.vx * player.vx + player.vy * player.vy;
            const cosTheta = -ny; // 아래 방향(수직)과의 각도 코사인 값
            const centripetalAcc = speedSq / ropeLength; // 구심가속도 (v^2 / r)
            
            // 총 장력 (N)
            tensionN = MASS * Math.max(0, (G * cosTheta + centripetalAcc));
            
            // 탑승자가 받는 체감 원심 G-Force
            gForce = (centripetalAcc + G * cosTheta) / G;

            // [패배 판정 1] 재료 인장 한계 초과 파단 검증
            if (tensionN > F_BREAK) {{
                triggerGameOver(
                    "🕸️ 거미줄 파단 (Material Fracture)", 
                    `스윙 최저점 순간 장력(${{Math.round(tensionN).toLocaleString()}} N)이 고분자 최대 파단 한도(${{F_BREAK.toLocaleString()}} N)를 초과하여 줄이 끊어졌습니다!`
                );
                return;
            }}
            
            // [패배 판정 2] 원심가속도 한계 초과 블랙아웃 검증
            if (gForce > MAX_SAFE_G) {{
                triggerGameOver(
                    "⚡ 파일럿 블랙아웃 (Blackout Fatal Crash)", 
                    `원심가속도가 ${{gForce.toFixed(1)}} G에 도달하여 뇌 혈류 공급 저하로 시야를 상실하고 추락했습니다!`
                );
                return;
            }}
        }}
    }}

    // 3) 공기 저항 (Drag, v' = -kv)
    player.vx *= 0.999;
    player.vy *= 0.999;

    // 4) 위치 적분
    player.x += player.vx * dt * PIXELS_PER_METER;
    player.y += player.vy * dt * PIXELS_PER_METER;

    // 5) 지면 충돌 및 건물 충돌 판정
    if (player.y >= canvas.height - 20) {{
        triggerGameOver("💥 지면 격돌 (Ground Impact)", "낙하 속도를 제어하지 못해 지면에 정면 충돌했습니다.");
        return;
    }}
    for (const b of buildings) {{
        if (player.x > b.x && player.x < b.x + b.w && player.y > b.y) {{
            triggerGameOver("🏢 빌딩 충돌 (Building Impact)", "고층 건물 외벽에 정면으로 부딪혔습니다.");
            return;
        }}
    }}

    // 무한 맵 건물 생성 및 불필요한 건물 컬링
    if (player.x + canvas.width > nextBuildingX) {{
        spawnBuilding();
    }}
    buildings = buildings.filter(b => b.x + b.w > player.x - 300);

    // 카메라 추적
    cameraX = player.x - 200;

    // HUD 업데이트
    score = Math.max(0, Math.floor((player.x - 100) / PIXELS_PER_METER));
    const speedKmh = Math.round(Math.sqrt(player.vx*player.vx + player.vy*player.vy) * 3.6);
    hudDist.innerText = score + " m";
    hudSpeed.innerText = speedKmh + " km/h";
    hudTension.innerText = Math.round(tensionN).toLocaleString() + " N";
    hudGforce.innerText = Math.max(1.0, gForce).toFixed(1) + " G";

    // G-Force에 따른 동적 비넷(블랙아웃 전조) 렌더링
    const vignetteOpacity = Math.min(1.0, Math.max(0, (gForce - 4.5) / (MAX_SAFE_G - 4.5)));
    blackoutOverlay.style.opacity = vignetteOpacity;
}}

function triggerGameOver(reason, desc) {{
    isAlive = false;
    isAttached = false;
    deathReason.innerText = reason;
    deathDesc.innerText = desc;
    finalDist.innerText = score;
    gameOverPanel.style.display = "block";
}}

function resetGame() {{
    player.x = 100;
    player.y = 300;
    player.vx = 12;
    player.vy = 0;
    isAlive = true;
    isAttached = false;
    gameOverPanel.style.display = "none";
    blackoutOverlay.style.opacity = 0;
    initBuildings();
}}

// =============================================================================
// 그래픽 렌더링 파이프라인
// =============================================================================
function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(-cameraX, 0);

    // 1) 고층 빌딩 렌더링
    for (const b of buildings) {{
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, b.y, b.w, b.h);
        
        // 빌딩 창문 야경 표현
        ctx.fillStyle = b.windowColor;
        for (let wy = b.y + 15; wy < canvas.height - 20; wy += 30) {{
            for (let wx = b.x + 10; wx < b.x + b.w - 10; wx += 20) {{
                if ((wx + wy) % 7 === 0) {{
                    ctx.fillRect(wx, wy, 8, 14);
                }}
            }}
        }}

        // 옥상 앵커 포인트 하이라이트 (스윙 타겟 시각화)
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2;
        ctx.strokeRect(b.x, b.y, b.w, 4);
    }}

    // 2) 거미줄 (Web-Line) 렌더링
    if (isAttached) {{
        ctx.beginPath();
        ctx.moveTo(anchor.x, anchor.y);
        ctx.lineTo(player.x, player.y);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2.5;
        ctx.shadowColor = "#38bdf8";
        ctx.shadowBlur = 8;
        ctx.stroke();
        ctx.shadowBlur = 0;

        // 앵커 고정 지점 시각화
        ctx.beginPath();
        ctx.arc(anchor.x, anchor.y, 5, 0, Math.PI * 2);
        ctx.fillStyle = "#ef4444";
        ctx.fill();
    }}

    // 3) 스파이더맨 캐릭터 (관성 틸트 각도 반영)
    ctx.save();
    ctx.translate(player.x, player.y);
    const angle = Math.atan2(player.vy, player.vx);
    ctx.rotate(angle);

    // 몸체 (레드 슈트)
    ctx.beginPath();
    ctx.ellipse(0, 0, 14, 8, 0, 0, Math.PI * 2);
    ctx.fillStyle = "#e11d48";
    ctx.fill();

    // 슈트 포인트 (블루)
    ctx.beginPath();
    ctx.ellipse(-4, 0, 6, 7, 0, 0, Math.PI * 2);
    ctx.fillStyle = "#2563eb";
    ctx.fill();

    // 마스크 눈 (화이트)
    ctx.beginPath();
    ctx.ellipse(6, -3, 4, 2, Math.PI / 4, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.restore();
    ctx.restore();
}}

// =============================================================================
// 메인 엔진 루프 (60FPS 고정 델타 타임)
// =============================================================================
let lastTime = performance.now();
function gameLoop(now) {{
    const dt = Math.min((now - lastTime) / 1000, 0.05); // 프레임 스파이크 방지
    lastTime = now;
    
    updatePhysics(dt);
    draw();
    
    requestAnimationFrame(gameLoop);
}}

// 초기화 실행
initBuildings();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

# HTML 컴포넌트를 Streamlit 페이지에 안전하게 삽입 (고정 높이 560px)
components.html(canvas_html, height=580, scrolling=False)

# ==============================================================================
# 4. 학생부 세특 / 학술 보고서 연계 수식 및 해설 정리
# ==============================================================================
with st.expander("📚 [생기부/세특 연계 가이드] 이 프로젝트에 내재된 수학·물리·재료역학 원리"):
    st.markdown(r"""
    ### 1. 고분자 재료역학 및 파단 메커니즘
    * **인장 응력(Tensile Stress)과 최대 파단 하중**:
      $$\sigma = \frac{F}{A} \quad \Longrightarrow \quad F_{\text{break}} = \sigma_{\text{uts}} \cdot \left(\pi \frac{d^2}{4}\right)$$
      스피드로인(거미 실크 단백질)은 $\beta$-시트 결정 영역의 가교 밀도($\rho_{xl}$)에 따라 극한 인장 강도($\sigma_{\text{uts}}$)가 결정됩니다. 
      본 시뮬레이터는 사용자가 선정한 노즐 직경($d$)과 가교 파라미터에 기반해 임계 파단 하중 $F_{\text{break}}$을 실시간 제약식으로 갱신합니다.

    ### 2. 가변 진자 운동과 구심 가속도 역학
    * **최하점 순간 장력($T$) 미분방정식**:
      $$T(\theta) = m \left( g\cos\theta + \frac{v^2}{r} \right)$$
      스윙 각도 $\theta$가 $0$에 도달하는 최저점 통과 시, 중력 성분 $mg$와 원심력 $m\frac{v^2}{r}$이 중첩되어 최대 장력이 집중됩니다. 
      이 값이 고분자의 $F_{\text{break}}$를 초과하면 재료의 취성 파괴(Brittle Fracture)가 발생하도록 알고리즘화되었습니다.

    ### 3. 생체 유체역학 및 허용 G-Force 한계
    * **정수압 감소와 뇌 혈류 차단 (Blackout)**:
      원심가속도가 $7.5\text{ G}$를 상회하면 안구 망막과 대뇌로 향하는 동맥혈 수축압이 정수압차($\Delta P = \rho g_{\text{eff}} h$)를 이기지 못해 시야 암전(Blackout)이 초래됩니다.
      게임 뷰의 방사형 비넷(Vignette) 강도를 G-Force에 실시간 결합하여 공학적 한계 조건을 시각적으로 체감하도록 설계했습니다.
    """)
