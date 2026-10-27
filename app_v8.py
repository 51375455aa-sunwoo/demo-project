
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FIGHT ARENA", page_icon="⚔️", layout="wide")

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}
.stApp{background:#090d17;color:#fff}
.block-container{max-width:1200px;padding:1rem 1rem}
div.stButton>button{
 width:100%;height:3em;border-radius:12px;font-weight:800;
 background:#202b42;color:white;border:1px solid #475675
}
</style>
""", unsafe_allow_html=True)

CHARACTERS = {
 "파이어":{"emoji":"🔥","color":"#ff4c36","hp":100,"speed":5.1,"damage":12,"skill":"인페르노 버스트","type":"projectile"},
 "썬더":{"emoji":"⚡","color":"#ffe15b","hp":92,"speed":6.0,"damage":10,"skill":"라이트닝 러시","type":"combo"},
 "섀도우":{"emoji":"🌑","color":"#b48aff","hp":94,"speed":5.8,"damage":11,"skill":"섀도우 블링크","type":"teleport"},
 "탱커":{"emoji":"🛡️","color":"#94a7bd","hp":135,"speed":3.8,"damage":16,"skill":"메테오 스매시","type":"heavy"},
 "아이스":{"emoji":"❄️","color":"#62ddff","hp":100,"speed":4.8,"damage":11,"skill":"프로즌 랜스","type":"projectile"},
 "윈드":{"emoji":"🌪️","color":"#70f5c0","hp":94,"speed":6.5,"damage":9,"skill":"토네이도 킥","type":"combo"},
 "드래곤":{"emoji":"🐉","color":"#ff9e48","hp":108,"speed":4.7,"damage":14,"skill":"드래곤 브레스","type":"projectile"},
 "복서":{"emoji":"🥊","color":"#ff76a5","hp":100,"speed":5.5,"damage":10,"skill":"인파이터 러시","type":"combo"},
 "닌자":{"emoji":"🥷","color":"#7d8cff","hp":88,"speed":6.7,"damage":10,"skill":"환영 베기","type":"teleport"},
 "사무라이":{"emoji":"⚔️","color":"#ff626d","hp":103,"speed":4.8,"damage":15,"skill":"일섬","type":"heavy"},
 "사이보그":{"emoji":"🤖","color":"#67e5df","hp":108,"speed":4.6,"damage":12,"skill":"플라즈마 캐논","type":"projectile"},
 "독술사":{"emoji":"☠️","color":"#b9f45d","hp":95,"speed":5.0,"damage":11,"skill":"베놈 스톰","type":"projectile"},
 "빛의 기사":{"emoji":"✨","color":"#fff1a6","hp":110,"speed":4.7,"damage":13,"skill":"홀리 슬래시","type":"heavy"},
 "마그마":{"emoji":"🌋","color":"#ff793d","hp":112,"speed":4.2,"damage":14,"skill":"라바 웨이브","type":"projectile"},
 "팬텀":{"emoji":"👻","color":"#c2c8ff","hp":90,"speed":6.1,"damage":10,"skill":"팬텀 스텝","type":"teleport"},
 "무도가":{"emoji":"🐯","color":"#f5c16c","hp":103,"speed":5.4,"damage":12,"skill":"호랑이 연격","type":"combo"},
}

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("""
    <div style="text-align:center;padding:24px 0 12px">
    <div style="font-size:14px;letter-spacing:7px;color:#8fa8d9">ULTIMATE FIGHTING GAME</div>
    <div style="font-size:clamp(36px,7vw,68px);font-weight:1000;
    font-style:italic;letter-spacing:2px;
    background:linear-gradient(90deg,#fff,#70a9ff,#ff637d);
    -webkit-background-clip:text;color:transparent">FIGHT ARENA</div>
    <div style="color:#a4b0c8">CHOOSE YOUR FIGHTER · BEST OF THREE</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        mode = st.radio("게임 모드", ["컴퓨터 대전", "2인용 대전"], horizontal=True)
        p1 = st.selectbox("🔴 PLAYER 1 캐릭터", list(CHARACTERS), index=0)
    with right:
        difficulty = st.selectbox("CPU 난이도", ["쉬움", "보통", "어려움"],
                                  disabled=mode == "2인용 대전")
        p2 = st.selectbox("🔵 PLAYER 2 캐릭터", list(CHARACTERS), index=8)

    st.markdown("### 전투 캐릭터")
    cards = st.columns(4)
    for i, (name, c) in enumerate(CHARACTERS.items()):
        with cards[i % 4]:
            st.markdown(f"""
            <div style="margin-bottom:10px;padding:12px;min-height:125px;
            border-radius:13px;border:1px solid {c['color']}66;
            background:linear-gradient(145deg,#1a2438,#101522)">
            <div style="font-size:28px">{c['emoji']}</div>
            <b style="color:{c['color']}">{name}</b>
            <div style="font-size:12px;color:#b7c3d9;margin-top:5px">{c['skill']}</div>
            <div style="font-size:11px;color:#7e8ca7;margin-top:5px">
            체력 {c['hp']} · 공격력 {c['damage']}
            </div></div>""", unsafe_allow_html=True)

    st.markdown("### 조작 방법")
    a, b = st.columns(2)
    with a:
        st.markdown("**🔴 1P**")
        st.caption("이동 A/D · 점프 W · 앉기 S · 방어 Q · 공격 Space · 필살기 C")
    with b:
        st.markdown("**🔵 2P**")
        st.caption("이동 H/K · 점프 U · 앉기 J · 방어 I · 공격 P · 필살기 O")

    if st.button("⚔️ 전투 시작", type="primary", use_container_width=True):
        st.session_state.settings = {
            "mode": mode, "difficulty": difficulty,
            "p1": p1, "p2": p2, "characters": CHARACTERS
        }
        st.session_state.started = True
        st.rerun()

else:
    if st.button("← 캐릭터 선택"):
        st.session_state.started = False
        st.rerun()

    settings_json = json.dumps(st.session_state.settings, ensure_ascii=False)

    html = r"""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;background:#090d17;color:white;font-family:Arial,sans-serif;overflow:hidden;user-select:none}
#hud{display:grid;grid-template-columns:1fr 105px 1fr;gap:8px;align-items:center;
padding:9px;background:linear-gradient(135deg,#1b263c,#101522);
border:1px solid #303d59;border-radius:12px;margin-bottom:8px}
.pname{font-weight:900;font-size:clamp(12px,2vw,17px);margin-bottom:5px}
.bar{height:14px;border-radius:4px;background:#353d51;overflow:hidden;border:1px solid #ffffff22}
.fill{height:100%;width:100%;transition:width .1s}
#middle{text-align:center}
#round{font-size:11px;color:#b8c7e6;font-weight:bold}
#score{font-size:23px;font-weight:1000}
#timer{font-size:12px;color:#ffdd8a}
#arena{width:100%;display:block;border-radius:12px;border:1px solid #34425e;
background:#111827;touch-action:none}
#notice{text-align:center;min-height:27px;padding:6px;font-size:15px;font-weight:900;color:#ffe5a5}
#pcHelp{font-size:11px;color:#9eabc4;text-align:center;padding:3px}
#mobile{display:none;justify-content:space-between;align-items:end;gap:8px;
padding:4px 0 3px;touch-action:none}
.side{display:flex;align-items:center;gap:8px}
#joy{
width:118px;height:118px;border-radius:50%;position:relative;flex-shrink:0;
background:radial-gradient(circle,#293852 0%,#182338 65%,#0e1524 100%);
border:2px solid #65799d;box-shadow:inset 0 0 18px #0009,0 4px 16px #0007;
touch-action:none
}
#joyknob{position:absolute;left:34px;top:34px;width:48px;height:48px;border-radius:50%;
background:linear-gradient(145deg,#9eb8e9,#465f88);
border:2px solid #d5e4ff;box-shadow:0 3px 10px #0008;pointer-events:none}
.actions{display:grid;grid-template-columns:repeat(2,53px);gap:7px}
.act{width:53px;height:48px;border-radius:15px;border:1px solid #ffffff55;
color:white;font-size:11px;font-weight:900;box-shadow:0 3px 0 #0008;
touch-action:none;background:linear-gradient(145deg,#3d4e6c,#1c263b)}
.act:active{filter:brightness(1.5);transform:translateY(2px)}
.red{background:linear-gradient(145deg,#ed5c60,#852d42)}
.blue{background:linear-gradient(145deg,#5f9dff,#284b9b)}
.purple{background:linear-gradient(145deg,#bc78ff,#6336a0)}
.gold{background:linear-gradient(145deg,#ffd66e,#a96521)}
@media(max-width:700px){
 body{padding-bottom:2px}
 #hud{padding:7px 6px;grid-template-columns:1fr 75px 1fr;gap:5px}
 .bar{height:11px}#score{font-size:20px}
 #mobile{display:flex}
 #pcHelp{display:none}
 #arena{max-height:43vh}
 #joy{width:100px;height:100px}
 #joyknob{left:27px;top:27px;width:42px;height:42px}
 .side{gap:6px}
 .actions{grid-template-columns:repeat(2,47px);gap:6px}
 .act{width:47px;height:43px;border-radius:13px;font-size:10px}
 #notice{font-size:13px;min-height:24px;padding:4px}
}
@media(max-width:380px){
 #joy{width:84px;height:84px}
 #joyknob{left:22px;top:22px;width:36px;height:36px}
 .actions{grid-template-columns:repeat(2,42px);gap:5px}
 .act{width:42px;height:40px;font-size:9px}
}
</style></head><body>
<div id="hud">
 <div>
  <div id="n1" class="pname">PLAYER 1</div>
  <div class="bar"><div id="h1" class="fill" style="background:linear-gradient(90deg,#ff334f,#ff8874)"></div></div>
 </div>
 <div id="middle"><div id="round">ROUND 1</div><div id="score">0 : 0</div><div id="timer">60 SEC</div></div>
 <div style="text-align:right">
  <div id="n2" class="pname">PLAYER 2</div>
  <div class="bar"><div id="h2" class="fill" style="float:right;background:linear-gradient(90deg,#48b8ff,#8ce7ff)"></div></div>
 </div>
</div>
<canvas id="arena" width="960" height="500"></canvas>
<div id="notice">READY? FIGHT!</div>
<div id="pcHelp">1P: A/D · W 점프 · Q 방어 · SPACE 공격 · C 필살기　 |　 2P: H/K · U 점프 · I 방어 · P 공격 · O 필살기</div>
<div id="mobile">
 <div class="side">
  <div id="joy"><div id="joyknob"></div></div>
 </div>
 <div class="side">
  <div class="actions">
   <button class="act red" data-action="attack">공격</button>
   <button class="act purple" data-action="special">필살기</button>
   <button class="act blue" data-action="guard">방어</button>
   <button class="act" data-action="jump">점프</button>
  </div>
 </div>
</div>

<script>
const CFG=__CONFIG__;
const C=CFG.characters;
const canvas=document.getElementById("arena"),ctx=canvas.getContext("2d");
const W=960,H=500,FLOOR=410;
const keys={};
const touch={x:0,y:0,guard:false,attack:false,special:false,jump:false};
const isCPU=CFG.mode==="컴퓨터 대전";
const difficulty={"쉬움":.45,"보통":.72,"어려움":.95}[CFG.difficulty]||.72;
let score1=0,score2=0,round=1,timeLeft=60,ended=false,waiting=0;
let particles=[],shots=[],shake=0,screenFlash=0;
let last=performance.now();

function fighter(name,x,dir,id){
 const c=C[name];
 return {name,x,y:FLOOR,dir,hp:c.hp,maxHp:c.hp,color:c.color,emoji:c.emoji,
 speed:c.speed,damage:c.damage,skill:c.skill,type:c.type,id,
 vx:0,vy:0,air:false,guard:false,crouch:false,attack:0,attackCd:0,
 specialCd:0,stun:0,flash:0,walk:0,skillTime:0,combo:0};
}
let p1=fighter(CFG.p1,235,1,1),p2=fighter(CFG.p2,725,-1,2);
document.getElementById("n1").textContent=p1.emoji+" "+p1.name;
document.getElementById("n2").textContent=p2.emoji+" "+p2.name;

function resetRound(){
 p1=fighter(CFG.p1,235,1,1);p2=fighter(CFG.p2,725,-1,2);
 timeLeft=60;ended=false;waiting=0;particles=[];shots=[];
 touch.x=touch.y=0;touch.guard=touch.attack=touch.special=touch.jump=false;
 document.getElementById("notice").textContent="ROUND "+round+" · FIGHT!";
}
function restartMatch(){
 score1=0;score2=0;round=1;resetRound();
}
window.addEventListener("keydown",e=>{
 const k=e.key.toLowerCase();
 if([" ","arrowleft","arrowright","arrowup","arrowdown"].includes(k))e.preventDefault();
 if(!keys[k]){
  keys[k]=true;
  if(k==="r"&&ended){
   if(score1>=2||score2>=2)restartMatch();
   else {round++;resetRound();}
  }
 }
});
window.addEventListener("keyup",e=>keys[e.key.toLowerCase()]=false);
window.addEventListener("blur",()=>{for(const k in keys)keys[k]=false;});

const joy=document.getElementById("joy"),knob=document.getElementById("joyknob");
let joyPointer=null;
function joystickMove(e){
 const r=joy.getBoundingClientRect();
 let dx=e.clientX-(r.left+r.width/2),dy=e.clientY-(r.top+r.height/2);
 const max=r.width*.32,len=Math.hypot(dx,dy);
 if(len>max){dx=dx/len*max;dy=dy/len*max;}
 touch.x=dx/max;touch.y=dy/max;
 const ksize=knob.offsetWidth;
 knob.style.left=(r.width/2-ksize/2+dx)+"px";
 knob.style.top=(r.height/2-ksize/2+dy)+"px";
}
function resetJoy(){
 touch.x=0;touch.y=0;joyPointer=null;
 knob.style.left=(joy.clientWidth-knob.offsetWidth)/2+"px";
 knob.style.top=(joy.clientHeight-knob.offsetHeight)/2+"px";
}
joy.addEventListener("pointerdown",e=>{
 e.preventDefault();joyPointer=e.pointerId;joy.setPointerCapture(e.pointerId);joystickMove(e);
});
joy.addEventListener("pointermove",e=>{if(e.pointerId===joyPointer)joystickMove(e);});
joy.addEventListener("pointerup",resetJoy);
joy.addEventListener("pointercancel",resetJoy);
document.querySelectorAll("[data-action]").forEach(btn=>{
 const a=btn.dataset.action;
 btn.addEventListener("pointerdown",e=>{
  e.preventDefault();btn.setPointerCapture(e.pointerId);touch[a]=true;
 });
 const up=e=>{e.preventDefault();touch[a]=false;};
 btn.addEventListener("pointerup",up);
 btn.addEventListener("pointercancel",up);
 btn.addEventListener("lostpointercapture",up);
});

function sound(freq=150,dur=.08,wave="square"){
 try{
  const ac=new (window.AudioContext||window.webkitAudioContext)();
  const o=ac.createOscillator(),g=ac.createGain();
  o.type=wave;o.frequency.setValueAtTime(freq,ac.currentTime);
  g.gain.setValueAtTime(.04,ac.currentTime);
  g.gain.exponentialRampToValueAtTime(.001,ac.currentTime+dur);
  o.connect(g);g.connect(ac.destination);o.start();o.stop(ac.currentTime+dur);
  o.onended=()=>ac.close();
 }catch(e){}
}
function burst(x,y,color,count=12,power=7){
 for(let i=0;i<count;i++){
  const ang=Math.random()*Math.PI*2,spd=Math.random()*power;
  particles.push({x,y,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd,
   life:20+Math.random()*24,max:44,color,size:2+Math.random()*5});
 }
}
function impact(target,damage,knock,attacker,heavy=false){
 if(target.guard){
  damage*=.17;knock*=.2;burst(target.x,target.y-55,"#9eeaff",6,3);
  sound(340,.05,"sine");
 }else{
  target.stun=heavy?24:12;target.flash=8;
  target.vy=heavy?-8:-3;target.air=heavy;
  shake=heavy?12:5;screenFlash=heavy?.18:.07;
  burst(target.x,target.y-55,attacker.color,heavy?24:11,heavy?11:6);
  sound(heavy?75:145,heavy?.18:.07);
 }
 target.hp=Math.max(0,target.hp-damage);
 target.x+=attacker.dir*knock;
 target.x=Math.max(35,Math.min(W-35,target.x));
}
function melee(a,b,heavy=false){
 if(a.attackCd>0||a.stun>0||ended)return;
 a.attackCd=heavy?42:20;a.attack=heavy?22:12;
 a.skillTime=heavy?20:0;
 const distance=Math.abs(a.x-b.x);
 const reach=heavy?145:104;
 if(distance<reach&&Math.abs(a.y-b.y)<105){
  impact(b,a.damage*(heavy?2:1),heavy?105:33,a,heavy);
  if(!heavy&&(a.type==="combo")){
   a.combo++;
   if(a.combo%2===0)setTimeout(()=>{
    if(!ended&&b.hp>0&&Math.abs(a.x-b.x)<155)impact(b,a.damage*.65,35,a,false);
   },90);
  }
 }else burst(a.x+a.dir*55,a.y-58,a.color,3,2);
}
function special(a,b){
 if(a.specialCd>0||a.stun>0||ended)return;
 a.specialCd=250;a.attack=30;a.skillTime=32;
 document.getElementById("notice").textContent=a.emoji+" "+a.skill+"!";
 sound(270,.2,"sawtooth");
 if(a.type==="teleport"){
  const old=a.x;
  burst(old,a.y-55,a.color,15,5);
  a.x=Math.max(55,Math.min(W-55,b.x-a.dir*75));
  a.dir=b.x>a.x?1:-1;
  burst(a.x,a.y-55,a.color,18,7);
  setTimeout(()=>{if(!ended&&b.hp>0)impact(b,a.damage*2.25,125,a,true);},100);
 }else if(a.type==="combo"){
  for(let i=0;i<4;i++)setTimeout(()=>{
   if(!ended&&b.hp>0&&Math.abs(a.x-b.x)<190)impact(b,a.damage*.72,30,a,false);
   burst(a.x+a.dir*45,a.y-55,a.color,4,3);
  },i*100);
  a.vy=-7;a.air=true;
 }else{
  const specialColor=a.name==="아이스"?"#a7f2ff":a.name==="독술사"?"#b9f45d":
   a.name==="마그마"?"#ff692f":a.color;
  shots.push({x:a.x+a.dir*40,y:a.y-62,dir:a.dir,owner:a,color:specialColor,
   damage:a.damage*2.2,life:100,speed:a.name==="탱커"?7:10,
   size:a.name==="탱커"?26:17,type:a.name});
 }
 setTimeout(()=>{if(!ended)document.getElementById("notice").textContent="";},800);
}
function input(a,b){
 const left=a.id===1?"a":"h",right=a.id===1?"d":"k";
 const jump=a.id===1?"w":"u",guard=a.id===1?"q":"i";
 const crouch=a.id===1?"s":"j",attack=a.id===1?" ":"p";
 const sk=a.id===1?"c":"o";
 let dx=0;
 if(a.id===1){dx=(keys[right]?1:0)-(keys[left]?1:0);}
 else {dx=(keys[right]?1:0)-(keys[left]?1:0);}
 if(a.id===1){
  if(Math.abs(touch.x)>.16)dx=touch.x;
  a.guard=!!keys[guard]||touch.guard;
  a.crouch=!!keys[crouch]||touch.y>.65;
 }else{
  a.guard=!!keys[guard];a.crouch=!!keys[crouch];
 }
 if(a.stun>0)return;
 if(!a.guard){a.x+=dx*a.speed;a.walk+=Math.abs(dx)*2;}
 if((keys[jump]||(a.id===1&&touch.jump))&&!a.air&&a.y>=FLOOR){
  a.vy=-12;a.air=true;sound(300,.05,"sine");
 }
 if(keys[attack]||(a.id===1&&touch.attack))melee(a,b,false);
 if(keys[sk]||(a.id===1&&touch.special))special(a,b);
}
let aiClock=0;
function cpuInput(a,b,dt){
 aiClock-=dt;a.guard=false;
 if(a.stun>0)return;
 const d=Math.abs(a.x-b.x),dir=b.x>a.x?1:-1;a.dir=dir;
 if(aiClock<=0){
  aiClock=10+Math.random()*15;
  if(b.attack>0&&d<150&&Math.random()<difficulty)a.guard=true;
  else if(d<130)melee(a,b,Math.random()<.28);
  if(Math.random()<.08+difficulty*.16)special(a,b);
  if(Math.random()<.1)a.vy=-11;
 }
 if(d>120)a.x+=dir*a.speed*(.7+difficulty*.55)*2.4;
}
function updateFighter(a,dt){
 a.attackCd=Math.max(0,a.attackCd-dt);a.specialCd=Math.max(0,a.specialCd-dt);
 a.stun=Math.max(0,a.stun-dt);a.flash=Math.max(0,a.flash-dt);
 a.attack=Math.max(0,a.attack-dt);a.skillTime=Math.max(0,a.skillTime-dt);
 a.vy+=.58*dt;a.y+=a.vy*dt;
 if(a.y>=FLOOR){a.y=FLOOR;a.vy=0;a.air=false;}
 a.x=Math.max(35,Math.min(W-35,a.x));
}
function finish(winner){
 if(ended)return;
 ended=true;
 if(winner===1)score1++;else score2++;
 const matchOver=score1>=2||score2>=2;
 document.getElementById("notice").textContent=
  (winner===1?p1.emoji+" "+p1.name:p2.emoji+" "+p2.name)+
  (matchOver?" · MATCH WINNER!":" · ROUND WIN!");
 waiting=matchOver?-1:100;
}
function update(dt){
 if(ended){
  if(waiting>0){waiting-=dt*60;if(waiting<=0){round++;resetRound();}}
  return;
 }
 timeLeft-=dt;
 if(timeLeft<=0){finish(p1.hp>=p2.hp?1:2);return;}
 if(isCPU)cpuInput(p2,p1,dt*60);
 else input(p2,p1);
 input(p1,p2);
 p1.dir=p1.x<p2.x?1:-1;p2.dir=-p1.dir;
 updateFighter(p1,dt*60);updateFighter(p2,dt*60);
 for(let i=shots.length-1;i>=0;i--){
  const s=shots[i];s.x+=s.dir*s.speed*dt*60;s.life-=dt*60;
  const target=s.owner.id===1?p2:p1;
  if(Math.abs(s.x-target.x)<s.size+23&&Math.abs(s.y-(target.y-55))<90){
   impact(target,s.damage,s.type==="탱커"?150:100,s.owner,true);
   burst(s.x,s.y,s.color,20,8);shots.splice(i,1);continue;
  }
  if(s.life<=0||s.x<0||s.x>W)shots.splice(i,1);
 }
 for(let i=particles.length-1;i>=0;i--){
  const q=particles[i];q.x+=q.vx*dt*60;q.y+=q.vy*dt*60;
  q.vy+=.13*dt*60;q.life-=dt*60;
  if(q.life<=0)particles.splice(i,1);
 }
 if(p1.hp<=0)finish(2);else if(p2.hp<=0)finish(1);
}
function poly(points,fill,stroke){
 ctx.beginPath();ctx.moveTo(points[0][0],points[0][1]);
 for(let i=1;i<points.length;i++)ctx.lineTo(points[i][0],points[i][1]);
 ctx.closePath();ctx.fillStyle=fill;ctx.fill();
 if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke();}
}
function background(){
 const g=ctx.createLinearGradient(0,0,0,H);
 g.addColorStop(0,"#1d2941");g.addColorStop(.55,"#151b2b");g.addColorStop(1,"#080b12");
 ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 // Dramatic arena lights
 for(let i=0;i<7;i++){
  const x=50+i*145;
  const glow=ctx.createRadialGradient(x,75,0,x,75,150);
  glow.addColorStop(0,"#a5c7ff22");glow.addColorStop(1,"#7ca8ff00");
  ctx.fillStyle=glow;ctx.fillRect(x-150,0,300,260);
 }
 // Buildings
 for(let i=0;i<12;i++){
  let x=i*88-10,h=95+(i*43%105);
  ctx.fillStyle=i%2?"#182239":"#202b42";
  ctx.fillRect(x,FLOOR-h,66,h);
  ctx.fillStyle="#8eb7ff20";
  for(let j=0;j<3;j++)ctx.fillRect(x+10+j*17,FLOOR-h+14,5,h-25);
 }
 // Floor
 ctx.fillStyle="#111827";ctx.fillRect(0,FLOOR,W,H-FLOOR);
 const fg=ctx.createLinearGradient(0,FLOOR,0,H);
 fg.addColorStop(0,"#25334b");fg.addColorStop(1,"#101522");
 ctx.fillStyle=fg;ctx.fillRect(0,FLOOR,W,H-FLOOR);
 ctx.strokeStyle="#52658155";ctx.lineWidth=1;
 for(let x=-500;x<W+500;x+=55){
  ctx.beginPath();ctx.moveTo(W/2+(x-W/2)*.15,FLOOR);ctx.lineTo(x,H);ctx.stroke();
 }
 for(let y=FLOOR+22;y<H;y+=22){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
 ctx.strokeStyle="#a3b9df";ctx.lineWidth=2;
 ctx.beginPath();ctx.moveTo(0,FLOOR);ctx.lineTo(W,FLOOR);ctx.stroke();
}
function drawFighter(a){
 ctx.save();ctx.translate(a.x,a.y);ctx.scale(a.dir,1);
 // Ground shadow
 ctx.fillStyle="#0009";ctx.beginPath();ctx.ellipse(0,2,36,8,0,0,Math.PI*2);ctx.fill();
 const bob=a.air?0:Math.sin(a.walk*.2)*2;
 const c=a.flash>0?"#fff":a.color;
 // Aura
 if(a.skillTime>0){
  ctx.globalAlpha=.24;
  const ag=ctx.createRadialGradient(0,-55,5,0,-55,75);
  ag.addColorStop(0,c);ag.addColorStop(1,"#00000000");
  ctx.fillStyle=ag;ctx.beginPath();ctx.arc(0,-55,75,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=1;
 }
 // Legs, angular armor
 ctx.lineCap="round";
 ctx.strokeStyle="#090e18";ctx.lineWidth=19;
 ctx.beginPath();ctx.moveTo(-8,-36+bob);ctx.lineTo(-18,-15);ctx.lineTo(-24,-3);ctx.stroke();
 ctx.beginPath();ctx.moveTo(8,-36+bob);ctx.lineTo(20,-16);ctx.lineTo(25,-3);ctx.stroke();
 ctx.strokeStyle=c;ctx.lineWidth=9;
 ctx.beginPath();ctx.moveTo(-17,-16);ctx.lineTo(-24,-4);ctx.stroke();
 ctx.beginPath();ctx.moveTo(19,-17);ctx.lineTo(25,-4);ctx.stroke();
 // Boots
 poly([[-34,-2],[-15,-9],[-8,0],[-30,4]],"#090e18");
 poly([[15,-5],[30,-11],[36,-2],[15,2]],"#090e18");
 // Torso armor
 poly([[-18,-77+bob],[12,-79+bob],[23,-43+bob],[12,-32+bob],[-15,-34+bob],[-25,-53+bob]],c,"#0b101a");
 poly([[-12,-73+bob],[8,-72+bob],[14,-48+bob],[-9,-44+bob]],"#111a2b");
 // Shoulder plates
 poly([[-20,-72+bob],[-31,-65+bob],[-23,-52+bob],[-12,-62+bob]],c,"#0b101a");
 poly([[13,-74+bob],[24,-68+bob],[20,-54+bob],[10,-63+bob]],c,"#0b101a");
 // Belt
 ctx.fillStyle="#090e18";ctx.fillRect(-16,-43+bob,31,6);
 ctx.fillStyle="#e4eaf5";ctx.fillRect(-2,-43+bob,6,6);
 // Head, helmet shape
 poly([[-14,-92+bob],[-5,-101+bob],[9,-98+bob],[17,-88+bob],[13,-74+bob],[-7,-72+bob],[-17,-81+bob]],c,"#090e18");
 poly([[-12,-88+bob],[2,-93+bob],[13,-86+bob],[8,-82+bob],[-9,-82+bob]],"#111827");
 ctx.fillStyle="#fff";ctx.fillRect(4,-87+bob,8,3);
 ctx.fillStyle=c;ctx.fillRect(2,-82+bob,12,2);
 // Back arm
 ctx.strokeStyle="#101725";ctx.lineWidth=13;
 ctx.beginPath();ctx.moveTo(-16,-68+bob);ctx.lineTo(-28,-51);ctx.lineTo(-18,-41);ctx.stroke();
 ctx.strokeStyle=c;ctx.lineWidth=7;
 ctx.beginPath();ctx.moveTo(-27,-52);ctx.lineTo(-18,-42);ctx.stroke();
 // Front arm poses
 let ax=a.attack>0?39:18, ay=a.attack>0?-58:-54+bob;
 if(a.guard){ax=8;ay=-79;}
 if(a.skillTime>0){ax=48;ay=-62;}
 ctx.strokeStyle="#0a101a";ctx.lineWidth=a.name==="탱커"?20:16;
 ctx.beginPath();ctx.moveTo(13,-69+bob);ctx.lineTo(ax,ay);ctx.stroke();
 ctx.strokeStyle=c;ctx.lineWidth=a.name==="탱커"?13:10;
 ctx.beginPath();ctx.moveTo(15,-69+bob);ctx.lineTo(ax,ay);ctx.stroke();
 poly([[ax-7,ay-8],[ax+5,ay-11],[ax+12,ay-1],[ax+4,ay+8],[ax-7,ay+3]],"#e7edf7","#111827");
 // Energy slash
 if(a.attack>0){
  ctx.globalAlpha=.55;ctx.strokeStyle=c;ctx.lineWidth=5;
  ctx.beginPath();ctx.arc(28,-56,30,-.8,.7);ctx.stroke();ctx.globalAlpha=1;
 }
 ctx.restore();
 ctx.textAlign="center";ctx.font="bold 15px Arial";
 ctx.fillStyle="#0009";ctx.fillText(a.name,a.x+1,a.y-119+1);
 ctx.fillStyle="#f5f7ff";ctx.fillText(a.name,a.x,a.y-120);
}
function drawEffects(){
 for(const q of particles){
  ctx.globalAlpha=Math.max(0,q.life/q.max);ctx.fillStyle=q.color;
  ctx.shadowColor=q.color;ctx.shadowBlur=8;
  ctx.fillRect(q.x,q.y,q.size,q.size);
 }
 ctx.globalAlpha=1;ctx.shadowBlur=0;
 for(const s of shots){
  ctx.save();ctx.translate(s.x,s.y);
  ctx.shadowColor=s.color;ctx.shadowBlur=24;ctx.fillStyle=s.color;
  if(s.type==="아이스"){
   poly([[0,-s.size],[s.size*.7,0],[0,s.size],[ -s.size*.7,0]],s.color,"#ffffff");
  }else if(s.type==="마그마"||s.type==="드래곤"){
   ctx.beginPath();ctx.ellipse(0,0,s.size*1.6,s.size*.8,0,0,Math.PI*2);ctx.fill();
   ctx.fillStyle="#fff4b0";ctx.beginPath();ctx.ellipse(-s.dir*5,0,s.size*.7,s.size*.35,0,0,Math.PI*2);ctx.fill();
  }else{
   ctx.beginPath();ctx.arc(0,0,s.size,0,Math.PI*2);ctx.fill();
   ctx.strokeStyle="#fff";ctx.lineWidth=2;ctx.stroke();
  }
  ctx.restore();
 }
 ctx.globalAlpha=1;ctx.shadowBlur=0;
}
function draw(){
 ctx.save();
 if(shake>0){ctx.translate((Math.random()-.5)*shake,(Math.random()-.5)*shake);shake*=.82;}
 background();drawEffects();drawFighter(p1);drawFighter(p2);
 ctx.restore();
 if(screenFlash>0){
  ctx.fillStyle="rgba(255,255,255,"+screenFlash+")";ctx.fillRect(0,0,W,H);
  screenFlash=Math.max(0,screenFlash-.025);
 }
 document.getElementById("h1").style.width=(100*p1.hp/p1.maxHp)+"%";
 document.getElementById("h2").style.width=(100*p2.hp/p2.maxHp)+"%";
 document.getElementById("score").textContent=score1+" : "+score2;
 document.getElementById("round").textContent="ROUND "+round;
 document.getElementById("timer").textContent=Math.ceil(Math.max(0,timeLeft))+" SEC";
}
function frame(now){
 const dt=Math.min(.035,(now-last)/1000);last=now;
 update(dt);draw();requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script></body></html>
    """

    html = html.replace("__CONFIG__", settings_json)
    components.html(html, height=780, scrolling=False)
