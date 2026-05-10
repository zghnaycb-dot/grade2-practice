import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('question_bank.json', 'r', encoding='utf-8') as f:
    qb = json.load(f)

# Convert to JS format
qb_js = json.dumps(qb, ensure_ascii=False, indent=2)
# Fix: convert Python True/False/None to JS true/false/null
qb_js = qb_js.replace('True','true').replace('False','false').replace('None','null')

daily_tasks = [
    {"id":1,"emoji":"📖","title":"语文小达人","desc":"完成5道语文题","target":5,"subject":"chinese","gemReward":15},
    {"id":2,"emoji":"🔢","title":"数学小天才","desc":"完成5道数学题","target":5,"subject":"math","gemReward":15},
    {"id":3,"emoji":"⚡","title":"连击挑战","desc":"连续答对10题","target":10,"combo":True,"gemReward":30},
    {"id":4,"emoji":"🌟","title":"初学者","desc":"完成第一道题","target":1,"gemReward":5},
]
dt_js = json.dumps(daily_tasks, ensure_ascii=False).replace('True','true')

badges = [
    {"id":"first","emoji":"🌟","name":"初次冒险","desc":"完成第一道题"},
    {"id":"combo5","emoji":"🔥","name":"5连击","desc":"连续答对5题"},
    {"id":"combo10","emoji":"⚡","name":"连击王者","desc":"连续答对10题"},
    {"id":"gem50","emoji":"💎","name":"宝石达人","desc":"收集50颗宝石"},
    {"id":"gem100","emoji":"👑","name":"宝石收藏家","desc":"收集100颗宝石"},
    {"id":"petlv2","emoji":"🦊","name":"伙伴诞生","desc":"小狐狸升到2级"},
    {"id":"petlv5","emoji":"🦊✨","name":"伙伴进化","desc":"小狐狸升到5级"},
    {"id":"daily3","emoji":"🏆","name":"今日之星","desc":"完成3个每日任务"},
]
bd_js = json.dumps(badges, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>\U0001f98a 学习大冒险</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--pink:#FF5E8A;--orange:#FF7B3D;--yellow:#FFC107;--green:#2ECC71;--blue:#3498DB;--purple:#9B59B6;--card:#FFF;--text:#2C3E50;--sub:#7F8C8D;--border:#F0F0F0}}
body{{background:linear-gradient(180deg,#E8F4FD 0%,#FFF5F5 30%,#FFFDE7 60%,#F0FFF4 100%);min-height:100vh;font-family:'Noto Sans SC',sans-serif;overflow-x:hidden}}
.clouds{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}}
.cloud{{position:absolute;background:#fff;border-radius:50%;box-shadow:0 8px 30px rgba(0,0,0,.04);opacity:.7;animation:fc var(--d) ease-in-out infinite;animation-delay:var(--dl)}}
@keyframes fc{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(var(--dx))}}}}
.float-e{{position:fixed;pointer-events:none;z-index:0;font-size:1.2em;animation:fu 4s ease-in-out infinite;animation-delay:var(--dl)}}
@keyframes fu{{0%{{transform:translateY(0) scale(0);opacity:0}}20%{{transform:scale(1);opacity:1}}100%{{transform:translateY(-50px) scale(0);opacity:0}}}}
.gem-pop{{position:fixed;top:20%;left:50%;transform:translateX(-50%);font-size:2.5em;z-index:9999;pointer-events:none;animation:gp 1.2s ease-out forwards}}
@keyframes gp{{0%{{transform:translateX(-50%) scale(0);opacity:0}}30%{{transform:translateX(-50%) scale(1.3);opacity:1}}60%{{transform:translateX(-50%) translateY(-20px);opacity:1}}100%{{transform:translateX(-50%) translateY(-60px) scale(.5);opacity:0}}}}
.combo-ban{{position:fixed;top:12%;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,var(--yellow),var(--orange));color:#fff;font-family:'Fredoka One',cursive;font-size:1.8em;padding:6px 28px;border-radius:50px;z-index:9999;pointer-events:none;box-shadow:0 6px 24px rgba(255,152,0,.4);animation:ca 1.4s ease-out forwards}}
@keyframes ca{{0%{{transform:translateX(-50%) scale(0);opacity:0}}20%{{transform:translateX(-50%) scale(1.2);opacity:1}}40%{{transform:translateX(-50%) scale(1)}}80%{{opacity:1}}100%{{transform:translateX(-50%) scale(.7);opacity:0}}}}
.overlay{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.4);z-index:9998}}
.bdg-pop{{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;border-radius:24px;padding:36px;text-align:center;z-index:9999;box-shadow:0 20px 60px rgba(0,0,0,.2);animation:ba .4s ease-out;min-width:260px}}
@keyframes ba{{0%{{transform:translate(-50%,-50%) scale(0)}}70%{{transform:translate(-50%,-50%) scale(1.06)}}100%{{transform:translate(-50%,-50%) scale(1)}}}}
.bdg-pop .big{{font-size:3.6em;display:block;margin-bottom:10px}}
.bdg-pop h2{{color:var(--text);font-family:'Fredoka One',cursive;font-size:1.4em;margin-bottom:4px}}
.bdg-pop p{{color:var(--sub);font-size:.9em}}
.bdg-pop button{{margin-top:18px;padding:10px 28px;border:none;border-radius:50px;background:linear-gradient(135deg,var(--pink),var(--orange));color:#fff;font-weight:700;cursor:pointer;font-size:1em}}
.bar{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:10px 16px;background:rgba(255,255,255,.92);backdrop-filter:blur(20px);box-shadow:0 2px 16px rgba(0,0,0,.06);border-radius:0 0 18px 18px}}
.bar .st{{display:flex;align-items:center;gap:4px;font-weight:700;font-size:.9em;cursor:pointer}}
.bar .lv{{background:linear-gradient(135deg,var(--yellow),var(--orange));color:#fff;padding:4px 12px;border-radius:50px;font-weight:800;font-size:.82em;box-shadow:0 2px 8px rgba(255,152,0,.3)}}
.main{{position:relative;z-index:1;max-width:920px;margin:0 auto;padding:68px 16px 20px}}
.scr{{display:none}}.scr.active{{display:block;animation:fi .3s ease-out}}
@keyframes fi{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
.hero{{text-align:center;padding:28px 16px 12px}}
.hero-badge{{display:inline-block;background:linear-gradient(135deg,var(--pink),var(--orange));color:#fff;font-size:.78em;font-weight:700;padding:5px 16px;border-radius:50px;margin-bottom:12px;box-shadow:0 4px 14px rgba(255,94,138,.25)}}
.hero h1{{font-family:'Fredoka One',cursive;font-size:2.6em;background:linear-gradient(135deg,#FF5E8A 0%,#FF7B3D 35%,#FFC107 70%,#2ECC71 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.2;margin-bottom:2px}}
.hero h1 .sub{{display:block;font-size:.4em;-webkit-text-fill-color:var(--blue);font-family:'Noto Sans SC',sans-serif;letter-spacing:3px}}
.pet-area{{display:flex;justify-content:center;margin:14px 0}}
.pet{{width:100px;height:100px;border-radius:50%;background:linear-gradient(135deg,#FFF9C4,#FFF176);display:flex;align-items:center;justify-content:center;font-size:2.8em;box-shadow:0 6px 24px rgba(255,193,7,.3),inset 0 0 0 3px #fff;animation:pb 1.8s ease-in-out infinite;cursor:pointer;position:relative;transition:transform .2s}}
.pet:hover{{transform:scale(1.06)}}
@keyframes pb{{0%,100%{{transform:translateY(0)}}40%{{transform:translateY(-14px)}}60%{{transform:translateY(-4px)}}}}
.pet-lv{{position:absolute;bottom:-2px;right:-2px;background:linear-gradient(135deg,var(--yellow),var(--orange));color:#fff;font-size:.65em;font-weight:800;padding:2px 7px;border-radius:50px;box-shadow:0 2px 6px rgba(255,152,0,.3)}}
.exp-bar{{width:100px;height:4px;background:#F0F0F0;border-radius:2px;margin-top:5px;overflow:hidden}}
.exp-fill{{height:100%;background:linear-gradient(90deg,var(--yellow),var(--orange));border-radius:2px;transition:width .5s}}
.srow{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0}}
.sc{{background:#fff;border:2px solid var(--border);border-radius:16px;padding:14px 8px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.03)}}
.sc .si{{font-size:1.6em;display:block;margin-bottom:2px}}
.sc .sv{{font-family:'Fredoka One',cursive;font-size:1.4em;color:var(--text)}}
.sc .sl{{color:var(--sub);font-size:.72em;margin-top:2px}}
.slbl{{display:flex;align-items:center;gap:8px;margin:24px 0 12px}}
.slbl .dot{{width:8px;height:8px;border-radius:50%;background:linear-gradient(135deg,var(--pink),var(--orange))}}
.slbl span{{text-transform:uppercase;font-size:.72em;font-weight:800;color:var(--pink);letter-spacing:3px}}
.subs{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:8px}}
@media(max-width:600px){{.subs{{grid-template-columns:repeat(2,1fr)}}}}
.subc{{background:#fff;border:2px solid var(--border);border-radius:16px;padding:14px 6px;text-align:center;cursor:pointer;transition:all .3s;box-shadow:0 2px 6px rgba(0,0,0,.03)}}
.subc:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(0,0,0,.08)}}
.subc:active{{transform:scale(.97)}}
.subc .em{{font-size:2.2em;display:block;margin-bottom:4px}}
.subc h4{{color:var(--text);font-size:.88em;font-weight:700}}
.subc .ct{{color:var(--sub);font-size:.72em;margin-top:2px}}
.subc .bb{{height:4px;background:#F0F0F0;border-radius:2px;margin-top:8px;overflow:hidden}}
.subc .bf{{height:100%;border-radius:2px;transition:width .8s}}
.dcard{{background:#fff;border:2px solid var(--border);border-radius:20px;padding:20px;margin-bottom:8px;box-shadow:0 2px 8px rgba(0,0,0,.03)}}
.dcard .dt{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}
.dcard h3{{font-size:1em;font-weight:900;color:var(--text)}}
.dcard .gb{{background:linear-gradient(135deg,var(--pink),var(--orange));color:#fff;border:none;padding:6px 14px;border-radius:50px;font-weight:700;font-size:.82em;cursor:pointer}}
.tlist{{display:flex;flex-direction:column;gap:8px}}
.ti{{display:flex;align-items:center;gap:10px;padding:10px 12px;background:#F8F9FA;border-radius:12px;border:2px solid transparent;transition:all .3s;cursor:pointer}}
.ti:hover{{border-color:var(--yellow);background:#FFFDE7}}
.ti.done{{background:#F0FFF4;border-color:#A3E635}}
.ti .tic{{font-size:1.4em}}
.ti .tinfo{{flex:1}}
.ti .tt{{font-weight:700;font-size:.9em;color:var(--text)}}
.ti .td{{font-size:.76em;color:var(--sub)}}
.ti .tp{{font-weight:800;font-size:.82em;color:var(--text)}}
.bg{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}}
@media(max-width:600px){{.bg{{grid-template-columns:repeat(4,1fr)}}}}
.bi{{text-align:center;padding:8px 2px;border-radius:12px;background:#F8F9FA;border:2px solid #F0F0F0;transition:all .3s}}
.bi.unlocked{{background:#FFFDE7;border-color:#FFE082}}
.bi .bico{{font-size:1.6em;display:block;margin-bottom:2px}}
.bi .bn{{font-size:.64em;font-weight:600;color:var(--text)}}
.bi.locked .bico{{filter:grayscale(1);opacity:.35}}
.bi.locked .bn{{color:#BDC3C7}}
.wh{{display:flex;justify-content:space-between;align-items:center;padding:18px 0 14px}}
.wh h2{{font-family:'Fredoka One',cursive;font-size:1.6em;color:var(--text)}}
.bbtn{{background:#fff;border:2px solid var(--border);border-radius:50px;padding:8px 16px;font-weight:700;cursor:pointer;font-size:.88em}}
.stitle{{display:flex;align-items:center;gap:8px;margin-bottom:16px}}
.stitle .em{{font-size:1.8em}}
.stitle h3{{font-size:1.2em;font-weight:900;color:var(--text)}}
.mscroll{{overflow-x:auto;padding:8px 0 16px}}
.mcont{{display:flex;align-items:center;gap:0;min-width:max-content;padding:18px 24px;background:#fff;border-radius:20px;box-shadow:0 4px 16px rgba(0,0,0,.04);border:2px solid var(--border)}}
.mn{{min-width:76px;text-align:center;position:relative;cursor:pointer}}
.mn .nc{{width:48px;height:48px;border-radius:50%;margin:0 auto 5px;display:flex;align-items:center;justify-content:center;font-size:1.2em;border:3px solid #EEE;background:#fff;transition:all .3s}}
.mn.done .nc{{background:linear-gradient(135deg,#2ECC71,#1ABC9C);border-color:#2ECC71;box-shadow:0 3px 12px rgba(46,204,113,.3);color:#fff}}
.mn.current .nc{{background:linear-gradient(135deg,#FFC107,#FF9800);border-color:#FFC107;box-shadow:0 3px 16px rgba(255,152,0,.4);animation:pn 2s ease-in-out infinite;color:#fff}}
@keyframes pn{{0%,100%{{box-shadow:0 3px 16px rgba(255,152,0,.4)}}50%{{box-shadow:0 6px 28px rgba(255,152,0,.6)}}}}
.mn.locked .nc{{opacity:.4}}
.mn .nn{{font-size:.68em;font-weight:700;color:var(--sub)}}
.mn.done .nn{{color:#2ECC71}}
.mn.current .nn{{color:#F57F17}}
.mc{{width:32px;height:3px;background:#EEE;border-radius:2px;flex-shrink:0;margin-top:-24px}}
.mc.done{{background:linear-gradient(90deg,#2ECC71,#1ABC9C)}}
.ph{{display:flex;justify-content:space-between;align-items:center;padding:14px 0 10px}}
.ph h2{{font-size:1.1em;font-weight:900;color:var(--text)}}
.pbar{{display:flex;align-items:center;gap:8px;margin-bottom:12px}}
.pbar .pb{{flex:1;height:6px;background:#F0F0F0;border-radius:3px;overflow:hidden}}
.pbar .pf{{height:100%;border-radius:3px;transition:width .5s;background:linear-gradient(90deg,var(--blue),var(--purple))}}
.pbar .pt{{font-weight:800;font-size:.85em;color:var(--text);min-width:36px;text-align:right}}
.cbdg{{display:flex;align-items:center;justify-content:center;gap:6px;margin-bottom:14px}}
.cbdg .cb{{display:inline-flex;align-items:center;gap:3px;padding:5px 14px;border-radius:50px;font-weight:800;font-size:.88em}}
.cbdg .cb.active{{background:linear-gradient(135deg,var(--yellow),var(--orange));color:#fff;box-shadow:0 3px 12px rgba(255,152,0,.3);animation:cp .4s ease-out}}
@keyframes cp{{0%{{transform:scale(1.3)}}100%{{transform:scale(1)}}}}
.cbdg .cb.inactive{{background:#F0F0F0;color:#BDC3C7}}
.qcard{{background:#fff;border-radius:20px;padding:24px 20px;box-shadow:0 3px 18px rgba(0,0,0,.05);border:2px solid var(--border);margin-bottom:16px}}
.qcard .qr{{display:inline-block;background:#EBF5FF;color:var(--blue);font-size:.72em;font-weight:700;padding:3px 10px;border-radius:50px;margin-bottom:10px}}
.qcard .qt{{font-size:1.15em;font-weight:700;color:var(--text);line-height:1.5;margin-bottom:6px}}
.qcard .qy{{display:inline-block;background:#FFF3E0;color:var(--orange);font-size:.68em;font-weight:700;padding:2px 8px;border-radius:50px;margin-left:6px}}
.olist{{display:flex;flex-direction:column;gap:8px;margin-top:14px}}
.oi{{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:#fff;border:2px solid var(--border);cursor:pointer;transition:all .2s;font-size:1em;font-weight:600;color:var(--text)}}
.oi:hover:not(.dis){{border-color:var(--blue);background:#EBF5FF;transform:translateX(3px)}}
.oi:active:not(.dis){{transform:scale(.98)}}
.oi.ok{{border-color:#2ECC71;background:#F0FFF4;color:#2ECC71}}
.oi.no{{border-color:#E74C3C;background:#FFEAEA;color:#E74C3C}}
.oi.dis{{cursor:default;opacity:.7}}
.oi .ol{{min-width:28px;height:28px;border-radius:50%;background:#F0F0F0;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.82em}}
.oi.ok .ol{{background:#2ECC71;color:#fff}}
.oi.no .ol{{background:#E74C3C;color:#fff}}
.fiw{{margin-top:14px}}
.finp{{width:100%;padding:12px 14px;border-radius:12px;border:2px solid var(--border);font-size:1em;font-weight:600;outline:none;transition:all .2s;font-family:'Noto Sans SC',sans-serif;color:var(--text)}}
.finp:focus{{border-color:var(--blue);background:#F8FBFF}}
.sbtn{{width:100%;padding:14px;border:none;border-radius:16px;background:linear-gradient(135deg,var(--pink),var(--orange));color:#fff;font-size:1.05em;font-weight:900;cursor:pointer;box-shadow:0 4px 18px rgba(255,94,138,.3);transition:all .2s;margin-top:12px;font-family:'Noto Sans SC',sans-serif}}
.sbtn:hover{{transform:translateY(-2px);box-shadow:0 8px 26px rgba(255,94,138,.4)}}
.sbtn:active{{transform:scale(.98)}}
.sbtn:disabled{{opacity:.5;cursor:not-allowed;transform:none}}
.rban{{background:#fff;border-radius:20px;padding:28px 20px;text-align:center;box-shadow:0 3px 18px rgba(0,0,0,.05);margin-bottom:14px;border:2px solid var(--border)}}
.rban .re{{font-size:3.5em;display:block;margin-bottom:8px}}
.rban h2{{font-family:'Fredoka One',cursive;font-size:1.8em;color:var(--text)}}
.rban .rs{{color:var(--sub);font-size:.9em;margin:6px 0 14px}}
.rstats{{display:flex;justify-content:center;gap:20px;margin-bottom:18px}}
.rstats .ri{{text-align:center}}
.rstats .rv{{font-family:'Fredoka One',cursive;font-size:1.6em}}
.rstats .rl{{font-size:.76em;color:var(--sub)}}
.rstats .ok .rv{{color:#2ECC71}}
.rstats .no .rv{{color:#E74C3C}}
.rstats .gem .rv{{color:#FF5E8A}}
.arow{{display:flex;gap:10px}}
.abtn{{flex:1;padding:12px;border:none;border-radius:16px;font-size:.95em;font-weight:800;cursor:pointer;font-family:'Noto Sans SC',sans-serif;transition:all .2s}}
.abtn.pri{{background:linear-gradient(135deg,var(--pink),var(--orange));color:#fff;box-shadow:0 4px 16px rgba(255,94,138,.3)}}
.abtn.sec{{background:#fff;color:var(--text);border:2px solid var(--border)}}
.abtn:hover{{transform:translateY(-2px)}}
.abtn:active{{transform:scale(.97)}}
.wi{{background:#fff;border:2px solid #FFCDD2;border-radius:14px;padding:14px;margin-bottom:8px}}
.wi .wq{{font-weight:700;color:var(--text);font-size:.9em;margin-bottom:6px}}
.wi .wa{{color:#2ECC71;font-size:.84em}}
.wi .wy{{color:#E74C3C;font-size:.84em}}
.setrow{{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--border)}}
.setrow:last-child{{border-bottom:none}}
.setrow h4{{font-weight:700;color:var(--text)}}
.setrow p{{font-size:.8em;color:var(--sub);margin-top:2px}}
.tgl{{width:44px;height:24px;border-radius:12px;border:none;cursor:pointer;position:relative;transition:all .3s}}
.tgl.on{{background:linear-gradient(135deg,var(--green),#27AE60)}}
.tgl.off{{background:#E0E0E0}}
.tgl::after{{content:'';position:absolute;top:3px;left:3px;width:18px;height:18px;background:#fff;border-radius:50%;transition:all .3s;box-shadow:0 1px 3px rgba(0,0,0,.2)}}
.tgl.on::after{{left:23px}}
.smbtn{{padding:8px 16px;border-radius:50px;border:none;font-weight:700;cursor:pointer;font-size:.85em;font-family:'Noto Sans SC',sans-serif}}
.smbtn.danger{{background:#FFEAEA;color:#E74C3C}}
@media(max-width:600px){{.hero h1{{font-size:2em}}.srow{{grid-template-columns:1fr 1fr}}.subs{{grid-template-columns:1fr 1fr}}.qcard .qt{{font-size:1.05em}}}}
</style>
</head>
<body>
<div class="clouds" id="clouds"></div>
<div id="floats"></div>
<div class="overlay" id="ovl" style="display:none" onclick="closeBP()"></div>
<div class="bdg-pop" id="bpop" style="display:none"><span class="big" id="bpE"></span><h2 id="bpT"></h2><p id="bpD"></p><button onclick="closeBP()">太棒了！</button></div>
<div class="bar"><div class="st" onclick="go('home')"><span style="font-size:1.2em">\U0001f98a</span><span id="lvD">Lv.1</span></div><div class="lv" id="gemD">\U0001f48e 0</div><div class="st" onclick="go('badges')"><span style="font-size:1.1em">\U0001f3c5</span><span id="bdgC">0/8</span></div></div>
<main class="main">
<div class="scr active" id="s-home">
<section class="hero"><div class="hero-badge">\u2726 学习大冒险 \u2726</div><h1>学习大冒险<span class="sub">LEARNING ADVENTURE</span></h1></section>
<div class="pet-area"><div style="text-align:center"><div class="pet" onclick="tapPet()">\U0001f98a</div><div class="pet-lv" id="plv">Lv.1</div><div class="exp-bar"><div class="exp-fill" id="pexp" style="width:0%"></div></div><div style="font-size:.68em;color:var(--sub);margin-top:3px">点击小狐狸</div></div></div>
<div class="srow"><div class="sc"><span class="si">\U0001f4d6</span><div class="sv" id="sDone">0</div><div class="sl">已完成</div></div><div class="sc"><span class="si">\U0001f525</span><div class="sv" id="sCombo">0</div><div class="sl">最高连击</div></div><div class="sc"><span class="si">\U0001f3c5</span><div class="sv" id="sBdg">0</div><div class="sl">徽章</div></div></div>
<div class="slbl"><div class="dot"></div><span>每日任务</span></div>
<div class="dcard"><div class="dt"><h3>\U0001f4cb 今日挑战</h3><button class="gb" id="dgT">\U0001f48e 0</button></div><div class="tlist" id="tList"></div></div>
<div class="slbl"><div class="dot" style="background:var(--green)"></div><span>开始练习</span></div>
<div class="subs" id="subRow"></div>
<div class="slbl"><div class="dot" style="background:var(--yellow)"></div><span>徽章收集</span></div>
<div class="dcard"><div class="bg" id="bGrid"></div></div>
<div style="text-align:center;padding:16px 0"><button class="smbtn" style="background:#F8F9FA;color:var(--sub);border:1px solid var(--border);margin:3px" onclick="go('settings')">\u2699\ufe0f 设置</button><button class="smbtn" style="background:#FFF3E0;color:var(--orange);margin:3px" onclick="go('wrong')">\U0001f4dd 错题本</button></div>
</div>
<div class="scr" id="s-world">
<div class="wh"><h2>\U0001f5fa\ufe0f 冒险地图</h2><button class="bbtn" onclick="go('home')">\u2190 返回</button></div>
<div class="stitle" id="sTtl"></div>
<div class="mscroll"><div class="mcont" id="mCont"></div></div>
<div style="text-align:center;margin-top:16px"><button class="abtn pri" style="max-width:280px;margin:0 auto" onclick="startFromMap()">\U0001f680 进入练习</button></div>
</div>
<div class="scr" id="s-practice">
<div class="ph"><button class="bbtn" onclick="quitP()">\u2715 退出</button><h2 id="pSubj"></h2><div style="font-weight:800;color:var(--pink)">\U0001f48e <span id="cGem">0</span></div></div>
<div class="pbar"><div class="pb"><div class="pf" id="pFill" style="width:0%"></div></div><span class="pt" id="pTxt">0/0</span></div>
<div class="cbdg"><div class="cb inactive" id="cBadge"><span>\U0001f525</span> 连击 <span id="cNum">0</span></div></div>
<div class="qcard" id="qCard"><div id="qCont"></div></div>
<div id="pRes" style="display:none"></div>
</div>
<div class="scr" id="s-badges">
<div class="wh"><h2>\U0001f3c5 徽章收集册</h2><button class="bbtn" onclick="go('home')">\u2190 返回</button></div>
<div class="dcard"><div class="bg" id="fbGrid"></div></div>
</div>
<div class="scr" id="s-wrong">
<div class="wh"><h2>\U0001f4dd 错题本</h2><button class="bbtn" onclick="go('home')">\u2190 返回</button></div>
<div id="wCont"></div>
</div>
<div class="scr" id="s-settings">
<div class="wh"><h2>\u2699\ufe0f 设置</h2><button class="bbtn" onclick="go('home')">\u2190 返回</button></div>
<div class="dcard"><div class="setrow"><div><h4>音效</h4><p>答对/答错音效</p></div><button class="tgl on" id="sndTgl" onclick="tglSnd()"></button></div><div class="setrow"><div><h4>震动反馈</h4><p>答对震动</p></div><button class="tgl on" id="vibTgl" onclick="tglVib()"></button></div></div>
<div class="dcard"><div class="setrow" style="border:none"><div><h4>重置进度</h4><p>清空所有数据</p></div><button class="smbtn danger" onclick="resetAll()">重置</button></div></div>
</div>
</main>
<script>
var QB={qb_js};
var DT={dt_js};
var BD={bd_js};
var S={{gems:0,petLv:1,petExp:0,petNext:10,maxC:0,curC:0,done:0,doneSub:{{chinese:0,math:0,english:0}},comp:[],wrong:[],badges:[],snd:true,vib:true,selSubj:null,selReg:null,pq:[],pi:0,pc:0,pw:0,daily:{{}}}};
function init(){{load();mkClouds();mkFloats();renderTasks();renderSubs();renderBdg();upStats()}}
function mkClouds(){{var c=document.getElementById('clouds');for(var i=0;i<5;i++){{var d=document.createElement('div');d.className='cloud';var w=80+Math.random()*100;var h=25+Math.random()*35;d.style.cssText='width:'+w+'px;height:'+h+'px;top:'+(5+Math.random()*80)+'%;left:'+(Math.random()*90)+'%;--d:'+(10+Math.random()*12)+'s;--dl:'+(Math.random()*6)+'s;--dx:'+(20+Math.random()*40)+'px';c.appendChild(d)}}}}
function mkFloats(){{var f=document.getElementById('floats');var em=['✨','⭐','💫','🌟','⚡','🦊'];setInterval(function(){{if(f.children.length>6)return;var e=document.createElement('div');e.className='float-e';e.textContent=em[Math.floor(Math.random()*em.length)];e.style.cssText='top:'+(10+Math.random()*80)+'%;left:'+(5+Math.random()*90)+'%;--dl:'+(Math.random()*3)+'s';f.appendChild(e);setTimeout(function(){{e.remove()}},4500)}},3500)}}
function save(){{localStorage.setItem('la',JSON.stringify(S))}}
function load(){{var s=localStorage.getItem('la');if(s){{var p=JSON.parse(s);for(var k in p)S[k]=p[k]}}}}
function go(id){{document.querySelectorAll('.scr').forEach(function(s){{s.classList.remove('active')}});if(id==='wrong')renderWrong();document.getElementById('s-'+id).classList.add('active')}}
function upStats(){{document.getElementById('lvD').textContent='Lv.'+S.petLv;document.getElementById('gemD').textContent='💎 '+S.gems;document.getElementById('sDone').textContent=S.done;document.getElementById('sCombo').textContent=S.maxC;document.getElementById('sBdg').textContent=S.badges.length;document.getElementById('bdgC').textContent=S.badges.length+'/'+BD.length;document.getElementById('plv').textContent='Lv.'+S.petLv;document.getElementById('pexp').style.width=(S.petExp/S.petNext*100)+'%';['chinese','math','english'].forEach(function(s){{var t=QB.filter(function(q){{return q.subject===s}}).length;var d=S.doneSub[s]||0;var b=document.querySelector('#sub-'+s+' .bf');if(b){{b.style.width=(d/t*100)+'%';if(s==='chinese')b.style.background='linear-gradient(90deg,#FF5E8A,#FF7B3D)';if(s==='math')b.style.background='linear-gradient(90deg,#3498DB,#9B59B6)';if(s==='english')b.style.background='linear-gradient(90deg,#9B59B6,#FF5E8A)'}}}});renderBdg();renderTasks()}}
function tapPet(){{showGP('💎');addG(1);addPE(1);vib(50)}}
function renderTasks(){{var l=document.getElementById('tList');l.innerHTML='';var tg=0;DT.forEach(function(t){{var p=S.daily[t.id]||0;var d=p>=t.target;var g=d?t.gemReward:0;tg+=g;var it=document.createElement('div');it.className='ti'+(d?' done':'');it.innerHTML='<span class="tic">'+t.emoji+'</span><div class="tinfo"><div class="tt">'+t.title+'</div><div class="td">'+t.desc+'</div></div><div><div class="tp">'+p+'/'+t.target+'</div>'+(g>0?'<div style="font-size:.85em">+'+g+'💎</div>':'')+'</div>';it.onclick=function(){{claimT(t)}};l.appendChild(it)}});document.getElementById('dgT').textContent='💎 '+tg}}
function claimT(t){{var p=S.daily[t.id]||0;if(p<t.target){{toast('继续加油！还差'+(t.target-p)+'题');return}}if(t.gemReward>0){{addG(t.gemReward);showGP('💎 x'+t.gemReward);t.gemReward=0;S.daily[t.id]=-1;save();renderTasks();chkBdg('daily3')}}}}
function renderSubs(){{var r=document.getElementById('subRow');r.innerHTML='';var ss=[{{id:'chinese',emoji:'📖',name:'语文'}},{{id:'math',emoji:'🔢',name:'数学'}},{{id:'english',emoji:'🔤',name:'英语'}},{{id:'mixed',emoji:'🧪',name:'综合'}}];ss.forEach(function(s){{var t=QB.filter(function(q){{return s.id==='mixed'||q.subject===s.id}}).length;var d=0;if(s.id==='mixed')d=S.done;else d=S.doneSub[s.id]||0;var div=document.createElement('div');div.className='subc';div.id='sub-'+s.id;div.innerHTML='<span class="em">'+s.emoji+'</span><h4>'+s.name+'</h4><div class="ct">'+d+'/'+t+'题</div><div class="bb"><div class="bf" style="width:'+((t?d/t:0)*100)+'%"></div></div>';div.onclick=function(){{startP(s.id==='mixed'?null:s.id)}};r.appendChild(div)}})}}
function selSubj(s){{S.selSubj=s;var regs=[];QB.forEach(function(q){{if(q.subject!==s)return;var ex=false;for(var i=0;i<regs.length;i++)if(regs[i].name===q.region)ex=true;if(!ex)regs.push({{name:q.region,total:0,done:0}})}});QB.forEach(function(q){{if(q.subject!==s)return;for(var i=0;i<regs.length;i++){{if(regs[i].name===q.region){{regs[i].total++;if(S.comp.indexOf(q.id)>=0)regs[i].done++;break}}}}}});var nm={{chinese:'📖 语文王国',math:'🔢 数学迷宫',english:'🔤 英语森林'}};document.getElementById('sTtl').innerHTML='<span class="em">'+(s==='chinese'?'📖':s==='math'?'🔢':'🔤')+'</span><h3>'+nm[s]+'</h3>';var c=document.getElementById('mCont');c.innerHTML='';regs.forEach(function(r,i){{if(i>0){{var cn=document.createElement('div');cn.className='mc'+(r.done>0?' done':'');c.appendChild(cn)}}var n=document.createElement('div');var st=r.done===0?(i===0?'current':'locked'):'done';n.className='mn '+st;n.innerHTML='<div class="nc">'+(r.done>0?'✅':(i===0?r.name[0]:'🔒'))+'</div><div class="nn">'+r.name+'</div>';n.onclick=function(){{S.selReg=r.name}};c.appendChild(n)}});go('world')}}
function startP(subj){{if(subj){{selSubj(subj);return}}var pool=QB.filter(function(q){{return S.comp.indexOf(q.id)<0}});if(!pool.length){{toast('全部完成啦！🎉');return}}shuf(pool);S.pq=pool.slice(0,Math.min(10,pool.length));S.pi=0;S.pc=0;S.pw=0;S.selSubj='mixed';showP()}}
function startFromMap(){{if(!S.selSubj)return;var pool=QB.filter(function(q){{if(q.subject!==S.selSubj)return false;if(S.selReg&&q.region!==S.selReg)return false;return S.comp.indexOf(q.id)<0}});if(!pool.length){{toast('这个区域已经完成啦！🎉');return}}shuf(pool);S.pq=pool.slice(0,Math.min(10,pool.length));S.pi=0;S.pc=0;S.pw=0;showP()}}
function showP(){{var nm={{chinese:'📖 语文',math:'🔢 数学',english:'🔤 英语',mixed:'🧪 综合'}};document.getElementById('pSubj').textContent=nm[S.selSubj];document.getElementById('cGem').textContent=S.gems;go('practice');renderQ()}}
function renderQ(){{if(S.pi>=S.pq.length){{showRes();return}}var q=S.pq[S.pi];var t=S.pq.length;var i=S.pi+1;document.getElementById('pFill').style.width=(i/t*100)+'%';document.getElementById('pTxt').textContent=i+'/'+t;document.getElementById('cNum').textContent=S.curC;var cb=document.getElementById('cBadge');cb.className='cb '+(S.curC>=2?'active':'inactive');var tl={{choice:'选择题',fill:'填空题'}};var h='<div class="qr">'+q.region+'</div><div class="qt">'+q.question+'</div><span class="qy">'+(tl[q.type]||'练习')+'</span>';if(q.type==='fill'){{h+='<div class="fiw"><input class="finp" id="fAns" placeholder="请输入答案..." onkeydown="if(event.key===\\'Enter\\')submitF()"></div><button class="sbtn" onclick="submitF()">确认答案 ✓</button>'}}else{{var lt=['A','B','C','D'];h+='<div class="olist">';q.options.forEach(function(o,j){{h+='<div class="oi" id="opt'+j+'" onclick="selOpt('+j+')"><span class="ol">'+lt[j]+'</span><span>'+o+'</span></div>'}});h+='</div><button class="sbtn" id="cfmBtn" onclick="cfmAns()" style="display:none">确认答案 ✓</button>'}}document.getElementById('qCont').innerHTML=h;document.getElementById('qCard').style.display='block';document.getElementById('pRes').style.display='none';if(q.type==='fill')setTimeout(function(){{var e=document.getElementById('fAns');if(e)e.focus()}},100);W.selAns=null;W.ansd=false}}
function selOpt(j){{if(W.ansd)return;document.querySelectorAll('.oi').forEach(function(e){{e.style.borderColor='var(--border)';e.style.background='#fff'}});var e=document.getElementById('opt'+j);e.style.borderColor='var(--blue)';e.style.background='#EBF5FF';W.selAns=j;document.getElementById('cfmBtn').style.display='block'}}
function cfmAns(){{if(W.ansd||W.selAns===null)return;W.ansd=true;var q=S.pq[S.pi];var ok=W.selAns===q.answer;document.querySelectorAll('.oi').forEach(function(e){{e.classList.add('dis')}});document.getElementById('opt'+q.answer).classList.add('ok');if(!ok)document.getElementById('opt'+W.selAns).classList.add('no');document.getElementById('cfmBtn').style.display='none';setTimeout(function(){{procRes(ok,q)}},700)}}
function submitF(){{if(W.ansd)return;var inp=document.getElementById('fAns');if(!inp)return;var ua=inp.value.trim();if(!ua){{toast('请输入答案');return}}W.ansd=true;var q=S.pq[S.pi];var ans=q.answer.split('|');var ok=ans.indexOf(ua)>=0;inp.style.borderColor=ok?'#2ECC71':'#E74C3C';inp.style.background=ok?'#F0FFF4':'#FFEAEA';setTimeout(function(){{procRes(ok,q,ua)}},700)}}
function procRes(ok,q,ua){{S.done++;if(!S.doneSub[q.subject])S.doneSub[q.subject]=0;S.doneSub[q.subject]++;if(ok){{S.curC++;if(S.curC>S.maxC)S.maxC=S.curC;S.pc++;var g=1+Math.floor(S.curC/3);addG(g);addPE(3);showGP('💎 +'+g);showCmb();chkTP(q);chkBdg('first');if(S.curC>=5)chkBdg('combo5');if(S.curC>=10)chkBdg('combo10');if(S.gems>=50)chkBdg('gem50');if(S.gems>=100)chkBdg('gem100')}}else{{S.curC=0;S.pw++;addWB(q,ua||'未作答');showGP('❌')}}if(ok&&S.comp.indexOf(q.id)<0)S.comp.push(q.id);document.getElementById('cNum').textContent=S.curC;upStats();S.pi++;W.ansd=false;W.selAns=null;renderQ()}}
function showRes(){{document.getElementById('qCard').style.display='none';var r=document.getElementById('pRes');r.style.display='block';var p=Math.round(S.pc/(S.pc+S.pw)*100)||0;var e=p>=80?'🎉':p>=50?'👍':'💪';var t=p>=80?'太厉害了！':p>=50?'不错的表现！':'继续加油！';r.innerHTML='<div class="rban"><span class="re">'+e+'</span><h2>'+t+'</h2><div class="rs">本次练习完成！</div><div class="rstats"><div class="ri ok"><div class="rv">'+S.pc+'</div><div class="rl">正确</div></div><div class="ri no"><div class="rv">'+S.pw+'</div><div class="rl">错误</div></div><div class="ri gem"><div class="rv">+'+S.pc+'</div><div class="rl">宝石</div></div></div></div><div class="arow"><button class="abtn sec" onclick="go(\\'home\\');renderSubs();upStats()">返回首页</button><button class="abtn pri" onclick="startP(S.selSubj)">再来一轮</button></div>';save()}}
function renderBdg(){{['bGrid','fbGrid'].forEach(function(gid){{var g=document.getElementById(gid);if(!g)return;g.innerHTML='';BD.forEach(function(b){{var u=S.badges.indexOf(b.id)>=0;var d=document.createElement('div');d.className='bi'+(u?' unlocked':' locked');d.innerHTML='<span class="bico">'+b.emoji+'</span><div class="bn">'+b.name+'</div>';d.title=b.desc;g.appendChild(d)}})}})}}
function chkBdg(id){{if(S.badges.indexOf(id)>=0)return;var c={{first:S.done>=1,combo5:S.maxC>=5,combo10:S.maxC>=10,gem50:S.gems>=50,gem100:S.gems>=100,petlv2:S.petLv>=2,petlv5:S.petLv>=5}};if(c[id]){{S.badges.push(id);var b=null;for(var i=0;i<BD.length;i++)if(BD[i].id===id)b=BD[i];if(b)showBP(b);save();upStats()}}}}
function addWB(q,ua){{var ex=false;for(var i=0;i<S.wrong.length;i++)if(S.wrong[i].id===q.id)ex=true;if(!ex){{S.wrong.push({{id:q.id,question:q.question,answer:q.answer,options:q.options,userAns:ua}});save()}}}}
function renderWrong(){{var c=document.getElementById('wCont');if(!S.wrong.length){{c.innerHTML='<div class="dcard" style="text-align:center;padding:36px"><span style="font-size:3em;display:block;margin-bottom:8px">🎉</span><h3 style="color:var(--text)">暂无错题</h3><p style="color:var(--sub);margin-top:6px">太棒了，全部正确！</p></div>';return}}var h='<div class="dcard"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><h3>错题 ('+S.wrong.length+'道)</h3><button class="smbtn danger" onclick="clrW()">清空</button></div>';S.wrong.forEach(function(w){{var a=typeof w.answer==='number'&&w.options?w.options[w.answer]:w.answer;h+='<div class="wi"><div class="wq">❓ '+w.question+'</div><div class="wa">✓ 正确答案：'+a+'</div><div class="wy">✗ 你的答案：'+w.userAns+'</div></div>'}});h+='</div>';c.innerHTML=h}}
function clrW(){{S.wrong=[];save();renderWrong()}}
function shuf(a){{for(var i=a.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}}}}
function addG(n){{S.gems+=n;save()}}
function addPE(n){{S.petExp+=n;while(S.petExp>=S.petNext){{S.petExp-=S.petNext;S.petLv++;S.petNext=S.petLv*10;chkBdg('petlv2');chkBdg('petlv5');showGP('⭐ 升级！Lv.'+S.petLv)}}save()}}
function showGP(t){{var d=document.createElement('div');d.className='gem-pop';d.textContent=t;document.body.appendChild(d);setTimeout(function(){{d.remove()}},1300)}}
function showCmb(){{if(S.curC<2)return;var d=document.createElement('div');d.className='combo-ban';d.textContent='🔥 '+S.curC+' 连击！';document.body.appendChild(d);setTimeout(function(){{d.remove()}},1500)}}
function showBP(b){{document.getElementById('bpE').textContent=b.emoji;document.getElementById('bpT').textContent=b.name+' 🏅';document.getElementById('bpD').textContent=b.desc;document.getElementById('ovl').style.display='block';document.getElementById('bpop').style.display='block';vib(200)}}
function closeBP(){{document.getElementById('ovl').style.display='none';document.getElementById('bpop').style.display='none'}}
function toast(m){{var d=document.createElement('div');d.style.cssText='position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:10px 22px;border-radius:50px;font-weight:700;z-index:9999;font-size:.9em;box-shadow:0 4px 14px rgba(0,0,0,.3)';d.textContent=m;document.body.appendChild(d);setTimeout(function(){{d.remove()}},2000)}}
function vib(ms){{if(S.vib&&navigator.vibrate)navigator.vibrate(ms)}}
function quitP(){{if(S.pi>0){{if(confirm('确定退出吗？')){{save();go('home');renderSubs();upStats()}}}}else{{go('home')}}}}
function tglSnd(){{S.snd=!S.snd;document.getElementById('sndTgl').className='tgl '+(S.snd?'on':'off');save()}}
function tglVib(){{S.vib=!S.vib;document.getElementById('vibTgl').className='tgl '+(S.vib?'on':'off');save()}}
function resetAll(){{if(confirm('确定重置所有进度？不可恢复！')){{localStorage.removeItem('la');location.reload()}}}}
function chkTP(q){{DT.forEach(function(t){{var p=S.daily[t.id]||0;if(p<0)return;if(t.subject&&t.subject!==q.subject)return;if(t.combo)return;if(!t.combo){{var d=S.doneSub[t.subject]||0;if(d>=t.target)S.daily[t.id]=t.target}}}});save();renderTasks()}}
var W={{selAns:null,ansd:false}};
init();
</script>
</body>
</html>'''

with open('learning-adventure.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'App created: learning-adventure.html ({len(html)} bytes)')
print(f'Questions: {len(qb)}')