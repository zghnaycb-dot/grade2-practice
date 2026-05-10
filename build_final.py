# -*- coding: utf-8 -*-
import json, os

# Load questions
with open('question_bank.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

Q = json.dumps(questions, ensure_ascii=False)
DT = json.dumps([
    {"id":1,"emoji":"📖","title":"语文小达人","desc":"完成5道语文题","target":5,"subject":"chinese","gemReward":15},
    {"id":2,"emoji":"🔢","title":"数学小天才","desc":"完成5道数学题","target":5,"subject":"math","gemReward":15},
    {"id":3,"emoji":"⚡","title":"连击挑战","desc":"连续答对10题","target":10,"combo":True,"gemReward":30},
    {"id":4,"emoji":"🌟","title":"初学者","desc":"完成第一道题","target":1,"gemReward":5},
], ensure_ascii=False)
BD = json.dumps([
    {"id":"first","emoji":"🌟","name":"初次冒险","desc":"完成第一道题"},
    {"id":"combo5","emoji":"🔥","name":"5连击","desc":"连续答对5题"},
    {"id":"combo10","emoji":"⚡","name":"连击王者","desc":"连续答对10题"},
    {"id":"gem50","emoji":"💎","name":"宝石达人","desc":"收集50颗宝石"},
    {"id":"gem100","emoji":"👑","name":"宝石收藏家","desc":"收集100颗宝石"},
    {"id":"petlv2","emoji":"🦊","name":"伙伴诞生","desc":"小狐狸升到2级"},
    {"id":"petlv5","emoji":"🦊✨","name":"伙伴进化","desc":"小狐狸升到5级"},
    {"id":"daily3","emoji":"🏆","name":"今日之星","desc":"完成3个每日任务"},
], ensure_ascii=False)

print(f'Questions: {len(questions)}')
for g in sorted(set(q['grade'] for q in questions)):
    print(f'  Grade {g}: {len([q for q in questions if q["grade"]==g])}')

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>🦊 学习大冒险</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--pink:#FF5E8A;--orange:#FF7B3D;--yellow:#FFC107;--green:#2ECC71;--blue:#3498DB;--purple:#9B59B6;--card:#FFF;--text:#2C3E50;--sub:#7F8C8D;--border:#F0F0F0}}
body{{background:linear-gradient(180deg,#E8F4FD 0%,#FFF5F5 30%,#FFFDE7 60%,#F0FFF4 100%);min-height:100vh;font-family:'Noto Sans SC',sans-serif;overflow-x:hidden}}
body::before{{content:'';position:fixed;top:0;left:0;width:100%;height:100%;background:url('school-bg.png') no-repeat center top / contain;opacity:.06;pointer-events:none;z-index:0}}
.clouds{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}}
.cloud{{position:absolute;background:#fff;border-radius:50%;box-shadow:0 8px 30px rgba(0,0,0,.04);opacity:.7;animation:fc var(--d) ease-in-out infinite;animation-delay:var(--dl)}}
@keyframes fc{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(var(--dx))}}}}
.float-e{{position:fixed;pointer-events:none;z-index:0;font-size:1.2em;animation:fu 4s ease-in-out infinite;animation-delay:var(--dl)}}
@keyframes fu{{0%,100%{{transform:translateY(0);opacity:.6}}50%{{transform:translateY(-20px);opacity:1}}}}
.container{{max-width:500px;margin:0 auto;padding:12px 16px 100px;position:relative;z-index:1}}
.topbar{{display:flex;align-items:center;justify-content:space-between;padding:8px 0;margin-bottom:8px}}
.topbar .gems{{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.85);backdrop-filter:blur(10px);border-radius:20px;padding:6px 14px;font-weight:700;color:#2C3E50;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.topbar .gems .gicon{{font-size:1.3em;animation:gemBounce 2s ease-in-out infinite}}
@keyframes gemBounce{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.2)}}}}
.topbar .actions{{display:flex;gap:6px}}
.topbar .btn-s{{width:36px;height:36px;border-radius:50%;border:none;background:rgba(255,255,255,.85);font-size:1.2em;cursor:pointer;backdrop-filter:blur(10px);box-shadow:0 2px 8px rgba(0,0,0,.06);transition:all .2s}}
.topbar .btn-s:active{{transform:scale(.9);background:#f0f0f0}}
.main-title{{text-align:center;margin:16px 0 4px}}
.main-title h1{{font-size:1.8em;font-weight:900;background:linear-gradient(135deg,#FF5E8A,#FF7B3D);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-family:'Fredoka One',cursive}}
.main-title .sub{{font-size:.85em;color:var(--sub);margin-top:2px}}
.pet-area{{text-align:center;margin:8px 0;position:relative}}
.pet-container{{display:inline-block;cursor:pointer;position:relative;transition:transform .3s}}
.pet-container:active{{transform:scale(.9)}}
.pet-fox{{font-size:4em;transition:all .3s}}
.pet-name{{font-weight:700;color:var(--text);font-size:.9em;margin-top:2px}}
.pet-lvl{{font-size:.75em;color:var(--sub)}}
.pet-exp{{width:120px;height:6px;background:#eee;border-radius:3px;margin:4px auto;overflow:hidden}}
.pet-exp-fill{{height:100%;background:linear-gradient(90deg,var(--orange),var(--pink));border-radius:3px;transition:width .5s}}
.float-gem{{position:absolute;font-size:1.5em;animation:fg .8s ease-out forwards;pointer-events:none}}
@keyframes fg{{0%{{opacity:1;transform:translateY(0) scale(1)}}100%{{opacity:0;transform:translateY(-60px) scale(.5)}}}}
.subject-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}}
.sub-card{{background:var(--card);border-radius:16px;padding:16px;text-align:center;cursor:pointer;box-shadow:0 4px 15px rgba(0,0,0,.06);border:2px solid transparent;border-top:4px solid var(--bc);transition:all .25s;position:relative;overflow:hidden}}
.sub-card:hover{{transform:translateY(-3px);box-shadow:0 8px 25px rgba(0,0,0,.1);border-color:var(--bc)}}
.sub-card:active{{transform:scale(.97)}}
.sub-card .icon{{font-size:2.5em;margin-bottom:6px}}
.sub-card .name{{font-weight:700;font-size:1.1em;color:var(--text)}}
.sub-card .count{{font-size:.8em;color:var(--sub);margin-top:2px}}
.section-title{{font-weight:700;font-size:1.1em;color:var(--text);margin:16px 0 8px;display:flex;align-items:center;gap:6px}}
.task-list{{display:flex;flex-direction:column;gap:8px}}
.task-item{{display:flex;align-items:center;gap:10px;background:var(--card);border-radius:14px;padding:12px 14px;box-shadow:0 2px 8px rgba(0,0,0,.04);transition:all .2s}}
.task-item.done{{opacity:.5}}
.task-item .ti-emoji{{font-size:1.5em;flex-shrink:0}}
.task-item .ti-info{{flex:1}}
.task-item .ti-title{{font-weight:600;font-size:.9em;color:var(--text)}}
.task-item .ti-sub{{font-size:.75em;color:var(--sub)}}
.task-item .ti-prog{{font-size:.8em;color:var(--blue);font-weight:600}}
.task-item .ti-claim{{padding:5px 12px;border-radius:12px;border:none;background:var(--yellow);color:#fff;font-weight:700;font-size:.8em;cursor:pointer;transition:all .2s;white-space:nowrap}}
.task-item .ti-claim:active{{transform:scale(.9)}}
.task-item .ti-claim.claimed{{background:#ccc;cursor:default}}
.quiz-screen{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:100;flex-direction:column;align-items:center;justify-content:center;padding:16px}}
.quiz-screen.active{{display:flex}}
.quiz-card{{background:#fff;border-radius:20px;padding:24px;width:100%;max-width:420px;box-shadow:0 20px 60px rgba(0,0,0,.15);position:relative;animation:slideUp .3s ease-out}}
@keyframes slideUp{{from{{transform:translateY(30px);opacity:0}}to{{transform:translateY(0);opacity:1}}}}
.quiz-close{{position:absolute;top:12px;right:14px;font-size:1.5em;cursor:pointer;color:#ccc;z-index:2;background:none;border:none}}
.quiz-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}}
.quiz-tag{{font-size:.8em;padding:4px 10px;border-radius:10px;font-weight:600}}
.quiz-tag.chinese{{background:#FFF0F0;color:#FF5E8A}}
.quiz-tag.math{{background:#F0F5FF;color:#3498DB}}
.quiz-tag.english{{background:#F0FFF4;color:#2ECC71}}
.quiz-tag.general{{background:#FFF8F0;color:#FF7B3D}}
.quiz-combo{{display:flex;align-items:center;gap:3px;font-size:.85em;font-weight:700;color:var(--orange)}}
.quiz-qnum{{font-size:.75em;color:var(--sub)}}
.quiz-progress{{height:4px;background:#eee;border-radius:2px;margin-bottom:16px;overflow:hidden}}
.quiz-progress .fill{{height:100%;background:linear-gradient(90deg,var(--green),var(--blue));transition:width .4s}}
.q-area{{font-size:.75em;color:var(--sub);margin-bottom:4px}}
.quiz-question{{font-size:1.15em;font-weight:700;color:var(--text);margin-bottom:16px;line-height:1.6}}
.quiz-options{{display:flex;flex-direction:column;gap:8px}}
.quiz-opt{{padding:12px 16px;border-radius:12px;border:2px solid var(--border);background:#fff;font-size:.95em;text-align:left;cursor:pointer;transition:all .2s;color:var(--text);display:flex;align-items:center;gap:10px}}
.quiz-opt:active{{transform:scale(.98)}}
.quiz-opt:hover{{border-color:var(--blue);background:#F0F8FF}}
.quiz-opt.correct{{border-color:var(--green)!important;background:#E8F8F0!important;animation:pop .3s}}
.quiz-opt.wrong{{border-color:var(--pink)!important;background:#FFF0F0!important;animation:shake .4s}}
.quiz-opt .oi{{width:26px;height:26px;border-radius:50%;background:#f5f5f5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85em;flex-shrink:0}}
@keyframes pop{{0%{{transform:scale(1)}}50%{{transform:scale(1.03)}}100%{{transform:scale(1)}}}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-4px)}}75%{{transform:translateX(4px)}}}}
.quiz-fill{{display:flex;gap:8px;flex-direction:column}}
.quiz-fill input{{width:100%;padding:12px 16px;border-radius:12px;border:2px solid var(--border);font-size:1em;outline:none;transition:all .2s;color:var(--text);font-family:inherit}}
.quiz-fill input:focus{{border-color:var(--blue)}}
.quiz-fill .submit-btn{{width:100%;padding:12px;border-radius:12px;border:none;background:var(--blue);color:#fff;font-weight:700;font-size:1em;cursor:pointer;transition:all .2s;margin-top:4px}}
.quiz-fill .submit-btn:active{{transform:scale(.97);opacity:.9}}
.quiz-feedback{{text-align:center;padding:8px;font-weight:700;font-size:.95em;display:none}}
.quiz-feedback.show{{display:block}}
.quiz-feedback.correct{{color:var(--green)}}
.quiz-feedback.wrong{{color:var(--pink)}}
.quiz-combo-pop{{position:absolute;font-size:1.5em;font-weight:900;pointer-events:none;animation:comboPop .8s ease-out forwards}}
@keyframes comboPop{{0%{{transform:scale(0);opacity:1}}50%{{transform:scale(1.5);opacity:.8}}100%{{transform:scale(2);opacity:0}}}}
.badge-toast{{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;border-radius:20px;padding:24px 32px;z-index:200;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.2);animation:bt .4s ease-out}}
@keyframes bt{{from{{transform:translate(-50%,-50%) scale(0);opacity:0}}to{{transform:translate(-50%,-50%) scale(1);opacity:1}}}}
.badge-toast .be{{font-size:4em;margin-bottom:8px}}
.badge-toast .bn{{font-weight:900;font-size:1.2em;color:var(--text)}}
.badge-toast .bd{{font-size:.85em;color:var(--sub);margin-top:4px}}
.badge-toast .bok{{margin-top:12px;padding:8px 24px;border-radius:14px;border:none;background:var(--yellow);color:#fff;font-weight:700;cursor:pointer}}
.overlay{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.6);z-index:150}}
.overlay.active{{display:flex;align-items:center;justify-content:center;padding:16px}}
.panel{{background:#fff;border-radius:20px;padding:20px;width:100%;max-width:400px;max-height:85vh;overflow-y:auto;animation:slideUp .3s ease-out}}
.panel h3{{font-size:1.2em;margin-bottom:14px;color:var(--text);text-align:center}}
.panel .close{{float:right;font-size:1.3em;cursor:pointer;background:none;border:none;color:#ccc}}
.badge-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.badge-cell{{text-align:center;padding:12px;border-radius:14px;border:2px solid var(--border);transition:all .2s}}
.badge-cell.unlocked{{border-color:var(--yellow);background:#FFFDE7}}
.badge-cell.locked{{opacity:.4}}
.badge-cell .bi{{font-size:2.5em;margin-bottom:4px}}
.badge-cell .nam{{font-weight:700;font-size:.85em;color:var(--text)}}
.badge-cell .dsc{{font-size:.7em;color:var(--sub)}}
.wrong-list{{display:flex;flex-direction:column;gap:8px;max-height:50vh;overflow-y:auto}}
.wrong-item{{background:#FFF0F0;border-radius:12px;padding:12px;border:1px solid #FFCDD2}}
.wrong-item .q{{font-weight:600;color:var(--text);font-size:.9em}}
.wrong-item .a{{font-size:.8em;color:var(--green);margin-top:4px}}
.wrong-item .ua{{font-size:.8em;color:var(--pink);margin-top:2px}}
.setting-row{{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border)}}
.setting-row .label{{font-weight:500;color:var(--text)}}
.toggle{{width:50px;height:28px;border-radius:14px;border:none;cursor:pointer;position:relative;transition:background .3s}}
.toggle.on{{background:var(--green)}}
.toggle.off{{background:#ccc}}
.toggle .knob{{position:absolute;top:3px;width:22px;height:22px;background:#fff;border-radius:50%;transition:left .3s;box-shadow:0 2px 4px rgba(0,0,0,.15)}}
.toggle.on .knob{{left:25px}}
.toggle.off .knob{{left:3px}}
.danger-btn{{width:100%;padding:10px;border-radius:12px;border:none;background:#FF4444;color:#fff;font-weight:700;cursor:pointer;margin:8px 0}}
.secondary-btn{{width:100%;padding:10px;border-radius:12px;border:none;background:var(--sub);color:#fff;font-weight:600;cursor:pointer;margin:4px 0}}
.map-area{{margin:12px 0}}
.map-row{{display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap}}
.map-node{{flex:1;min-width:80px;padding:12px 8px;border-radius:14px;text-align:center;cursor:pointer;border:2px solid var(--border);background:#fff;transition:all .2s}}
.map-node.unlocked{{border-color:var(--green);background:#F0FFF4}}
.map-node.locked{{opacity:.5;cursor:not-allowed}}
.map-node.current{{border-color:var(--blue);background:#F0F8FF;animation:pulse 2s infinite}}
.map-node .mn-emoji{{font-size:1.5em}}
.map-node .mn-name{{font-size:.75em;font-weight:600;color:var(--text);margin-top:2px}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(52,152,219,.3)}}50%{{box-shadow:0 0 0 8px rgba(52,152,219,0)}}}}
.nav-tabs{{display:flex;gap:4px;margin-bottom:12px;background:#f5f5f5;border-radius:12px;padding:4px}}
.nav-tab{{flex:1;padding:8px;text-align:center;border-radius:10px;cursor:pointer;font-weight:600;font-size:.85em;color:var(--sub);transition:all .2s;border:none;background:none}}
.nav-tab.active{{background:#fff;color:var(--text);box-shadow:0 2px 4px rgba(0,0,0,.08)}}
.modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.6);z-index:160;flex-direction:column;align-items:center;justify-content:center;padding:16px}}
.modal.active{{display:flex}}
.modal-content{{background:#fff;border-radius:20px;padding:24px;width:100%;max-width:380px;text-align:center;animation:slideUp .3s ease-out}}
.modal-content .mc-emoji{{font-size:3em;margin-bottom:8px}}
.modal-content .mc-title{{font-weight:900;font-size:1.2em;color:var(--text)}}
.modal-content .mc-text{{color:var(--sub);margin:8px 0 14px;font-size:.9em}}
.modal-content .mc-btn{{padding:10px 28px;border-radius:14px;border:none;font-weight:700;cursor:pointer;font-size:.95em;margin:4px}}
.modal-content .mc-btn.primary{{background:var(--blue);color:#fff}}
.modal-content .mc-btn.danger{{background:var(--pink);color:#fff}}
.modal-content .mc-btn.secondary{{background:#eee;color:var(--text)}}
</style>
</head>
<body>
<div class="clouds" id="clouds"></div>

<div class="container" id="app">
  <!-- Topbar -->
  <div class="topbar">
    <div class="gems"><span class="gicon">💎</span><span id="gemCount">0</span></div>
    <div class="actions">
      <button class="btn-s" onclick="showBadges()" title="🏅徽章">🏅</button>
      <button class="btn-s" onclick="showWrongBook()" title="📝错题">📝</button>
      <button class="btn-s" onclick="showSettings()" title="⚙️设置">⚙️</button>
    </div>
  </div>

  <!-- Pet -->
  <div class="pet-area">
    <div class="pet-container" onclick="clickPet(event)">
      <div class="pet-fox" id="petIcon">🦊</div>
      <div class="pet-name" id="petName">小狐狸</div>
      <div class="pet-lvl">Lv.<span id="petLvl">1</span></div>
      <div class="pet-exp"><div class="pet-exp-fill" id="petExp" style="width:0%"></div></div>
    </div>
  </div>

  <!-- Title -->
  <div class="main-title">
    <h1>🦊 学习大冒险</h1>
    <div class="sub" id="todayInfo">今日欢迎语</div>
  </div>

  <!-- Nav -->
  <div class="nav-tabs" id="navTabs">
    <button class="nav-tab active" onclick="switchTab('subjects')">📚 练习</button>
    <button class="nav-tab" onclick="switchTab('map')">🗺️ 冒险</button>
    <button class="nav-tab" onclick="switchTab('tasks')">📋 任务</button>
  </div>

  <!-- Subjects Tab -->
  <div id="tab-subjects">
    <div class="subject-grid" id="subjectGrid"></div>
  </div>

  <!-- Map Tab -->
  <div id="tab-map" style="display:none">
    <div class="map-area" id="mapArea"></div>
  </div>

  <!-- Tasks Tab -->
  <div id="tab-tasks" style="display:none">
    <div class="task-list" id="taskList"></div>
  </div>
</div>

<!-- Quiz Overlay -->
<div class="quiz-screen" id="quizScreen">
  <div class="quiz-card" id="quizCard"></div>
</div>

<!-- Badge Toast -->
<div id="badgeToast"></div>

<!-- Overlays -->
<div class="overlay" id="badgeOverlay"><div class="panel" id="badgePanel"></div></div>
<div class="overlay" id="wrongOverlay"><div class="panel" id="wrongPanel"></div></div>
<div class="overlay" id="settingsOverlay"><div class="panel" id="settingsPanel"></div></div>
<div class="modal" id="confirmModal"></div>

<script>
const QUESTION_BANK = {Q};
const DAILY_TASKS = {DT};
const BADGE_DEFS = {BD};

// ===== State =====
let gems = parseInt(localStorage.getItem('la_gems')||'0');
let petExp = parseInt(localStorage.getItem('la_petExp')||'0');
let petLevel = parseInt(localStorage.getItem('la_petLevel')||'1');
let combo = 0, maxCombo = parseInt(localStorage.getItem('la_maxCombo')||'0');
let totalCorrect = parseInt(localStorage.getItem('la_totalCorrect')||'0');
let totalAnswered = parseInt(localStorage.getItem('la_totalAnswered')||'0');
let unlockedBadges = new Set(JSON.parse(localStorage.getItem('la_badges')||'[]'));
let wrongBook = JSON.parse(localStorage.getItem('la_wrongBook')||'[]');
let todayTaskStates = JSON.parse(localStorage.getItem('la_taskStates_'+new Date().toDateString())||'[]');
let soundOn = localStorage.getItem('la_sound')!=='false';
let currentQuiz = null, quizIndex = 0, quizQuestions = [];
let currentGrade = 2; // default grade

// ===== Init =====
const petStages = [
  {{level:1,emoji:'🦊',name:'小狐狸',expNeeded:5}},
  {{level:2,emoji:'🦊',name:'小伙伴',expNeeded:15}},
  {{level:3,emoji:'🦊✨',name:'探险家',expNeeded:30}},
  {{level:4,emoji:'🦊🌟',name:'冒险王',expNeeded:60}},
  {{level:5,emoji:'🦊👑',name:'传奇伙伴',expNeeded:100}},
];

function updatePetUI(){{
  let stage = petStages[0];
  for(let i=petStages.length-1;i>=0;i--){{
    if(petLevel>=petStages[i].level){{ stage=petStages[i]; break; }}
  }}
  document.getElementById('petIcon').textContent = stage.emoji;
  document.getElementById('petName').textContent = stage.name;
  document.getElementById('petLvl').textContent = petLevel;
  
  let currentStage = petStages.find(s=>s.level<=petLevel)||petStages[0];
  let nextStage = petStages.find(s=>s.level>petLevel)||petStages[petStages.length-1];
  let stageExp = petExp - currentStage.expNeeded + (petStages.findIndex(s=>s===currentStage)>0?petStages.slice(0,petStages.findIndex(s=>s===currentStage)).reduce((a,s)=>a+s.expNeeded,0):0);
  let stageMax = nextStage.expNeeded;
  let pct = Math.min(100, Math.max(0, (petExp / (petLevel>=5?100:stageMax)) * 100));
  document.getElementById('petExp').style.width = pct+'%';
}}

function updateTopbar(){{
  document.getElementById('gemCount').textContent = gems;
}}

function renderSubjects(){{
  let grid = document.getElementById('subjectGrid');
  let allGrades = [...new Set(QUESTION_BANK.map(q=>q.grade))].sort();
  let subs = [
    {{id:'chinese',name:'📖 语文',bc:'#FF5E8A',emoji:'📖'}},
    {{id:'math',name:'🔢 数学',bc:'#3498DB',emoji:'🔢'}},
    {{id:'english',name:'🔤 英语',bc:'#2ECC71',emoji:'🔤'}},
    {{id:'all',name:'🧪 综合',bc:'#FF7B3D',emoji:'🧪'}},
  ];
  
  // Grade selector
  let gradeHtml = '<div style="grid-column:1/-1;display:flex;gap:6px;justify-content:center;margin-bottom:4px;flex-wrap:wrap">';
  allGrades.forEach(g=>{{
    gradeHtml += '<button style="padding:4px 12px;border-radius:12px;border:none;cursor:pointer;font-weight:600;font-size:.8em;'+(g===currentGrade?'background:var(--blue);color:#fff':'background:#eee;color:var(--text)')+'" onclick="setGrade('+g+')">'+g+'年级</button>';
  }});
  gradeHtml += '</div>';
  grid.innerHTML = gradeHtml;
  
  subs.forEach(s=>{{
    let qs = s.id==='all' ? QUESTION_BANK.filter(q=>q.grade===currentGrade) : QUESTION_BANK.filter(q=>q.subject===s.id && q.grade===currentGrade);
    let card = document.createElement('div');
    card.className = 'sub-card';
    card.style.setProperty('--bc', s.bc);
    card.innerHTML = '<div class="icon">'+s.emoji+'</div><div class="name">'+s.name+'</div><div class="count">'+qs.length+'道题</div>';
    card.onclick = ()=>startQuiz(s.id);
    grid.appendChild(card);
  }});
  
  // Show total count
  let total = QUESTION_BANK.filter(q=>q.grade===currentGrade).length;
  let info = document.createElement('div');
  info.style.cssText = 'grid-column:1/-1;text-align:center;font-size:.8em;color:var(--sub);margin-top:4px';
  info.textContent = currentGrade+'年级共 '+total+' 道题';
  grid.appendChild(info);
}}

function setGrade(g){{
  currentGrade = g;
  renderSubjects();
  renderMap();
}}

function renderMap(){{
  let map = document.getElementById('mapArea');
  let regions = [...new Set(QUESTION_BANK.filter(q=>q.grade===currentGrade).map(q=>q.region).filter(Boolean))];
  if(regions.length===0) regions = ['练习区'];
  
  let unlockedRegions = Math.min(regions.length, Math.ceil(totalCorrect/5)+1);
  
  let html = '<div style="text-align:center;margin-bottom:8px;font-weight:600;color:var(--text)">'+currentGrade+'年级冒险地图</div>';
  html += '<div class="map-row">';
  regions.forEach((r,i)=>{{
    let cls = i<unlockedRegions ? (i===unlockedRegions-1?'unlocked current':'unlocked') : 'locked';
    html += '<div class="map-node '+cls+'" onclick="'+((i<unlockedRegions)?'startQuizByRegion(\''+r.replace(/'/g,"\\'")+'\')':'')+'"><div class="mn-emoji">'+(i<unlockedRegions?'🗺️':'🔒')+'</div><div class="mn-name">'+r+'</div></div>';
  }});
  html += '</div>';
  html += '<div style="text-align:center;font-size:.8em;color:var(--sub);margin-top:8px">答对题目解锁更多区域！</div>';
  map.innerHTML = html;
}}

function startQuizByRegion(region){{
  let qs = QUESTION_BANK.filter(q=>q.grade===currentGrade && q.region===region);
  if(qs.length===0) return;
  startQuizSession(qs);
}}

function startQuiz(subject){{
  let qs = subject==='all' ? 
    QUESTION_BANK.filter(q=>q.grade===currentGrade) :
    QUESTION_BANK.filter(q=>q.subject===subject && q.grade===currentGrade);
  if(qs.length===0){{ alert('当前年级暂无该科目题目！'); return; }}
  startQuizSession(qs);
}}

function startQuizSession(qs){{
  quizQuestions = qs.sort(()=>Math.random()-.5).slice(0,10);
  quizIndex = 0;
  currentQuiz = {{correct:0,total:0,combo:0,gemEarned:0}};
  showQuiz();
}}

function showQuiz(){{
  if(quizIndex >= quizQuestions.length){{
    endQuiz();
    return;
  }}
  
  let q = quizQuestions[quizIndex];
  let card = document.getElementById('quizCard');
  let subColors = {{chinese:'#FF5E8A',math:'#3498DB',english:'#2ECC71'}};
  let subNames = {{chinese:'语文',math:'数学',english:'英语',general:'综合'}};
  let regionText = q.region ? '<div class="q-area">📍 '+q.region+' · '+q.grade+'年级</div>' : '';
  
  let html = '<button class="quiz-close" onclick="closeQuiz()">✕</button>';
  html += '<div class="quiz-header">';
  html += '<span class="quiz-tag '+q.subject+'" style="background:'+(subColors[q.subject]||'#FFF8F0')+'20">'+q.subject.toUpperCase()+'</span>';
  html += '<div class="quiz-combo" id="quizComboDisplay">'+((combo>0)?'🔥 '+combo+'连击':'')+'</div>';
  html += '<span class="quiz-qnum">'+(quizIndex+1)+'/'+quizQuestions.length+'</span>';
  html += '</div>';
  html += '<div class="quiz-progress"><div class="fill" style="width:'+((quizIndex/quizQuestions.length)*100)+'%"></div></div>';
  html += regionText;
  html += '<div class="quiz-question">'+q.question+'</div>';
  
  if(q.type==='fill'){{
    html += '<div class="quiz-fill"><input type="text" id="fillAnswer" placeholder="输入你的答案..." autocomplete="off"><button class="submit-btn" onclick="submitFill('+q.id+')">确认答案 ✓</button></div>';
  }} else {{
    html += '<div class="quiz-options">';
    let labels = ['A','B','C','D'];
    q.options.forEach((opt,i)=>{{
      html += '<div class="quiz-opt" onclick="answerQuestion('+q.id+','+i+',this)"><span class="oi">'+labels[i]+'</span>'+opt+'</div>';
    }});
    html += '</div>';
  }}
  
  card.innerHTML = html;
  document.getElementById('quizScreen').classList.add('active');
  
  // Focus input for fill questions
  setTimeout(()=>{{
    let inp = document.getElementById('fillAnswer');
    if(inp) inp.focus();
  }}, 300);
}}

function submitFill(qid){{
  let inp = document.getElementById('fillAnswer');
  if(!inp || !inp.value.trim()){{ inp.focus(); return; }}
  
  let q = QUESTION_BANK.find(x=>x.id===qid);
  if(!q) return;
  
  let userAnswer = inp.value.trim();
  let correctAnswers = q.answer.split('|');
  let isCorrect = correctAnswers.some(a=>userAnswer===a || userAnswer.includes(a) || a.includes(userAnswer));
  
  totalAnswered++;
  if(isCorrect){{
    combo++;
    if(combo>maxCombo){{ maxCombo=combo; localStorage.setItem('la_maxCombo',maxCombo); }}
    totalCorrect++;
    petExp++;
    currentQuiz.correct++;
    currentQuiz.combo = Math.max(currentQuiz.combo||0, combo);
    let gemBonus = Math.min(combo, 10);
    gems += gemBonus;
    currentQuiz.gemEarned += gemBonus;
  }} else {{
    combo = 0;
    wrongBook.push({{id:q.id,question:q.question,answer:q.answer,userAnswer:userAnswer,date:new Date().toISOString()}});
    localStorage.setItem('la_wrongBook', JSON.stringify(wrongBook));
  }}
  
  saveState();
  checkBadges();
  updatePetUI();
  updateTopbar();
  
  // Show inline feedback
  let card = document.getElementById('quizCard');
  let fb = document.createElement('div');
  fb.className = 'quiz-feedback show '+(isCorrect?'correct':'wrong');
  fb.textContent = isCorrect ? '✅ 正确！+'+(Math.min(combo,10))+'💎' : '❌ 正确答案：'+q.answer.replace(/\|/g,' 或 ');
  card.appendChild(fb);
  
  // Disable input
  document.getElementById('fillAnswer').disabled = true;
  document.querySelector('.submit-btn').setAttribute('onclick','');
  
  setTimeout(()=>{{
    quizIndex++;
    showQuiz();
  }}, isCorrect?600:1200);
}}

function answerQuestion(qid, optIdx, el){{
  let q = QUESTION_BANK.find(x=>x.id===qid);
  if(!q) return;
  
  // Disable all options
  let opts = el.parentElement.querySelectorAll('.quiz-opt');
  opts.forEach(o=>o.style.pointerEvents='none');
  
  totalAnswered++;
  let isCorrect = optIdx === q.answer;
  
  if(isCorrect){{
    el.classList.add('correct');
    combo++;
    if(combo>maxCombo){{ maxCombo=combo; localStorage.setItem('la_maxCombo',maxCombo); }}
    totalCorrect++;
    petExp++;
    currentQuiz.correct++;
    currentQuiz.combo = Math.max(currentQuiz.combo||0, combo);
    let gemBonus = Math.min(combo, 10);
    gems += gemBonus;
    currentQuiz.gemEarned += gemBonus;
    
    // Combo popup
    if(combo>=3){{
      let pop = document.createElement('div');
      pop.className = 'quiz-combo-pop';
      pop.textContent = '🔥x'+combo;
      pop.style.left = '50%';
      pop.style.top = '30%';
      document.getElementById('quizCard').appendChild(pop);
      setTimeout(()=>pop.remove(), 800);
    }}
  }} else {{
    el.classList.add('wrong');
    combo = 0;
    wrongBook.push({{id:q.id,question:q.question,answer:(typeof q.answer==='number'?q.options[q.answer]:q.answer),userAnswer:q.options[optIdx],date:new Date().toISOString()}});
    localStorage.setItem('la_wrongBook', JSON.stringify(wrongBook));
    // Highlight correct
    setTimeout(()=>opts[q.answer].classList.add('correct'), 200);
  }}
  
  saveState();
  checkBadges();
  updatePetUI();
  updateTopbar();
  document.getElementById('quizComboDisplay').textContent = combo>0?'🔥 '+combo+'连击':'';
  
  setTimeout(()=>{{
    quizIndex++;
    showQuiz();
  }}, isCorrect?600:1200);
}}

function closeQuiz(){{
  document.getElementById('quizScreen').classList.remove('active');
}}

function endQuiz(){{
  document.getElementById('quizScreen').classList.remove('active');
  checkTaskProgress();
  updatePetUI();
  updateTopbar();
  
  // Congratulate if did well
  if(currentQuiz.correct>=5){{
    let m = document.getElementById('confirmModal');
    m.innerHTML = '<div class="modal-content"><div class="mc-emoji">🎉</div><div class="mc-title">太棒了！</div><div class="mc-text">答对 '+currentQuiz.correct+'/'+quizQuestions.length+' 题，获得 '+currentQuiz.gemEarned+' 💎！'+((currentQuiz.combo||0)>=5?'最高'+currentQuiz.combo+'连击！':'')+'</div><button class="mc-btn primary" onclick="document.getElementById(\'confirmModal\').classList.remove(\'active\')">继续冒险</button></div>';
    m.classList.add('active');
  }}
}}

function checkTaskProgress(){{
  let today = new Date().toDateString();
  let states = JSON.parse(localStorage.getItem('la_taskStates_'+today)||'[]');
  DAILY_TASKS.forEach(t=>{{
    let st = states.find(s=>s.id===t.id)||{{id:t.id,progress:0,claimed:false}};
    if(st.claimed) return;
    if(t.combo && maxCombo>=t.target) st.progress = maxCombo;
    else if(t.subject) st.progress = Math.min(st.progress||0, t.target);
    else st.progress = Math.min((st.progress||0)+1, t.target);
    
    // Update state
    let idx = states.findIndex(s=>s.id===t.id);
    if(idx>=0) states[idx] = st; else states.push(st);
  }});
  localStorage.setItem('la_taskStates_'+today, JSON.stringify(states));
  renderTasks();
}}

function claimTask(taskId){{
  let today = new Date().toDateString();
  let states = JSON.parse(localStorage.getItem('la_taskStates_'+today)||'[]');
  let t = DAILY_TASKS.find(t=>t.id===taskId);
  if(!t) return;
  let st = states.find(s=>s.id===taskId)||{{id:taskId,progress:0,claimed:false}};
  if(st.progress>=t.target && !st.claimed){{
    st.claimed = true;
    gems += t.gemReward;
    petExp += Math.floor(t.gemReward/5);
    // Update state
    let idx = states.findIndex(s=>s.id===taskId);
    if(idx>=0) states[idx] = st; else states.push(st);
    localStorage.setItem('la_taskStates_'+today, JSON.stringify(states));
    saveState();
    updatePetUI();
    updateTopbar();
    renderTasks();
  }}
}}

function renderTasks(){{
  let today = new Date().toDateString();
  let states = JSON.parse(localStorage.getItem('la_taskStates_'+today)||'[]');
  let list = document.getElementById('taskList');
  list.innerHTML = DAILY_TASKS.map(t=>{{
    let st = states.find(s=>s.id===t.id)||{{id:t.id,progress:0,claimed:false}};
    let done = st.claimed || st.progress>=t.target;
    return '<div class="task-item'+(done?' done':'')+'"><div class="ti-emoji">'+t.emoji+'</div><div class="ti-info"><div class="ti-title">'+t.title+'</div><div class="ti-sub">'+t.desc+'</div></div><div class="ti-prog">'+Math.min(st.progress,t.target)+'/'+t.target+'</div>'+(st.claimed?'<button class="ti-claim claimed">已领</button>':(st.progress>=t.target?'<button class="ti-claim" onclick="claimTask('+t.id+')">领'+t.gemReward+'💎</button>':'<button class="ti-claim" style="background:#ddd;cursor:default">+'+t.gemReward+'💎</button>'))+'</div>';
  }}).join('');
}}

function checkBadges(){{
  BADGE_DEFS.forEach(b=>{{
    if(unlockedBadges.has(b.id)) return;
    let unlock = false;
    if(b.id==='first' && totalAnswered>=1) unlock=true;
    if(b.id==='combo5' && maxCombo>=5) unlock=true;
    if(b.id==='combo10' && maxCombo>=10) unlock=true;
    if(b.id==='gem50' && gems>=50) unlock=true;
    if(b.id==='gem100' && gems>=100) unlock=true;
    if(b.id==='petlv2' && petLevel>=2) unlock=true;
    if(b.id==='petlv5' && petLevel>=5) unlock=true;
    
    if(unlock){{
      unlockedBadges.add(b.id);
      localStorage.setItem('la_badges', JSON.stringify([...unlockedBadges]));
      showBadgeToast(b);
    }}
  }});
  
  // Level check
  if(petExp>=5 && petLevel<2){{ petLevel=2; petExp=0; checkBadges(); }}
  else if(petExp>=15 && petLevel<3){{ petLevel=3; petExp=0; checkBadges(); }}
  else if(petExp>=30 && petLevel<4){{ petLevel=4; petExp=0; checkBadges(); }}
  else if(petExp>=60 && petLevel<5){{ petLevel=5; petExp=0; checkBadges(); }}
}}

function dailyReset(){{
  let today = new Date().toDateString();
  // Check if tasks need init
  if(!localStorage.getItem('la_taskStates_'+today)){{
    localStorage.setItem('la_taskStates_'+today, '[]');
    renderTasks();
  }}
  // Count tasks done for daily badge
  let states = JSON.parse(localStorage.getItem('la_taskStates_'+today)||'[]');
  let done = states.filter(s=>s.claimed).length;
  if(done>=3 && !unlockedBadges.has('daily3')){{
    unlockedBadges.add('daily3');
    localStorage.setItem('la_badges', JSON.stringify([...unlockedBadges]));
    showBadgeToast(BADGE_DEFS.find(b=>b.id==='daily3'));
  }}
}}

function showBadgeToast(b){{
  let toast = document.getElementById('badgeToast');
  toast.innerHTML = '<div class="badge-toast"><div class="be">'+b.emoji+'</div><div class="bn">'+b.name+'解锁！</div><div class="bd">'+b.desc+'</div><button class="bok" onclick="this.parentElement.remove()">太棒了！</button></div>';
  setTimeout(()=>{{
    let el = toast.querySelector('.badge-toast');
    if(el) el.remove();
  }}, 3500);
}}

// ===== Overlays =====
function showBadges(){{
  let panel = document.getElementById('badgePanel');
  panel.innerHTML = '<h3>🏅 我的徽章</h3><div class="badge-grid">'+BADGE_DEFS.map(b=>{{
    let un = unlockedBadges.has(b.id);
    return '<div class="badge-cell '+(un?'unlocked':'locked')+'"><div class="bi">'+b.emoji+'</div><div class="nam">'+b.name+'</div><div class="dsc">'+(un?'已解锁':'未解锁')+'</div></div>';
  }}).join('')+'</div><button class="secondary-btn" onclick="document.getElementById(\'badgeOverlay\').classList.remove(\'active\')">关闭</button>';
  document.getElementById('badgeOverlay').classList.add('active');
}}

function showWrongBook(){{
  let panel = document.getElementById('wrongPanel');
  if(wrongBook.length===0){{
    panel.innerHTML = '<h3>📝 错题本</h3><div style="text-align:center;padding:20px;color:var(--sub)">还没有错题，太厉害了！🎉</div><button class="secondary-btn" onclick="document.getElementById(\'wrongOverlay\').classList.remove(\'active\')">关闭</button>';
  }} else {{
    panel.innerHTML = '<h3>📝 错题本 ('+wrongBook.length+'题)</h3><div class="wrong-list">'+wrongBook.slice().reverse().map(w=>'<div class="wrong-item"><div class="q">'+w.question+'</div><div class="a">✅ 正确答案：'+w.answer+'</div><div class="ua">❌ 你的答案：'+(w.userAnswer||'（无）')+'</div></div>').join('')+'</div><button class="secondary-btn" onclick="document.getElementById(\'wrongOverlay\').classList.remove(\'active\')">关闭</button><button class="danger-btn" onclick="clearWrongBook()">🗑️ 清空错题本</button>';
  }}
  document.getElementById('wrongOverlay').classList.add('active');
}}

function clearWrongBook(){{
  if(confirm('确定要清空所有错题吗？')){{
    wrongBook = [];
    localStorage.setItem('la_wrongBook','[]');
    showWrongBook();
  }}
}}

function showSettings(){{
  let panel = document.getElementById('settingsPanel');
  panel.innerHTML = '<h3>⚙️ 设置</h3><div class="setting-row"><span class="label">🔊 音效</span><button class="toggle '+(soundOn?'on':'off')+'" onclick="toggleSound(this)"><div class="knob"></div></button></div><div class="setting-row"><span class="label">📊 统计</span><span style="font-size:.85em;color:var(--sub)">答对 '+totalCorrect+'/'+totalAnswered+' · 最高'+maxCombo+'连击</span></div><button class="secondary-btn" onclick="document.getElementById(\'settingsOverlay\').classList.remove(\'active\')">关闭</button><button class="danger-btn" onclick="resetAll()">🔄 重置所有进度</button>';
  document.getElementById('settingsOverlay').classList.add('active');
}}

function toggleSound(btn){{
  soundOn = !soundOn;
  localStorage.setItem('la_sound', soundOn);
  btn.className = 'toggle '+(soundOn?'on':'off');
}}

function resetAll(){{
  let m = document.getElementById('confirmModal');
  m.innerHTML = '<div class="modal-content"><div class="mc-emoji">⚠️</div><div class="mc-title">确认重置？</div><div class="mc-text">所有进度将被清除，无法恢复！</div><button class="mc-btn secondary" onclick="document.getElementById(\'confirmModal\').classList.remove(\'active\')">取消</button><button class="mc-btn danger" onclick="doReset()">确认重置</button></div>';
  m.classList.add('active');
}}

function doReset(){{
  localStorage.clear();
  location.reload();
}}

// ===== Pet interaction =====
function clickPet(e){{
  let gemBonus = Math.floor(Math.random()*3)+1;
  gems += gemBonus;
  petExp += 1;
  
  // Float animation
  let container = document.querySelector('.pet-container');
  let gem = document.createElement('div');
  gem.className = 'float-gem';
  gem.textContent = '💎';
  gem.style.left = '50%';
  gem.style.top = '20%';
  container.appendChild(gem);
  setTimeout(()=>gem.remove(), 800);
  
  saveState();
  checkBadges();
  updatePetUI();
  updateTopbar();
}}

// ===== Tabs =====
function switchTab(tab){{
  document.querySelectorAll('#tab-subjects,#tab-map,#tab-tasks').forEach(el=>el.style.display='none');
  document.querySelectorAll('.nav-tab').forEach(el=>el.classList.remove('active'));
  document.getElementById('tab-'+tab).style.display = 'block';
  event.target.classList.add('active');
  if(tab==='tasks') renderTasks();
  if(tab==='map') renderMap();
}}

// ===== Save/Load =====
function saveState(){{
  localStorage.setItem('la_gems', gems);
  localStorage.setItem('la_petExp', petExp);
  localStorage.setItem('la_petLevel', petLevel);
  localStorage.setItem('la_maxCombo', maxCombo);
  localStorage.setItem('la_totalCorrect', totalCorrect);
  localStorage.setItem('la_totalAnswered', totalAnswered);
}}

// ===== Clouds decoration =====
function genClouds(){{
  let clouds = document.getElementById('clouds');
  for(let i=0;i<5;i++){{
    let c = document.createElement('div');
    let w = 60+Math.random()*80;
    let h = 20+Math.random()*15;
    c.className = 'cloud';
    c.style.cssText = 'width:'+w+'px;height:'+h+'px;top:'+(5+Math.random()*25)+'%;left:'+Math.random()*80+'%;--d:'+(8+Math.random()*6)+'s;--dl:-'+(Math.random()*5)+'s;--dx:'+(20+Math.random()*30)+'px';
    clouds.appendChild(c);
  }}
}}

// ===== Init =====
function init(){{
  // Set today info
  let greetings = ['新的一天，开始冒险吧！🌟','加油，小探险家！🚀','今天也要努力学习哦！💪','知识就是力量！📚'];
  document.getElementById('todayInfo').textContent = greetings[Math.floor(Math.random()*greetings.length)];
  
  genClouds();
  renderSubjects();
  renderTasks();
  renderMap();
  updatePetUI();
  updateTopbar();
  dailyReset();
  
  // Overlay close handlers
  document.getElementById('badgeOverlay').onclick = function(e){{ if(e.target===this) this.classList.remove('active'); }};
  document.getElementById('wrongOverlay').onclick = function(e){{ if(e.target===this) this.classList.remove('active'); }};
  document.getElementById('settingsOverlay').onclick = function(e){{ if(e.target===this) this.classList.remove('active'); }};
  document.getElementById('confirmModal').onclick = function(e){{ if(e.target===this) this.classList.remove('active'); }};
  document.getElementById('quizScreen').onclick = function(e){{ if(e.target===this) closeQuiz(); }};
}}

init();
</script>
</body>
</html>'''

with open('learning-adventure.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✓ learning-adventure.html generated ({len(html.encode("utf-8"))/1024:.0f} KB)')
print(f'  Questions: {len(questions)} (Grades 1-{max(q["grade"] for q in questions)})')
print(f'  Background: school-bg.png added')