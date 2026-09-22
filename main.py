import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. Streamlit 페이지 설정
# ==============================================================================
st.set_page_config(
    page_title="스파이더맨 웹슈터 & 벽타기 액션 랩",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0b0f19; }
    h1, h2, h3 { color: #f8fafc; font-family: 'Pretendard', sans-serif; }
    .stMetric { background-color: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

st.title("🕸️ 피터 파커의 고공 스파이더 액션 & 역학 시뮬레이터")
st.caption("건물 벽 흡착 및 반발 도약, 진자 스윙, 고공 추락 충격량 역학 결합")

# ==============================================================================
# 2. 사이드바: 고분자 물성 및 신체 조건
# ==============================================================================
with st.sidebar:
    st.header("🧪 피터 파커 바이오 스펙 (Lab)")
    
    crosslink = st.slider(
        "거미줄 가교 밀도 (Crosslink, %)",
        min_value=30, max_value=100, value=85, step=5,
        help="단백질 사슬 결합도. 높을수록 장력을 잘 버팁니다."
    )
    
    nozzle_diam = st.slider(
        "웹슈터 노즐 구경 (Nozzle, mm)",
        min_value=0.8, max_value=3.0, value=1.5, step=0.1
    )
    
    mass = st.number_input(
        "피터 파커 체중 (kg)",
        min_value=50, max_value=90, value=70, step=1
    )

    # --------------------------------------------------------------------------
    # 재료역학 계산
    # --------------------------------------------------------------------------
    radius_mm = nozzle_diam / 2.0
    area_mm2 = 3.141592 * (radius_mm ** 2)
    tensile_strength_mpa = 600.0 + (crosslink * 15.0)
    f_break_n = tensile_strength_mpa * area_mm2
    youngs_modulus_gpa = 5.0 + (crosslink * 0.2)

    st.divider()
    st.subheader("📊 웹슈터 역학 제원")
    st.metric("최대 인장 하중 (F_break)", f"{f_break_n:,.0f} N")
    st.metric("영률 (Elasticity)", f"{youngs_modulus_gpa:.1f} GPa")

# 조작법 가이드
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("🎯 **1. 스윙 조작**")
    st.info("**[스페이스바]** or **[마우스 꾹]**: 건물 옥상에 거미줄을 걸어 진자 스윙 가속을 합니다.")
with c2:
    st.markdown("🧗 **2. 벽 붙기 & 슈퍼 도약**")
    st.success("건물 옆면에 닿으면 **달라붙습니다**. 이 상태에서 **클릭/스페이스바**를 누르면 반대편 위로 **슈퍼 점프**합니다!")
with c3:
    st.markdown("💀 **3. 지면 추락 즉사**")
    st.error("스윙 타이밍을 놓치거나 벽에서 끝까지 흘러내려 **바닥에 닿는 순간 즉시 사망(Game Over)**합니다.")

# ==============================================================================
# 3. HTML5 Canvas 물리 엔진 (바닥 충돌 즉사 & 벽점프 로직)
# ==============================================================================
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
        background: linear-gradient(to bottom, #050814 0%, #0f172a 60%, #1e1b4b 100%);
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
        gap: 12px;
        font-size: 14px;
        font-weight: 600;
        text-shadow: 1px 1px 3px black;
    }}
    .hud-box {{
        background: rgba(15, 23, 42, 0.85);
        padding: 8px 12px;
        border-radius: 6px;
        border: 1px solid #475569;
    }}
    #state-badge {{
        color: #38bdf8;
        font-weight: 700;
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
        padding: 10px 22px;
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
    
    <div id="hud">
        <div class="hud-box">거리: <span id="hud-dist" style="color:#38bdf8;">0 m</span></div>
        <div class="hud-box">속도: <span id="hud-speed" style="color:#4ade80;">0 km/h</span></div>
        <div class="hud-box">상태: <span id="state-badge">비행 중 (Flying)</span></div>
        <div class="hud-box">장력: <span id="hud-tension" style="color:#fbbf24;">0 N</span></div>
    </div>

    <div id="game-over">
        <h2 id="death-reason" style="color: #ef4444; margin:0 0 10px 0;">게임 오버</h2>
        <p id="death-desc" style="color: #cbd5e1; font-size:14px; margin:0;">추락했습니다.</p>
        <p style="margin: 12px 0 0 0; font-size: 16px; font-weight: bold;">최종 비행 거리: <span id="final-dist">0</span> m</p>
        <button class="retry-btn" onclick="resetGame()">다시 시작하기</button>
    </div>
</div>

<script>
// =============================================================================
// 파이썬 공학 상수 주입
// =============================================================================
const F_BREAK = {f_break_n};         // 파단 장력 (N)
const MASS = {mass};                 // 질량 (kg)
const G = 9.81;
const PIXELS_PER_METER = 20;

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const hudDist = document.getElementById("hud-dist");
const hudSpeed = document.getElementById("hud-speed");
const hudTension = document.getElementById("hud-tension");
const stateBadge = document.getElementById("state-badge");
const gameOverPanel = document.getElementById("game-over");
const deathReason = document.getElementById("death-reason");
const deathDesc = document.getElementById("death-desc");
const finalDist = document.getElementById("final-dist");

// =============================================================================
// 상태 변수
// =============================================================================
let isAlive = true;
let isAttached = false;
let isWallClinging = false; // 벽 부착 여부
let clingSide = 1;          // 1: 왼쪽 벽, -1: 오른쪽 벽
let anchor = {{ x: 0, y: 0 }};
let ropeLength = 0;
let score = 0;
let cameraX = 0;

const player = {{
    x: 100,
    y: 220,
    vx: 14,
    vy: 0,
    radius: 12
}};

// 건물 생성
let buildings = [];
let nextBuildingX = 0;

function initBuildings() {{
    buildings = [];
    nextBuildingX = 0;
    while (nextBuildingX < canvas.width * 3) {{
        spawnBuilding();
    }}
}}

function spawnBuilding() {{
    const width = 110 + Math.random() * 80;
    const height = 230 + Math.random() * 90; // 안전한 비행 고도 확보
    const gap = 35 + Math.random() * 35;
    buildings.push({{
        x: nextBuildingX,
        y: canvas.height - height,
        w: width,
        h: height,
        color: '#1e293b',
        windowColor: Math.random() > 0.4 ? '#fde047' : '#0f172a'
    }});
    nextBuildingX += width + gap;
}}

// =============================================================================
// 조작 로직 (스윙 & 벽점프)
// =============================================================================
function handleActionDown() {{
    if (!isAlive) return;

    // 1) 벽에 붙어있는 경우 -> 벽을 발로 차며 슈퍼 점프!
    if (isWallClinging) {{
        isWallClinging = false;
        player.vx = (clingSide === 1 ? -1 : 1) * -17; // 건물 바깥 전방으로 추진
        player.vy = -18;                              // 높은 수직 도약력
        isAttached = false;
        return;
    }}

    // 2) 공중 상태인 경우 -> 거미줄 사출
    tryAttachWeb();
}}

function handleActionUp() {{
    if (isAttached) {{
        isAttached = false; // 관성 비행으로 전환
    }}
}}

window.addEventListener("keydown", (e) => {{
    if (e.code === "Space" && !e.repeat) {{
        handleActionDown();
        e.preventDefault();
    }}
}});
window.addEventListener("keyup", (e) => {{
    if (e.code === "Space") {{
        handleActionUp();
        e.preventDefault();
    }}
}});
canvas.addEventListener("mousedown", handleActionDown);
window.addEventListener("mouseup", handleActionUp);

// 옥상 모서리 자동 타겟팅 거미줄 사출
function tryAttachWeb() {{
    if (isAttached || isWallClinging) return;
    
    let bestAnchor = null;
    let minDistance = 9999;
    
    for (const b of buildings) {{
        const rooftopX = b.x + b.w * 0.4;
        const rooftopY = b.y;
        
        const dx = (rooftopX - player.x) / PIXELS_PER_METER;
        const dy = (rooftopY - player.y) / PIXELS_PER_METER;
        const dist = Math.sqrt(dx*dx + dy*dy);
        
        if (dx > 3 && dist < 50 && dist < minDistance) {{
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
// 물리 업데이트 (추락 즉사 & 벽타기)
// =============================================================================
function updatePhysics(dt) {{
    if (!isAlive) return;

    let tensionN = 0;

    // [사망 조건 1] 지면(바닥) 추락 시 즉각 사망 처리
    const groundLevel = canvas.height - player.radius - 2;
    if (player.y >= groundLevel) {{
        player.y = groundLevel;
        triggerGameOver("💥 지면 격돌 추락사 (Ground Fatal Impact)", "완충 없이 지면에 정면 충돌하여 치명상을 입었습니다!");
        return;
    }}

    // A. 벽에 달라붙어 있는 상태
    if (isWallClinging) {{
        player.vx = 0;
        player.vy = 2.2; // 벽을 타고 천천히 미끄러져 내려옴
        player.y += player.vy * dt * PIXELS_PER_METER;
        
        stateBadge.innerText = "🧗 벽 달라붙음 (클릭으로 점프!)";
        stateBadge.style.color = "#f97316";

        // 벽을 타고 내려오다가 바닥에 닿는 순간 사망
        if (player.y >= groundLevel) {{
            triggerGameOver("💥 지면 격돌 추락사 (Ground Fatal Impact)", "벽에서 탈출하지 못하고 지면으로 추락했습니다!");
            return;
        }}
    }}
    // B. 비행 / 스윙 상태
    else {{
        // 중력 가속
        player.vy += G * dt;

        // 거미줄 진자 스윙
        if (isAttached) {{
            stateBadge.innerText = "🕸️ 진자 스윙 중 (Swinging)";
            stateBadge.style.color = "#38bdf8";

            const dx = (player.x - anchor.x) / PIXELS_PER_METER;
            const dy = (player.y - anchor.y) / PIXELS_PER_METER;
            const currentDist = Math.sqrt(dx*dx + dy*dy);
            
            if (currentDist >= ropeLength) {{
                const nx = dx / currentDist;
                const ny = dy / currentDist;
                const vr = player.vx * nx + player.vy * ny;
                
                if (vr > 0) {{
                    player.vx -= vr * nx;
                    player.vy -= vr * ny;
                }}
                
                player.x = anchor.x + nx * ropeLength * PIXELS_PER_METER;
                player.y = anchor.y + ny * ropeLength * PIXELS_PER_METER;
                
                // 장력 T = m * (g*cosθ + v^2/r)
                const speedSq = player.vx * player.vx + player.vy * player.vy;
                const cosTheta = -ny;
                const centripetalAcc = speedSq / ropeLength;
                tensionN = MASS * Math.max(0, (G * cosTheta + centripetalAcc));
                
                // [사망 조건 2] 거미줄 허용 장력 초과 파단
                if (tensionN > F_BREAK) {{
                    triggerGameOver(
                        "🕸️ 거미줄 파단 (Tensile Failure)", 
                        `스윙 최저점 순간 장력(${{Math.round(tensionN).toLocaleString()}} N)이 고분자 최대 인장한도(${{F_BREAK.toLocaleString()}} N)를 초과하여 줄이 끊어졌습니다!`
                    );
                    return;
                }}
            }}
        }} else {{
            stateBadge.innerText = "🦅 자유 비행 (Free Flight)";
            stateBadge.style.color = "#4ade80";
        }}

        // 공기 저항
        player.vx *= 0.9995;
        player.vy *= 0.9995;

        // 위치 적분
        player.x += player.vx * dt * PIXELS_PER_METER;
        player.y += player.vy * dt * PIXELS_PER_METER;

        // 건물 충돌 검사 (벽 달라붙기 판정)
        for (const b of buildings) {{
            // 건물 좌측 벽면에 닿았을 때
            if (player.x + player.radius >= b.x && player.x - player.radius <= b.x + 10 &&
                player.y > b.y && player.y < canvas.height - 20) {{
                isWallClinging = true;
                clingSide = 1;
                player.x = b.x - player.radius;
                isAttached = false;
                break;
            }}
            // 건물 옥상 상단에 닿았을 때 (러닝 바운드)
            if (player.x >= b.x && player.x <= b.x + b.w &&
                Math.abs(player.y - b.y) < 14 && player.vy > 0) {{
                player.y = b.y - player.radius;
                player.vy = -11; // 옥상을 밟고 높이 튀어오름
                player.vx = Math.max(player.vx, 15);
            }}
        }}
    }}

    // 건물 생성 및 제거
    if (player.x + canvas.width > nextBuildingX) {{
        spawnBuilding();
    }}
    buildings = buildings.filter(b => b.x + b.w > player.x - 400);

    // 카메라 추적
    cameraX = player.x - 220;

    // HUD 수치 갱신
    score = Math.max(0, Math.floor((player.x - 100) / PIXELS_PER_METER));
    const speedKmh = Math.round(Math.sqrt(player.vx*player.vx + player.vy*player.vy) * 3.6);
    hudDist.innerText = score + " m";
    hudSpeed.innerText = speedKmh + " km/h";
    hudTension.innerText = Math.round(tensionN).toLocaleString() + " N";
}}

function triggerGameOver(reason, desc) {{
    isAlive = false;
    isAttached = false;
    isWallClinging = false;
    deathReason.innerText = reason;
    deathDesc.innerText = desc;
    finalDist.innerText = score;
    gameOverPanel.style.display = "block";
}}

function resetGame() {{
    player.x = 100;
    player.y = 220;
    player.vx = 14;
    player.vy = 0;
    isAlive = true;
    isAttached = false;
    isWallClinging = false;
    gameOverPanel.style.display = "none";
    initBuildings();
}}

// =============================================================================
// 그래픽 렌더링
// =============================================================================
function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(-cameraX, 0);

    // 1) 고층 빌딩
    for (const b of buildings) {{
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, b.y, b.w, b.h);
        
        // 창문
        ctx.fillStyle = b.windowColor;
        for (let wy = b.y + 16; wy < canvas.height - 20; wy += 32) {{
            for (let wx = b.x + 12; wx < b.x + b.w - 12; wx += 22) {{
                if ((wx + wy) % 5 === 0) {{
                    ctx.fillRect(wx, wy, 8, 14);
                }}
            }}
        }}

        // 옥상 타겟 가이드라인
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2;
        ctx.strokeRect(b.x, b.y, b.w, 4);
    }}

    // 2) 위험 지면 (추락 시 사망 경고 붉은 라인)
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(player.x - 400, canvas.height - 8, canvas.width + 800, 8);

    // 3) 거미줄 렌더링
    if (isAttached) {{
        ctx.beginPath();
        ctx.moveTo(anchor.x, anchor.y);
        ctx.lineTo(player.x, player.y);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 3;
        ctx.shadowColor = "#38bdf8";
        ctx.shadowBlur = 10;
        ctx.stroke();
        ctx.shadowBlur = 0;

        // 앵커 표시
        ctx.beginPath();
        ctx.arc(anchor.x, anchor.y, 6, 0, Math.PI * 2);
        ctx.fillStyle = "#ef4444";
        ctx.fill();
    }}

    // 4) 스파이더맨 캐릭터
    ctx.save();
    ctx.translate(player.x, player.y);
    
    if (isWallClinging) {{
        ctx.rotate(clingSide === 1 ? -Math.PI / 2 : Math.PI / 2);
    }} else {{
        const angle = Math.atan2(player.vy, player.vx);
        ctx.rotate(angle);
    }}

    // 몸체 (레드 슈트)
    ctx.beginPath();
    ctx.ellipse(0, 0, 15, 9, 0, 0, Math.PI * 2);
    ctx.fillStyle = "#e11d48";
    ctx.fill();

    // 슈트 블루 패턴
    ctx.beginPath();
    ctx.ellipse(-4, 0, 6, 7, 0, 0, Math.PI * 2);
    ctx.fillStyle = "#2563eb";
    ctx.fill();

    // 마스크 화이트 아이
    ctx.beginPath();
    ctx.ellipse(6, -3, 5, 2.5, Math.PI / 5, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.restore();
    ctx.restore();
}}

// 애니메이션 루프
let lastTime = performance.now();
function gameLoop(now) {{
    const dt = Math.min((now - lastTime) / 1000, 0.05);
    lastTime = now;
    
    updatePhysics(dt);
    draw();
    
    requestAnimationFrame(gameLoop);
}}

initBuildings();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(canvas_html, height=580, scrolling=False)

# ==============================================================================
# 4. 세특 탐구 보고서 연계 정리 (충격량 및 생체역학)
# ==============================================================================
with st.expander("📝 [생기부 세특 작성 팁] 지면 충돌 충격량(Impulse)과 고분자 장력 역학"):
    st.markdown(r"""
    * **운동량-충격량 정리와 인체 손상 임계치**:
      $$I = \int F \, dt = \Delta p = m \Delta v$$
      고공 낙하 시 바닥과의 충돌 시간이 극히 짧을 경우($\Delta t \to 0$), 파일럿에게 가해지는 순간 충격력($F = \frac{\Delta p}{\Delta t}$)이 인체 뼈와 장기의 한계 지탱 응력을 초과하여 사망에 이르게 됩니다.
    * **고분자 거미줄 파단과 안전 계수(Safety Factor)**:
      $$S_F = \frac{F_{\text{break}}}{T_{\max}} > 1.0$$
      스윙 최저점에서 장력($T$)이 재료의 극한 하중을 넘어서면 줄이 끊어지며 강제 자유 낙하 상태로 전환되도록 설계하여 재료역학적 안전 계수의 중요성을 실증했습니다.
    """)
