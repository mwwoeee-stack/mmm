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

st.title("🕸️ 피터 파커의 스파이더 액션 & 생체모방 벽타기 시뮬레이터")
st.caption("게코 도마뱀·거미 족모의 반데르발스 정전기 흡착 원리와 진자 스윙 공학 결합")

# ==============================================================================
# 2. 사이드바: 고분자 물성 및 피터 파커 신체 조건
# ==============================================================================
with st.sidebar:
    st.header("🧪 피터 파커 바이오 스펙 (Lab)")
    
    crosslink = st.slider(
        "거미줄 가교 밀도 (Crosslink, %)",
        min_value=30, max_value=100, value=85, step=5,
        help="단백질 사슬 결합도. 피터 파커 공식 사양은 고가교 초강도 섬유입니다."
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
    # 인장강도 (피터의 웹플루이드는 일반 강철의 5배 이상, 약 1200~2000 MPa)
    tensile_strength_mpa = 600.0 + (crosslink * 15.0)
    f_break_n = tensile_strength_mpa * area_mm2
    
    # 영률 (GPa)
    youngs_modulus_gpa = 5.0 + (crosslink * 0.2)

    st.divider()
    st.subheader("📊 웹슈터 역학 제원")
    st.metric("최대 인장 하중 (F_break)", f"{f_break_n:,.0f} N")
    st.metric("영률 (Elasticity)", f"{youngs_modulus_gpa:.1f} GPa")
    st.metric("스파이더 근력 허용 G", "15.0 G (초인 스펙)")

# 조작법 가이드 안내
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("🎯 **1. 넉넉한 스윙 사출**")
    st.info("**[스페이스바]**나 **[마우스 꾹]**: 전방 건물에 자동으로 거미줄을 발사해 부드럽게 가속합니다.")
with c2:
    st.markdown("🧗 **2. 벽 달라붙기 (Wall Stick)**")
    st.success("건물 옆면에 닿으면 죽지 않고 **탁 달라붙어 천천히 슬라이딩**합니다. (반데르발스 인력)")
with c3:
    st.markdown("🚀 **3. 스파이더 슈퍼 점프**")
    st.warning("벽에 붙은 상태에서 **클릭/스페이스바**를 튕기면 건물 벽을 차고 **공중으로 솟구칩니다!**")

# ==============================================================================
# 3. HTML5 Canvas 물리 엔진 (벽타기 & 슈퍼도약 & 이지 맵 탑재)
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
        <h2 id="death-reason" style="color: #ef4444; margin:0 0 10px 0;">거미줄 파단!</h2>
        <p id="death-desc" style="color: #cbd5e1; font-size:14px; margin:0;">장력이 허용 한도를 초과했습니다.</p>
        <p style="margin: 12px 0 0 0; font-size: 16px; font-weight: bold;">최종 이동 거리: <span id="final-dist">0</span> m</p>
        <button class="retry-btn" onclick="resetGame()">다시 스윙하기</button>
    </div>
</div>

<script>
// =============================================================================
// 파이썬 공학 상수 주입
// =============================================================================
const F_BREAK = {f_break_n};         // 파단 장력 (N)
const MASS = {mass};                 // 피터 파커 질량 (kg)
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
// 플레이어 & 월드 상태
// =============================================================================
let isAlive = true;
let isAttached = false;
let isWallClinging = false; // 벽에 붙어있는 상태
let clingWall = null;        // 현재 붙어있는 건물 정보
let clingSide = 1;          // 1: 건물의 왼쪽 벽, -1: 건물의 오른쪽 벽
let anchor = {{ x: 0, y: 0 }};
let ropeLength = 0;
let score = 0;
let cameraX = 0;

const player = {{
    x: 100,
    y: 260,
    vx: 14,                  // 쾌적한 시작 수평 속도
    vy: 0,
    radius: 12
}};

// 건물 생성 (간격 좁히고 루프탑 높이 균일화하여 쾌적한 맵 구성)
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
    const width = 100 + Math.random() * 80;
    // 옥상 높이를 플레이하기 편하게 안정적인 범위(220~300px)로 설정
    const height = 220 + Math.random() * 80;
    const gap = 30 + Math.random() * 40; // 간격을 확 줄여 끊김 방지
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
// 원터치 조작 로직 (스윙 & 벽타기 슈퍼 점프)
// =============================================================================
let inputPressed = false;

function handleActionDown() {{
    if (!isAlive) return;
    inputPressed = true;

    // [피터 파커 특수능력] 벽에 붙어있을 때 클릭 시 -> 반대편으로 슈퍼 도약!
    if (isWallClinging) {{
        isWallClinging = false;
        // 붙어있던 벽을 강하게 발로 차며 도약 (Wall Jump Vector)
        player.vx = (clingSide === 1 ? -1 : 1) * -16; // 전방 방향으로 튕겨나감
        player.vy = -18;                               // 높은 상승력
        isAttached = false;
        return;
    }}

    // 공중에 있을 때 클릭 시 -> 거미줄 사출
    tryAttachWeb();
}}

function handleActionUp() {{
    inputPressed = false;
    if (isAttached) {{
        isAttached = false; // 줄을 놓으면 관성 탄도 비행
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

// 넉넉한 자동 타겟팅 거미줄 사출
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
        
        // 전방 5m ~ 50m 넓은 범위 내의 옥상 자동 흡착
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
// 물리 업데이트 (벽타기 흡착 + 진자 스윙)
// =============================================================================
function updatePhysics(dt) {{
    if (!isAlive) return;

    let tensionN = 0;

    // A. 벽에 달라붙어 있는 상태 (Wall Cling & Slide)
    if (isWallClinging) {{
        player.vx = 0;
        // 천천히 미끄러져 내려옴 (게코 도마뱀/거미 족모 마찰 제동)
        player.vy = 2.0; 
        player.y += player.vy * dt * PIXELS_PER_METER;
        
        stateBadge.innerText = "🧗 벽 달라붙음 (점프 준비!)";
        stateBadge.style.color = "#f97316";

        // 벽의 끝(지면 근처)까지 내려왔을 때 처리
        if (player.y >= canvas.height - 30) {{
            isWallClinging = false;
        }}
    }}
    // B. 공중 비행 / 스윙 상태
    else {{
        // 1) 기본 중력
        player.vy += G * dt;

        // 2) 거미줄 스윙 처리
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
                
                // 장력 계산: T = m * (g*cos(theta) + v^2/r)
                const speedSq = player.vx * player.vx + player.vy * player.vy;
                const cosTheta = -ny;
                const centripetalAcc = speedSq / ropeLength;
                tensionN = MASS * Math.max(0, (G * cosTheta + centripetalAcc));
                
                // 거미줄 파단 검증
                if (tensionN > F_BREAK) {{
                    triggerGameOver(
                        "🕸️ 거미줄 파단 (Material Limit Exceeded)", 
                        `장력(${{Math.round(tensionN).toLocaleString()}} N)이 웹슈터 한도(${{F_BREAK.toLocaleString()}} N)를 초과하여 끊어졌습니다!`
                    );
                    return;
                }}
            }}
        }} else {{
            stateBadge.innerText = "🦅 탄도 비행 (Free Flight)";
            stateBadge.style.color = "#4ade80";
        }}

        // 공기 저항 완화 (시원한 비행 감각)
        player.vx *= 0.9995;
        player.vy *= 0.9995;

        // 위치 적분
        player.x += player.vx * dt * PIXELS_PER_METER;
        player.y += player.vy * dt * PIXELS_PER_METER;

        // 3) [핵심 개선] 건물 충돌 시 사망 대신 '벽 달라붙기' 발동!
        for (const b of buildings) {{
            // 건물 좌측 벽 흡착
            if (player.x + player.radius >= b.x && player.x - player.radius <= b.x + 8 &&
                player.y > b.y && player.y < canvas.height) {{
                isWallClinging = true;
                clingWall = b;
                clingSide = 1;
                player.x = b.x - player.radius;
                isAttached = false;
                break;
            }}
            // 건물 옥상 착지
            if (player.x >= b.x && player.x <= b.x + b.w &&
                Math.abs(player.y - b.y) < 15 && player.vy > 0) {{
                // 옥상 살짝 밟고 튕겨오름 (슈퍼 러닝)
                player.vy = -10;
                player.vx = Math.max(player.vx, 14);
            }}
        }}
    }}

    // 지면 충돌 시 바운드 처리 (낙사 방지 패시브)
    if (player.y >= canvas.height - 25) {{
        player.y = canvas.height - 25;
        player.vy = -12; // 바닥을 짚고 높이 바운드
        player.vx = Math.max(player.vx * 0.8, 8);
    }}

    // 건물 순환 생성
    if (player.x + canvas.width > nextBuildingX) {{
        spawnBuilding();
    }}
    buildings = buildings.filter(b => b.x + b.w > player.x - 400);

    // 카메라 추적
    cameraX = player.x - 220;

    // HUD 갱신
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
    player.y = 260;
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

    // 1) 건물 렌더링
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

        // 옥상 타겟 가이드
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2;
        ctx.strokeRect(b.x, b.y, b.w, 4);
    }}

    // 2) 거미줄
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

        // 앵커 지점
        ctx.beginPath();
        ctx.arc(anchor.x, anchor.y, 6, 0, Math.PI * 2);
        ctx.fillStyle = "#ef4444";
        ctx.fill();
    }}

    // 3) 스파이더맨 캐릭터
    ctx.save();
    ctx.translate(player.x, player.y);
    
    // 벽에 붙었을 때와 날아갈 때의 포즈 각도 제어
    if (isWallClinging) {{
        ctx.rotate(clingSide === 1 ? -Math.PI / 2 : Math.PI / 2);
    }} else {{
        const angle = Math.atan2(player.vy, player.vx);
        ctx.rotate(angle);
    }}

    // 몸체 (스파이더 슈트)
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

// 60FPS 애니메이션 루프
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
# 4. 세특 탐구 보고서 연계 정리 (생체모방 정전기 흡착 공학)
# ==============================================================================
with st.expander("📝 [생기부 세특 작성 팁] 벽타기(Wall-Cling)의 생체모방 공학적 원리"):
    st.markdown(r"""
    * **반데르발스 힘(Van der Waals Force)과 건식 접착(Dry Adhesion)**:
      * 스파이더맨이 매끄러운 고층 빌딩 벽면에 달라붙을 수 있는 원리는 도마뱀붙이(Gecko)와 거미의 발바닥에 수억 개 존재하는 미세 주걱 형태의 **나노 강모(Setae & Spatulae)** 구조에 기반합니다.
      * 접촉 면적이 극대화되면서 순간적인 쌍극자 유도에 의한 분자 간 인력(반데르발스 힘, 단위 면적당 수십 $\text{N/cm}^2$)이 발생하여 체중을 지탱합니다.
    * **동적 벽면 반발 도약(Wall Jump Mechanics)**:
      * 벽면에 부착된 상태에서 탄성 근섬유의 에너지를 순간적으로 방출($F_{\text{push}} = m \cdot a$)하여 수평 및 수직 운동량 성분을 동시에 생성하는 생체 모멘텀 전환 알고리즘을 프로그램에 적용했습니다.
    """)
