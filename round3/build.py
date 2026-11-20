# build.py — round 3: photo-first variants of friendly/v3 ("gentle wa-modern").
# Facts from ../friendly/v3.html. Photos are referenced from ../friendly/img (not copied).
# Run: python3 build.py
import pathlib, json
H = pathlib.Path(__file__).parent
I = "../friendly/img/yuri-"
KZ = "https://yuri.kanazawa-guide.com/"

SIZE = {"kimono-window": (788, 1400), "azalea": (1208, 1354)}
LAND = {"cheesecake", "garden-pond", "green-smile", "lunch-set", "sakura-arms", "sakura-wave", "street-wave"}
ALT = {
    "alley-sign": "Yuri on a tree-lined Tokyo side street",
    "azalea": "Yuri standing among azaleas in a garden",
    "cafe-cake": "Yuri smiling at a café table with tea and cake",
    "cafe-cushion": "Yuri hugging a cushion in a cozy café",
    "cafe-smile": "Yuri laughing at a café",
    "cheesecake": "Yuri with a slice of cheesecake",
    "garden-pond": "Yuri beside a Japanese garden pond",
    "green-smile": "Yuri smiling in the greenery by a river",
    "izakaya-beer": "Yuri raising a glass of beer at an izakaya",
    "izakaya-fan": "Yuri with a folding fan and a drink at an izakaya",
    "kimono-window": "Yuri in a pink kimono, smiling with her hands by her face",
    "lunch-set": "Yuri smiling over a set lunch",
    "old-house": "Yuri in front of an old wooden house",
    "rain-street": "Yuri with an umbrella on a rainy old street",
    "ramen-lunch": "Yuri enjoying an early meal",
    "sakura-arms": "Yuri with both hands up under cherry blossoms",
    "sakura-close": "Yuri smiling under cherry blossoms",
    "sakura-wave": "Yuri waving under cherry blossoms",
    "street-wave": "Yuri waving on a sunny Tokyo street",
    "tower-view": "Yuri posing at a city viewpoint",
    "yukata-fan": "Yuri in a yukata with a folding fan, Tokyo Skytree behind her",
    "yukata-river": "Yuri in a yukata by the Sumida River, Tokyo Skytree behind",
}

def wh(n):
    return SIZE.get(n, (1400, 1050) if n in LAND else (1050, 1400))

def img(n, cls="", pos="", eager=False):
    w, h = wh(n)
    c = f' class="{cls}"' if cls else ""
    s = f' style="object-position:{pos}"' if pos else ""
    l = "" if eager else ' loading="lazy"'
    return f'<img src="{I}{n}.jpg" alt="{ALT[n]}" width="{w}" height="{h}"{c}{s}{l}>'

def fit(tag, text, mx=40, cls=""):
    # one-line heading that shrinks to its container (needs a container ancestor)
    return f'<{tag} class="fit {cls}" style="--ch:{len(text)};--mx:{mx}px">{text}</{tag}>'

TOURS = [
    dict(n="01", jp="新橋の夜", t="Shimbashi Night", s="Kimono bar-hopping", when="Evening · about 2.5 h",
         tags=["Sit-down izakaya", "Guide in kimono", "Solo welcome"],
         main="izakaya-fan", sub="izakaya-beer", pos="50% 30%"),
    dict(n="02", jp="清澄白河", t="Kiyosumi-Shirakawa Art Walk", s="Museum · garden · lunch", when="Morning · about 3 h",
         tags=["Museum of Contemporary Art Tokyo", "Kiyosumi Gardens", "Lunch at Fukagawatei"],
         main="garden-pond", sub="lunch-set", pos="70% 50%"),
    dict(n="03", jp="神楽坂から新橋へ", t="Kagurazaka Stroll", t2="& a Shimbashi Evening Hop", s="Afternoon into evening",
         when="Afternoon · about 3.5 h", tags=["Akagi Shrine", "Stone-paved lanes", "One train to Shimbashi"],
         main="street-wave", sub="alley-sign", pos="45% 40%"),
]
CARE = ["Sit-down bars & cafés", "Short walks", "Your guide is a nurse"]

def tour_head(t, mx=40):
    h = fit("h2", t["t"], mx, "tt")
    if t.get("t2"):
        h += f'<p class="tt2 it">{t["t2"]}</p>'
    return h

def tags(t):
    return '<ul class="tags">' + "".join(f"<li>{x}</li>" for x in t["tags"]) + "</ul>"

def care(cls=""):
    return (f'<section class="care cq {cls}"><p class="jp">ゆっくり、座れる</p><h2>'
            + fit("span", "A relaxed pace,", 34, "ln") + fit("span", "plenty of places to sit", 34, "ln")
            + '</h2><ul>' + "".join(f"<li>{x}</li>" for x in CARE) + "</ul></section>")

BOOK = '<p class="book"><span>Price on request</span><span>Bookings opening soon</span></p>'
KZLINK = f'<a class="kz" href="{KZ}" target="_blank" rel="noopener">See her Kanazawa tours ↗</a>'
GUIDE_LINE = '<p class="gl">Nurse · lives in Kanazawa · guides in kimono</p>'
NAV = '<div class="bar"></div><nav class="top"><a class="logo" href="#">Tokyo with <b>Yuri</b></a><span class="soon">Opening soon</span></nav>'
FOOT = '<footer class="foot"><p>Tokyo with Yuri · in preparation</p><p>Photos of Yuri are her own.</p></footer>'

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fbf9f4;--card:#fff;--ink:#2c3440;--mut:#76808b;--ai:#4b6c8f;--ai2:#e5ecf3;--mc:#8a9a5b;--mc2:#eef1e3;--line:#e4e2da}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font:400 16px/1.7 "Source Sans 3",sans-serif;overflow-x:clip;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%;height:auto}
a{color:inherit}ul{list-style:none}
h1,h2,h3{font-family:Lora,serif;font-weight:500;line-height:1.15}
.cq{container-type:inline-size}
.fit{display:block;white-space:nowrap;font-size:min(var(--mx),calc(176cqi / var(--ch)))}
.jp{font-family:"Zen Old Mincho",serif;color:var(--mc);font-size:13px;letter-spacing:.24em}
.it{font-family:Lora,serif;font-style:italic}
.bar{height:5px;background:linear-gradient(90deg,var(--ai) 0 50%,var(--mc) 50%)}
.top{display:flex;justify-content:space-between;align-items:center;height:60px;padding:0 22px;max-width:1180px;margin:0 auto}
.logo{font-family:Lora,serif;font-size:20px;text-decoration:none}.logo b{color:var(--ai);font-weight:500}
.soon{font-size:12.5px;font-weight:600;color:var(--ai);border:1px solid currentColor;border-radius:99px;padding:2px 12px;white-space:nowrap}
.book{display:flex;flex-wrap:wrap;gap:8px 22px;font-size:14px;font-weight:600;color:var(--ai)}
.book span{white-space:nowrap}.book span::before{content:"";display:inline-block;width:14px;height:1px;background:currentColor;vertical-align:middle;margin-right:8px}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tags li{font-size:12.5px;font-weight:600;color:var(--ai);background:var(--ai2);border-radius:6px;padding:2px 10px}
.when{font-size:13px;color:var(--mut);letter-spacing:.04em}
.tt{color:var(--ai)}.tt2{color:var(--ai);font-size:min(22px,6cqi);white-space:nowrap;margin-top:2px}
.sub{font-family:Lora,serif;font-style:italic;color:var(--mc);font-size:16px}
.kz{font-weight:600;color:var(--ai);text-decoration:none;border-bottom:1px solid var(--ai);white-space:nowrap}
.gl{font-size:14px;color:var(--mut)}
.care h2{color:#4b5a2a;margin-top:6px}
.care ul{display:flex;flex-wrap:wrap;gap:8px 10px;margin-top:16px}
.care li{font-size:14px;font-weight:600;color:#4b5a2a;background:#fff;border-radius:99px;padding:4px 14px}
.foot{max-width:1180px;margin:0 auto;padding:28px 22px 40px;font-size:12.5px;color:var(--mut);text-align:center}
@media (prefers-reduced-motion:reduce){*{animation:none!important;scroll-behavior:auto!important}}
"""

def page(v, title, css, body, head_extra="", script=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tokyo with Yuri | {title}</title>
<meta name="description" content="Small private tours in Tokyo with Yuri, a nurse and guide from Kanazawa. Shimbashi at night, an art walk in Kiyosumi-Shirakawa, and a Kagurazaka stroll. Sit-down places, no rushing.">
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="../favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Source+Sans+3:wght@400;600&family=Zen+Old+Mincho:wght@500&display=swap">
{head_extra}<style>{BASE}{css}</style>
</head>
<body class="{v}">
{body}
{FOOT}
{script}</body>
</html>
"""

# ---------------- v1: layered windows (sticky full-bleed photos, cards slide over) ----------------
V1_CSS = """
.lay{display:grid;min-height:175svh;view-timeline:--lay}
.lay>*{grid-area:1/1}
.bgw{position:sticky;top:0;height:100svh;overflow:hidden;align-self:start}
.bgw img{width:100%;height:100%;object-fit:cover}
.card{align-self:end;justify-self:start;position:relative;z-index:2;width:min(460px,88vw);margin:0 0 14svh 7vw;background:rgba(251,249,244,.95);padding:30px 32px 28px;display:flex;flex-direction:column;gap:10px}
.lay.r .card{justify-self:end;margin-right:7vw}
.card .fl{position:absolute;width:40%;aspect-ratio:3/4;object-fit:cover;right:-16%;top:-42%;border:6px solid var(--bg)}
.lay.r .card .fl{right:auto;left:-16%}
.card .num{font-family:Lora,serif;font-size:13px;color:var(--mut);letter-spacing:.12em}
.hero .card{gap:12px}.lay.hero{min-height:calc(100svh - 65px)}.hero .bgw{height:calc(100svh - 65px)}
@media(min-width:701px){.pt .bgw{background:var(--mc2)}.pt .bgw img{width:54%;margin-left:auto}.pt .card{margin-left:9vw}}
.hero .it{font-size:18px;color:#4a525d}
@supports (animation-timeline:view()){
 .bgw img{animation:kb linear both;animation-timeline:--lay}
 .card .fl{animation:drift linear both;animation-timeline:view()}
 @keyframes kb{from{transform:scale(1.08)}to{transform:scale(1)}}
 @keyframes drift{from{transform:translateY(70px)}to{transform:translateY(-70px)}}
}
.care{max-width:860px;margin:0 auto;padding:110px 22px;text-align:center}
.care ul{justify-content:center}
.end{text-align:center;padding:110px 22px 40px;display:flex;flex-direction:column;align-items:center;gap:14px}
@media(max-width:700px){
 .card{margin:0 auto 10svh;justify-self:center;padding:24px 22px}
 .lay.r .card{justify-self:center;margin-right:auto}
 .card .fl,.lay.r .card .fl{width:34%;right:6%;left:auto;top:auto;bottom:calc(100% - 28px)}
 .care,.end{padding:80px 22px}
}
"""
def v1():
    t1, t2, t3 = TOURS
    def tl(t, r=""):
        return f"""<section class="lay {r}{' pt' if wh(t['main'])[1] > wh(t['main'])[0] else ''}" id="t{t['n']}"><div class="bgw">{img(t['main'], pos=t['pos'])}</div>
<div class="card cq">{img(t['sub'], 'fl')}<p class="num">TOUR {t['n']} <span class="jp">{t['jp']}</span></p>{tour_head(t, 34)}<p class="sub">{t['s']}</p>{tags(t)}<p class="when">{t['when']}</p></div></section>"""
    body = f"""{NAV}
<header class="lay hero pt"><div class="bgw">{img('kimono-window', pos='50% 28%', eager=True)}</div>
<div class="card cq"><p class="jp">東京を、ゆりと</p>{fit('h1', 'Tokyo, slowly', 54)}<p class="it">As if you were visiting a friend.</p>{BOOK}</div></header>
{care()}
{tl(t1)}{tl(t2, 'r')}{tl(t3)}
<section class="lay r" id="guide"><div class="bgw">{img('sakura-wave', pos='55% 40%')}</div>
<div class="card cq">{img('sakura-close', 'fl')}<p class="num">YOUR GUIDE <span class="jp">ゆり</span></p>{fit('h2', "Hi, I'm Yuri", 40, 'tt')}{GUIDE_LINE}{KZLINK}</div></section>
<section class="end cq"><p class="jp">料金はお問い合わせください</p>{fit('h2', 'See you in Tokyo', 40, 'tt')}{BOOK}</section>"""
    return page("v1", "Layered windows", V1_CSS, body)

# ---------------- v2: photo river (two drifting rows + a meandering path of stops) ----------------
WAVE = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='640'%3E%3Cpath d='M80 0 C150 160 10 160 80 320 C150 480 10 480 80 640' "
        "fill='none' stroke='%234b6c8f' stroke-opacity='.28' stroke-width='1.5' stroke-dasharray='2 7' stroke-linecap='round'/%3E%3C/svg%3E")
V2_CSS = """
.hero{text-align:center;padding:40px 22px 34px;max-width:900px;margin:0 auto;display:flex;flex-direction:column;align-items:center;gap:10px}
.hero .it{font-size:18px;color:#4a525d}
.river{overflow:hidden;display:flex;flex-direction:column;gap:14px;padding:6px 0 10px}
.row{display:flex;align-items:center;gap:14px;width:max-content;animation:flow 90s linear infinite}
.row.b{animation-direction:reverse;animation-duration:110s}
.row img{height:clamp(170px,24vw,300px);width:auto;border-radius:8px}
.row img:nth-child(3n+2){height:clamp(130px,18vw,230px)}
.river:hover .row{animation-play-state:paused}
@keyframes flow{to{transform:translateX(-50%)}}
.stream{max-width:1080px;margin:0 auto;padding:90px 22px 30px;background:url("WAVE") center top/160px 640px repeat-y;display:flex;flex-direction:column;gap:110px}
.stop{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.stop:nth-child(even) .cl{order:2}
.cl{position:relative;padding-bottom:12%}
.cl .m{width:80%;aspect-ratio:4/5;object-fit:cover;border-radius:10px}
.cl .s{position:absolute;right:0;bottom:0;width:44%;aspect-ratio:3/4;object-fit:cover;border-radius:8px;border:6px solid var(--bg)}
.stop:nth-child(even) .cl .m{margin-left:auto}.stop:nth-child(even) .cl .s{right:auto;left:0}
.tx{display:flex;flex-direction:column;gap:10px;background:var(--bg);padding:12px 0}
.tx .num{font-family:Lora,serif;font-size:56px;line-height:1;color:var(--mc);opacity:.5}
.care{max-width:860px;margin:60px auto 0;background:var(--mc2);border-radius:28px;padding:54px 32px;text-align:center}
.care ul{justify-content:center}
.guide{max-width:860px;margin:0 auto;padding:90px 22px 40px;display:grid;grid-template-columns:200px 1fr;gap:36px;align-items:center}
.guide img{width:200px;aspect-ratio:1;object-fit:cover;border-radius:50%}
.guide>div{display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.end{text-align:center;padding:50px 22px 30px;display:flex;flex-direction:column;align-items:center;gap:12px}
@media(max-width:760px){
 .stream{background:none;gap:76px;padding-top:64px}
 .stop{grid-template-columns:1fr;gap:20px}.stop:nth-child(even) .cl{order:0}
 .care{margin:50px 16px 0;padding:40px 20px}
 .guide{grid-template-columns:1fr;justify-items:center;text-align:center;gap:20px}.guide>div{align-items:center;width:100%}
 .guide img{width:160px}
}
""".replace("WAVE", WAVE)
RIVER_A = ["kimono-window", "cafe-cake", "sakura-arms", "yukata-river", "cheesecake", "old-house", "tower-view"]
RIVER_B = ["azalea", "cafe-smile", "sakura-wave", "rain-street", "yukata-fan", "cafe-cushion", "green-smile"]
def v2():
    def row(ns, c):
        one = "".join(img(n, eager=i < 3) for i, n in enumerate(ns))
        dup = one.replace(' alt="', ' aria-hidden="true" alt="')  # second copy for the seamless loop
        return f'<div class="row {c}">{one}{dup}</div>'
    stops = "".join(f"""<article class="stop" id="t{t['n']}"><div class="cl">{img(t['main'], 'm', t['pos'])}{img(t['sub'], 's')}</div>
<div class="tx cq"><span class="num">{t['n']}</span><p class="jp">{t['jp']}</p>{tour_head(t, 40)}<p class="sub">{t['s']}</p>{tags(t)}<p class="when">{t['when']}</p></div></article>""" for t in TOURS)
    body = f"""{NAV}
<header class="hero cq"><p class="jp">東京を、ゆりと</p>{fit('h1', 'Small moments in Tokyo', 58)}<p class="it">As if you were visiting a friend.</p>{BOOK}</header>
<div class="river">{row(RIVER_A, 'a')}{row(RIVER_B, 'b')}</div>
{care()}
<div class="stream">{stops}</div>
<section class="guide" id="guide">{img('sakura-close')}<div class="cq"><p class="jp">ガイド</p>{fit('h2', "Hi, I'm Yuri", 40, 'tt')}{GUIDE_LINE}{KZLINK}</div></section>
<section class="end cq">{fit('h2', 'See you in Tokyo', 38, 'tt')}{BOOK}</section>"""
    return page("v2", "Photo river", V2_CSS, body)

# ---------------- v3: big photo grid, few words (with an Esri map tile) ----------------
V3_CSS = """
.grid{max-width:1180px;margin:0 auto;padding:6px 22px 30px;display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:130px;gap:12px}
.t{position:relative;overflow:hidden;border-radius:6px;background:var(--card)}
.t>img,.t>#map{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.t .cap{position:absolute;left:0;right:0;bottom:0;padding:40px 16px 12px;font-family:Lora,serif;font-style:italic;color:#fff;font-size:15px;background:linear-gradient(transparent,rgba(30,40,55,.55))}
.tour .cap{padding:70px 22px 20px;font-style:normal;display:flex;flex-direction:column;gap:6px;background:linear-gradient(transparent,rgba(30,40,55,.72) 55%)}
.tour .cap .tt,.tour .cap .tt2{color:#fff}.tour .cap .when{color:#e6ebf0}.tour .cap .jp{color:#d9e3c2}
.txt{padding:28px;display:flex;flex-direction:column;gap:12px;justify-content:center}
.ttl{background:var(--bg);padding-left:6px}.ttl .it{font-size:19px;color:#4a525d}
.care{background:var(--mc2)}
.gd{background:var(--ai);color:#fff}.gd .tt,.gd .kz{color:#fff;border-color:#fff}.gd .gl{color:#dbe4ee}.gd .jp{color:#cfe0b0}
.bk{background:var(--card)}
#map{z-index:1}
.w2{grid-column:span 2}.w3{grid-column:span 3}.w4{grid-column:span 4}.w6{grid-column:span 6}
.h1{grid-row:span 1}.h2{grid-row:span 2}.h3{grid-row:span 3}.h4{grid-row:span 4}
.pin{background:var(--ai);color:#fff;font:600 12px/1 "Source Sans 3";padding:5px 8px;border-radius:99px;white-space:nowrap;transform:translate(-50%,-50%);display:inline-block}
@media(max-width:760px){
 .grid{grid-template-columns:1fr 1fr;grid-auto-rows:minmax(44vw,auto);gap:8px;padding:4px 12px 24px}
 .w2{grid-column:span 1}.w3,.w4,.w6{grid-column:span 2}
 .h1,.h2,.h3,.h4{grid-row:span 1}.m2{grid-row:span 2}.mw{grid-column:span 2}
 .txt{padding:22px 18px}
 .mapt{min-height:72vw}
}
"""
def v3():
    t1, t2, t3 = TOURS
    def ph(n, cap, cls, pos=""):
        return f'<figure class="t {cls}">{img(n, pos=pos)}<figcaption class="cap">{cap}</figcaption></figure>'
    def tour(t, cls):
        return f"""<article class="t tour {cls}" id="t{t['n']}">{img(t['main'], pos=t['pos'])}<div class="cap cq"><p class="jp">{t['n']} · {t['jp']}</p>{tour_head(t, 36)}<p class="when">{t['s']} · {t['when']}</p></div></article>"""
    body = f"""{NAV}
<main class="grid">
{ph('kimono-window', 'In kimono', 'w3 h4 m2', '50% 25%')}
<div class="t txt ttl w3 h2 cq"><p class="jp">東京を、ゆりと</p>{fit('h1', 'Tokyo, slowly.', 64)}<p class="it">As if you were visiting a friend.</p></div>
{ph('sakura-arms', 'Spring', 'w3 h2', '50% 35%')}
{tour(t1, 'w2 h4 m2 mw')}{tour(t2, 'w2 h4 m2 mw')}{tour(t3, 'w2 h4 m2 mw')}
<section class="t txt care w2 h3 mw cq">{care()[len('<section class="care cq ">'):-len('</section>')]}</section>
<div class="t w4 h3 mapt"><div id="map"></div></div>
{ph('izakaya-beer', 'Evenings', 'w2 h3 mw', '50% 20%')}
<div class="t txt gd w2 h3 mw cq" id="guide"><p class="jp">ガイド</p>{fit('h2', "Hi, I'm Yuri", 40, 'tt')}<p class="gl">Nurse · lives in Kanazawa · guides in kimono</p>{KZLINK}</div>
{ph('sakura-close', 'Yuri', 'w2 h3', '50% 40%')}{ph('ramen-lunch', 'Early dinner', 'w2 h3', '50% 30%')}
{ph('lunch-set', 'Lunch', 'w2 h3 mw', '50% 40%')}{ph('yukata-fan', 'Summer, in yukata', 'w2 h3 mw', '50% 55%')}
<div class="t txt bk w6 h2 cq"><p class="jp">料金はお問い合わせください</p>{fit('h2', 'See you in Tokyo', 40, 'tt')}{BOOK}</div>
</main>"""
    head = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'
    script = """<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
var m=L.map('map',{scrollWheelZoom:false,attributionControl:true});
m.fitBounds([[35.6671,139.7355],[35.7020,139.7970]],{padding:[50,50]});
var E='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_';
L.tileLayer(E+'Base/MapServer/tile/{z}/{y}/{x}',{attribution:'Tiles &copy; Esri &mdash; Esri, HERE, Garmin, &copy; OpenStreetMap contributors',maxZoom:16}).addTo(m);
L.tileLayer(E+'Reference/MapServer/tile/{z}/{y}/{x}',{maxZoom:16,pane:'overlayPane'}).addTo(m);
[['Shimbashi',35.6671,139.7576],['Kagurazaka',35.702,139.7355],['Kiyosumi',35.6799,139.797]].forEach(function(p){
 L.marker([p[1],p[2]],{icon:L.divIcon({className:'',html:'<span class="pin">'+p[0]+'</span>',iconSize:[0,0]})}).addTo(m);});
</script>
"""
    return page("v3", "Big photos, few words", V3_CSS, body, head, script)

# ---------------- v4: vertical Japanese type beside tall photos ----------------
V4_CSS = """
.vt{writing-mode:vertical-rl;font-family:"Zen Old Mincho",serif;color:var(--ai);letter-spacing:.28em;line-height:1;font-size:clamp(34px,4.2vw,54px);white-space:nowrap}
.sec{max-width:1120px;margin:0 auto;padding:90px 22px 0;display:grid;grid-template-columns:auto 1fr 1fr;gap:0 48px;align-items:start}
.sec .vt{border-right:1px solid var(--line);padding-right:24px}
.ph{display:grid;grid-template-columns:3fr 2fr;gap:12px;align-items:end}
.ph img{width:100%;object-fit:cover;aspect-ratio:3/4}
.ph img+img{aspect-ratio:3/4;margin-bottom:-48px}
.tx{display:flex;flex-direction:column;gap:10px;align-self:center}
.tx .num{font-family:Lora,serif;font-size:13px;letter-spacing:.16em;color:var(--mut)}
.hero{padding-top:30px;grid-template-columns:auto 1.3fr 1fr}
.hero .big{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 25%}
.hero .it{font-size:19px;color:#4a525d}
.sec.r .ph{order:2}.sec.r .tx{order:1}
.care{max-width:1120px;margin:110px auto 0;padding:56px 22px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);display:grid;grid-template-columns:auto 1fr;gap:0 40px;align-items:center}
.care .vt{grid-row:span 3;color:var(--mc);font-size:clamp(28px,3.4vw,40px)}
.care .jp{display:none}
.end{text-align:center;padding:120px 22px 30px;display:flex;flex-direction:column;align-items:center;gap:12px}
@media(max-width:820px){
 .sec,.hero{grid-template-columns:auto 1fr;gap:0 16px;padding-top:64px}
 .hero{padding-top:20px}
 .sec .vt{grid-row:span 2;padding-right:14px}
 .tx{grid-column:2;margin-top:64px}
 .hero .tx{margin-top:28px}
 .sec.r .ph{order:0}.sec.r .tx{order:0}
 .care{margin-top:80px;gap:0 18px;padding:40px 22px}
}
"""
def v4():
    def sec(t, r=""):
        return f"""<section class="sec {r}" id="t{t['n']}"><p class="vt" lang="ja">{t['jp']}</p>
<div class="ph">{img(t['main'], pos=t['pos'])}{img(t['sub'])}</div>
<div class="tx cq"><p class="num">TOUR {t['n']}</p>{tour_head(t, 38)}<p class="sub">{t['s']}</p>{tags(t)}<p class="when">{t['when']}</p></div></section>"""
    t1, t2, t3 = TOURS
    care_inner = care()
    body = f"""{NAV}
<header class="sec hero"><p class="vt" lang="ja">東京を、ゆりと</p>
<div>{img('kimono-window', 'big', eager=True)}</div>
<div class="tx cq">{fit('h1', 'Tokyo with Yuri', 52, 'tt')}<p class="it">As if you were visiting a friend.</p>{BOOK}</div></header>
<div class="care cq"><p class="vt" lang="ja">ゆっくり、座れる</p>{care_inner[len('<section class="care cq ">'):-len('</section>')]}</div>
{sec(t1)}{sec(t2, 'r')}{sec(t3)}
<section class="sec" id="guide"><p class="vt" lang="ja">ゆり</p>
<div class="ph">{img('rain-street')}{img('old-house')}</div>
<div class="tx cq"><p class="num">YOUR GUIDE</p>{fit('h2', "Hi, I'm Yuri", 40, 'tt')}{GUIDE_LINE}{KZLINK}</div></section>
<section class="end cq"><p class="jp">料金はお問い合わせください</p>{fit('h2', 'See you in Tokyo', 40, 'tt')}{BOOK}</section>"""
    return page("v4", "Vertical type", V4_CSS, body)

# ---------------- v5: carousels (hero slideshow, a carousel per tour, small moments) ----------------
V5_CSS = """
.car{position:relative}
.trk{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;gap:12px;overscroll-behavior-x:contain}
.trk::-webkit-scrollbar{display:none}
.trk>*{flex:0 0 auto;scroll-snap-align:start;position:relative}
.trk img{width:100%;height:100%;object-fit:cover}
.cap{position:absolute;left:14px;bottom:12px;font-family:Lora,serif;font-style:italic;color:#fff;font-size:15px;text-shadow:0 1px 8px rgba(0,0,0,.45)}
.dots{display:flex;justify-content:center;gap:8px;margin-top:12px}
.dots button{width:8px;height:8px;border-radius:50%;border:0;background:#cfd6de;cursor:pointer;padding:0}
.dots button[aria-current=true]{background:var(--ai);width:22px;border-radius:4px}
.nav{position:absolute;top:50%;translate:0 -50%;width:42px;height:42px;border-radius:50%;border:0;background:rgba(251,249,244,.92);color:var(--ai);font:500 20px/1 Lora,serif;cursor:pointer}
.nav.p{left:12px}.nav.n{right:12px}
.hero .trk{gap:12px;padding:0 22px;scroll-padding:0 22px}.hero .trk>*{width:min(520px,40vw);height:min(74svh,680px);border-radius:8px;overflow:hidden}
.intro{max-width:900px;margin:0 auto;padding:34px 22px 10px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px}
.intro .it{font-size:18px;color:#4a525d}
.care{max-width:1180px;margin:40px auto 0;padding:0 22px;text-align:center}.care ul{justify-content:center}
.tours{max-width:1180px;margin:0 auto;padding:80px 22px 0;display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.tc .trk>*{width:86%;aspect-ratio:4/5;border-radius:8px;overflow:hidden}
.tc .tx{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.mom{padding:90px 0 0}
.mom .hd{max-width:1180px;margin:0 auto 18px;padding:0 22px}
.mom .trk{padding:0 22px;scroll-padding:0 22px}
.mom .trk>*{width:min(270px,64vw);aspect-ratio:3/4;border-radius:8px;overflow:hidden}
.guide{max-width:900px;margin:0 auto;padding:90px 22px 0;display:grid;grid-template-columns:240px 1fr;gap:36px;align-items:center}
.guide img{aspect-ratio:4/5;object-fit:cover;border-radius:8px}
.guide>div{display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.end{text-align:center;padding:90px 22px 30px;display:flex;flex-direction:column;align-items:center;gap:12px}
@media(max-width:900px){.tours{grid-template-columns:1fr;gap:56px;padding-top:64px}.tc .trk>*{width:82%}}
@media(max-width:620px){.nav{display:none}.hero .trk{gap:0;padding:0}.hero .trk>*{width:100%;height:72svh;border-radius:0}.guide{grid-template-columns:1fr;gap:20px}.guide>div{width:100%}.guide img{width:70%}}
"""
HERO5 = [("kimono-window", "In kimono", "50% 25%"), ("sakura-wave", "Spring", "55% 40%"), ("yukata-river", "Summer, in yukata", "50% 30%"),
         ("green-smile", "Green days", "45% 40%"), ("izakaya-fan", "Evenings", "50% 35%")]
TOURPICS = {"01": ["izakaya-fan", "izakaya-beer", "kimono-window"], "02": ["garden-pond", "green-smile", "lunch-set"], "03": ["alley-sign", "street-wave", "ramen-lunch"]}
MOMENTS = [("cafe-cake", "Tea and cake"), ("azalea", "Azaleas"), ("cheesecake", "Cheesecake"), ("tower-view", "City views"), ("cafe-cushion", "Cozy cafés"),
           ("sakura-arms", "Cherry blossoms"), ("rain-street", "Rainy days"), ("old-house", "Old houses"), ("cafe-smile", "Laughing a lot"), ("yukata-fan", "Summer, in yukata")]
V5_JS = """<script>
document.querySelectorAll('.car').forEach(function(c){
 var t=c.querySelector('.trk'),s=[].slice.call(t.children),d=c.querySelector('.dots'),bs=[];
 s.forEach(function(e,i){var b=document.createElement('button');b.setAttribute('aria-label','Photo '+(i+1));b.onclick=function(){go(i)};d.appendChild(b);bs.push(b)});
 function cur(){var x=t.scrollLeft,k=0;s.forEach(function(e,i){if(Math.abs(e.offsetLeft-t.offsetLeft-x)<Math.abs(s[k].offsetLeft-t.offsetLeft-x))k=i});return k}
 function go(i){i=(i+s.length)%s.length;t.scrollTo({left:s[i].offsetLeft-t.offsetLeft,behavior:'smooth'})}
 function upd(){var k=cur();bs.forEach(function(b,i){b.setAttribute('aria-current',i===k)})}
 t.addEventListener('scroll',function(){requestAnimationFrame(upd)},{passive:true});upd();
 c.querySelectorAll('.nav').forEach(function(b){b.onclick=function(){go(cur()+(b.classList.contains('n')?1:-1))}});
 if(c.classList.contains('auto')&&!matchMedia('(prefers-reduced-motion:reduce)').matches){var iv=setInterval(function(){go(cur()+1)},5200);
  ['pointerdown','wheel','touchstart'].forEach(function(e){t.addEventListener(e,function(){clearInterval(iv)},{passive:true})});c.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){clearInterval(iv)})})}
});
</script>
"""
def v5():
    def car(items, cls="", navb=False):
        nb = '<button class="nav p" aria-label="Previous photo">‹</button><button class="nav n" aria-label="Next photo">›</button>' if navb else ""
        return f'<div class="car {cls}"><div class="trk">{items}</div>{nb}<div class="dots"></div></div>'
    hero = "".join(f'<figure>{img(n, pos=p, eager=i == 0)}<figcaption class="cap">{c}</figcaption></figure>' for i, (n, c, p) in enumerate(HERO5))
    tours = "".join(f"""<article class="tc" id="t{t['n']}">{car(''.join(f'<figure>{img(n)}</figure>' for n in TOURPICS[t['n']]))}
<div class="tx cq"><p class="jp">{t['n']} · {t['jp']}</p>{tour_head(t, 30)}<p class="sub">{t['s']}</p>{tags(t)}<p class="when">{t['when']}</p></div></article>""" for t in TOURS)
    mom = "".join(f'<figure>{img(n)}<figcaption class="cap">{c}</figcaption></figure>' for n, c in MOMENTS)
    body = f"""{NAV}
<header class="hero">{car(hero, 'auto', True)}</header>
<div class="intro cq"><p class="jp">東京を、ゆりと</p>{fit('h1', 'Tokyo with Yuri', 56, 'tt')}<p class="it">As if you were visiting a friend.</p>{BOOK}</div>
{care()}
<section class="tours">{tours}</section>
<section class="mom"><div class="hd cq"><p class="jp">小さなひととき</p>{fit('h2', 'Small moments', 40, 'tt')}</div>{car(mom)}</section>
<section class="guide" id="guide">{img('sakura-close')}<div class="cq"><p class="jp">ガイド</p>{fit('h2', "Hi, I'm Yuri", 40, 'tt')}{GUIDE_LINE}{KZLINK}</div></section>
<section class="end cq"><p class="jp">料金はお問い合わせください</p>{fit('h2', 'See you in Tokyo', 40, 'tt')}{BOOK}</section>"""
    return page("v5", "Carousels", V5_CSS, body, script=V5_JS)

# ---------------- comparison board (Japanese notes for Yuuki) ----------------
VARIANTS = [
    ("v1", "重なる窓", "全面写真が画面に貼りつき、その上を短いカードが滑っていく。スクロールで写真がゆっくり寄り、小窓の写真が浮く（パララックス）。"),
    ("v2", "写真の川", "冒頭で写真2列が左右逆向きにゆっくり流れ続ける。ツアーは点線の川筋に沿って左右交互に、写真2枚の重なりで並ぶ。"),
    ("v3", "大判グリッド＋ひとこと", "雑誌の見開きのような大判写真のタイル組み。文字は写真に添える一言だけ。地図（Esri）もタイルの1枚として入る。"),
    ("v4", "縦書きの地名", "明朝の縦書き（新橋の夜／清澄白河／神楽坂から新橋へ）を細い罫線で区切り、縦長の写真2枚と並べる。いちばん和の空気が強い案。"),
    ("v5", "カルーセル", "ヒーローは全幅の自動スライド（季節ごとの5枚）。ツアーごとに3枚の写真カルーセル、最後に「Small moments」10枚の横送り。"),
]
def board():
    cards = "".join(f"""<article><a href="{v}.html"><img src="shots/{v}-pc.jpg" alt="{v} PC版のスクリーンショット" loading="lazy"><img class="sp" src="shots/{v}-sp.jpg" alt="{v} スマホ版のスクリーンショット" loading="lazy"></a>
<div><p class="no">{v.upper()}</p><h2>{name}</h2><p>{desc}</p><a class="go" href="{v}.html">開いて見る →</a></div></article>""" for v, name, desc in VARIANTS)
    return f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ゆりっぺ東京ツアー 第3ラウンド 見比べボード</title><meta name="robots" content="noindex"><link rel="icon" type="image/png" href="../favicon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@500&family=Zen+Old+Mincho:wght@500&family=Source+Sans+3:wght@400;600&display=swap">
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#fbf9f4;color:#2c3440;font:400 15px/1.8 "Source Sans 3","Hiragino Sans",sans-serif;overflow-x:clip}}
.w{{max-width:1100px;margin:0 auto;padding:40px 22px 60px}}h1{{font-family:"Zen Old Mincho",serif;font-weight:500;font-size:clamp(20px,5vw,30px)}}
.lead{{color:#76808b;margin-top:8px}}.bar{{height:5px;background:linear-gradient(90deg,#4b6c8f 0 50%,#8a9a5b 50%)}}
article{{display:grid;grid-template-columns:1.4fr 1fr;gap:28px;align-items:center;padding:34px 0;border-bottom:1px solid #e4e2da}}
article>a{{position:relative;display:block;padding-right:16%}}article img{{width:100%;border-radius:6px;box-shadow:0 6px 24px rgba(40,50,60,.12);display:block}}
article img.sp{{position:absolute;right:0;bottom:-14px;width:24%;border:4px solid #fff;border-radius:10px}}
.no{{font-family:Lora,serif;color:#8a9a5b;letter-spacing:.14em;font-size:13px}}h2{{font-family:"Zen Old Mincho",serif;font-weight:500;font-size:24px;color:#4b6c8f}}
.go{{display:inline-block;margin-top:10px;color:#4b6c8f;font-weight:600;text-decoration:none;border-bottom:1px solid}}
@media(max-width:760px){{article{{grid-template-columns:1fr;gap:22px}}}}</style></head>
<body><div class="bar"></div><div class="w"><h1>東京ツアーページ 第3ラウンド 見比べボード</h1>
<p class="lead">第2ラウンドのv3「やさしい和モダン」の色と書体のまま、説明文を削って写真を主役にした5案です。案ごとに「ワクワクの仕掛け」を変えています。全案共通で、ツアー3本・座れる配慮・Price on request・Bookings opening soon・金沢サイトへのリンクを入れています。</p>
{cards}</div></body></html>
"""

if __name__ == "__main__":
    for f, fn in [("v1", v1), ("v2", v2), ("v3", v3), ("v4", v4), ("v5", v5)]:
        (H / f"{f}.html").write_text(fn())
    (H / "index.html").write_text(board())
    # self-check: required facts present in every variant
    for f in ["v1", "v2", "v3", "v4", "v5"]:
        s = (H / f"{f}.html").read_text()
        for need in ["Shimbashi Night", "Kiyosumi-Shirakawa Art Walk", "Kagurazaka Stroll", "Shimbashi Evening Hop",
                     "A relaxed pace,", "plenty of places to sit", "Price on request", "Bookings opening soon", KZ, "nurse"]:
            assert need in s, (f, need)
        assert "Maru" not in s
    print("built + checks ok")
