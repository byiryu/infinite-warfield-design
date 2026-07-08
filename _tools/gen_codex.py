#!/usr/bin/env python3
# infinite-warfield 유닛 코덱스(스펙) 재생성 — 현행 data/units.json 파생 뷰
# design 세션 소유(boards). SoT = ../data/units.json (PM). 손유지 X = 데이터 변경 시 재실행.
import json, sys, html

SRC = sys.argv[1] if len(sys.argv) > 1 else "../../data/units.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "unit-codex.html"

THEME_ORDER = ["Combat", "Necro", "Spirit", "Machine", "Beast"]
THEME_KOR = {"Combat": "전투 Combat", "Necro": "사령 Necro", "Spirit": "정령 Spirit",
             "Machine": "기계 Machine", "Beast": "야수 Beast"}
THEME_HEX = {"Combat": "#E03A5C", "Necro": "#9D3EE8", "Spirit": "#5DDD7E",
             "Machine": "#00D4FF", "Beast": "#E06B14"}
THEME_NOTE = {"Combat": "마젠타 강철 · 투구+검", "Necro": "보라 · 해골+낫 · 림라이트",
              "Spirit": "에메랄드 · 정령관+지팡이", "Machine": "시안 · 바이저+포",
              "Beast": "주황 · 짐승머리+발톱"}
ROLE_KOR = {"Dealer": "딜러", "Support": "서포터", "Tank": "탱커"}
EFFMAP = {"buffEffects": "buff", "debuffEffects": "debuff", "dotEffects": "dot",
          "healEffects": "heal", "stunEffects": "stun", "multiHitEffects": "multihit",
          "onHitEffects": "onhit", "onDeathEffects": "ondeath", "teleportEffects": "teleport",
          "pullEffects": "pull", "dashEffects": "dash", "cleansEffects": "cleanse",
          "areaBrustEffects": "burst", "damageEffects": "damage", "summonEffects": "summon",
          "tauntEffects": "taunt"}

data = json.load(open(SRC, encoding="utf-8"))
units = [u for u in data["unitData"] if u.get("unitID") != "999999"]
dataver = data.get("dataVersion", "?")

def e(s): return html.escape(str(s))

def eff_tags(skill):
    tags = [v for k, v in EFFMAP.items() if skill.get(k)]
    # dedup, keep order
    seen, out = set(), []
    for t in tags:
        if t not in seen:
            seen.add(t); out.append(t)
    return out

def stat_rows(us):
    rows = []
    for u in us:
        role = u.get("role", "")
        atk = u.get("attackType", "")
        crit = u.get("baseCritRate", 0)
        crit_s = f"{round(crit*100)}%" if crit else "0%"
        rows.append(
            f"<tr><td class='uid'>{e(u['unitID'])}</td>"
            f"<td><span class='unit-name'>{e(u['unitName_kor'])}</span> <span class='uid'>{e(u.get('unitName_eng',''))}</span></td>"
            f"<td><span class='role {e(role)}'>{ROLE_KOR.get(role, role)}</span></td>"
            f"<td><span class='atk {e(atk)}'>{'물리' if atk=='Physical' else '마법' if atk=='Magical' else e(atk)}</span></td>"
            f"<td>{'근접' if u.get('isMelee') else '원거리'}</td>"
            f"<td class='num'>{e(u.get('cost',0))}</td>"
            f"<td class='num'>{e(u.get('baseHP',0))}</td>"
            f"<td class='num'>{e(u.get('baseDefense',0))}</td>"
            f"<td class='num'>{e(u.get('baseMagicResist',0))}</td>"
            f"<td class='num'>{e(u.get('basePhysicalPower',0))}</td>"
            f"<td class='num'>{e(u.get('baseMagicalPower',0))}</td>"
            f"<td class='num'>{e(u.get('baseAttackSpeed',0))}</td>"
            f"<td class='num'>{crit_s}</td>"
            f"<td class='num'>{e(u.get('baseCritMultiplier',0))}</td>"
            f"<td class='num'>{e(u.get('baseMoveSpeed',0))}</td>"
            f"<td class='num'>{e(u.get('attackRange',0))}</td></tr>")
    return "".join(rows)

def skill_cards(us):
    cards = []
    for u in us:
        role = u.get("role", "")
        tagchips = "".join(f"<span class='tag'>{e(t)}</span>" for t in u.get("tags", []))
        sk_html = []
        for slot, key in [("P1", "passiveSkill1"), ("P2", "passiveSkill2"), ("ACT", "activeSkill")]:
            sk = u.get(key) or {}
            if not sk or not sk.get("skillName_kor"):
                continue
            efs = "".join(f"<span class='ef'>[{t}]</span>" for t in eff_tags(sk))
            sk_html.append(
                f"<div class='sk'><span class='slot'>{slot}</span>"
                f"<span class='skn'>{e(sk['skillName_kor'])}</span>{efs}<br>"
                f"<span class='skd'>{e(sk.get('description',''))}</span></div>")
        if not sk_html:
            sk_html.append("<div class='sk'><span class='empty'>스킬 없음</span></div>")
        cards.append(
            f"<div class='uskill'><div class='uh'>"
            f"<b>{e(u['unitName_kor'])}</b> <span class='uid'>{e(u['unitID'])} · {e(u.get('unitName_eng',''))}</span> "
            f"<span class='role {e(role)}'>{ROLE_KOR.get(role, role)}</span>"
            f"{('<span class=tagline>'+tagchips+'</span>') if tagchips else ''}</div>"
            + "".join(sk_html) + "</div>")
    return "".join(cards)

TH = ("<tr><th>ID</th><th>유닛</th><th>역할</th><th>공격</th><th>근/원</th>"
      "<th class='num'>코스트</th><th class='num'>HP</th><th class='num'>물방</th><th class='num'>마저</th>"
      "<th class='num'>물공</th><th class='num'>마공</th><th class='num'>공속</th>"
      "<th class='num'>치명</th><th class='num'>치배</th><th class='num'>이속</th><th class='num'>사거리</th></tr>")

def section(title, note, us, accent=None):
    stitle = f"<span style='color:{accent}'>●</span> {e(title)}" if accent else e(title)
    return (f"<section><div class='shead'><h2>{stitle}</h2><span class='note'>{e(note)}</span></div>"
            f"<div class='tbl-scroll'><table><thead>{TH}</thead><tbody>{stat_rows(us)}</tbody></table></div>"
            f"<div class='skills'>{skill_cards(us)}</div></section>")

heroes = sorted([u for u in units if u.get("isHero")], key=lambda x: (THEME_ORDER.index(x["unitType"]), int(x["unitID"])))
normals = [u for u in units if not u.get("isHero")]
from collections import Counter
rolec = Counter(u["role"] for u in units)

secs = [section("영웅 (5)", "cost 0 · 사망=패배 · 온보딩 해금 · Active 시그니처 보유", heroes)]
for th in THEME_ORDER:
    us = sorted([u for u in normals if u["unitType"] == th], key=lambda x: int(x["unitID"]))
    secs.append(section(f"{THEME_KOR[th]} ({len(us)})", THEME_NOTE[th], us, THEME_HEX[th]))

STYLE = """<style>
    :root{--ground:#14181c;--panel:#1b2228;--panel2:#212a31;--line:#2d383f;--text:#dde4e1;--muted:#8a9691;
      --dealer:#c2565b;--support:#56c2d0;--tank:#d8b768;--mag:#8a7fd0;--phy:#e8a33d;--gold:#d8b768;
      --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;--sans:ui-sans-serif,system-ui,-apple-system,sans-serif;}
    *{box-sizing:border-box}body{margin:0;background:var(--ground);color:var(--text);font-family:var(--sans);line-height:1.5;-webkit-font-smoothing:antialiased}
    .wrap{max-width:1180px;margin:0 auto;padding:0 22px}a{color:var(--support)}
    header{border-bottom:1px solid var(--line);padding:34px 0 24px}
    .eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--muted)}
    h1{margin:10px 0 0;font-size:clamp(24px,4vw,38px);font-weight:800;text-transform:uppercase;letter-spacing:-.01em}
    .sub{color:var(--muted);font-size:14px;margin-top:10px;max-width:70ch}
    .gen{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:12px}
    .summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin:22px 0}
    .scard{background:var(--panel);border:1px solid var(--line);border-radius:5px;padding:12px 14px}
    .scard .n{font-size:20px;font-weight:800;font-family:var(--mono)}.scard .l{font-size:11px;color:var(--muted);font-family:var(--mono);text-transform:uppercase;letter-spacing:.06em}
    section{padding:30px 0;border-bottom:1px solid var(--line)}
    .shead{display:flex;align-items:baseline;gap:12px;margin-bottom:14px;flex-wrap:wrap}
    .shead h2{margin:0;font-size:20px;text-transform:uppercase;font-family:var(--mono);letter-spacing:.04em}
    .shead .note{color:var(--muted);font-size:12.5px}
    .tbl-scroll{overflow-x:auto}
    table{width:100%;border-collapse:collapse;font-size:12.5px;min-width:820px}
    th{text-align:left;font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:6px 8px;border-bottom:1px solid var(--line);white-space:nowrap}
    td{padding:7px 8px;border-bottom:1px solid var(--panel2);white-space:nowrap}
    tr:hover td{background:var(--panel)}
    .unit-name{font-weight:700}.uid{font-family:var(--mono);color:var(--muted);font-size:11px}
    .role{font-family:var(--mono);font-size:10px;font-weight:700;padding:2px 6px;border-radius:3px}
    .role.Dealer{background:rgba(194,86,91,.16);color:var(--dealer)}.role.Support{background:rgba(86,194,208,.14);color:var(--support)}.role.Tank{background:rgba(216,183,104,.14);color:var(--tank)}
    .atk{font-family:var(--mono);font-size:10px}.atk.Magical{color:var(--mag)}.atk.Physical{color:var(--phy)}
    .num{font-family:var(--mono);text-align:right}
    .skills{margin-top:18px;display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}
    .uskill{background:var(--panel);border:1px solid var(--line);border-radius:5px;padding:12px 14px}
    .uskill .uh{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;margin-bottom:6px}
    .uskill .uh b{font-size:14px}
    .tagline{display:inline-flex;gap:4px;flex-wrap:wrap;margin-left:2px}
    .tag{font-family:var(--mono);font-size:9px;padding:1px 5px;border-radius:2px;background:var(--panel2);color:var(--muted)}
    .sk{font-size:12.5px;padding:5px 0;border-top:1px solid var(--panel2)}
    .sk:first-of-type{border-top:none}
    .sk .slot{font-family:var(--mono);font-size:9.5px;font-weight:700;padding:1px 5px;border-radius:2px;background:var(--panel2);color:var(--muted);margin-right:6px}
    .sk .skn{font-weight:600}.sk .skd{color:var(--muted)} .sk .ef{font-family:var(--mono);font-size:9.5px;color:var(--gold);margin-left:4px}
    .empty{color:var(--muted);font-style:italic;font-size:12px}
    footer{padding:24px 0 56px;color:var(--muted);font-size:11.5px;font-family:var(--mono);line-height:1.8}
    footer a{color:var(--support)}
    @media(max-width:680px){table{font-size:11px}.skills{grid-template-columns:1fr}}
    </style>"""

HTML = f"""<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>IWF 유닛 코덱스 (스펙)</title>
{STYLE}</head>
<body>
<header><div class="wrap">
  <div class="eyebrow">infinite warfield · 유닛 코덱스 · 스펙 확인</div>
  <h1>유닛 스탯 · 스킬 명세</h1>
  <p class="sub">전 39유닛(영웅 5 + 일반 34) 스탯·스킬 한눈에 — <b>유닛 스펙 확인용</b> 참조 표. ★ <b>파생 뷰</b> — 데이터 SoT = <code>../data/units.json</code>(PM 저작). 값 변경 시 재생성(손유지 X). 더미(999999) 제외.</p>
  <div class="gen">파생 = data/units.json (dataVersion {e(dataver)}) · 애니 확인 = <a href="sanity/unit-codex-board.html">트래커</a> · 인게임 화면 = <a href="sanity/codex-screen-board.html">인게임 도감</a> · 밸런스 = <a href="balance-report.html">밸런싱 보고서</a></div>
  <div class="summary">
    <div class="scard"><div class="n">39</div><div class="l">총 유닛</div></div>
    <div class="scard"><div class="n">5</div><div class="l">영웅</div></div>
    <div class="scard"><div class="n">34</div><div class="l">일반</div></div>
    <div class="scard"><div class="n">5</div><div class="l">테마</div></div>
    <div class="scard"><div class="n">{rolec['Dealer']}</div><div class="l">딜러</div></div>
    <div class="scard"><div class="n">{rolec['Tank']}</div><div class="l">탱커</div></div>
    <div class="scard"><div class="n">{rolec['Support']}</div><div class="l">서포터</div></div>
  </div>
</div></header>
<div class="wrap">
{''.join(secs)}
</div>
<footer><div class="wrap">
  유닛 코덱스 (스펙) · 파생 뷰 · SoT = data/units.json (dataVersion {e(dataver)}) · 재생성 = <code>python3 _tools/gen_codex.py</code> (boards/ 에서) · 더미 제외<br>
  용도 = 유닛 스펙 확인 (스탯·스킬) / 애니 확인 = 트래커 / 인게임 화면 = 인게임 도감<br>
  <a href="index.html">‹ 디자인 보드</a>
</div></footer>
</body></html>"""

open(OUT, "w", encoding="utf-8").write(HTML)
print(f"OK · {len(units)} units · {len(HTML)} bytes → {OUT}")
