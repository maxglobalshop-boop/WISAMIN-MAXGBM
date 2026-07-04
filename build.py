#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — WISAMIN Competitor Radar
สร้าง index.html แบบ self-contained จากไฟล์รายงานใน data/reports/*.json
รัน: python3 build.py
"""
import json, glob, os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(ROOT, "data", "reports")
OUT = os.path.join(ROOT, "index.html")


def norm_channel(c):
    c = (c or "").lower()
    if "tiktok" in c: return "TikTok"
    if "face" in c or "fb" in c: return "Facebook"
    if "you" in c: return "YouTube"
    if c.strip() == "x" or "twitter" in c or c.startswith("x "): return "X"
    return "X" if c.strip() == "x" else "อื่นๆ"


def compute_counts(report):
    """นับจำนวนคอนเทนต์ต่อช่องทางอัตโนมัติ (ไม่ต้องกรอกมือ)"""
    counts = {"TikTok": 0, "Facebook": 0, "YouTube": 0, "X": 0}
    for c in report.get("competitors", []):
        ch = norm_channel(c.get("channel"))
        counts[ch] = counts.get(ch, 0) + 1
    report.setdefault("summary", {})["channel_counts"] = counts
    return report


def load_reports():
    files = sorted(glob.glob(os.path.join(REPORTS_DIR, "*.json")))
    reports, seen_urls = [], {}
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                r = json.load(fh)
            # เตือนถ้า URL ซ้ำกับรายงานวันก่อน (กันเอาของเดิมมาแจ้งซ้ำ)
            for c in r.get("competitors", []):
                u = c.get("url", "")
                if u in seen_urls:
                    print(f"  ⚠ URL ซ้ำกับ {seen_urls[u]}: {u}")
                else:
                    seen_urls[u] = r.get("date")
            reports.append(compute_counts(r))
        except Exception as e:
            print(f"  ! ข้ามไฟล์ {f}: {e}")
    # เรียงใหม่สุดขึ้นก่อน
    reports.sort(key=lambda r: r.get("date", ""), reverse=True)
    return reports


def build():
    reports = load_reports()
    if not reports:
        print("ไม่พบรายงานใน data/reports/ — สร้างรายงานก่อน (ดู PLAYBOOK.md)")
        return
    payload = json.dumps(reports, ensure_ascii=False)
    built_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    html = TEMPLATE.replace("/*__DATA__*/null", payload).replace("__BUILT_AT__", built_at)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"✓ สร้าง index.html แล้ว ({len(reports)} รายงาน, ล่าสุด {reports[0].get('date')})")
    print(f"  เปิดไฟล์: {OUT}")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WISAMIN · Competitor Radar</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0b0f14; --panel:#131a23; --panel2:#1a232e; --line:#25313f;
  --text:#e8eef5; --muted:#8ea0b5; --accent:#28e0a8; --accent2:#7c5cff;
  --tiktok:#ff2d55; --facebook:#1877f2; --youtube:#ff0000; --x:#1da1f2;
  --hot:#ff4d5e; --warn:#ffb020; --ok:#28e0a8;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Prompt','Sarabun',sans-serif;line-height:1.5;padding-bottom:60px}
a{color:inherit;text-decoration:none}
.wrap{max-width:1240px;margin:0 auto;padding:0 20px}

header{background:linear-gradient(135deg,#0e1520,#141d2b);border-bottom:1px solid var(--line);padding:22px 0;position:sticky;top:0;z-index:50;backdrop-filter:blur(8px)}
.brandrow{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:12px}
.logo .mark{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:700;font-size:20px;color:#08131a}
.logo h1{font-size:19px;font-weight:600;letter-spacing:.3px}
.logo p{font-size:12px;color:var(--muted)}
.datepick{display:flex;align-items:center;gap:8px}
.datepick select{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:10px;padding:9px 12px;font-family:inherit;font-size:14px}
.live{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--accent);border:1px solid var(--line);padding:6px 10px;border-radius:20px}
.live .dot{width:8px;height:8px;border-radius:50%;background:var(--accent);animation:pulse 1.6s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(40,224,168,.5)}70%{box-shadow:0 0 0 8px rgba(40,224,168,0)}100%{box-shadow:0 0 0 0 rgba(40,224,168,0)}}

.headline{margin:22px 0 6px;font-size:15px;color:var(--text);background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;padding:14px 16px}
.headline b{color:var(--accent)}

.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:18px 0}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}
.kpi .n{font-size:28px;font-weight:700}
.kpi .l{font-size:12px;color:var(--muted);margin-top:2px}
.kpi.tiktok .n{color:var(--tiktok)} .kpi.facebook .n{color:var(--facebook)}
.kpi.youtube .n{color:var(--youtube)} .kpi.x .n{color:var(--x)}

.tabs{display:flex;gap:6px;margin:24px 0 16px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.tab{padding:10px 16px;font-size:14px;color:var(--muted);cursor:pointer;border-bottom:2px solid transparent;font-weight:500}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab:hover{color:var(--text)}

.search{width:100%;background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:12px 16px;color:var(--text);font-family:inherit;font-size:15px;margin-bottom:14px}
.search:focus{outline:none;border-color:var(--accent)}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.filters .lbl{font-size:12px;color:var(--muted);align-self:center;margin-right:2px}
.chip{padding:7px 14px;border-radius:20px;font-size:13px;background:var(--panel2);border:1px solid var(--line);color:var(--muted);cursor:pointer}
.chip.active{background:var(--accent);color:#08131a;border-color:var(--accent);font-weight:600}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:10px;transition:.15s;position:relative;overflow:hidden}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card .top{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.badge{font-size:11px;font-weight:600;padding:4px 9px;border-radius:6px;white-space:nowrap}
.b-tiktok{background:rgba(255,45,85,.15);color:#ff6b85} .b-facebook{background:rgba(24,119,242,.15);color:#5a9bff}
.b-youtube{background:rgba(255,0,0,.15);color:#ff5c5c} .b-x{background:rgba(29,161,242,.15);color:#5ec1ff}
.b-yt{background:rgba(255,0,0,.15);color:#ff5c5c}
.tier{font-size:11px;font-weight:600;padding:4px 9px;border-radius:6px}
.t-viral{background:rgba(255,77,94,.18);color:#ff8593} .t-high{background:rgba(255,176,32,.18);color:#ffca6b} .t-medium{background:rgba(142,160,181,.15);color:#a9b8c9}
.card h3{font-size:16px;font-weight:600;line-height:1.35}
.card .brand{font-size:13px;color:var(--accent);font-weight:500}
.card .cat{font-size:12px;color:var(--muted)}
.card .why{font-size:13px;color:#c4d0dd;background:var(--panel2);border-radius:8px;padding:9px 11px}
.card .why b{color:var(--text)}
.card .threat{font-size:12px;display:flex;align-items:center;gap:6px}
.card .threat .lv{font-weight:600}
.card .meta{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:8px;border-top:1px solid var(--line)}
.card .creator{font-size:12px;color:var(--muted)}
.card .link{font-size:13px;color:var(--accent);font-weight:600;display:inline-flex;align-items:center;gap:5px}
.card .link:hover{text-decoration:underline}

.ins{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}
.inscard{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;border-top:3px solid var(--accent2)}
.inscard h3{font-size:16px;margin-bottom:10px}
.inscard .row{font-size:13px;margin:8px 0;color:#c4d0dd}
.inscard .row b{color:var(--accent)}
.idea{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;border-left:3px solid var(--accent)}
.idea h3{font-size:16px;margin-bottom:8px}
.idea .hook{font-size:14px;font-style:italic;color:var(--warn);background:var(--panel2);padding:10px;border-radius:8px;margin:8px 0}
.idea .k{font-size:13px;margin:6px 0;color:#c4d0dd}
.idea .k b{color:var(--text)}
.fda{display:inline-block;font-size:11px;padding:3px 8px;border-radius:6px;background:rgba(40,224,168,.15);color:var(--accent);margin-top:6px}
.trendlist{display:flex;flex-direction:column;gap:10px}
.trend{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;font-size:14px;display:flex;gap:12px;align-items:center}
.trend .num{width:28px;height:28px;border-radius:8px;background:var(--accent2);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0}

.section-title{font-size:14px;color:var(--muted);margin:6px 0 12px;text-transform:uppercase;letter-spacing:1px}
.hide{display:none}
footer{text-align:center;color:var(--muted);font-size:12px;margin-top:40px;padding-top:20px;border-top:1px solid var(--line)}
footer .note{max-width:700px;margin:0 auto 8px}
@media(max-width:640px){.logo h1{font-size:16px}.kpi .n{font-size:22px}}
</style>
</head>
<body>
<header><div class="wrap brandrow">
  <div class="logo">
    <div class="mark">W</div>
    <div><h1>WISAMIN · Competitor Radar</h1><p>เรดาร์คอนเทนต์คู่แข่งอาหารเสริมไทย · รายวัน</p></div>
  </div>
  <div class="datepick">
    <span class="live"><span class="dot"></span> LIVE</span>
    <select id="dateSel" onchange="selectDate(this.value)"></select>
  </div>
</div></header>

<div class="wrap">
  <div class="headline" id="headline"></div>
  <div class="kpis" id="kpis"></div>

  <div class="tabs">
    <div class="tab active" data-tab="feed" onclick="switchTab('feed')">📡 คอนเทนต์คู่แข่ง</div>
    <div class="tab" data-tab="insight" onclick="switchTab('insight')">🧠 Customer Insight</div>
    <div class="tab" data-tab="idea" onclick="switchTab('idea')">💡 ไอเดียคอนเทนต์ WISAMIN</div>
    <div class="tab" data-tab="trend" onclick="switchTab('trend')">📈 เทรนด์</div>
  </div>

  <div id="tab-feed">
    <input id="search" class="search" type="text" placeholder="🔍 ค้นหาแบรนด์ / คอนเทนต์ / คีย์เวิร์ด…" oninput="renderFeed()">
    <div class="filters" id="chFilters"></div>
    <div class="filters" id="catFilters"></div>
    <div class="grid" id="feed"></div>
  </div>
  <div id="tab-insight" class="hide"><div class="ins" id="insights"></div></div>
  <div id="tab-idea" class="hide"><div class="section-title">คอนเทนต์ต่อยอดที่ใช้ได้จริง + ปลอดคำต้องห้าม อย.</div><div class="ins" id="ideas"></div></div>
  <div id="tab-trend" class="hide"><div class="trendlist" id="trends"></div></div>

  <footer>
    <div class="note">ข้อมูลรวบรวมจากการค้นเว็บสาธารณะ (TikTok/Facebook/YouTube/X) เพื่อวิเคราะห์การแข่งขัน · ยอด engagement จัดระดับเชิงคุณภาพ ดูวิธีเก็บตัวเลขแม่นยำใน PLAYBOOK.md</div>
    <div>สร้างเมื่อ __BUILT_AT__ · อัปเดตรายวันด้วย <code>python3 build.py</code></div>
  </footer>
</div>

<script>
const DATA = /*__DATA__*/null;
let current = DATA[0];
let chFilter = 'all';
let catFilter = 'all';

function chBadgeClass(c){c=(c||'').toLowerCase();if(c.includes('tiktok'))return'b-tiktok';if(c.includes('face'))return'b-facebook';if(c.includes('you'))return'b-yt';if(c.includes('x'))return'b-x';return'b-tiktok';}
function tierClass(t){t=(t||'').toLowerCase();if(t.includes('viral'))return't-viral';if(t.includes('high'))return't-high';return't-medium';}
function tierLabel(t){t=(t||'').toLowerCase();if(t.includes('viral'))return'🔥 ไวรัล';if(t.includes('high'))return'⬆ engagement สูง';return'engagement กลาง';}
function threatColor(t){t=(t||'').toLowerCase();if(t.includes('สูง'))return'var(--hot)';if(t.includes('กลาง'))return'var(--warn)';return'var(--muted)';}

function initDates(){
  const sel=document.getElementById('dateSel');
  sel.innerHTML=DATA.map((r,i)=>`<option value="${i}">${r.date}${i===0?' (ล่าสุด)':''}</option>`).join('');
}
function selectDate(i){current=DATA[i];render();}

function render(){
  // headline
  const s=current.summary||{};
  document.getElementById('headline').innerHTML=`<b>สรุปวันที่ ${current.date}:</b> ${s.headline||''}`;
  // kpis
  const cc=s.channel_counts||{};
  const total=(current.competitors||[]).length;
  document.getElementById('kpis').innerHTML=`
    <div class="kpi"><div class="n">${total}</div><div class="l">คอนเทนต์คู่แข่งวันนี้</div></div>
    <div class="kpi tiktok"><div class="n">${cc.TikTok||0}</div><div class="l">TikTok</div></div>
    <div class="kpi facebook"><div class="n">${cc.Facebook||0}</div><div class="l">Facebook</div></div>
    <div class="kpi youtube"><div class="n">${cc.YouTube||0}</div><div class="l">YouTube</div></div>
    <div class="kpi x"><div class="n">${cc.X||0}</div><div class="l">X (Twitter)</div></div>
    <div class="kpi"><div class="n" style="color:var(--accent2)">${(current.content_ideas||[]).length}</div><div class="l">ไอเดียต่อยอด</div></div>`;
  renderFilters();
  renderFeed();
  renderInsights();
  renderIdeas();
  renderTrends();
}

function renderFilters(){
  const chans=['all',...new Set((current.competitors||[]).map(c=>c.channel))];
  document.getElementById('chFilters').innerHTML='<span class="lbl">ช่องทาง:</span>'+chans.map(c=>
    `<div class="chip ${chFilter===c?'active':''}" onclick="setFilter('${c}')">${c==='all'?'ทั้งหมด':c}</div>`).join('');
  const cats=['all',...new Set((current.competitors||[]).map(c=>c.category))];
  document.getElementById('catFilters').innerHTML='<span class="lbl">หมวด:</span>'+cats.map(c=>
    `<div class="chip ${catFilter===c?'active':''}" onclick="setCat('${c.replace(/'/g,"\\'")}')">${c==='all'?'ทั้งหมด':c}</div>`).join('');
}
function setFilter(c){chFilter=c;renderFilters();renderFeed();}
function setCat(c){catFilter=c;renderFilters();renderFeed();}

function renderFeed(){
  let items=current.competitors||[];
  if(chFilter!=='all')items=items.filter(c=>c.channel===chFilter);
  if(catFilter!=='all')items=items.filter(c=>c.category===catFilter);
  const q=(document.getElementById('search')?.value||'').trim().toLowerCase();
  if(q)items=items.filter(c=>JSON.stringify(c).toLowerCase().includes(q));
  // เรียงตาม tier: viral > high > medium
  const order={viral:0,high:1,medium:2};
  items=[...items].sort((a,b)=>(order[(a.engagement_tier||'').toLowerCase()]??3)-(order[(b.engagement_tier||'').toLowerCase()]??3));
  document.getElementById('feed').innerHTML=items.map(c=>`
    <div class="card">
      <div class="top">
        <span class="badge ${chBadgeClass(c.channel)}">${c.channel}</span>
        <span class="tier ${tierClass(c.engagement_tier)}">${tierLabel(c.engagement_tier)}</span>
      </div>
      <div class="brand">${c.brand}</div>
      <h3>${c.title}</h3>
      <div class="cat">หมวด: ${c.category} · รูปแบบ: ${c.format||'-'}</div>
      <div class="why"><b>ทำไมปัง:</b> ${c.why_it_works||'-'}</div>
      ${c.threat_to_wisamin?`<div class="threat">⚠️ ภัยต่อ WISAMIN: <span class="lv" style="color:${threatColor(c.threat_to_wisamin)}">${c.threat_to_wisamin}</span></div>`:''}
      <div class="meta">
        <span class="creator">👤 ${c.creator||'-'}</span>
        <a class="link" href="${c.url}" target="_blank" rel="noopener">ดูคอนเทนต์ ↗</a>
      </div>
    </div>`).join('') || '<p style="color:var(--muted)">ไม่มีคอนเทนต์ในช่องนี้</p>';
}

function renderInsights(){
  document.getElementById('insights').innerHTML=(current.insights||[]).map(i=>`
    <div class="inscard">
      <h3>🧠 ${i.insight}</h3>
      <div class="row"><b>หลักฐาน:</b> ${i.evidence}</div>
      <div class="row"><b>โอกาสของ WISAMIN:</b> ${i.opportunity}</div>
    </div>`).join('');
}
function renderIdeas(){
  document.getElementById('ideas').innerHTML=(current.content_ideas||[]).map(i=>`
    <div class="idea">
      <h3>💡 ${i.idea}</h3>
      <div class="hook">"${i.hook}"</div>
      <div class="k"><b>รูปแบบ:</b> ${i.format}</div>
      <div class="k"><b>CTA:</b> ${i.cta}</div>
      ${i.counters_competitor?`<div class="k"><b>ชนคู่แข่ง:</b> ${i.counters_competitor}</div>`:''}
      ${i.fda_safe?'<span class="fda">✓ ปลอดคำต้องห้าม อย.</span>':''}
    </div>`).join('');
}
function renderTrends(){
  document.getElementById('trends').innerHTML=(current.trends||[]).map((t,i)=>`
    <div class="trend"><div class="num">${i+1}</div><div>${t}</div></div>`).join('');
}

function switchTab(t){
  document.querySelectorAll('.tab').forEach(el=>el.classList.toggle('active',el.dataset.tab===t));
  ['feed','insight','idea','trend'].forEach(x=>document.getElementById('tab-'+x).classList.toggle('hide',x!==t));
}

initDates();render();
</script>
</body>
</html>"""

if __name__ == "__main__":
    build()
