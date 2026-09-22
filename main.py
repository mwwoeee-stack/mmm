import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. Streamlit 페이지 설정
# ==============================================================================
st.set_page_config(
    page_title="스파이더맨 웹슈터 공학 랩 & 더블 탭 묘기 액션",
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

st.title("🕸️ 피터 파커의 고분자 웹슈터 역학 랩 & 아크로바틱 묘기 액션")
st.caption("진자 스윙 역학, 고분자 파단 피드백, 그리고 공중 360° 회전 묘기(Acrobatic Trick) 결합")

# ==============================================================================
# 2. 사이드바: 고분자 물성 및 피터 파커 신체 조건
# ==============================================================================
with st.sidebar:
    st.header("🧪 웹 플루이드 고분자 배합 (Lab)")
    
    crosslink = st.slider(
        "거미줄 가교 밀도 (Crosslink, %)",
        min_value=20, max_value=100, value=75, step=5,
        help="단백질 사슬 결합 강도. 인장 강도와 영률을 좌우합니다."
    )
    
    nozzle_diam = st.slider(
        "웹슈터 사출 구경 (Nozzle Gauge, mm)",
        min_value=0.6, max_value=3.0, value=1.3, step=0.1,
        help="거미줄의 굵기. 단면적이 커질수록 견디는 절대 하중이 급증합니다."
    )
    
    mass = st.number_input(
        "피터 파커 체중 (kg)",
        min_value=50, max_value=90, value=70, step=1
    )

    # 재료역학 계산
    radius_mm = nozzle_diam / 2.0
    area_mm2 = 3.141592 * (radius_mm ** 2)
    tensile_strength_mpa = 500.0 + (crosslink * 14.0)
    f_break_n = tensile_strength_mpa * area_mm2
    youngs_modulus_gpa = 4.0 + (crosslink * 0.18)

    st.divider()
    st.subheader("📊 웹슈터 역학 제원")
    st.metric("최대 허용 장력 (F_break)", f"{f_break_n:,.0f} N")
    st.metric("인장 강도 (Tensile Strength)", f"{tensile_strength_mpa:,.0f} MPa")
    st.metric("영률 (Elasticity)", f"{youngs_modulus_gpa:.1f} GPa")

# 조작 가이드 안내
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("🎯 **1. 스페이스바 거미줄 사출**")
    st.info("**[스페이스바 누름]**: 거미줄이 옥상으로 즉시 사출되어 진자 스윙을 합니다. 떼면 줄을 놓고 날아갑니다.")
with c2:
    st.markdown("🤸‍♂️ **2. 더블 스페이스바 묘기 (Trick)**")
    st.success("**[스페이스바 2번 연속 따닥!]**: 공중에서 360° 공중제비 묘기를 펼치며 추가 가속 추진을 얻습니다!")
with c3:
    st.markdown("🧗 **3. 벽 붙기 & 슈퍼 점프**")
    st.warning("건물 옆면에 닿으면 벽에 흡착되며, 이때 **[스페이스바]**를 누르면 대각선 위로 **슈퍼 점프**합니다.")

# ==============================================================================
# 3. HTML5 Canvas 물리 엔진 (더블 탭 묘기 시스템 탑재)
# ==============================================================================
raw_html_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {
        margin: 0;
        padding: 0;
        background: #020617;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        user-select: none;
        overflow: hidden;
    }
    #game-container {
        position: relative;
        width: 100%;
        max-width: 960px;
        margin: 0 auto;
    }
    canvas {
        display: block;
        background: linear-gradient(to bottom, #050814 0%, #0f172a 60%, #1e1b4b 100%);
        border: 2px solid #334155;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    #hud {
        position: absolute;
        top: 15px;
        left: 20px;
        pointer-events: none;
        display: flex;
        gap: 12px;
        font-size: 14px;
        font-weight: 600;
        text-shadow: 1px 1px 3px black;
    }
    .hud-box {
        background: rgba(15, 23, 42, 0.85);
        padding: 8px 12px;
        border-radius: 6px;
        border: 1px solid #475569;
    }
    #state-badge {
        color: #38bdf8;
        font-weight: 700;
    }
    #trick-banner {
        position: absolute;
        top: 65px;
        left: 50%;
        transform: translateX(-50%);
        pointer-events: none;
        background: linear-gradient(90deg, #f59e0b, #ef4444);
        color: white;
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 15px;
        font-weight: 800;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.6);
        display: none;
        animation: pulse 0.3s infinite alternate;
    }
    @keyframes pulse {
        from { transform: translateX(-50%) scale(1); }
        to { transform: translateX(-50%) scale(1.08); }
    }
    #game-over {
        display: none;
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(15, 23, 42, 0.96);
        padding: 24px 32px;
        border-radius: 14px;
        border: 2px solid #ef4444;
        width: 82%;
        max-width: 620px;
        box-shadow: 0 20px 30px -5px rgba(239, 68, 68, 0.4);
    }
    .diag-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 12px 0;
        text-align: left;
        font-size: 13px;
        line-height: 1.6;
    }
    .diag-title {
        color: #fca5a5;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    button.retry-btn {
        margin-top: 14px;
        background: #ef4444;
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 15px;
        font-weight: 700;
        border-radius: 6px;
        cursor: pointer;
        width: 100%;
    }
    button.retry-btn:hover {
        background: #dc2626;
    }
</style>
</head>
<body>

<div id="game-container">
    <canvas id="canvas" width="960" height="540"></canvas>
    
    <div id="hud">
        <div class="hud-box">거리: <span id="hud-dist" style="color:#38bdf8;">0 m</span></div>
        <div class="hud-box">속도: <span id="hud-speed" style="color:#4ade80;">0 km/h</span></div>
        <div class="hud-box">상태: <span id="state-badge">비행 중</span></div>
        <div class="hud-box">장력: <span id="hud-tension" style="color:#fbbf24;">0 N</span> / __F_BREAK_FORMATTED__ N</div>
    </div>

    <!-- 묘기 발동 배너 -->
    <div id="trick-banner">✨ 360° 공중제비 묘기 발동! (+부스트)</div>

    <!-- 파단 및 게임오버 진단 창 -->
    <div id="game-over">
        <h2 id="death-reason" style="color: #ef4444; margin:0 0 8px 0; font-size: 22px;">거미줄 파단!</h2>
        <p id="death-desc" style="color: #cbd5e1; font-size:14px; margin:0;">장력 초과 파단이 발생했습니다.</p>
        
        <div class="diag-card" id="diag-panel">
            <div class="diag-title">🔬 피터 파커의 공학적 원인 분석 (Diagnostic Report)</div>
            <div id="diag-details" style="color: #e2e8f0;">분석 데이터를 계산 중입니다...</div>
        </div>

        <p style="margin: 8px 0 0 0; font-size: 15px; font-weight: bold; text-align: center;">
            최종 비행 기록: <span id="final-dist" style="color:#38bdf8;">0</span> m
        </p>
        <button class="retry-btn" onclick="resetGame()">다시 도전하기</button>
    </div>
</div>

<script>
const F_BREAK = __F_BREAK__;
const MASS = __MASS__;
const G = 9.81;
const PIXELS_PER_METER = 20;
const NOZZLE_DIAM = __NOZZLE_DIAM__;
const CROSSLINK = __CROSSLINK__;

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const hudDist = document.getElementById("hud-dist");
const hudSpeed = document.getElementById("hud-speed");
const hudTension = document.getElementById("hud-tension");
const stateBadge = document.getElementById("state-badge");
const trickBanner = document.getElementById("trick-banner");
const gameOverPanel = document.getElementById("game-over");
const deathReason = document.getElementById("death-reason");
const deathDesc = document.getElementById("death-desc");
const diagDetails = document.getElementById("diag-details");
const finalDist = document.getElementById("final-dist");

let isAlive = true;
let isAttached = false;
let isWallClinging = false;
let clingSide = 1;
let anchor = { x: 0, y: 0 };
let ropeLength = 0;
let score = 0;
let cameraX = 0;

// 더블 탭(더블 스페이스바) 및 묘기(Trick) 상태 변수
let lastSpacePressTime = 0;
const DOUBLE_TAP_DELAY = 280; // 280ms 이내 재입력 시 더블탭 인정
let isDoingTrick = false;
let trickRotation = 0;        // 360도 회전 각도 누적
let trickTrail = [];          // 묘기 발동 잔상 궤적

const player = {
    x: 100,
    y: 220,
    vx: 14,
    vy: 0,
    radius: 12
};

let buildings = [];
let nextBuildingX = 0;

function initBuildings() {
    buildings = [];
    nextBuildingX = 0;
    while (nextBuildingX < canvas.width * 3) {
        spawnBuilding();
    }
}

function spawnBuilding() {
    const width = 110 + Math.random() * 80;
    const height = 230 + Math.random() * 90;
    const gap = 35 + Math.random() * 35;
    buildings.push({
        x: nextBuildingX,
        y: canvas.height - height,
        w: width,
        h: height,
        color: '#1e293b',
        windowColor: Math.random() > 0.4 ? '#fde047' : '#0f172a'
    });
    nextBuildingX += width + gap;
}

// =============================================================================
// 스페이스바 단발 & 더블 클릭 묘기 제어
// =============================================================================
function handleSpacePress() {
    if (!isAlive) return;

    const now = performance.now();
    const timeSinceLastPress = now - lastSpacePressTime;

    // 1) 벽에 붙어있는 경우 -> 슈퍼 점프 도약
    if (isWallClinging) {
        isWallClinging = false;
        player.vx = (clingSide === 1 ? -1 : 1) * -17;
        player.vy = -18;
        isAttached = false;
        lastSpacePressTime = now;
        return;
    }

    // 2) [더블 스페이스바 감지] 공중에서 280ms 이내에 다시 누른 경우 -> 묘기 발동!
    if (timeSinceLastPress < DOUBLE_TAP_DELAY && !isAttached) {
        triggerAcrobaticTrick();
        lastSpacePressTime = 0; // 더블탭 소비
        return;
    }
    lastSpacePressTime = now;

    // 3) 단발 스페이스바 -> 거미줄 발사
    tryAttachWeb();
}

function handleSpaceRelease() {
    if (isAttached) {
        isAttached = false; // 거미줄 놓고 탄도 비행
    }
}

// 묘기(Trick) 실행: 360도 공중제비 및 추가 부스트
function triggerAcrobaticTrick() {
    isDoingTrick = true;
    trickRotation = 0;
    isAttached = false; // 묘기 중에는 거미줄 해제
    
    // 묘기 공중 부스트 가속 (전방 추진 + 상공 부양)
    player.vx += 5.5;
    player.vy = -11.5;
    
    trickBanner.style.display = "block";
    setTimeout(() => {
        trickBanner.style.display = "none";
    }, 800);
}

window.addEventListener("keydown", (e) => {
    if (e.code === "Space" && !e.repeat) {
        handleSpacePress();
        e.preventDefault();
    }
});
window.addEventListener("keyup", (e) => {
    if (e.code === "Space") {
        handleSpaceRelease();
        e.preventDefault();
    }
});
canvas.addEventListener("mousedown", handleSpacePress);
window.addEventListener("mouseup", handleSpaceRelease);

// 전방 옥상 자동 조준 사출
function tryAttachWeb() {
    if (isAttached || isWallClinging || isDoingTrick) return;
    
    let bestAnchor = null;
    let minDistance = 9999;
    
    for (const b of buildings) {
        const rooftopX = b.x + b.w * 0.4;
        const rooftopY = b.y;
        
        const dx = (rooftopX - player.x) / PIXELS_PER_METER;
        const dy = (rooftopY - player.y) / PIXELS_PER_METER;
        const dist = Math.sqrt(dx*dx + dy*dy);
        
        if (dx > 3 && dist < 50 && dist < minDistance) {
            minDistance = dist;
            bestAnchor = { x: rooftopX, y: rooftopY };
        }
    }
    
    if (bestAnchor) {
        anchor = bestAnchor;
        const dx = (player.x - anchor.x) / PIXELS_PER_METER;
        const dy = (player.y - anchor.y) / PIXELS_PER_METER;
        ropeLength = Math.sqrt(dx*dx + dy*dy);
        isAttached = true;
    }
}

// 파단 진단 피드백 엔진
function analyzeWebFracture(tensionN, speedKmh, radiusM, centripetalAcc, gravityComponent) {
    const excess = tensionN - F_BREAK;
    const excessPct = Math.round((excess / F_BREAK) * 100);
    
    const currentSigma = 500.0 + (CROSSLINK * 14.0);
    const reqNozzleDiam = (2.0 * Math.sqrt(tensionN / (Math.PI * currentSigma))).toFixed(2);
    
    let primaryCause = "";
    let actionGuide = "";

    if (centripetalAcc > 40) {
        primaryCause = "🌪️ <b>구심 가속도 폭증 (" + (centripetalAcc/G).toFixed(1) + " G)</b>: 스윙 속도(" + speedKmh + " km/h)가 너무 빨라 원심력이 거미줄 지탱 한계를 압도했습니다.";
        actionGuide = "👉 <b>플레이 처방</b>: 최저점에 도달하기 전 스페이스바를 떼서 탄도 비행으로 넘어가거나, 좌측에서 <b>노즐 구경을 " + reqNozzleDiam + " mm 이상</b>으로 키우십시오.";
    } else if (radiusM < 12) {
        primaryCause = "📐 <b>초단거리 곡률 반경 (" + radiusM.toFixed(1) + " m)</b>: 앵커와 너무 가까운 거리에서 급격히 회전하여 회전 반경(r) 감소로 인한 장력 집중이 발생했습니다.";
        actionGuide = "👉 <b>플레이 처방</b>: 전방 먼 지점에 거미줄을 걸어 완만한 스윙 호(Arc)를 그리거나, <b>가교 밀도</b>를 높여 기본 인장강도를 보강하십시오.";
    } else {
        primaryCause = "⚖️ <b>동적 하중 한계 초과</b>: 고공 낙하 중력 성분과 운동 에너지가 복합되어 거미줄 안전계수를 상쇄했습니다.";
        actionGuide = "👉 <b>공학 튜닝 처방</b>: 현재 배합(" + NOZZLE_DIAM + "mm, " + CROSSLINK + "%)으로는 " + tensionN.toFixed(0) + " N의 충격을 감당할 수 없습니다. <b>노즐을 최소 " + reqNozzleDiam + " mm</b>로 개조하십시오.";
    }

    return "• <b>순간 측정 장력</b>: <span style='color:#ef4444; font-weight:bold;'>" + Math.round(tensionN).toLocaleString() + " N</span> (허용 한도 대비 <b>+" + excessPct + "%</b> 초과)<br>" +
           "• <b>주요 역학 원인</b>: " + primaryCause + "<br>" +
           "• <b>공학적 솔루션</b>: " + actionGuide;
}

// 물리 업데이트
function updatePhysics(dt) {
    if (!isAlive) return;

    let tensionN = 0;
    const groundLevel = canvas.height - player.radius - 2;

    // 지면 충돌 사망 판정
    if (player.y >= groundLevel) {
        player.y = groundLevel;
        triggerGroundGameOver();
        return;
    }

    // 묘기(360도 공중제비) 회전 적분
    if (isDoingTrick) {
        trickRotation += dt * 18; // 빠른 회전 속도
        stateBadge.innerText = "🤸‍♂️ 360° 공중 묘기 중!";
        stateBadge.style.color = "#f59e0b";
        
        // 잔상 이펙트 기록
        trickTrail.push({ x: player.x, y: player.y, alpha: 0.8 });

        if (trickRotation >= Math.PI * 2) {
            isDoingTrick = false;
            trickRotation = 0;
        }
    }

    // 잔상 페이드아웃
    for (let i = trickTrail.length - 1; i >= 0; i--) {
        trickTrail[i].alpha -= dt * 2.5;
        if (trickTrail[i].alpha <= 0) trickTrail.splice(i, 1);
    }

    // A. 벽에 달라붙은 상태
    if (isWallClinging) {
        player.vx = 0;
        player.vy = 2.2;
        player.y += player.vy * dt * PIXELS_PER_METER;
        
        stateBadge.innerText = "🧗 벽 달라붙음 (스페이스바로 도약!)";
        stateBadge.style.color = "#f97316";

        if (player.y >= groundLevel) {
            triggerGroundGameOver();
            return;
        }
    } 
    // B. 비행 및 스윙 상태
    else {
        player.vy += G * dt;

        if (isAttached) {
            stateBadge.innerText = "🕸️ 진자 스윙 중";
            stateBadge.style.color = "#38bdf8";

            const dx = (player.x - anchor.x) / PIXELS_PER_METER;
            const dy = (player.y - anchor.y) / PIXELS_PER_METER;
            const currentDist = Math.sqrt(dx*dx + dy*dy);
            
            if (currentDist >= ropeLength) {
                const nx = dx / currentDist;
                const ny = dy / currentDist;
                const vr = player.vx * nx + player.vy * ny;
                
                if (vr > 0) {
                    player.vx -= vr * nx;
                    player.vy -= vr * ny;
                }
                
                player.x = anchor.x + nx * ropeLength * PIXELS_PER_METER;
                player.y = anchor.y + ny * ropeLength * PIXELS_PER_METER;
                
                const speedSq = player.vx * player.vx + player.vy * player.vy;
                const cosTheta = -ny;
                const centripetalAcc = speedSq / ropeLength;
                const gravityComponent = G * cosTheta;
                tensionN = MASS * Math.max(0, (gravityComponent + centripetalAcc));
                
                if (tensionN > F_BREAK) {
                    const speedKmh = Math.round(Math.sqrt(speedSq) * 3.6);
                    const feedbackHTML = analyzeWebFracture(tensionN, speedKmh, ropeLength, centripetalAcc, gravityComponent);
                    triggerFractureGameOver(feedbackHTML);
                    return;
                }
            }
        } else if (!isDoingTrick) {
            stateBadge.innerText = "🦅 자유 탄도 비행";
            stateBadge.style.color = "#4ade80";
        }

        player.vx *= 0.9995;
        player.vy *= 0.9995;

        player.x += player.vx * dt * PIXELS_PER_METER;
        player.y += player.vy * dt * PIXELS_PER_METER;

        // 건물 벽 충돌 검사
        for (const b of buildings) {
            if (player.x + player.radius >= b.x && player.x - player.radius <= b.x + 10 &&
                player.y > b.y && player.y < canvas.height - 20) {
                isWallClinging = true;
                clingSide = 1;
                player.x = b.x - player.radius;
                isAttached = false;
                isDoingTrick = false;
                break;
            }
            if (player.x >= b.x && player.x <= b.x + b.w &&
                Math.abs(player.y - b.y) < 14 && player.vy > 0) {
                player.y = b.y - player.radius;
                player.vy = -11;
                player.vx = Math.max(player.vx, 15);
            }
        }
    }

    if (player.x + canvas.width > nextBuildingX) {
        spawnBuilding();
    }
    buildings = buildings.filter(b => b.x + b.w > player.x - 400);

    cameraX = player.x - 220;

    score = Math.max(0, Math.floor((player.x - 100) / PIXELS_PER_METER));
    const currentSpeedKmh = Math.round(Math.sqrt(player.vx*player.vx + player.vy*player.vy) * 3.6);
    hudDist.innerText = score + " m";
    hudSpeed.innerText = currentSpeedKmh + " km/h";
    
    const tensionRatio = tensionN / F_BREAK;
    if (tensionRatio > 0.85) {
        hudTension.innerHTML = "<span style='color:#ef4444;'>" + Math.round(tensionN).toLocaleString() + " N (과부하!)</span>";
    } else {
        hudTension.innerText = Math.round(tensionN).toLocaleString() + " N";
    }
}

function triggerFractureGameOver(feedbackHTML) {
    isAlive = false;
    isAttached = false;
    isWallClinging = false;
    isDoingTrick = false;
    deathReason.innerText = "💥 거미줄 인장 파단 (Web Line Snapped!)";
    deathDesc.innerText = "스윙 도중 줄에 걸린 순간 장력이 고분자 한계치를 초과하여 끊어졌습니다.";
    diagDetails.innerHTML = feedbackHTML;
    finalDist.innerText = score;
    gameOverPanel.style.display = "block";
}

function triggerGroundGameOver() {
    isAlive = false;
    isAttached = false;
    isWallClinging = false;
    isDoingTrick = false;
    deathReason.innerText = "💀 지면 충돌 추락사 (Ground Impact)";
    deathDesc.innerText = "고공 낙하 충격량을 분산하지 못하고 바닥에 정면 충돌했습니다.";
    diagDetails.innerHTML = "• <b>충돌 상황</b>: 스윙 앵커가 끊기거나 벽에서 탈출하지 못해 지면에 격돌함.<br>" +
                           "• <b>플레이 처방</b>: 바닥에 닿기 전 <b>[스페이스바]</b>로 다음 건물에 재사출하거나 <b>[더블 스페이스바]</b>로 공중제비를 돌아 고도를 복원하십시오!";
    finalDist.innerText = score;
    gameOverPanel.style.display = "block";
}

function resetGame() {
    player.x = 100;
    player.y = 220;
    player.vx = 14;
    player.vy = 0;
    isAlive = true;
    isAttached = false;
    isWallClinging = false;
    isDoingTrick = false;
    trickRotation = 0;
    trickTrail = [];
    gameOverPanel.style.display = "none";
    initBuildings();
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(-cameraX, 0);

    // 1) 빌딩 렌더링
    for (const b of buildings) {
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, b.y, b.w, b.h);
        
        ctx.fillStyle = b.windowColor;
        for (let wy = b.y + 16; wy < canvas.height - 20; wy += 32) {
            for (let wx = b.x + 12; wx < b.x + b.w - 12; wx += 22) {
                if ((wx + wy) % 5 === 0) {
                    ctx.fillRect(wx, wy, 8, 14);
                }
            }
        }

        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2;
        ctx.strokeRect(b.x, b.y, b.w, 4);
    }

    // 2) 바닥 위험선
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(player.x - 400, canvas.height - 8, canvas.width + 800, 8);

    // 3) 묘기 발동 잔상 궤적
    for (const trail of trickTrail) {
        ctx.beginPath();
        ctx.arc(trail.x, trail.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(245, 158, 11, " + trail.alpha + ")";
        ctx.fill();
    }

    // 4) 거미줄
    if (isAttached) {
        ctx.beginPath();
        ctx.moveTo(anchor.x, anchor.y);
        ctx.lineTo(player.x, player.y);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 3;
        ctx.shadowColor = "#38bdf8";
        ctx.shadowBlur = 10;
        ctx.stroke();
        ctx.shadowBlur = 0;

        ctx.beginPath();
        ctx.arc(anchor.x, anchor.y, 6, 0, Math.PI * 2);
        ctx.fillStyle = "#ef4444";
        ctx.fill();
    }

    // 5) 스파이더맨 캐릭터 렌더링
    ctx.save();
    ctx.translate(player.x, player.y);
    
    if (isDoingTrick) {
        // 공중제비 360도 회전
        ctx.rotate(trickRotation);
    } else if (isWallClinging) {
        ctx.rotate(clingSide === 1 ? -Math.PI / 2 : Math.PI / 2);
    } else {
        const angle = Math.atan2(player.vy, player.vx);
        ctx.rotate(angle);
    }

    // 몸체 (레드 슈트)
    ctx.beginPath();
    ctx.ellipse(0, 0, 15, 9, 0, 0, Math.PI * 2);
    ctx.fillStyle = isDoingTrick ? "#f59e0b" : "#e11d48";
    ctx.fill();

    // 슈트 블루 패턴
    ctx.beginPath();
    ctx.ellipse(-4, 0, 6, 7, 0, 0, Math.PI * 2);
    ctx.fillStyle = "#2563eb";
    ctx.fill();

    // 눈 마스크
    ctx.beginPath();
    ctx.ellipse(6, -3, 5, 2.5, Math.PI / 5, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.restore();
    ctx.restore();
}

let lastTime = performance.now();
function gameLoop(now) {
    const dt = Math.min((now - lastTime) / 1000, 0.05);
    lastTime = now;
    
    updatePhysics(dt);
    draw();
    
    requestAnimationFrame(gameLoop);
}

initBuildings();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

# 파이썬 수치 치환
final_html = raw_html_template \
    .replace("__F_BREAK__", str(f_break_n)) \
    .replace("__F_BREAK_FORMATTED__", f"{f_break_n:,.0f}") \
    .replace("__MASS__", str(mass)) \
    .replace("__NOZZLE_DIAM__", str(nozzle_diam)) \
    .replace("__CROSSLINK__", str(crosslink))

components.html(final_html, height=590, scrolling=False)

# ==============================================================================
# 4. 세특 탐구 보고서 연계 정리
# ==============================================================================
with st.expander("📝 [생기부 세특 작성 팁] 거미줄 파단 진단 알고리즘과 각운동량 보존 법칙"):
    st.markdown(r"""
    * **공중 묘기(Acrobatic Trick)와 각운동량 보존 법칙(Conservation of Angular Momentum)**:
      * 스파이더맨이 공중제비를 도는 동작은 신체 중심축으로 팔다리를 웅크려 관성 모멘트($I = \sum m_i r_i^2$)를 감소시키고, 이에 따라 각속도($\omega = \frac{L}{I}$)를 급증시키는 회전 역학 원리를 모사함.
    * **파단 원인 분해 알고리즘(Failure Analysis Algorithm)**:
      * 스윙 장력 수식 $T = m\left(g\cos\theta + \frac{v^2}{r}\right)$에서 파단 순간의 각 항의 기여도를 분해하여, 구심 가속도 폭증인지 곡률 반경 부족인지 역학적으로 판별하도록 프로그래밍함.
    * **임계 노즐 구경 역산(Inverse Design of Nozzle Diameter)**:
      * 파단 장력 $T_{\text{fail}}$ 발생 시, 재료가 이를 견디기 위해 요구되는 최소 노즐 직경 $d_{\text{req}}$를 극한 인장강도($\sigma_{\text{uts}}$)로부터 역산하는 수식을 피드백 패널에 실시간 렌더링함:
      $$d_{\text{req}} = 2 \cdot \sqrt{\frac{T_{\text{fail}}}{\pi \cdot \sigma_{\text{uts}}}}$$
    """)
