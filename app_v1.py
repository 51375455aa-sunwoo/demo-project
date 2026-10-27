
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="IRON FIGHT 2",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {background:#070b17;color:white}
.block-container {
    max-width:1400px;
    padding:0.5rem 0.4rem 1rem;
}
header[data-testid="stHeader"] {background:transparent}
iframe {border:0}
</style>
""", unsafe_allow_html=True)

game = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
html,body{
 margin:0;padding:0;background:#070b17;color:white;
 font-family:Arial,sans-serif;
 overscroll-behavior:none;
}
#gamebox{position:relative;width:100%;max-width:1200px;margin:auto}
canvas{
 display:block;width:100%;height:auto;
 border:2px solid #425477;border-radius:10px;
 background:#0b1020;touch-action:none;
}
.panel{
 position:absolute;inset:0;display:flex;
 flex-direction:column;align-items:center;
 justify-content:center;
 background:rgba(4,8,23,.86);
 z-index:5;text-align:center;padding:12px;
 border-radius:10px;
}
.hidden{display:none!important}
h1{
 font-size:clamp(26px,5vw,70px);margin:6px;
 color:#fff;text-shadow:0 0 18px #ef4444;
}
h2{font-size:clamp(16px,3vw,28px);color:#facc15}
p{margin:8px}
button{
 border:1px solid #fb923c;border-radius:10px;
 background:linear-gradient(120deg,#991b1b,#ef4444);
 color:white;font-weight:bold;padding:11px 18px;
 margin:5px;cursor:pointer;font-size:15px;
 touch-action:manipulation;
}
button.secondary{background:#24334f;border-color:#64748b}
.help{
 max-width:650px;width:96%;max-height:96%;
 overflow:auto;background:#111b32;border-radius:12px;
 padding:12px;line-height:1.5;
}
.helpgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
kbd{background:#34425e;padding:2px 5px;border-radius:4px}
#mobileControls{
 display:none;width:100%;max-width:1200px;
 margin:5px auto 0;gap:5px;justify-content:space-between;
 align-items:center;touch-action:none;user-select:none;
 -webkit-user-select:none;
}
.controlSide{
 display:flex;align-items:center;justify-content:center;
 gap:5px;min-width:0;flex:1;
}
.controlLabel{
 text-align:center;font-size:10px;
 font-weight:bold;margin-bottom:3px;
}
.pad{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 grid-template-rows:repeat(3,1fr);
 gap:2px;width:min(25vw,145px);
 aspect-ratio:1;
}
.controlBtn{
 display:flex;align-items:center;justify-content:center;
 background:rgba(55,72,105,.65);
 border:1px solid rgba(180,200,240,.4);
 border-radius:10px;color:white;
 font-size:clamp(11px,2.5vw,20px);
 font-weight:bold;touch-action:none;
 cursor:pointer;min-width:0;
}
.controlBtn.active{
 background:rgba(250,204,21,.7);
 border-color:#fff;transform:scale(.96);
}
.actions{
 display:grid;grid-template-columns:repeat(3,1fr);
 gap:4px;flex:1;max-width:210px;
}
.actionBtn{
 aspect-ratio:1;min-width:0;border-radius:50%;
 font-size:clamp(10px,2vw,14px);
 text-align:center;padding:2px;
}
.punch{background:rgba(37,99,235,.65)}
.kick{background:rgba(220,38,38,.65)}
.guard{background:rgba(22,163,74,.65)}
.utility{
 display:flex;justify-content:center;gap:5px;
 margin:5px auto;flex-wrap:wrap;
}
.utility button{font-size:12px;padding:7px 12px;margin:0}
#mobileControls.show{display:flex}
@media(max-width:650px){
 .panel{padding:5px}
 .help{font-size:11px}
 .help h2{margin:4px}
 .helpgrid{gap:3px}
 .panel button{padding:7px 10px;font-size:12px}
 .controlBtn{border-radius:6px}
 .controlSide{gap:3px}
 .actions{gap:2px}
}
</style>
</head>
<body>

<div id="gamebox">
<canvas id="arena" width="1200" height="650"></canvas>

<div id="menu" class="panel">
 <div style="color:#facc15;letter-spacing:3px">
 ULTIMATE ARCADE FIGHTING
 </div>
 <h1>IRON FIGHT 2</h1>
 <h2>FINAL SHOWDOWN</h2>
 <p>⚡ 두 전사의 마지막 결투 ⚡</p>
 <button onclick="startGame()">🥊 게임 시작</button>
 <button class="secondary" onclick="showHelp()">📖 조작법 / 설명</button>
 <p style="font-size:12px">3판 2선승 · PC / 모바일 지원</p>
</div>

<div id="helpPanel" class="panel hidden">
 <div class="help">
  <h2>📖 게임 조작법</h2>
  <div class="helpgrid">
   <div>
    <b style="color:#60a5fa">PLAYER 1</b>
    <p>W 점프 / A D 이동 / S 앉기</p>
    <p>SPACE 주먹 / C 발차기 / Q 방어</p>
   </div>
   <div>
    <b style="color:#fb7185">PLAYER 2</b>
    <p>U 점프 / H K 이동 / J 앉기</p>
    <p>P 주먹 / O 발차기 / I 방어</p>
   </div>
  </div>
  <p>📱 스마트폰에서는 화면 아래 조작 버튼 사용</p>
  <p>🥊 연속 공격으로 콤보를 쌓으세요.</p>
  <p>🛡️ 방어하면 피해가 감소합니다.</p>
  <p>🏆 먼저 2승을 달성하면 승리!</p>
  <p>R 재시작 / ESC 일시정지</p>
  <button onclick="backMenu()">돌아가기</button>
 </div>
</div>

<div id="pausePanel" class="panel hidden">
 <h1>PAUSED</h1>
 <button onclick="togglePause()">▶ 계속하기</button>
 <button class="secondary" onclick="backMenu()">메인 메뉴</button>
</div>

<div id="endPanel" class="panel hidden">
 <h1>CHAMPION!</h1>
 <h2 id="winnerText"></h2>
 <button onclick="startGame()">🔄 다시 대결</button>
 <button class="secondary" onclick="backMenu()">🏠 메인 메뉴</button>
</div>
</div>

<div id="mobileControls">
 <div style="flex:1;min-width:0">
  <div class="controlLabel" style="color:#60a5fa">PLAYER 1</div>
  <div class="controlSide">
   <div class="pad">
    <div></div>
    <div class="controlBtn" data-key="KeyW">▲</div>
    <div></div>
    <div class="controlBtn" data-key="KeyA">◀</div>
    <div class="controlBtn" data-key="KeyS">▼</div>
    <div class="controlBtn" data-key="KeyD">▶</div>
    <div></div><div></div><div></div>
   </div>
   <div class="actions">
    <div class="controlBtn actionBtn punch" data-key="Space">👊</div>
    <div class="controlBtn actionBtn kick" data-key="KeyC">🦶</div>
    <div class="controlBtn actionBtn guard" data-key="KeyQ">🛡️</div>
   </div>
  </div>
 </div>
 <div style="flex:1;min-width:0">
  <div class="controlLabel" style="color:#fb7185">PLAYER 2</div>
  <div class="controlSide">
   <div class="actions">
    <div class="controlBtn actionBtn punch" data-key="KeyP">👊</div>
    <div class="controlBtn actionBtn kick" data-key="KeyO">🦶</div>
    <div class="controlBtn actionBtn guard" data-key="KeyI">🛡️</div>
   </div>
   <div class="pad">
    <div></div>
    <div class="controlBtn" data-key="KeyU">▲</div>
    <div></div>
    <div class="controlBtn" data-key="KeyH">◀</div>
    <div class="controlBtn" data-key="KeyJ">▼</div>
    <div class="controlBtn" data-key="KeyK">▶</div>
    <div></div><div></div><div></div>
   </div>
  </div>
 </div>
</div>

<div class="utility">
 <button class="secondary" onclick="togglePause()">⏸️ 일시정지</button>
 <button class="secondary" onclick="startGame()">🔄 재시작</button>
 <button class="secondary" onclick="backMenu()">🏠 메뉴</button>
 <button class="secondary" onclick="toggleMobile()" id="controlToggle">
 📱 조작 버튼
 </button>
</div>

<script>
const canvas=document.getElementById("arena");
const ctx=canvas.getContext("2d");
const W=1200,H=650,FLOOR=540;
const keys={};
let audio=null;
let state="menu",round=1,wins=[0,0];
let p1,p2,timer=75,transition=0;
let banner="",bannerTime=0;
let particles=[],texts=[];
let worldTime=0,lastTime=0,shake=0,flash=0;
let slowmo=0,pausedFrom="fight";
let mobileVisible=false;
let pointerKeys=new Map();

function el(id){return document.getElementById(id)}
function hidePanels(){
 ["menu","helpPanel","pausePanel","endPanel"].forEach(
  id=>el(id).classList.add("hidden")
 );
}
function sound(freq,duration=.12,type="sawtooth",vol=.07){
 try{
  if(!audio)audio=new(window.AudioContext||window.webkitAudioContext)();
  if(audio.state==="suspended")audio.resume();
  let o=audio.createOscillator(),g=audio.createGain();
  o.type=type;
  o.frequency.setValueAtTime(freq,audio.currentTime);
  o.frequency.exponentialRampToValueAtTime(
   Math.max(40,freq*.4),audio.currentTime+duration
  );
  g.gain.setValueAtTime(vol,audio.currentTime);
  g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+duration);
  o.connect(g);g.connect(audio.destination);
  o.start();o.stop(audio.currentTime+duration);
 }catch(e){}
}
function fighter(x,color,accent,id){
 return {
  x,y:FLOOR,vx:0,vy:0,hp:100,
  color,accent,id,face:id===1?1:-1,
  attack:null,attackTimer:0,cooldown:0,
  hasHit:false,guard:false,crouch:false,
  stun:0,flash:0,walk:0,combo:0,comboTimer:0
 };
}
function resetRound(){
 p1=fighter(300,"#2563eb","#93c5fd",1);
 p2=fighter(900,"#dc2626","#fda4af",2);
 timer=75;
 particles=[];texts=[];
 state="fight";
 banner="ROUND "+round+" - FIGHT!";
 bannerTime=1.6;
}
function clearInputs(){
 for(let k in keys)delete keys[k];
 pointerKeys.clear();
 document.querySelectorAll(".controlBtn").forEach(
  b=>b.classList.remove("active")
 );
}
function startGame(){
 hidePanels();
 clearInputs();
 wins=[0,0];round=1;
 resetRound();
 sound(600,.25,"triangle");
}
function showHelp(){
 hidePanels();
 el("helpPanel").classList.remove("hidden");
 state="help";
}
function backMenu(){
 hidePanels();
 clearInputs();
 state="menu";
 el("menu").classList.remove("hidden");
}
function togglePause(){
 if(state==="fight"||state==="roundover"){
  pausedFrom=state;
  state="pause";
  el("pausePanel").classList.remove("hidden");
 }else if(state==="pause"){
  state=pausedFrom;
  el("pausePanel").classList.add("hidden");
 }
}
function toggleMobile(){
 mobileVisible=!mobileVisible;
 el("mobileControls").classList.toggle("show",mobileVisible);
 el("controlToggle").textContent=
  mobileVisible?"📱 버튼 숨기기":"📱 조작 버튼";
 clearInputs();
}
if(window.matchMedia("(pointer:coarse)").matches ||
   window.innerWidth<800){
 mobileVisible=true;
 el("mobileControls").classList.add("show");
 el("controlToggle").textContent="📱 버튼 숨기기";
}
function setInput(k,down){
 const was=!!keys[k];
 keys[k]=down;
 if(down&&!was&&state==="fight"){
  if(k==="Space")attack(p1,"punch");
  if(k==="KeyC")attack(p1,"kick");
  if(k==="KeyP")attack(p2,"punch");
  if(k==="KeyO")attack(p2,"kick");
 }
}
window.addEventListener("keydown",e=>{
 if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"]
 .includes(e.code))e.preventDefault();
 if(e.code==="KeyR"&&!e.repeat){startGame();return}
 if(e.code==="Escape"&&!e.repeat){togglePause();return}
 setInput(e.code,true);
});
window.addEventListener("keyup",e=>setInput(e.code,false));
window.addEventListener("blur",clearInputs);

document.querySelectorAll("[data-key]").forEach(btn=>{
 btn.addEventListener("pointerdown",e=>{
  e.preventDefault();
  btn.setPointerCapture(e.pointerId);
  pointerKeys.set(e.pointerId,btn.dataset.key);
  btn.classList.add("active");
  setInput(btn.dataset.key,true);
 });
 function release(e){
  e.preventDefault();
  const k=pointerKeys.get(e.pointerId);
  if(!k)return;
  pointerKeys.delete(e.pointerId);
  btn.classList.remove("active");
  if(![...pointerKeys.values()].includes(k))setInput(k,false);
 }
 btn.addEventListener("pointerup",release);
 btn.addEventListener("pointercancel",release);
 btn.addEventListener("lostpointercapture",release);
});

function attack(p,type){
 if(!p||state!=="fight"||p.cooldown>0||
    p.stun>0||p.attack||p.guard)return;
 p.attack=type;
 p.attackTimer=type==="punch"?.25:.39;
 p.cooldown=type==="punch"?.34:.55;
 p.hasHit=false;
 sound(type==="punch"?200:130,.10);
}
function spark(x,y,color,n=16){
 for(let i=0;i<n;i++){
  let a=Math.random()*Math.PI*2;
  let s=80+Math.random()*300;
  particles.push({
   x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,
   life:.25+Math.random()*.3,
   color,size:2+Math.random()*6
  });
 }
}
function floating(text,x,y,color){
 texts.push({text,x,y,life:.85,color});
}
function hit(a,b){
 if(!a.attack||a.hasHit)return;
 const reach=a.attack==="kick"?120:90;
 const dist=Math.abs(a.x-b.x);
 const facing=(b.x-a.x)*a.face>0;
 const vertical=Math.abs(a.y-b.y)<115;
 if(dist>reach||!facing||!vertical)return;
 a.hasHit=true;
 const blocked=b.guard&&b.face===-a.face;
 let damage=a.attack==="kick"?15:9;
 if(blocked)damage=Math.max(1,Math.floor(damage*.2));
 b.hp=Math.max(0,b.hp-damage);
 b.stun=blocked?.10:.23;
 b.flash=.14;
 b.vx=a.face*(blocked?90:270);
 shake=blocked?3:10;
 flash=blocked?.02:.08;
 spark((a.x+b.x)/2,Math.min(a.y,b.y)-110,
  blocked?"#7dd3fc":"#facc15",blocked?8:22);
 sound(blocked?440:90,blocked?.09:.20);
 if(blocked){
  floating("BLOCK!",b.x,b.y-190,"#7dd3fc");
 }else{
  a.combo=a.comboTimer>0?a.combo+1:1;
  a.comboTimer=1.2;
  floating("-"+damage,b.x,b.y-190,"#facc15");
  if(a.combo>=2){
   floating(a.combo+" HIT COMBO!",a.x,a.y-230,"#fb923c");
  }
 }
 if(b.hp<=0)endRound(a.id);
}
function endRound(winner){
 if(state!=="fight")return;
 state="roundover";
 transition=2.6;
 slowmo=.35;
 if(winner){
  wins[winner-1]++;
  banner="PLAYER "+winner+" K.O.!";
  sound(100,.6);
  if(wins[winner-1]>=2){
   state="gameover";
   transition=2.8;
   el("winnerText").textContent="PLAYER "+winner+" 승리!";
  }
 }else{
  banner="DRAW!";
 }
 bannerTime=3;
}
function updatePlayer(p,other,dt,c){
 p.cooldown=Math.max(0,p.cooldown-dt);
 p.stun=Math.max(0,p.stun-dt);
 p.flash=Math.max(0,p.flash-dt);
 p.comboTimer=Math.max(0,p.comboTimer-dt);
 if(p.comboTimer===0)p.combo=0;
 if(p.attack){
  p.attackTimer-=dt;
  if(p.attackTimer<=0)p.attack=null;
 }
 p.face=other.x>=p.x?1:-1;
 p.guard=!!keys[c.guard]&&p.stun===0&&!p.attack;
 p.crouch=!!keys[c.down]&&p.stun===0&&!p.attack;
 let move=0;
 if(p.stun===0&&!p.guard&&!p.attack){
  if(keys[c.left])move--;
  if(keys[c.right])move++;
 }
 if(p.stun===0)p.vx=move*(p.crouch?100:260);
 else p.vx*=Math.max(0,1-5*dt);
 p.x+=p.vx*dt;
 p.x=Math.max(50,Math.min(W-50,p.x));
 if(move)p.walk+=dt*13;
 if(keys[c.up]&&p.y>=FLOOR&&p.stun===0&&!p.guard){
  p.vy=-670;
  sound(330,.08,"sine",.03);
 }
 p.vy+=1700*dt;
 p.y+=p.vy*dt;
 if(p.y>FLOOR){p.y=FLOOR;p.vy=0}
}
function update(dt){
 worldTime+=dt;
 shake*=Math.max(0,1-12*dt);
 flash=Math.max(0,flash-dt);
 bannerTime=Math.max(0,bannerTime-dt);
 for(let i=particles.length-1;i>=0;i--){
  let p=particles[i];
  p.x+=p.vx*dt;p.y+=p.vy*dt;
  p.vy+=350*dt;p.life-=dt;
  if(p.life<=0)particles.splice(i,1);
 }
 for(let i=texts.length-1;i>=0;i--){
  texts[i].y-=40*dt;
  texts[i].life-=dt;
  if(texts[i].life<=0)texts.splice(i,1);
 }
 if(state==="roundover"||state==="gameover"){
  transition-=dt;
  if(transition<=0){
   if(state==="gameover"){
    state="finished";
    el("endPanel").classList.remove("hidden");
   }else{
    round++;
    resetRound();
   }
  }
  return;
 }
 if(state!=="fight")return;
 timer-=dt;
 if(timer<=0){
  timer=0;
  endRound(p1.hp===p2.hp?0:p1.hp>p2.hp?1:2);
  return;
 }
 updatePlayer(p1,p2,dt,{
  left:"KeyA",right:"KeyD",up:"KeyW",
  down:"KeyS",guard:"KeyQ"
 });
 updatePlayer(p2,p1,dt,{
  left:"KeyH",right:"KeyK",up:"KeyU",
  down:"KeyJ",guard:"KeyI"
 });
 const dx=p2.x-p1.x;
 if(Math.abs(dx)<65){
  const push=(65-Math.abs(dx))/2;
  const dir=dx>=0?1:-1;
  p1.x=Math.max(50,p1.x-dir*push);
  p2.x=Math.min(W-50,p2.x+dir*push);
 }
 if(p1.attack&&p1.attackTimer<
    (p1.attack==="punch"?.19:.29))hit(p1,p2);
 if(p2.attack&&p2.attackTimer<
    (p2.attack==="punch"?.19:.29))hit(p2,p1);
}
function rect(x,y,w,h,c){
 ctx.fillStyle=c;ctx.fillRect(x,y,w,h);
}
function line(x,y,x2,y2,w,c){
 ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x2,y2);
 ctx.strokeStyle=c;ctx.lineWidth=w;ctx.lineCap="round";ctx.stroke();
}
function circle(x,y,r,c){
 ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);
 ctx.fillStyle=c;ctx.fill();
}
function background(){
 let g=ctx.createLinearGradient(0,0,0,H);
 g.addColorStop(0,"#090d25");
 g.addColorStop(.6,"#402052");
 g.addColorStop(1,"#e16b62");
 rect(0,0,W,H,g);
 circle(890,160,85,"#fca5a5");
 circle(890,160,69,"#ffdbb0");
 for(let i=0;i<22;i++){
  let x=i*60,h=120+(i*57%170);
  rect(x,450-h,55,h+30,"#12172e");
  for(let y=460-h;y<440;y+=25){
   for(let xx=x+10;xx<x+50;xx+=18){
    if((i+y+xx)%5!==0)rect(xx,y,7,12,"#e9a96b");
   }
  }
 }
 rect(0,450,W,200,"#22253d");
 rect(0,450,W,9,"#ec4899");
 for(let i=0;i<=12;i++)
  line(W/2,450,i*110,650,1.5,"#565273");
 for(let y=480;y<650;y+=37)
  line(0,y,W,y,1,"#514b70");
}
function drawFighter(p){
 ctx.save();
 ctx.translate(p.x,p.y);
 let jump=FLOOR-p.y;
 ctx.globalAlpha=.3;
 ctx.beginPath();
 ctx.ellipse(0,jump+3,Math.max(18,48-jump*.1),10,
  0,0,Math.PI*2);
 ctx.fillStyle="#000";ctx.fill();
 ctx.globalAlpha=1;
 let crouch=p.crouch?28:0;
 let step=Math.sin(p.walk)*10;
 let color=p.flash>0?"white":p.color;
 line(-13,-70+crouch,-24+step,0,21,"#182238");
 line(13,-70+crouch,25-step,0,21,"#182238");
 line(-24+step,0,-42+step,0,13,p.accent);
 line(25-step,0,42-step,0,13,p.accent);
 ctx.fillStyle=color;
 ctx.beginPath();
 ctx.roundRect(-28,-148+crouch,56,82,12);
 ctx.fill();
 rect(-28,-85+crouch,56,12,"#0f172a");
 rect(-7,-86+crouch,14,14,"#facc15");
 circle(0,-176+crouch,27,"#e9ad84");
 ctx.fillStyle="#151827";
 ctx.beginPath();
 ctx.arc(0,-185+crouch,27,Math.PI,0);
 ctx.fill();
 circle(p.face*12,-176+crouch,3,"#111827");
 line(-p.face*18,-128+crouch,
      -p.face*40,-100+crouch,18,color);
 if(p.guard){
  line(p.face*19,-130+crouch,
       p.face*27,-172+crouch,19,p.accent);
  circle(p.face*27,-172+crouch,12,"#facc15");
  ctx.strokeStyle="#7dd3fc";
  ctx.lineWidth=5;
  ctx.globalAlpha=.6;
  ctx.beginPath();
  ctx.arc(p.face*28,-115+crouch,72,
   -Math.PI/2,Math.PI/2,p.face<0);
  ctx.stroke();
  ctx.globalAlpha=1;
 }else if(p.attack==="punch"){
  line(p.face*19,-130+crouch,
       p.face*94,-130+crouch,20,p.accent);
  circle(p.face*96,-130+crouch,13,"#f8fafc");
 }else{
  line(p.face*19,-130+crouch,
       p.face*43,-105+crouch,18,p.accent);
  circle(p.face*43,-105+crouch,12,"#f8fafc");
 }
 if(p.attack==="kick"){
  line(p.face*12,-69+crouch,
       p.face*112,-88+crouch,23,"#182238");
  circle(p.face*116,-88+crouch,13,p.accent);
 }
 ctx.restore();
}
function hud(){
 rect(0,0,W,110,"rgba(4,8,23,.9)");
 ctx.textAlign="left";
 ctx.font="bold 23px Arial";
 ctx.fillStyle="#93c5fd";ctx.fillText("PLAYER 1",45,32);
 ctx.textAlign="right";
 ctx.fillStyle="#fda4af";ctx.fillText("PLAYER 2",1155,32);
 rect(45,45,445,28,"#4b2535");
 rect(710,45,445,28,"#4b2535");
 rect(45,45,445*p1.hp/100,28,"#38bdf8");
 let w=445*p2.hp/100;
 rect(1155-w,45,w,28,"#fb4f67");
 ctx.strokeStyle="#fff";ctx.lineWidth=2;
 ctx.strokeRect(45,45,445,28);
 ctx.strokeRect(710,45,445,28);
 ctx.textAlign="center";
 ctx.font="bold 37px Arial";
 ctx.fillStyle="white";
 ctx.fillText(Math.ceil(timer),600,70);
 ctx.font="bold 17px Arial";
 ctx.fillText("ROUND "+round,600,95);
 for(let i=0;i<2;i++){
  circle(58+i*30,94,10,i<wins[0]?"#38bdf8":"#41445d");
  circle(1142-i*30,94,10,i<wins[1]?"#fb7185":"#41445d");
 }
}
function drawMenuAction(){
 let t=worldTime;
 let a=fighter(370+Math.sin(t*1.8)*65,
  "#2563eb","#93c5fd",1);
 let b=fighter(830-Math.sin(t*1.8)*65,
  "#dc2626","#fda4af",2);
 a.walk=t*12;b.walk=t*12;
 if(Math.sin(t*3)>0.55)a.attack="punch";
 if(Math.sin(t*3)<-0.55)b.attack="kick";
 drawFighter(a);drawFighter(b);
 if(Math.abs(Math.sin(t*3))>.95){
  sparkVisual(600,350);
 }
}
function sparkVisual(x,y){
 for(let i=0;i<6;i++){
  let a=i*Math.PI/3+worldTime;
  line(x,y,x+Math.cos(a)*35,y+Math.sin(a)*35,
   3,"#facc15");
 }
}
function draw(){
 ctx.save();
 ctx.translate((Math.random()-.5)*shake,
               (Math.random()-.5)*shake);
 background();
 if(state==="menu"||state==="help"){
  drawMenuAction();
 }else{
  if(p1&&p2){
   drawFighter(p1);drawFighter(p2);
  }
 }
 for(let p of particles){
  ctx.globalAlpha=Math.max(0,p.life/.55);
  circle(p.x,p.y,p.size,p.color);
 }
 ctx.globalAlpha=1;
 ctx.restore();
 if(state!=="menu"&&state!=="help"&&p1&&p2)hud();
 for(let t of texts){
  ctx.globalAlpha=Math.max(0,t.life/.85);
  ctx.textAlign="center";
  ctx.font="bold 27px Arial";
  ctx.fillStyle=t.color;
  ctx.fillText(t.text,t.x,t.y);
 }
 ctx.globalAlpha=1;
 if(bannerTime>0&&state!=="menu"&&state!=="help"){
  ctx.textAlign="center";
  ctx.font="900 53px Arial";
  ctx.lineWidth=7;
  ctx.strokeStyle="#101426";
  ctx.strokeText(banner,600,260);
  ctx.fillStyle="#facc15";
  ctx.fillText(banner,600,260);
 }
 if(flash>0){
  ctx.globalAlpha=flash*2;
  rect(0,0,W,H,"white");
  ctx.globalAlpha=1;
 }
}
function loop(time){
 if(!lastTime)lastTime=time;
 let dt=Math.min((time-lastTime)/1000,.04);
 lastTime=time;
 if(state!=="pause"&&state!=="finished"){
  update(dt);
 }
 draw();
 requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

components.html(game, height=900, scrolling=True)
