import json

d = json.load(open('/tmp/slides.json', encoding='utf-8'))
CLUSTERS = d['clusters']
SLIDES = d['slides']
by_id = {c['id']: c for c in CLUSTERS}

PLAY_ORDER = []
for c in CLUSTERS:
    for s in SLIDES[c['id']]:
        PLAY_ORDER.append(s['id'])

slide_cluster = {}
for c in CLUSTERS:
    for s in SLIDES[c['id']]:
        slide_cluster[s['id']] = c['id']

CSS = r"""
:root{
  --bg:#F3F5F8; --surface:#FFFFFF; --surface-2:#E7ECF1; --surface-3:#DCE3EA;
  --ink:#151E27; --ink-dim:#57646F; --border:#D2DAE1;
  --accent:#1B6E8C; --accent-strong:#0F4F66; --accent-soft:#DCEEF4;
  --shadow: 0 1px 2px rgba(21,30,39,.06), 0 8px 24px -12px rgba(21,30,39,.18);
}
*{box-sizing:border-box;}
html,body{margin:0; background:var(--bg); color:var(--ink);}
body{font-family:'IBM Plex Sans','Noto Sans TC',ui-sans-serif,system-ui,sans-serif; line-height:1.6;}
h1,h2,h3{margin:0 0 .3em; text-wrap:balance;}
p{margin:0 0 .8em;}
::selection{background:var(--accent-soft); color:var(--accent-strong);}
@media (prefers-reduced-motion: reduce){ *{animation-duration:.001ms !important; transition-duration:.001ms !important;} }
.mono,code{font-family:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9em;}

.screen{display:none;}
.screen.active{display:block;}

/* ---------- slide screen ---------- */
#slide{min-height:100vh; display:flex; flex-direction:column;}
.slide-topbar{position:sticky; top:0; z-index:5; background:var(--surface); border-bottom:1px solid var(--border); box-shadow:var(--shadow); padding:10px 24px; display:flex; align-items:center; gap:14px; flex-wrap:wrap;}
.outlineBtn{all:unset; cursor:pointer; font-weight:600; font-size:.85rem; padding:7px 15px; border-radius:999px;}
.outlineBtn{color:var(--ink); background:var(--surface-2); border:1px solid var(--border);}
.outlineBtn:hover{border-color:var(--accent); color:var(--accent-strong);}
.crumb{font-size:.85rem; color:var(--ink-dim);}
.crumb b{color:var(--accent-strong);}
.progress{margin-left:auto; font-family:'IBM Plex Mono',monospace; font-size:.78rem; color:var(--ink-dim);}
.progress-bar{height:3px; background:var(--surface-2);}
.progress-bar i{display:block; height:100%; background:var(--accent); transition:width .2s ease;}

.slide-main{flex:1; display:flex; align-items:center; justify-content:center; padding:40px 24px 60px; cursor:pointer;}
.slide-main button, .slide-main a{cursor:pointer;}
.slide-bullets, .slide-title, figcaption{cursor:pointer;}
.slide-card{max-width:820px; width:100%;}

.cover-block{text-align:center; padding:40px 10px;}
.cover-eyebrow{font-family:'IBM Plex Mono',monospace; font-size:.85rem; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); font-weight:700;}
.cover-title{font-size:2.6rem; color:var(--accent-strong); margin-top:18px; line-height:1.3;}
.cover-subtitle{color:var(--ink-dim); font-size:1.1rem; margin-top:16px; max-width:52ch; margin-left:auto; margin-right:auto;}
.slide-eyebrow{font-family:'IBM Plex Mono',monospace; font-size:.78rem; letter-spacing:.08em; text-transform:uppercase; color:var(--accent); font-weight:700; display:flex; align-items:center; gap:10px;}
.slide-eyebrow .src{background:var(--surface-2); color:var(--ink-dim); padding:1px 9px; border-radius:999px; font-weight:600; letter-spacing:0; text-transform:none;}
.slide-title{font-size:1.5rem; color:var(--accent-strong); margin-top:10px; line-height:1.4;}
.slide-bullets{list-style:none; margin:22px 0 0; padding:0; display:flex; flex-direction:column; gap:14px;}
.slide-bullets li{position:relative; padding-left:26px; font-size:1.12rem; color:var(--ink); max-width:70ch;}
.slide-bullets li::before{content:"—"; position:absolute; left:0; color:var(--accent);}

.diagram{background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:18px; margin:22px 0 4px; overflow-x:auto; box-shadow:var(--shadow);}
.diagram svg{display:block; margin:0 auto;}
.diagram .dg-box{fill:var(--surface-2); stroke:var(--border); stroke-width:1.5;}
.diagram .dg-box.accent{fill:var(--accent-soft); stroke:var(--accent);}
.diagram .dg-line{stroke:var(--ink-dim); stroke-width:1.5; fill:none;}
.diagram .dg-text{fill:var(--ink); font-size:12.5px;}
.diagram .dg-mono{fill:var(--ink-dim); font-family:'IBM Plex Mono',monospace; font-size:10.5px;}
.diagram table{width:100%; border-collapse:collapse; font-size:.85rem;}
.diagram table th,.diagram table td{padding:9px 12px; text-align:left; border-bottom:1px solid var(--border); vertical-align:top;}
.diagram table th{background:var(--surface-2); font-weight:700; color:var(--ink-dim); font-size:.72rem; text-transform:uppercase; letter-spacing:.03em;}
.diagram table td:first-child{font-weight:700; color:var(--accent-strong); white-space:nowrap;}
.diagram table tr:last-child td{border-bottom:none;}
figcaption{margin-top:8px; font-size:.82rem; color:var(--ink-dim); text-align:center;}

.impl-toggle{all:unset; cursor:pointer; margin-top:22px; display:inline-flex; align-items:center; gap:8px; font-size:.88rem; font-weight:600; color:var(--accent-strong); background:var(--accent-soft); border:1px solid var(--accent); padding:8px 16px; border-radius:999px;}
.impl-toggle:hover{filter:brightness(1.05);}
.impl-toggle .arw{transition:transform .15s ease;}
.impl-toggle.open .arw{transform:rotate(90deg);}
.impl-body{display:none; margin-top:14px; padding:16px 18px; background:var(--surface-2); border:1px dashed var(--border); border-radius:10px;}
.impl-body.open{display:block;}
.impl-body .impl-label{font-family:'IBM Plex Mono',monospace; font-size:.7rem; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-dim); font-weight:700; margin-bottom:8px;}
.impl-body ul{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:10px;}
.impl-body li{position:relative; padding-left:20px; font-size:.92rem; color:var(--ink);}
.impl-body li::before{content:"▸"; position:absolute; left:0; color:var(--accent);}
.impl-body code, .impl-body .mono{background:var(--surface); border:1px solid var(--border); border-radius:4px; padding:0 4px;}

.rel-links{margin-top:26px; display:flex; flex-wrap:wrap; gap:8px;}
.rel-links .rl-label{font-size:.8rem; color:var(--ink-dim); width:100%; margin-bottom:2px;}
.rel-link{all:unset; cursor:pointer; font-size:.86rem; color:var(--accent-strong); background:var(--accent-soft); border:1px solid var(--accent); padding:7px 14px; border-radius:999px;}
.rel-link:hover{filter:brightness(1.05);}
.rel-link .tag{font-size:.72rem; color:var(--ink-dim); margin-left:6px;}

.fsBtn{all:unset; cursor:pointer; font-weight:600; font-size:.85rem; padding:7px 15px; border-radius:999px; color:var(--ink); background:var(--surface-2); border:1px solid var(--border);}
.fsBtn:hover{border-color:var(--accent); color:var(--accent-strong);}

/* ---------- outline side drawer (while viewing a slide) ---------- */
#drawerBackdrop{position:fixed; inset:0; background:rgba(21,30,39,.35); z-index:20; display:none;}
#drawerBackdrop.open{display:block;}
#drawer{position:fixed; top:0; right:-360px; width:340px; max-width:88vw; height:100vh; background:var(--surface); box-shadow:-8px 0 24px rgba(21,30,39,.18); z-index:21; transition:right .2s ease; overflow-y:auto; padding:20px 18px;}
#drawer.open{right:0;}
#drawer h3{font-size:1rem; color:var(--accent-strong); margin-bottom:14px;}
.drawer-sec{margin-bottom:14px;}
.drawer-sec-title{font-family:'IBM Plex Mono',monospace; font-size:.72rem; letter-spacing:.06em; text-transform:uppercase; color:var(--accent); font-weight:700; margin-bottom:4px;}
.drawer-sec ul{list-style:none; margin:0; padding:0;}
.drawer-sec button{all:unset; box-sizing:border-box; width:100%; cursor:pointer; padding:6px 8px; border-radius:6px; font-size:.86rem; color:var(--ink-dim);}
.drawer-sec button:hover{background:var(--accent-soft); color:var(--accent-strong);}
.drawer-sec button.current{background:var(--accent-strong); color:#fff; font-weight:600;}
"""

def drawer_html():
    parts = []
    for c in CLUSTERS:
        items = ''.join(
          '<li><button data-jump="%s" data-slide="%s">%s</button></li>' % (s['id'], s['id'], s['title'])
          for s in SLIDES[c['id']]
        )
        parts.append('<div class="drawer-sec"><div class="drawer-sec-title">%s</div><ul>%s</ul></div>' % (c['label'], items))
    return ''.join(parts)

SLIDES_JS = json.dumps(SLIDES, ensure_ascii=False)
CLUSTERS_JS = json.dumps(CLUSTERS, ensure_ascii=False)
PLAY_ORDER_JS = json.dumps(PLAY_ORDER, ensure_ascii=False)
SLIDE_CLUSTER_JS = json.dumps(slide_cluster, ensure_ascii=False)
CLUSTER_ORDER_JS = json.dumps([c['id'] for c in CLUSTERS], ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>hermes-agent Harness 拆解簡報</title>
<style>%(css)s</style>
</head>
<body>

<div id="slide" class="screen active">
  <div class="progress-bar"><i id="progressBar" style="width:0%%"></i></div>
  <div class="slide-topbar">
    <button class="outlineBtn" id="outlineToggle">☰ 章節導覽</button>
    <div class="crumb" id="crumb">—</div>
    <div class="progress" id="progressLabel">—</div>
    <button class="fsBtn" id="fsToggle">⛶ 全螢幕</button>
  </div>
  <div class="slide-main">
    <div class="slide-card">
      <div class="cover-block" id="coverBlock" hidden>
        <div class="cover-eyebrow">HARNESS 拆解簡報</div>
        <h1 class="cover-title" id="coverTitle">—</h1>
        <p class="cover-subtitle" id="coverSubtitle"></p>
      </div>
      <div id="normalBlock">
        <div class="slide-eyebrow"><span id="eyebrowLabel">NODE</span></div>
        <h2 class="slide-title" id="sTitle">—</h2>
        <ul class="slide-bullets" id="sBullets"></ul>
        <div id="sDiagram"></div>
        <button class="impl-toggle" id="implToggle" hidden><span class="arw">▸</span> hermes-agent 實作細節</button>
        <div class="impl-body" id="implBody"><div class="impl-label">原始碼對照</div><ul id="implList"></ul></div>
        <div class="rel-links" id="sLinks"></div>
      </div>
    </div>
  </div>
</div>

<div id="drawerBackdrop"></div>
<div id="drawer">
  <h3>章節導覽</h3>
  %(drawer)s
</div>

<script>
var SLIDES = %(slidesjs)s;
var CLUSTERS = %(clustersjs)s;
var PLAY_ORDER = %(playorderjs)s;
var SLIDE_CLUSTER = %(slideclusterjs)s;
var CLUSTER_ORDER = %(clusterorderjs)s;

var clusterById = {};
CLUSTERS.forEach(function(c){ clusterById[c.id] = c; });
var slideById = {};
Object.keys(SLIDES).forEach(function(cid){ SLIDES[cid].forEach(function(s){ slideById[s.id] = s; }); });

function $(id){ return document.getElementById(id); }

function refreshDrawerHighlight(currentId){
  document.querySelectorAll('#drawer button[data-slide]').forEach(function(b){
    b.classList.toggle('current', b.getAttribute('data-slide') === currentId);
  });
}

function openSlide(slideId){
  var s = slideById[slideId];
  var cid = SLIDE_CLUSTER[slideId];
  var c = clusterById[cid];
  var list = SLIDES[cid];
  var idx = list.findIndex(function(x){ return x.id === slideId; });

  $('coverBlock').hidden = !s.cover;
  $('normalBlock').hidden = !!s.cover;
  if (s.cover){
    $('coverTitle').textContent = s.title;
    $('coverSubtitle').textContent = s.subtitle || '';
    $('crumb').innerHTML = '<b>' + c.label + '</b>';
    var pIdx0 = PLAY_ORDER.indexOf(slideId);
    $('progressLabel').textContent = (pIdx0+1) + ' / ' + PLAY_ORDER.length;
    $('progressBar').style.width = ((pIdx0+1)/PLAY_ORDER.length*100) + '%%';
    window.scrollTo(0,0);
    $('slide').dataset.current = slideId;
    refreshDrawerHighlight(slideId);
    return;
  }

  $('eyebrowLabel').textContent = c.label;
  $('sTitle').textContent = s.title;
  $('crumb').innerHTML = '<b>' + c.label + '</b> — ' + c.gap + ' · ' + (idx+1) + '/' + list.length;

  var bullets = $('sBullets');
  bullets.innerHTML = '';
  s.bullets.forEach(function(b){
    var li = document.createElement('li');
    li.textContent = b;
    bullets.appendChild(li);
  });

  $('sDiagram').innerHTML = s.diagram || '';

  var implToggle = $('implToggle');
  var implBody = $('implBody');
  var implList = $('implList');
  implBody.classList.remove('open');
  implToggle.classList.remove('open');
  implToggle.querySelector('.arw').textContent = '▸';
  if (s.impl && s.impl.length > 1){
    implToggle.hidden = false;
    implList.innerHTML = '';
    s.impl.forEach(function(t){
      var li = document.createElement('li');
      li.innerHTML = t;
      implList.appendChild(li);
    });
  } else {
    implToggle.hidden = true;
    implBody.classList.remove('open');
  }

  var linksWrap = $('sLinks');
  linksWrap.innerHTML = '';
  if (s.links && s.links.length){
    var lbl = document.createElement('div');
    lbl.className = 'rl-label';
    lbl.textContent = '交叉引用：';
    linksWrap.appendChild(lbl);
    s.links.forEach(function(pair){
      var target = pair[0], text = pair[1];
      var btn = document.createElement('button');
      btn.className = 'rel-link';
      btn.textContent = text;
      var tcid = SLIDE_CLUSTER[target];
      var tag = document.createElement('span');
      tag.className = 'tag';
      tag.textContent = '→ ' + clusterById[tcid].label;
      btn.appendChild(tag);
      btn.addEventListener('click', function(){ openSlide(target); closeDrawer(); });
      linksWrap.appendChild(btn);
    });
  }

  var pIdx = PLAY_ORDER.indexOf(slideId);
  $('progressLabel').textContent = (pIdx+1) + ' / ' + PLAY_ORDER.length;
  $('progressBar').style.width = ((pIdx+1)/PLAY_ORDER.length*100) + '%%';

  window.scrollTo(0,0);
  $('slide').dataset.current = slideId;
  refreshDrawerHighlight(slideId);
}

function stepPlay(delta){
  var cur = $('slide').dataset.current;
  var i = PLAY_ORDER.indexOf(cur);
  var next = i + delta;
  if (next < 0 || next >= PLAY_ORDER.length) return;
  openSlide(PLAY_ORDER[next]);
}

function openDrawer(){ $('drawer').classList.add('open'); $('drawerBackdrop').classList.add('open'); }
function closeDrawer(){ $('drawer').classList.remove('open'); $('drawerBackdrop').classList.remove('open'); }

document.querySelectorAll('#drawer [data-jump]').forEach(function(el){
  el.addEventListener('click', function(){ openSlide(el.getAttribute('data-jump')); closeDrawer(); });
});

$('outlineToggle').addEventListener('click', function(ev){ ev.stopPropagation(); openDrawer(); });
$('implToggle').addEventListener('click', function(ev){
  ev.stopPropagation();
  var open = $('implBody').classList.toggle('open');
  this.classList.toggle('open', open);
  this.querySelector('.arw').textContent = open ? '▾' : '▸';
});
$('drawerBackdrop').addEventListener('click', function(ev){ ev.stopPropagation(); closeDrawer(); });
$('drawer').addEventListener('click', function(ev){ ev.stopPropagation(); });

function toggleFullscreen(){
  if (!document.fullscreenElement){
    document.documentElement.requestFullscreen().catch(function(){});
  } else {
    document.exitFullscreen();
  }
}
$('fsToggle').addEventListener('click', function(ev){ ev.stopPropagation(); toggleFullscreen(); });

document.addEventListener('click', function(ev){
  if ($('drawer').classList.contains('open')) return;
  if (ev.target.closest('button, a')) return;
  stepPlay(1);
});

document.addEventListener('keydown', function(ev){
  if (ev.key === 'Escape'){
    if ($('drawer').classList.contains('open')) { closeDrawer(); }
    return;
  }
  if (ev.key >= '0' && ev.key <= '9'){
    var idx = ev.key === '0' ? 9 : parseInt(ev.key,10)-1;
    var cid = CLUSTER_ORDER[idx];
    if (cid) openSlide(SLIDES[cid][0].id);
    return;
  }
  if (ev.key === 'f' || ev.key === 'F'){ toggleFullscreen(); return; }
  if (ev.key === ' ' || ev.key === 'ArrowRight' || ev.key === 'PageDown'){ ev.preventDefault(); stepPlay(1); return; }
  if (ev.key === 'ArrowLeft' || ev.key === 'Backspace' || ev.key === 'PageUp'){ ev.preventDefault(); stepPlay(-1); return; }
});

openSlide(PLAY_ORDER[0]);
</script>
</body>
</html>
""" % {"css": CSS, "drawer": drawer_html(), "slidesjs": SLIDES_JS,
       "clustersjs": CLUSTERS_JS, "playorderjs": PLAY_ORDER_JS, "slideclusterjs": SLIDE_CLUSTER_JS,
       "clusterorderjs": CLUSTER_ORDER_JS}

import os
out_path = os.path.expanduser("~/Desktop/Harness 心智圖＋課程.html")
open(out_path, "w", encoding="utf-8").write(HTML)
print("wrote", out_path, len(HTML), "chars")
