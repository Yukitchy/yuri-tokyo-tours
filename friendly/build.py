# build.py — generates v1.html..v5.html + index.html (friendly round, English editions)
# Facts come from ../index.html (v1). Run: python3 build.py
import json, pathlib
HERE = pathlib.Path(__file__).parent

# ---------- shared content (English) ----------
KEY = [
    ("For", "Guests who want Tokyo's evening drinks and art at an easy, local pace."),
    ("When", "Only on days Yuri is in Tokyo. Once your booking is confirmed, she travels down from Kanazawa."),
    ("Meet", "An easy-to-find spot for each tour, like the steam locomotive at Shimbashi Station's SL Square."),
    ("First", "Sit down for a drink, or step into the museum. Nothing rushed from the start."),
    ("Then", "The rest follows the mood of the day. Peek down side streets and drop into places that catch your eye."),
]
CARE_T = "A relaxed pace, plenty of places to sit"
CARE_SHORT = "Easy pace, lots of seats"
CARE_H = "A relaxed pace,<br>plenty of places to sit"
CARE = [
    "Mostly sit-down bars and restaurants, not standing bars.",
    "Short walks between stops. We agree on the walking distance before the day.",
    "Your guide is a nurse, and walks close enough to notice when you need a break.",
]
TOURS = [
    dict(id="t1", t="Shimbashi Night", s="Kimono bar-hopping", img="img/yuri-izakaya-fan.jpg", alt="Yuri raising a drink and a folding fan at an izakaya",
         lead="An evening of bar-hopping in Shimbashi, the after-work heart of Tokyo, with a guide in kimono. We meet at SL Square and wander into the izakaya lanes by the Karasumori exit. Not a tourist strip, just Tokyo's real after-work night.",
         do="We start with a toast at a sit-down izakaya and try the day's specials. Yuri takes care of the little alleys, how to walk in without breaking the regulars' easy mood, and how to order. You can add one slightly special stop, like fugu or seasonal small plates. We end by the steam locomotive at SL Square, talking over the night.",
         inc="Your private guide, help choosing and booking places, and help with ordering. Food and drinks are paid on the day, at cost.",
         know="This is not a stand-all-night tour. Non-drinkers enjoy it just as much with soft drinks. Solo travelers are welcome.",
         chips=["Sit-down bars", "Guided in kimono", "Small groups, solo welcome"], dur="About 2.5 hours", start="Around 18:00"),
    dict(id="t2", t="Kiyosumi Art Walk", s="Museum, garden and a classic lunch", img="img/yuri-garden-pond.jpg", alt="Yuri smiling beside a Japanese garden pond",
         lead="The daytime tour Yuri, an art lover, recommends most. Take your time at the Museum of Contemporary Art Tokyo and Kiyosumi Gardens in Kiyosumi-Shirakawa, then lunch at a long-loved local spot. Quiet, green, and light on walking.",
         do="At the museum, Yuri picks the highlights from the special and collection exhibitions. Then a loop of Kiyosumi Gardens, slowly. We rest by the pond and talk about the stones and pines. Lunch is a teppan set meal at Fukagawatei, a long-standing local favorite.",
         inc="Your private guide, route planning, and guiding on the day. Admission fees and meals are extra, paid at cost.",
         know="A knee-friendly pace with breaks along the way. Not held on Mondays, when the museum is closed.",
         chips=["Museum and garden", "Plenty of rest stops", "Lunch at a local classic"], dur="About 3 hours", start="Around 10:30"),
    dict(id="t3", t="Kagurazaka to Shimbashi", s="An afternoon stroll, then an evening hop", img="img/yuri-street-wave.jpg", alt="Yuri waving on a sunny Tokyo street",
         lead="Walk the stone-paved lanes of Kagurazaka in the late afternoon, then ride over to Shimbashi for a drink. Tokyo by day and Tokyo by night, in one outing.",
         do="We stop at Akagi Shrine, then wander down Kagurazaka, peeking into the stone-paved alleys. Early dinner is ramen at Menya Fuufuutei, a popular Kagurazaka spot. Then one train to Shimbashi: SL Square lit up at night, and a last drink at an izakaya. One train ride and short walks, by design.",
         inc="Your private guide, and help choosing places and ordering. Food, drinks and train fares are extra, paid at cost.",
         know="We take Kagurazaka's slopes at an easy pace. On rainy days we can switch to a shorter, Shimbashi-only version.",
         chips=["Alleys and lanes", "Just one train ride", "Daylight into evening"], dur="About 3.5 hours", start="Around 16:00"),
]
FOOD = [
    ("Genpin Ginza-Shimbashi", "Fugu · Shimbashi", "Weekdays 16:00–22:00", "../img/tile-genpin.jpg", "Fugu sashimi at Genpin", "%E7%8E%84%E5%93%81+%E9%8A%80%E5%BA%A7%E6%96%B0%E6%A9%8B"),
    ("Fukagawatei", "Teppan set meals · Kiyosumi-Shirakawa", "11:30–14:00 / 17:30–21:00", "../img/tile-fukagawatei.jpg", "Teppan dishes at Fukagawatei", "%E6%B7%B1%E5%B7%9D%E4%BA%AD+%E6%B8%85%E6%BE%84%E7%99%BD%E6%B2%B3"),
    ("Menya Fuufuutei", "Ramen · Kagurazaka", "11:30–22:00", "../img/tile-fuufuutei.jpg", "Ramen at Menya Fuufuutei", "%E9%BA%BA%E5%B1%8B%E3%81%B5%E3%81%85%E3%81%B5%E3%81%85%E4%BA%AD+%E7%A5%9E%E6%A5%BD%E5%9D%82"),
]
SPOTS = [
    dict(n=1, short="Shimbashi", name="SL Square, Shimbashi", sub="Meeting point for Shimbashi Night", img="../img/pin-sl.jpg", lat=35.6671, lng=139.7576),
    dict(n=2, short="Kagurazaka", name="Akagi Shrine, Kagurazaka", sub="Where the afternoon stroll begins", img="../img/pin-kagurazaka.jpg", lat=35.7020, lng=139.7355),
    dict(n=3, short="Kiyosumi", name="Kiyosumi Gardens", sub="The garden on the art walk", img="../img/pin-kiyosumi.jpg", lat=35.6799, lng=139.7970),
]
BIO = [
    "I live in Kanazawa and work as a nurse.",
    "In Tokyo, I love the stretch from Shinjuku to Shimbashi. In the bar streets of Shimbashi you can almost hear people saying “otsukaresama” (good work today) on their way home, and I never get tired of it. Walking in kimono changes how the city looks, just a little. I'd love to share that feeling with you.",
    "I love art, too. Walking around neighborhoods with museums is how I spend my days off. In Shirakawa-go, people I guided asked me to guide them again.",
    "My knees aren't the best, so I build my tours around two things: places to sit, and no rushing. If walking worries you, come just as you are.",
    "When a booking comes in, I travel from Kanazawa to Tokyo. I'm looking forward to meeting you.",
]
FACTS = ["Lives in Kanazawa", "Nurse", "Guides in kimono", "Art lover", "Asked back as a Shirakawa-go guide", "Also guides in Kanazawa"]
KZ = "https://yuri.kanazawa-guide.com/"
STEPS = [
    ("Send your dates", "Tell us which tour and which dates you'd like, how many of you, and how much you want to walk."),
    ("We set the day", "The date is fixed to match Yuri's Tokyo trip. She takes care of the restaurant bookings."),
    ("Meet and enjoy", "That's it. Ordering and train changes are all on her."),
]
CTA_T = "Let's start with a chat"
CTA_P = "This page is still being prepared. Full details on tours and dates are coming soon."
CTA_NOTE = "Booking isn't open yet. We're getting it ready."
CREDIT = "Photos of Yuri are her own. SL Square photo: Mike Peel (CC BY-SA 4.0, Wikimedia Commons). Other place photos taken on the tour routes."
TITLE = "Tokyo with Yuri | Small private tours, as if visiting a friend"
DESC = "Yuri, a nurse and guide from Kanazawa, comes to Tokyo for small private tours: Shimbashi at night in kimono, an art walk in Kiyosumi-Shirakawa, and a Kagurazaka stroll. Sit-down places, no rushing."

def head(title_suffix, fonts, css, tiles):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE} ({title_suffix})</title>
<meta name="description" content="{DESC}">
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="../favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{overflow-x:hidden;-webkit-font-smoothing:antialiased}}
img{{display:block;max-width:100%}}
.cq,.sh,.cta,.tour .tx{{container-type:inline-size}}
a{{color:inherit}}
ul,ol{{list-style:none}}
.nw{{white-space:nowrap}}
#map{{height:400px;z-index:1}}
@media(max-width:560px){{#map{{height:330px}}}}
.pin-card{{width:auto;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,.22);position:relative}}
.pin-card img{{width:96px;height:62px;object-fit:cover}}
.pin-card .nm{{font-size:12px;font-weight:600;text-align:center;padding:2px 3px 4px;line-height:1.3;color:#333;white-space:nowrap}}
.pin-card::after{{content:"";position:absolute;left:50%;bottom:-8px;transform:translateX(-50%);border:5px solid transparent;border-top:9px solid #fff}}
{css}
</style>
</head>
<body>
"""

def map_js(tiles, hd_bg, hd_fg="#fff"):
    return f"""<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
var map=L.map('map',{{scrollWheelZoom:false}});var S=innerWidth<560,PW=S?70:96,PH=S?84:104;
map.fitBounds([[35.6671,139.7355],[35.7020,139.7970]],{{padding:S?[60,40]:[90,90]}});
var E='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_';
L.tileLayer(E+'Base/MapServer/tile/{{z}}/{{y}}/{{x}}',{{attribution:'Tiles &copy; Esri &mdash; Esri, HERE, Garmin, &copy; OpenStreetMap contributors',maxZoom:16}}).addTo(map);
L.tileLayer(E+'Reference/MapServer/tile/{{z}}/{{y}}/{{x}}',{{maxZoom:16,pane:'overlayPane'}}).addTo(map);
document.querySelector('.leaflet-tile-pane').style.filter='{tiles}';
{json.dumps(SPOTS)}.forEach(function(s){{
 var icon=L.divIcon({{className:'',html:'<div class="pin-card"><div style="background:{hd_bg};color:{hd_fg};font-size:12px;font-weight:700;text-align:center;padding:1px 0">'+s.n+'</div><img src="'+s.img+'" alt="" style="width:'+PW+'px;height:'+(S?44:62)+'px"><div class="nm">'+s.short+'</div></div>',iconSize:[PW,PH],iconAnchor:[PW/2,PH],popupAnchor:[0,-PH+6]}});
 L.marker([s.lat,s.lng],{{icon:icon}}).addTo(map).bindPopup('<b>'+s.name+'</b><br>'+s.sub);
}});
</script>
</body>
</html>
"""

POS = {"img/yuri-izakaya-fan.jpg": "50% 62%", "img/yuri-garden-pond.jpg": "72% 50%", "img/yuri-street-wave.jpg": "50% 40%", "img/yuri-azalea.jpg": "50% 45%", "img/yuri-lunch-set.jpg": "50% 40%", "img/yuri-alley-sign.jpg": "50% 45%", "img/yuri-ramen-lunch.jpg": "50% 35%", "img/yuri-izakaya-beer.jpg": "40% 12%", "img/yuri-green-smile.jpg": "55% 40%"}
def timg(t, swap=None):
    src, alt = (swap or {}).get(t["id"], (t["img"], t["alt"]))
    return f'<img src="{src}" alt="{alt}" loading="lazy" style="object-position:{POS.get(src, "50% 50%")}">'

def tour_body(t, h4="h4"):
    return f"""<{h4}>What you'll do</{h4}><p>{t['do']}</p>
<{h4}>What's included</{h4}><p>{t['inc']}</p>
<{h4}>Good to know</{h4}><p>{t['know']}</p>"""

def chips(t, cls="chips"):
    return f'<ul class="{cls}">' + "".join(f"<li>{c}</li>" for c in t["chips"]) + "</ul>"

def meta(t, cls="meta"):
    return f"""<dl class="{cls}"><div><dt>Duration</dt><dd>{t['dur']}</dd></div><div><dt>Starts</dt><dd>{t['start']}</dd></div><div><dt>Price</dt><dd>On request</dd></div></dl>"""

def food_tiles(cls="tiles"):
    out = f'<div class="{cls}">'
    for nm, tag, hr, img, alt, q in FOOD:
        out += f"""<a class="tile" href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener"><div class="ph"><img src="{img}" alt="{alt}" loading="lazy"></div><div class="tx"><span class="tag">{tag}</span><span class="nm">{nm}</span><span class="hr">{hr}</span></div></a>"""
    return out + "</div>"

def key_list(cls="key"):
    return f'<dl class="{cls}">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in KEY) + "</dl>"

def care_list():
    return "<ul>" + "".join(f"<li>{c}</li>" for c in CARE) + "</ul>"

def bio():
    return "".join(f"<p>{p}</p>" for p in BIO)

def facts(cls="facts"):
    return f'<ul class="{cls}">' + "".join(
        f'<li><a href="{KZ}" target="_blank" rel="noopener">{f} ↗</a></li>' if f.startswith("Also") else f"<li>{f}</li>" for f in FACTS) + "</ul>"

def steps(cls="steps"):
    return f'<ol class="{cls}">' + "".join(f"<li><span class=\"n\">{i+1}</span><h3>{h}</h3><p>{p}</p></li>" for i, (h, p) in enumerate(STEPS)) + "</ol>"

def footer(cls="foot"):
    return f'<footer class="{cls}"><p>Tokyo with Yuri · in preparation</p><p>{CREDIT}</p></footer>'

# ============ V1  Warm cream × coral ============
def v1():
    css = """
:root{--bg:#fff7ee;--card:#fffdf9;--ink:#3a2a24;--mut:#8a746a;--co:#ee6c58;--co2:#fbd9cf;--line:#f0dfd2}
body{background:var(--bg);color:var(--ink);font:400 16px/1.75 "Work Sans",sans-serif}
.w{max-width:1040px;margin:0 auto;padding:0 22px}
h1,h2,h3{font-family:"Fraunces",serif;font-weight:600;font-variation-settings:"SOFT" 100,"WONK" 1;letter-spacing:-.01em}
.hand{font-family:"Caveat","Klee One",cursive;color:var(--co);font-weight:600}
.jp{font-family:"Klee One",serif;font-size:13px;color:var(--mut);letter-spacing:.08em}
nav.top{display:flex;justify-content:space-between;align-items:center;height:64px}
nav.top .logo{font-family:"Caveat",cursive;font-size:30px;font-weight:700;color:var(--co);text-decoration:none}
nav.top .links{display:flex;gap:22px;font-size:14px}nav.top .links a{text-decoration:none}
@media(max-width:600px){nav.top .links a:nth-child(n+3){display:none}nav.top .links{gap:14px}}
.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center;padding:30px 0 56px}
.hero .hand{font-size:30px;line-height:1}
.hero h1{font-size:min(56px,8.4cqi);line-height:1.1;margin:10px 0 18px;white-space:nowrap}
.hero h1 em{font-style:italic;color:var(--co)}
.hero p{font-size:17px;max-width:30em}
.hero .btns{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap}
.btn{display:inline-block;background:var(--co);color:#fff;text-decoration:none;font-weight:600;border-radius:999px;padding:13px 28px;font-size:15px}
.btn.ghost{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.arch{position:relative}
.arch img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:999px 999px 28px 28px;object-position:50% 35%}
.arch .sm{position:absolute;left:-34px;bottom:-26px;width:42%;aspect-ratio:1;border-radius:50%;border:6px solid var(--bg);object-fit:cover}
.arch .note{position:absolute;right:-6px;top:20px;background:var(--card);padding:10px 16px;border-radius:16px;box-shadow:0 8px 24px rgba(120,60,40,.12);font-family:"Caveat",cursive;font-size:22px;line-height:1.1;color:var(--ink)}
@media(max-width:820px){.hero{grid-template-columns:1fr;gap:34px;padding-top:10px}.arch{max-width:420px;margin:0 auto 20px;width:88%}.arch .sm{left:-16px}}
.key{display:grid;grid-template-columns:repeat(5,1fr);gap:0;background:var(--card);border-radius:24px;padding:8px;box-shadow:0 1px 0 var(--line)}
.key div{padding:16px 16px 14px;border-right:1px dashed var(--line)}.key div:last-child{border:0}
.key dt{font-family:"Caveat",cursive;font-size:24px;color:var(--co);line-height:1}
.key dd{font-size:14px;line-height:1.6;margin-top:6px}
@media(max-width:860px){.key{grid-template-columns:1fr 1fr}.key div{border-right:0;border-bottom:1px dashed var(--line)}.key div:last-child{grid-column:1/3}}
@media(max-width:420px){.key{grid-template-columns:1fr}.key div:last-child{grid-column:auto}}
.care{margin-top:24px;display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;background:var(--co2);border-radius:24px;padding:24px 28px}
.care h2{font-size:min(28px,8.2cqi);white-space:nowrap;line-height:1.2}
.care ul{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:10px}
.care li{font-size:14.5px;line-height:1.6;padding-left:26px;position:relative}
.care li::before{content:"✓";position:absolute;left:0;top:0;color:var(--co);font-weight:700}
.care img{width:120px;height:120px;border-radius:50%;object-fit:cover;border:5px solid #fff}
@media(max-width:760px){.care{grid-template-columns:1fr;padding:22px 20px}.care ul{grid-template-columns:1fr}.care img{display:none}}
section{padding:72px 0 0}
.sh{margin-bottom:26px}.sh .hand{font-size:26px}
.sh h2{font-size:min(40px,7.6cqi);white-space:nowrap;line-height:1.15}
.tour{display:grid;grid-template-columns:1fr 1.15fr;gap:44px;align-items:start;margin-bottom:64px}
.tour:nth-of-type(even) .ph{order:2}
.tour .ph img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:28px}
.tour h3{font-size:min(36px,8cqi);white-space:nowrap;line-height:1.1}
.tour .sub{font-family:"Caveat",cursive;font-size:24px;color:var(--co);margin:2px 0 12px}
.tour .lead{font-size:16.5px}
.tour h4{font-family:"Fraunces",serif;font-size:16px;font-weight:600;margin:18px 0 2px}
.tour p{font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.chips li{background:var(--co2);color:#8e3a2c;border-radius:999px;padding:5px 14px;font-size:13px;font-weight:500}
.meta{display:flex;flex-wrap:wrap;gap:6px 28px;margin-top:20px;padding-top:14px;border-top:1px dashed var(--line)}
.meta dt{font-size:12px;color:var(--mut)}.meta dd{font-family:"Fraunces",serif;font-size:18px;font-weight:600}
@media(max-width:820px){.tour{grid-template-columns:1fr;gap:20px}.tour:nth-of-type(even) .ph{order:0}.tour .ph img{aspect-ratio:4/3}}
#map{border-radius:24px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.tile{background:var(--card);border-radius:22px;overflow:hidden;text-decoration:none;box-shadow:0 1px 0 var(--line)}
.tile .ph{height:180px;overflow:hidden}.tile img{width:100%;height:100%;object-fit:cover}
.tile .tx{display:flex;flex-direction:column;padding:14px 16px 16px}
.tile .tag{font-size:12px;color:var(--co);font-weight:600}.tile .nm{font-family:"Fraunces",serif;font-size:19px;font-weight:600}.tile .hr{font-size:13px;color:var(--mut)}
@media(max-width:760px){.tiles{grid-template-columns:1fr}}
.guide{display:grid;grid-template-columns:.9fr 1.1fr;gap:44px;align-items:start}
.guide .pics{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.guide .pics img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:22px}
.guide .pics img:first-child{grid-column:1/3;aspect-ratio:4/3}
.guide .msg p{font-size:15.5px;margin-top:12px}.guide .msg p:first-child{margin-top:0;font-family:"Fraunces",serif;font-size:21px;line-height:1.45}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.facts li{border:1.5px solid var(--line);background:var(--card);border-radius:999px;padding:4px 14px;font-size:13px}
.facts a{text-decoration:none;color:var(--co);font-weight:600}
@media(max-width:820px){.guide{grid-template-columns:1fr}}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;counter-reset:s}
.steps li{background:var(--card);border-radius:22px;padding:24px}
.steps .n{font-family:"Caveat",cursive;font-size:44px;color:var(--co);line-height:1}
.steps h3{font-size:20px;margin:6px 0}.steps p{font-size:14.5px}
@media(max-width:760px){.steps{grid-template-columns:1fr}}
.cta{margin-top:56px;background:var(--co);color:#fff;border-radius:32px;padding:44px 26px;text-align:center}
.cta .hand{color:#fff;font-size:26px}.cta h2{font-size:min(40px,8.4cqi);white-space:nowrap}
.cta p{max-width:34em;margin:10px auto 22px;opacity:.95}
.cta .btn{background:#fff;color:var(--co)}.cta small{display:block;margin-top:14px;font-size:13px;opacity:.9}
.foot{margin:60px auto 0;max-width:1040px;padding:24px 22px 40px;border-top:1px dashed var(--line);font-size:12.5px;color:var(--mut);display:flex;flex-direction:column;gap:4px}
"""
    T = TOURS
    h = head("Warm cream", "family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..700,100,1;1,9..144,400..700,100,1&family=Caveat:wght@500;700&family=Work+Sans:wght@400;500;600&family=Klee+One:wght@600", css, "")
    h += f"""<div class="w">
<nav class="top"><a class="logo" href="#">Yuri in Tokyo</a><div class="links"><a href="#tours">Tours</a><a href="#guide">About Yuri</a><a href="#area">Area</a><a href="#how">How it works</a></div></nav>
<header class="hero">
 <div class="cq">
  <div class="hand">Hello from Yuri!</div>
  <h1>Tokyo, <em>as if</em> you were<br>visiting a friend</h1>
  <p>Not just famous spots, but the small moments of everyday life. Yuri usually lives in Kanazawa and comes to Tokyo for small, calm tours on the days you book.</p>
  <div class="btns"><a class="btn" href="#tours">See the 3 tours</a><a class="btn ghost" href="#guide">Meet Yuri</a></div>
 </div>
 <div class="arch">
  <img src="img/yuri-yukata-fan.jpg" alt="Yuri in a yukata with a folding fan, Tokyo Skytree behind her">
  <img class="sm" src="img/yuri-sakura-arms.jpg" alt="Yuri smiling under cherry blossoms">
  <div class="note">Kanazawa nurse,<br>Tokyo guide</div>
 </div>
</header>
{key_list()}
<div class="care"><img src="img/yuri-cafe-cake.jpg" alt="Yuri at a café table with tea and cake"><div class="cq"><h2>{CARE_H}</h2><div class="jp">ゆっくり、座れるツアー</div>{care_list()}</div></div>

<section id="tours"><div class="sh"><div class="hand">Tours · ツアー</div><h2>Three ways to spend a day</h2></div>
""" + "".join(f"""<article class="tour" id="{t['id']}"><div class="ph">{timg(t,{"t2":("img/yuri-azalea.jpg","Yuri standing among azaleas in a garden")})}</div><div class="cq"><h3>{t['t']}</h3><div class="sub">{t['s']}</div><p class="lead">{t['lead']}</p>{tour_body(t)}{chips(t)}{meta(t)}</div></article>""" for t in T) + f"""</section>

<section id="guide"><div class="sh"><div class="hand">Your guide · ガイド</div><h2>Hi, I'm Yuri</h2></div>
<div class="guide"><div class="pics"><img src="img/yuri-sakura-wave.jpg" alt="Yuri waving under cherry blossoms" loading="lazy"><img src="img/yuri-kimono-window.jpg" alt="Yuri in a pink kimono" loading="lazy"><img src="img/yuri-cafe-smile.jpg" alt="Yuri laughing at a café" loading="lazy"></div>
<div><div class="msg">{bio()}</div>{facts()}</div></div></section>

<section id="area"><div class="sh"><div class="hand">Area · エリア</div><h2>Where we'll go</h2></div><div id="map"></div></section>
<section id="food"><div class="sh"><div class="hand">Where we eat · 寄る店</div><h2>Places on the way</h2></div>{food_tiles()}</section>
<section id="how"><div class="sh"><div class="hand">How it works · 流れ</div><h2>Three easy steps</h2></div>{steps()}
<div class="cta"><div class="hand">Price on request</div><h2>{CTA_T}</h2><p>{CTA_P}</p><a class="btn" href="#tours">Look at the tours</a><small>{CTA_NOTE}</small></div></section>
</div>
{footer()}
"""
    return h + map_js("sepia(.35) saturate(1.4) hue-rotate(-12deg) brightness(1.03)", "#ee6c58")

# ============ V2  Photo-forward magazine ============
def v2():
    css = """
:root{--bg:#fbf6ee;--ink:#2b2226;--mut:#7d6e72;--pl:#8f5f6e;--pl2:#efe2e4;--line:#e6d9d3}
body{background:var(--bg);color:var(--ink);font:400 16px/1.75 "Lora",serif}
.sans{font-family:"Manrope",sans-serif}
.w{max-width:1120px;margin:0 auto;padding:0 22px}
.script{font-family:"Great Vibes",cursive;color:var(--pl);font-weight:400}
h1,h2,h3{font-family:"Lora",serif;font-weight:500;letter-spacing:-.01em}
.kick{white-space:nowrap;font-family:"Manrope",sans-serif;font-size:12px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--pl)}
.kick span{letter-spacing:.1em;font-weight:500;color:var(--mut);margin-left:6px}
.hero{position:relative;height:min(100svh,880px);min-height:560px;overflow:hidden;color:#fff}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 12%}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,18,22,.35) 0%,rgba(30,18,22,0) 26%,rgba(30,18,22,0) 40%,rgba(30,18,22,.55) 62%,rgba(30,18,22,.86) 100%)}
.hero nav{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center;padding:16px 24px}
.hero nav .script{color:#fff;font-size:44px;line-height:1}
.hero nav .sans{font-size:13px;letter-spacing:.06em}
.hero nav a{text-decoration:none}
.hero .cap{position:absolute;z-index:2;left:0;right:0;bottom:0;padding:0 24px 44px;max-width:1120px;margin:0 auto}
.hero h1{font-size:min(72px,7.4cqi);line-height:1.06;white-space:nowrap}
.hero p{font-size:clamp(15px,2.3vw,19px);margin-top:14px;max-width:32em;opacity:.95}
.hero .sans.k{font-size:12px;letter-spacing:.24em;text-transform:uppercase;margin-bottom:12px;font-weight:600}
.strip{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin-top:4px}
.strip img{width:100%;aspect-ratio:1;object-fit:cover}
@media(max-width:600px){.strip{grid-template-columns:repeat(3,1fr)}.strip img:nth-child(n+4){display:none}}
.intro{display:grid;grid-template-columns:1fr 1.4fr;gap:56px;padding:72px 0 0}
.intro .big{font-size:clamp(22px,3.4vw,32px);line-height:1.4}
.intro .big em{color:var(--pl)}
.key{border-top:1px solid var(--ink)}
.key div{display:grid;grid-template-columns:90px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}
.key dt{font-family:"Manrope",sans-serif;font-weight:700;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--pl);padding-top:4px}
.key dd{font-size:15px}
@media(max-width:820px){.intro{grid-template-columns:1fr;gap:28px;padding-top:52px}}
.care{margin-top:56px;display:grid;grid-template-columns:1fr 1fr;background:var(--pl2)}
.care img{width:100%;height:100%;object-fit:cover;min-height:280px}
.care .tx{padding:40px 40px}
.care h2{font-size:min(32px,8.4cqi);white-space:nowrap;line-height:1.2;margin:8px 0 14px}
.care li{font-family:"Manrope",sans-serif;font-size:15px;padding:10px 0;border-top:1px solid rgba(143,95,110,.25)}
@media(max-width:760px){.care{grid-template-columns:1fr}.care img{min-height:0;aspect-ratio:4/3}.care .tx{padding:28px 22px}}
section{padding:88px 0 0}
.sh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:6px 20px;border-bottom:1px solid var(--ink);padding-bottom:12px;margin-bottom:36px}
.sh h2{font-size:min(52px,9cqi);white-space:nowrap;line-height:1}
.tour{display:grid;grid-template-columns:1.25fr 1fr;gap:0;margin-bottom:72px;background:#fff}
.tour:nth-of-type(even){grid-template-columns:1fr 1.25fr}.tour:nth-of-type(even) .ph{order:2}
.tour .ph{position:relative;min-height:520px}
.tour .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tour .ph .no{position:absolute;left:18px;top:8px;font-family:"Lora",serif;font-size:96px;color:#fff;line-height:1;text-shadow:0 2px 20px rgba(0,0,0,.25)}
.tour .tx{padding:40px 38px}
.tour h3{font-size:min(40px,8.2cqi);white-space:nowrap;line-height:1.1}
.tour .sub{font-style:italic;color:var(--pl);font-size:18px;margin:6px 0 16px}
.tour .lead{font-size:17px;line-height:1.7}
.tour h4{font-family:"Manrope",sans-serif;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--pl);margin:22px 0 4px}
.tour p{font-size:15.5px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;font-family:"Manrope",sans-serif}
.chips li{border:1px solid var(--pl);color:var(--pl);border-radius:999px;padding:4px 14px;font-size:12.5px;font-weight:600}
.meta{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:4px 34px;margin-top:22px;padding-top:16px;border-top:1px solid var(--line)}
.meta dt{font-family:"Manrope",sans-serif;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}.meta dd{font-size:18px}
@media(max-width:860px){.tour,.tour:nth-of-type(even){grid-template-columns:1fr}.tour:nth-of-type(even) .ph{order:0}.tour .ph{min-height:0;aspect-ratio:4/5}.tour .tx{padding:28px 22px}}
@media(max-width:420px){.meta{grid-template-columns:repeat(2,auto)}}
.moments{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:220px;grid-auto-flow:dense;gap:8px}
.moments figure{overflow:hidden;position:relative}.moments img{width:100%;height:100%;object-fit:cover}
.moments .t{grid-row:span 2}.moments .wd{grid-column:span 2}
.moments figcaption{position:absolute;left:10px;bottom:8px;color:#fff;font-size:13px;font-style:italic;text-shadow:0 1px 8px rgba(0,0,0,.6)}
@media(max-width:760px){.moments{grid-template-columns:1fr 1fr;grid-auto-rows:160px}}
.mnote{font-size:13px;color:var(--mut);margin-top:12px;font-family:"Manrope",sans-serif}
.guide{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.guide>img{width:100%;aspect-ratio:3/4;object-fit:cover}
.guide .script{font-size:72px;line-height:1}
.guide .msg p{margin-top:12px;font-size:16px}
.guide .msg p:first-child{font-size:21px;line-height:1.5}
.facts{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:22px;font-family:"Manrope",sans-serif;font-size:13px;font-weight:600;color:var(--pl)}
.facts li::before{content:"— ";color:var(--line)}
@media(max-width:820px){.guide{grid-template-columns:1fr;gap:26px}}
#map{border:1px solid var(--line)}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.tile{text-decoration:none}.tile .ph{aspect-ratio:4/3;overflow:hidden}.tile img{width:100%;height:100%;object-fit:cover}
.tile .tx{display:flex;flex-direction:column;padding-top:12px}
.tile .tag{font-family:"Manrope",sans-serif;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--pl);font-weight:700}.tile .nm{font-size:22px}.tile .hr{font-family:"Manrope",sans-serif;font-size:13px;color:var(--mut)}
@media(max-width:760px){.tiles{grid-template-columns:1fr}}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.steps .n{font-size:56px;color:var(--pl);line-height:1}.steps h3{font-size:22px;margin:8px 0}.steps p{font-size:15px}
@media(max-width:760px){.steps{grid-template-columns:1fr;gap:20px}}
.cta{margin-top:80px;position:relative;color:#fff;text-align:center;overflow:hidden}
.cta img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%}
.cta::before{content:"";position:absolute;inset:0;background:rgba(60,30,40,.55);z-index:1}
.cta>div{position:relative;z-index:2;padding:80px 22px}
.cta h2{font-size:min(52px,8.6cqi);white-space:nowrap}.cta p{max-width:34em;margin:12px auto 24px}
.btn{display:inline-block;font-family:"Manrope",sans-serif;font-weight:700;font-size:14px;letter-spacing:.06em;text-decoration:none;background:#fff;color:var(--pl);padding:14px 30px;border-radius:2px}
.cta small{display:block;margin-top:14px;font-family:"Manrope",sans-serif;font-size:13px;opacity:.9}
.foot{max-width:1120px;margin:0 auto;padding:28px 22px 44px;font-family:"Manrope",sans-serif;font-size:12.5px;color:var(--mut);display:flex;flex-direction:column;gap:4px}
"""
    T = TOURS
    h = head("Magazine", "family=Lora:ital,wght@0,400;0,500;1,400&family=Great+Vibes&family=Manrope:wght@500;600;700", css, "")
    h += f"""<header class="hero"><img src="img/yuri-yukata-river.jpg" alt="Yuri in a yukata by the Sumida River, Tokyo Skytree behind">
<nav><a class="script" href="#">Yuri</a><a class="sans" href="#tours">Tours &nbsp;·&nbsp; About &nbsp;·&nbsp; Area</a></nav>
<div class="cap cq"><div class="sans k">Private guide · Tokyo edition</div><h1>Discover Tokyo with Yuri,<br>a friend in the city</h1><p>Not just famous spots, but the small moments of everyday life. Calm and personal, from Shimbashi's after-work lanes to a quiet garden.</p></div></header>
<div class="strip"><img src="img/yuri-sakura-wave.jpg" alt="Yuri under cherry blossoms"><img src="img/yuri-izakaya-beer.jpg" alt="Yuri with a glass of beer"><img src="img/yuri-cafe-cake.jpg" alt="Yuri at a café"><img src="img/yuri-garden-pond.jpg" alt="Yuri by a garden pond"><img src="img/yuri-alley-sign.jpg" alt="Yuri on a Tokyo side street"></div>
<div class="w">
<div class="intro"><div><div class="kick">The basics<span>はじめに</span></div><p class="big" style="margin-top:14px">A walk through the city, <em>as if you were visiting a friend.</em></p></div>{key_list()}</div>
</div>
<div class="w"><div class="care"><img src="img/yuri-lunch-set.jpg" alt="Yuri seated at a table with a set lunch"><div class="tx cq"><div class="kick">Take it slow<span>ゆっくり</span></div><h2>{CARE_H}</h2>{care_list()}</div></div></div>
<div class="w">
<section id="tours"><div class="sh"><h2>The tours</h2><div class="kick">Tours<span>ツアー</span></div></div>
""" + "".join(f"""<article class="tour" id="{t['id']}"><div class="ph">{timg(t,{"t3":("img/yuri-alley-sign.jpg","Yuri on a tree-lined Tokyo side street")})}<span class="no">0{i+1}</span></div><div class="tx"><h3>{t['t']}</h3><div class="sub">{t['s']}</div><p class="lead">{t['lead']}</p>{tour_body(t)}{chips(t)}{meta(t)}</div></article>""" for i, t in enumerate(T)) + f"""</section>

<section id="moments"><div class="sh"><h2>Small moments</h2><div class="kick">Yuri<span>ゆりの日常</span></div></div>
<div class="moments">
<figure class="t"><img src="img/yuri-kimono-window.jpg" alt="Yuri in a pink kimono" loading="lazy"><figcaption>In kimono</figcaption></figure>
<figure class="wd"><img src="img/yuri-green-smile.jpg" alt="Yuri smiling by a green river gorge" loading="lazy"><figcaption>A green walk</figcaption></figure>
<figure><img src="img/yuri-cheesecake.jpg" alt="Yuri with cheesecake" loading="lazy"><figcaption>Cake break</figcaption></figure>
<figure><img src="img/yuri-sakura-close.jpg" alt="Yuri under cherry blossoms" loading="lazy"><figcaption>Spring</figcaption></figure>
<figure class="wd"><img src="img/yuri-azalea.jpg" alt="Yuri among azaleas" loading="lazy" style="object-position:50% 40%"><figcaption>Azaleas in bloom</figcaption></figure>
<figure class="t"><img src="img/yuri-old-house.jpg" alt="Yuri in front of an old wooden house" loading="lazy"><figcaption>Old streets</figcaption></figure>
<figure><img src="img/yuri-cafe-smile.jpg" alt="Yuri laughing at a café" loading="lazy"><figcaption>Coffee time</figcaption></figure>
<figure><img src="img/yuri-tower-view.jpg" alt="Yuri posing at a city viewpoint" loading="lazy" style="object-position:50% 30%"><figcaption>City views</figcaption></figure>
</div><p class="mnote">Photos from Yuri's own days off and travels.</p></section>

<section id="guide"><div class="sh"><h2>Meet Yuri</h2><div class="kick">Your guide<span>ガイド</span></div></div>
<div class="guide"><img src="img/yuri-sakura-arms.jpg" alt="Yuri with arms up under cherry blossoms" loading="lazy" style="object-position:40% 50%"><div><div class="script">Yuri</div><div class="msg">{bio()}</div>{facts()}</div></div></section>

<section id="area"><div class="sh"><h2>The area</h2><div class="kick">Area<span>エリア</span></div></div><div id="map"></div></section>
<section id="food"><div class="sh"><h2>Where we eat</h2><div class="kick">Food<span>寄る店</span></div></div>{food_tiles()}</section>
<section id="how"><div class="sh"><h2>How it works</h2><div class="kick">Steps<span>流れ</span></div></div>{steps()}</section>
</div>
<div class="cta"><img src="img/yuri-yukata-fan.jpg" alt="" loading="lazy"><div><div class="kick" style="color:#fff;white-space:normal">Price on request<span style="color:#f3dfe4">料金は応相談</span></div><h2 style="margin-top:10px">{CTA_T}</h2><p>{CTA_P}</p><a class="btn" href="#tours">Look at the tours</a><small>{CTA_NOTE}</small></div></div>
{footer()}
"""
    return h + map_js("sepia(.2) hue-rotate(290deg) saturate(1.2)", "#8f5f6e")

# ============ V3  Gentle wa-modern ============
def v3():
    css = """
:root{--bg:#fbf9f4;--card:#fff;--ink:#2c3440;--mut:#76808b;--ai:#4b6c8f;--ai2:#e5ecf3;--mc:#8a9a5b;--mc2:#eef1e3;--line:#e4e2da}
body{background:var(--bg);color:var(--ink);font:400 16px/1.8 "Source Sans 3",sans-serif}
.w{max-width:980px;margin:0 auto;padding:0 22px}
h1,h2,h3{font-family:"Lora",serif;font-weight:500}
.jp{font-family:"Zen Old Mincho",serif;color:var(--mc);font-size:14px;letter-spacing:.2em}
.bar{height:6px;background:linear-gradient(90deg,var(--ai) 0 33.3%,var(--mc) 33.3% 66.6%,#d8b98a 66.6%)}
nav.top{display:flex;justify-content:space-between;align-items:center;height:64px}
nav.top .logo{font-family:"Lora",serif;font-size:21px;text-decoration:none}
nav.top .logo b{color:var(--ai);font-weight:500}
nav.top .links{display:flex;gap:22px;font-size:14px;color:var(--mut)}nav.top .links a{text-decoration:none}
@media(max-width:600px){nav.top .links a:nth-child(n+3){display:none}nav.top .links{gap:14px}}
.hero{text-align:center;padding:34px 0 64px}
.hero .ring{width:min(300px,70vw);aspect-ratio:1;border-radius:50%;margin:0 auto;padding:10px;background:conic-gradient(var(--ai2),var(--mc2),var(--ai2))}
.hero .ring img{width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:50% 22%}
.hero .jp{margin-top:26px}
.hero h1{font-size:min(52px,8.4cqi);line-height:1.2;margin-top:8px;white-space:nowrap}
.hero h1 i{color:var(--ai)}
.hero p{max-width:34em;margin:16px auto 0;color:#4a525d;font-size:17px}
.hero .pair{display:flex;justify-content:center;gap:14px;margin-top:30px}
.hero .pair img{width:min(150px,28vw);aspect-ratio:3/4;object-fit:cover;border-radius:14px}
.key{display:grid;grid-template-columns:repeat(5,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.key div{padding:20px 14px;text-align:center;border-right:1px solid var(--line)}.key div:last-child{border:0}
.key dt{font-family:"Lora",serif;font-style:italic;color:var(--ai);font-size:20px}
.key dd{font-size:14px;line-height:1.6;margin-top:4px;color:#4a525d}
@media(max-width:820px){.key{grid-template-columns:1fr}.key div{border-right:0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:70px 1fr;text-align:left;gap:10px;padding:14px 4px}.key div:last-child{border:0}}
.care{margin-top:40px;background:var(--mc2);border-radius:20px;padding:30px 32px;text-align:center}
.care h2{font-size:min(28px,8.4cqi);white-space:nowrap;line-height:1.25;color:#4b5a2a}
.care ul{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:20px;text-align:left}
.care li{background:#fff;border-radius:14px;padding:16px 18px;font-size:14.5px;line-height:1.6}
.care li::before{content:"";display:block;width:22px;height:3px;background:var(--mc);margin-bottom:10px;border-radius:2px}
@media(max-width:760px){.care{padding:24px 18px}.care ul{grid-template-columns:1fr}}
section{padding:84px 0 0}
.sh{text-align:center;margin-bottom:36px}
.sh h2{font-size:min(40px,9cqi);white-space:nowrap;margin-top:6px}
.sh h2::after{content:"";display:block;width:36px;height:2px;background:var(--ai);margin:14px auto 0}
.tour{background:var(--card);border-radius:22px;overflow:hidden;margin-bottom:34px;box-shadow:0 1px 2px rgba(40,50,60,.05),0 8px 30px rgba(40,50,60,.05);display:grid;grid-template-columns:320px 1fr}
.tour .ph img{width:100%;height:100%;object-fit:cover;min-height:100%}
.tour .tx{padding:32px 34px}
.tour .lbl{font-family:"Lora",serif;font-style:italic;color:var(--mc);font-size:15px}
.tour h3{font-size:min(32px,8.2cqi);white-space:nowrap;line-height:1.2;color:var(--ai)}
.tour .sub{color:var(--mut);margin-bottom:12px}
.tour .lead{font-size:16.5px}
.tour h4{font-family:"Lora",serif;font-size:16px;font-weight:600;margin:18px 0 2px;padding-left:12px;border-left:3px solid var(--mc)}
.tour p{font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.chips li{background:var(--ai2);color:var(--ai);border-radius:8px;padding:4px 12px;font-size:13px;font-weight:600}
.meta{display:flex;flex-wrap:wrap;gap:6px 30px;margin-top:20px;padding-top:14px;border-top:1px solid var(--line)}
.meta dt{font-size:12px;color:var(--mut)}.meta dd{font-family:"Lora",serif;font-size:18px}
@media(max-width:820px){.tour{grid-template-columns:1fr}.tour .ph img{aspect-ratio:16/11;height:auto}.tour .tx{padding:24px 20px}}
#map{border-radius:20px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.tile{background:var(--card);border-radius:18px;overflow:hidden;text-decoration:none;box-shadow:0 1px 2px rgba(40,50,60,.06)}
.tile .ph{height:180px}.tile img{width:100%;height:100%;object-fit:cover}
.tile .tx{display:flex;flex-direction:column;padding:14px 16px 16px}
.tile .tag{font-size:12px;color:var(--mc);font-weight:700}.tile .nm{font-family:"Lora",serif;font-size:19px}.tile .hr{font-size:13px;color:var(--mut)}
@media(max-width:760px){.tiles{grid-template-columns:1fr}}
.guide{background:var(--card);border-radius:24px;padding:40px;display:grid;grid-template-columns:240px 1fr;gap:40px}
.guide .col{display:flex;flex-direction:column;gap:12px}
.guide .col img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:50%}
.guide .col img+img{border-radius:16px;aspect-ratio:4/5}
.guide h3{font-size:30px;color:var(--ai)}.guide .msg p{margin-top:12px;font-size:15.5px}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.facts li{background:var(--mc2);color:#4b5a2a;border-radius:8px;padding:4px 12px;font-size:13px;font-weight:600}
.facts a{text-decoration:none}
@media(max-width:760px){.guide{grid-template-columns:1fr;padding:26px 20px}.guide .col{flex-direction:row}.guide .col img{width:50%}.guide .col img+img{aspect-ratio:1}}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--line)}
.steps li{padding:24px 22px;border-right:1px solid var(--line);text-align:center}.steps li:last-child{border:0}
.steps .n{display:inline-flex;width:40px;height:40px;border-radius:50%;background:var(--ai);color:#fff;align-items:center;justify-content:center;font-family:"Lora",serif;font-size:18px}
.steps h3{font-size:20px;margin:12px 0 4px}.steps p{font-size:14.5px;color:#4a525d}
@media(max-width:760px){.steps{grid-template-columns:1fr}.steps li{border-right:0;border-bottom:1px solid var(--line)}}
.cta{margin-top:60px;background:var(--ai);color:#fff;border-radius:24px;padding:48px 24px;text-align:center}
.cta .jp{color:#cfe0b0}.cta h2{font-size:min(38px,8.6cqi);white-space:nowrap;margin-top:6px}
.cta p{max-width:34em;margin:10px auto 22px;color:#e2e9f1}
.btn{display:inline-block;background:#fff;color:var(--ai);text-decoration:none;font-weight:700;border-radius:12px;padding:13px 30px}
.cta small{display:block;margin-top:14px;color:#cdd8e4}
.foot{max-width:980px;margin:56px auto 0;padding:24px 22px 40px;border-top:1px solid var(--line);font-size:12.5px;color:var(--mut);display:flex;flex-direction:column;gap:4px;text-align:center}
"""
    T = TOURS
    h = head("Gentle wa-modern", "family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Source+Sans+3:wght@400;600;700&family=Zen+Old+Mincho:wght@500", css, "")
    h += f"""<div class="bar"></div><div class="w">
<nav class="top"><a class="logo" href="#">Tokyo with <b>Yuri</b></a><div class="links"><a href="#tours">Tours</a><a href="#guide">Yuri</a><a href="#area">Area</a><a href="#how">How</a></div></nav>
<header class="hero cq">
 <div class="ring"><img src="img/yuri-kimono-window.jpg" alt="Yuri in a pink kimono, smiling with her hands by her face"></div>
 <div class="jp">東京を、ゆりと</div>
 <h1>Calm and personal days<br>in <i>Tokyo</i></h1>
 <p>Not just famous spots, but the small moments of everyday life. A walk through the city, as if you were visiting a friend.</p>
 <div class="pair"><img src="img/yuri-garden-pond.jpg" alt="Yuri by a garden pond"><img src="img/yuri-azalea.jpg" alt="Yuri among azaleas"><img src="img/yuri-izakaya-fan.jpg" alt="Yuri with a fan at an izakaya"></div>
</header>
{key_list()}
<div class="care cq"><div class="jp">ゆっくり、座れる</div><h2>{CARE_H}</h2>{care_list()}</div>

<section id="tours"><div class="sh"><div class="jp">ツアー</div><h2>Three tours</h2></div>
""" + "".join(f"""<article class="tour" id="{t['id']}"><div class="ph">{timg(t,{"t1":("img/yuri-izakaya-beer.jpg","Yuri raising a glass of beer at an izakaya"),"t2":("img/yuri-green-smile.jpg","Yuri smiling in the greenery by a river")})}</div><div class="tx"><div class="lbl">Tour {i+1}</div><h3>{t['t']}</h3><div class="sub">{t['s']}</div><p class="lead">{t['lead']}</p>{tour_body(t)}{chips(t)}{meta(t)}</div></article>""" for i, t in enumerate(T)) + f"""</section>

<section id="guide"><div class="sh"><div class="jp">ガイド</div><h2>Your guide</h2></div>
<div class="guide"><div class="col"><img src="img/yuri-sakura-close.jpg" alt="Yuri smiling under cherry blossoms" loading="lazy"><img src="img/yuri-rain-street.jpg" alt="Yuri with an umbrella on a rainy old street" loading="lazy"></div><div><h3>Hi, I'm Yuri</h3><div class="msg">{bio()}</div>{facts()}</div></div></section>

<section id="area"><div class="sh"><div class="jp">エリア</div><h2>Where we'll walk</h2></div><div id="map"></div></section>
<section id="food"><div class="sh"><div class="jp">寄る店</div><h2>Where we eat</h2></div>{food_tiles()}</section>
<section id="how"><div class="sh"><div class="jp">流れ</div><h2>How it works</h2></div>{steps()}
<div class="cta"><div class="jp">料金はお問い合わせください</div><h2>{CTA_T}</h2><p>Price on request. {CTA_P}</p><a class="btn" href="#tours">Look at the tours</a><small>{CTA_NOTE}</small></div></section>
</div>
{footer()}
"""
    return h + map_js("sepia(.25) hue-rotate(170deg) saturate(1.1)", "#4b6c8f")

# ============ V4  Café-style cozy ============
def v4():
    css = """
:root{--kraft:#e8d9bf;--paper:#f7efe1;--ink:#3b2b1e;--mut:#7a6650;--br:#9a5b2e;--gr:#5e7550;--line:#cdb894}
body{background:var(--kraft);background-image:radial-gradient(rgba(120,80,40,.07) 1px,transparent 1.2px);background-size:7px 7px;color:var(--ink);font:400 16px/1.75 "Libre Franklin",sans-serif}
.w{max-width:1000px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:"Young Serif",serif;font-weight:400}
.mono{font-family:"Courier Prime",monospace}
.stamp{display:inline-block;font-family:"Courier Prime",monospace;font-weight:700;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--br);border:2px solid var(--br);border-radius:6px;padding:2px 10px;transform:rotate(-2deg)}
.stamp span{letter-spacing:.04em;font-weight:400;margin-left:6px}
nav.top{display:flex;justify-content:space-between;align-items:center;height:64px}
nav.top .logo{font-family:"Young Serif",serif;font-size:22px;text-decoration:none}
nav.top .links{display:flex;gap:20px;font-family:"Courier Prime",monospace;font-size:14px}nav.top .links a{text-decoration:none}
@media(max-width:600px){nav.top .links a:nth-child(n+3){display:none}nav.top .links{gap:14px}}
.hero{display:grid;grid-template-columns:1fr 1fr;gap:0;background:var(--paper);border-radius:6px;box-shadow:0 2px 0 var(--line),0 18px 40px rgba(80,50,20,.12);overflow:hidden;margin-top:6px}
.hero .ph{position:relative}.hero .ph img{width:100%;height:100%;object-fit:cover;min-height:520px;object-position:50% 30%}
.hero .tx{padding:44px 40px;display:flex;flex-direction:column;justify-content:center}
.hero .open{font-family:"Courier Prime",monospace;font-size:13px;color:var(--gr);letter-spacing:.12em;text-transform:uppercase}
.hero h1{font-size:min(50px,10cqi);line-height:1.12;margin:12px 0 16px;white-space:nowrap}
.hero p{font-size:16.5px;color:#55432f}
.hero .sig{margin-top:22px;display:flex;gap:12px;align-items:center}
.hero .sig img{width:56px;height:56px;border-radius:50%;object-fit:cover;border:3px solid #fff}
.hero .sig span{font-family:"Courier Prime",monospace;font-size:14px}
@media(max-width:820px){.hero{grid-template-columns:1fr}.hero .ph img{min-height:0;aspect-ratio:4/5}.hero .tx{padding:28px 22px}}
.key{margin-top:26px;display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.key div{background:var(--paper);border-radius:6px;padding:16px;box-shadow:0 2px 0 var(--line)}
.key dt{font-family:"Courier Prime",monospace;font-weight:700;color:var(--br);font-size:13px;letter-spacing:.14em;text-transform:uppercase;border-bottom:1px dashed var(--line);padding-bottom:6px;margin-bottom:8px}
.key dd{font-size:14px;line-height:1.6}
@media(max-width:860px){.key{grid-template-columns:1fr 1fr}.key div:last-child{grid-column:1/3}}
@media(max-width:420px){.key{grid-template-columns:1fr}.key div:last-child{grid-column:auto}}
.care{margin-top:26px;background:var(--gr);color:#f5efe0;border-radius:6px;padding:26px 28px;display:grid;grid-template-columns:1fr 1.6fr;gap:26px;align-items:center}
.care h2{font-size:min(28px,8cqi);white-space:nowrap;line-height:1.2}
.care .stamp{color:#f1e3c4;border-color:#f1e3c4;margin-bottom:10px}
.care li{font-size:14.5px;padding:8px 0;border-bottom:1px dashed rgba(245,239,224,.35)}.care li:last-child{border:0}
@media(max-width:760px){.care{grid-template-columns:1fr;gap:10px;padding:22px 18px}}
section{padding:76px 0 0}
.sh{display:flex;flex-direction:column;align-items:flex-start;gap:8px;margin-bottom:24px}
.sh h2{font-size:min(42px,9cqi);white-space:nowrap;line-height:1.1}
.menu{background:var(--paper);border-radius:6px;box-shadow:0 2px 0 var(--line),0 18px 40px rgba(80,50,20,.1);padding:14px 34px 30px}
.menu .hd{text-align:center;padding:16px 0 6px;border-bottom:2px solid var(--ink)}
.menu .hd h3{font-size:min(28px,8cqi);white-space:nowrap}
.menu .hd .mono{font-size:13px;color:var(--mut)}
.tour{display:grid;grid-template-columns:230px 1fr;gap:28px;padding:30px 0;border-bottom:1px dashed var(--line)}
.tour:last-child{border:0;padding-bottom:6px}
.tour .ph img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:4px;border:6px solid #fff;box-shadow:0 3px 10px rgba(80,50,20,.15)}
.tour .line{display:flex;align-items:baseline;gap:10px}
.tour h3{font-size:min(30px,8.2cqi);white-space:nowrap;line-height:1.15}
.tour .line i{flex:1;border-bottom:2px dotted var(--mut);transform:translateY(-6px);min-width:10px}
.tour .line .pr{font-family:"Courier Prime",monospace;font-size:14px;white-space:nowrap;color:var(--br);font-weight:700}
.tour .sub{font-family:"Courier Prime",monospace;color:var(--gr);font-size:14.5px;margin:2px 0 12px}
.tour .lead{font-size:16px}
.tour h4{font-family:"Courier Prime",monospace;font-size:13.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--br);margin:16px 0 2px}
.tour p{font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.chips li{font-family:"Courier Prime",monospace;font-size:13px;font-weight:700;color:var(--gr);border:2px solid var(--gr);border-radius:6px;padding:2px 10px;transform:rotate(-2deg)}
.meta{display:flex;flex-wrap:wrap;gap:6px 26px;margin-top:18px;font-family:"Courier Prime",monospace}
.meta dt{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.1em}.meta dd{font-size:16px;font-weight:700}
@media(max-width:760px){.menu{padding:10px 18px 22px}.tour{grid-template-columns:1fr;gap:16px}.tour .ph img{aspect-ratio:4/3}.tour .line .pr{display:none}.tour .line i{display:none}}
#map{border-radius:6px;border:6px solid var(--paper)}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.tile{background:var(--paper);border-radius:6px;padding:10px 10px 14px;text-decoration:none;box-shadow:0 2px 0 var(--line)}
.tile .ph{height:170px;overflow:hidden;border-radius:3px}.tile img{width:100%;height:100%;object-fit:cover}
.tile .tx{display:flex;flex-direction:column;padding:10px 4px 0}
.tile .tag{font-family:"Courier Prime",monospace;font-size:12.5px;color:var(--gr);font-weight:700}.tile .nm{font-family:"Young Serif",serif;font-size:19px}.tile .hr{font-family:"Courier Prime",monospace;font-size:13px;color:var(--mut)}
@media(max-width:760px){.tiles{grid-template-columns:1fr}}
.guide{display:grid;grid-template-columns:1fr 1.2fr;gap:36px;align-items:start}
.board{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.board img{width:100%;aspect-ratio:1;object-fit:cover;border:7px solid #fff;box-shadow:0 3px 10px rgba(80,50,20,.18)}
.board img:nth-child(1){aspect-ratio:3/4}.board img:nth-child(2){aspect-ratio:3/4}
.letter{background:var(--paper);border-radius:6px;padding:30px 30px;box-shadow:0 2px 0 var(--line);background-image:repeating-linear-gradient(transparent 0 31px,rgba(154,91,46,.12) 31px 32px)}
.letter h3{font-size:28px}.letter .msg p{margin-top:12px;font-size:15.5px}
.letter .sign{font-family:"Young Serif",serif;font-size:22px;text-align:right;margin-top:12px;color:var(--br)}
.facts{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.facts li{font-family:"Courier Prime",monospace;font-size:12.5px;font-weight:700;color:var(--br);border:2px solid var(--br);border-radius:6px;padding:1px 9px;transform:rotate(-2deg)}
.facts a{text-decoration:none}
@media(max-width:820px){.guide{grid-template-columns:1fr}.letter{padding:22px 18px}}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.steps li{background:var(--paper);border-radius:6px;padding:22px;box-shadow:0 2px 0 var(--line);position:relative}
.steps .n{position:absolute;right:16px;top:10px;font-family:"Young Serif",serif;font-size:46px;color:rgba(154,91,46,.25)}
.steps h3{font-size:20px}.steps p{font-size:14.5px;margin-top:6px}
@media(max-width:760px){.steps{grid-template-columns:1fr}}
.cta{margin-top:56px;background:var(--ink);color:#f3e8d4;border-radius:6px;padding:44px 24px;text-align:center}
.cta h2{font-size:min(38px,8.4cqi);white-space:nowrap;margin:12px 0 6px}
.cta p{max-width:34em;margin:0 auto 22px;color:#d8c8ac}
.cta .stamp{color:#f1c58a;border-color:#f1c58a}
.btn{display:inline-block;background:#f1c58a;color:var(--ink);text-decoration:none;font-family:"Courier Prime",monospace;font-weight:700;border-radius:6px;padding:12px 26px}
.cta small{display:block;margin-top:14px;font-family:"Courier Prime",monospace;color:#bfae90}
.foot{max-width:1000px;margin:52px auto 0;padding:22px 20px 40px;border-top:1px dashed var(--line);font-size:12.5px;color:var(--mut);display:flex;flex-direction:column;gap:4px}
"""
    T = TOURS
    h = head("Café cozy", "family=Young+Serif&family=Courier+Prime:wght@400;700&family=Libre+Franklin:wght@400;600", css, "")
    h += f"""<div class="w">
<nav class="top"><a class="logo" href="#">Yuri's Tokyo</a><div class="links"><a href="#tours">Menu</a><a href="#guide">Yuri</a><a href="#area">Map</a><a href="#how">Steps</a></div></nav>
<header class="hero">
 <div class="ph"><img src="img/yuri-cafe-cake.jpg" alt="Yuri smiling at a café table with tea and cake"></div>
 <div class="tx cq">
  <div class="open">Open on booked days only</div>
  <h1>Come sit with me<br>in Tokyo</h1>
  <p>Not just famous spots, but the small moments of everyday life. A cup of tea, a quiet garden, a cozy izakaya at night. A walk through the city, as if you were visiting a friend.</p>
  <div class="sig"><img src="img/yuri-sakura-close.jpg" alt="Yuri"><span>— Yuri, nurse and guide from Kanazawa</span></div>
 </div>
</header>
{key_list()}
<div class="care"><div class="cq"><div class="stamp">Take it slow<span>ゆっくり</span></div><h2>{CARE_H}</h2></div>{care_list()}</div>

<section id="tours"><div class="sh"><div class="stamp">Tours<span>ツアー</span></div><h2>Today's menu</h2></div>
<div class="menu"><div class="hd cq"><h3>Three tours, all small</h3><div class="mono">Price on request · 料金は応相談</div></div>
""" + "".join(f"""<article class="tour" id="{t['id']}"><div class="ph">{timg(t,{"t2":("img/yuri-lunch-set.jpg","Yuri smiling over a set lunch"),"t3":("img/yuri-ramen-lunch.jpg","Yuri enjoying an early meal")})}</div><div class="cq"><div class="line"><h3>{t['t']}</h3><i></i><span class="pr">On request</span></div><div class="sub">{t['s']}</div><p class="lead">{t['lead']}</p>{tour_body(t)}{chips(t)}{meta(t)}</div></article>""" for t in T) + f"""</div></section>

<section id="guide"><div class="sh"><div class="stamp">Your guide<span>ガイド</span></div><h2>A note from Yuri</h2></div>
<div class="guide"><div class="board"><img src="img/yuri-cafe-cushion.jpg" alt="Yuri hugging a cushion in a cozy café" loading="lazy"><img src="img/yuri-old-house.jpg" alt="Yuri in front of an old wooden house" loading="lazy"><img src="img/yuri-cheesecake.jpg" alt="Yuri with cheesecake" loading="lazy"><img src="img/yuri-cafe-smile.jpg" alt="Yuri laughing at a café" loading="lazy"></div>
<div class="letter"><h3>Hi, I'm Yuri</h3><div class="msg">{bio()}</div><div class="sign">Yuri</div>{facts()}</div></div></section>

<section id="area"><div class="sh"><div class="stamp">Area<span>エリア</span></div><h2>Our neighborhoods</h2></div><div id="map"></div></section>
<section id="food"><div class="sh"><div class="stamp">Food<span>寄る店</span></div><h2>Where we eat</h2></div>{food_tiles()}</section>
<section id="how"><div class="sh"><div class="stamp">Steps<span>流れ</span></div><h2>How it works</h2></div>{steps()}
<div class="cta"><div class="stamp">Price on request</div><h2>{CTA_T}</h2><p>{CTA_P}</p><a class="btn" href="#tours">Back to the menu</a><small>{CTA_NOTE}</small></div></section>
</div>
{footer()}
"""
    return h + map_js("sepia(.6) saturate(1.1) brightness(.98)", "#9a5b2e")

# ============ V5  Bright & playful ============
def v5():
    css = """
:root{--bg:#fffaf0;--ink:#1f1d2b;--mut:#6b6878;--y:#ffd23f;--p:#ff5d8f;--b:#3fa7ff;--g:#3ccf91;--line:#1f1d2b}
body{background:var(--bg);color:var(--ink);font:500 16px/1.7 "Figtree",sans-serif}
.w{max-width:1080px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;letter-spacing:-.02em}
.jp{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:700;font-size:12px;letter-spacing:.1em}
nav.top{display:flex;justify-content:space-between;align-items:center;height:66px}
nav.top .logo{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:22px;text-decoration:none}
nav.top .logo span{background:var(--y);padding:0 6px;border-radius:6px}
nav.top .links{display:flex;gap:8px}
nav.top .links a{text-decoration:none;font-weight:700;font-size:14px;border:2px solid var(--line);border-radius:999px;padding:4px 14px;background:#fff}
@media(max-width:600px){nav.top .links a:nth-child(n+2){display:none}}
.hero{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center;padding:20px 0 50px}
.hero h1{font-size:min(76px,13cqi);line-height:1.02;white-space:nowrap}
.hero h1 .hl{background:var(--p);color:#fff;padding:0 .12em;border-radius:.12em}
.hero p{font-size:18px;margin-top:18px;max-width:28em}
.hero .stk{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.stk li,.chips li{font-weight:800;font-size:13.5px;border:2px solid var(--line);border-radius:999px;padding:5px 14px;background:#fff;box-shadow:3px 3px 0 var(--line)}
.stk li:nth-child(3n+1),.chips li:nth-child(3n+1){background:var(--y)}.stk li:nth-child(3n+2),.chips li:nth-child(3n+2){background:#ffd0de}.stk li:nth-child(3n),.chips li:nth-child(3n){background:#cfe8ff}
.collage{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:12px;aspect-ratio:1}
.collage img{width:100%;height:100%;object-fit:cover;border:3px solid var(--line);border-radius:22px;box-shadow:6px 6px 0 var(--line)}
.collage img:first-child{grid-row:1/3}
@media(max-width:820px){.hero{grid-template-columns:1fr;gap:26px;padding-top:6px}.collage{aspect-ratio:5/4}}
.bento{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.bx{border:3px solid var(--line);border-radius:22px;padding:18px 20px;background:#fff}
.bx dt{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:22px}
.bx dd{font-size:15px;margin-top:4px}
.b1{grid-column:span 2;background:var(--y)}.b2{grid-column:span 2;background:#ffd0de}.b3{grid-column:span 2;background:#cfe8ff}.b4{grid-column:span 3;background:#d4f5e6}.b5{grid-column:span 3}
.care{grid-column:1/-1;background:var(--ink);color:#fff;display:grid;grid-template-columns:1fr 1.5fr;gap:24px;align-items:center}
.care h2{font-size:min(34px,8.4cqi);white-space:nowrap;color:var(--y)}
.care li{padding:6px 0 6px 30px;position:relative;font-size:15px}
.care li::before{content:"";position:absolute;left:0;top:12px;width:16px;height:16px;border-radius:50%;background:var(--p)}
.care li:nth-child(2)::before{background:var(--b)}.care li:nth-child(3)::before{background:var(--g)}
@media(max-width:820px){.bento{grid-template-columns:1fr 1fr}.b1,.b2,.b3,.b4,.b5{grid-column:span 1}.b5{grid-column:1/-1}.care{grid-template-columns:1fr;gap:6px}}
@media(max-width:420px){.bento{grid-template-columns:1fr}}
section{padding:80px 0 0}
.sh{margin-bottom:28px}
.sh .jp{display:inline-block;background:var(--ink);color:#fff;border-radius:999px;padding:3px 12px;margin-bottom:10px}
.sh h2{font-size:min(52px,10cqi);white-space:nowrap;line-height:1}
.tours{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;align-items:start}
.tour{border:3px solid var(--line);border-radius:26px;overflow:hidden;background:#fff;box-shadow:6px 6px 0 var(--line)}
.tour .ph{position:relative}.tour .ph img{width:100%;aspect-ratio:4/5;object-fit:cover}
.tour .ph .no{position:absolute;left:12px;top:12px;width:44px;height:44px;border-radius:50%;border:3px solid var(--line);display:flex;align-items:center;justify-content:center;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:20px}
.tour:nth-child(1) .no{background:var(--y)}.tour:nth-child(2) .no{background:#ffd0de}.tour:nth-child(3) .no{background:#cfe8ff}
.tour .tx{padding:20px 20px 22px;border-top:3px solid var(--line)}
.tour h3{font-size:min(26px,7.4cqi);white-space:nowrap;line-height:1.1}
.tour .sub{color:var(--p);font-weight:800;margin:4px 0 10px;font-size:15px}
.tour .lead{font-size:15px}
.tour details{margin-top:12px;border-top:2px dashed #d6d2c6;padding-top:10px}
.tour summary{cursor:pointer;font-weight:800;font-size:14px;list-style:none}
.tour summary::-webkit-details-marker{display:none}
.tour summary::after{content:" +";color:var(--p)}.tour details[open] summary::after{content:" –"}
.tour h4{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:15px;margin:12px 0 2px}
.tour p{font-size:14.5px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chips li{font-size:12px;padding:3px 10px;box-shadow:2px 2px 0 var(--line)}
.meta{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:16px}
.meta div{background:var(--bg);border-radius:12px;padding:8px 10px}
.meta dt{font-size:12px;color:var(--mut);font-weight:700}.meta dd{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:15px;line-height:1.25}
@media(max-width:900px){.tours{grid-template-columns:1fr;max-width:520px;margin:0 auto}}
#map{border:3px solid var(--line);border-radius:26px;box-shadow:6px 6px 0 var(--line)}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.tile{border:3px solid var(--line);border-radius:22px;overflow:hidden;background:#fff;text-decoration:none;box-shadow:5px 5px 0 var(--line)}
.tile .ph{height:170px;border-bottom:3px solid var(--line)}.tile img{width:100%;height:100%;object-fit:cover}
.tile .tx{display:flex;flex-direction:column;padding:12px 16px 16px}
.tile .tag{align-self:flex-start;font-size:12px;font-weight:800;background:var(--y);border-radius:999px;padding:1px 10px;border:2px solid var(--line)}.tile .nm{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:19px;margin-top:6px}.tile .hr{font-size:13px;color:var(--mut)}
@media(max-width:760px){.tiles{grid-template-columns:1fr}}
.guide{display:grid;grid-template-columns:1fr 1.15fr;gap:36px;align-items:start}
.guide .pics{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
.guide .pics img{width:100%;aspect-ratio:1;object-fit:cover;border:3px solid var(--line);border-radius:18px}
.guide .pics img:first-child{grid-column:1/4;aspect-ratio:4/3;border-radius:24px;box-shadow:6px 6px 0 var(--line)}
.guide .card{border:3px solid var(--line);border-radius:26px;background:#fff;padding:28px}
.guide h3{font-size:34px}.guide h3 span{background:var(--y);padding:0 8px;border-radius:8px}
.guide .msg p{margin-top:12px;font-size:15.5px}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.facts li{font-weight:800;font-size:13px;border:2px solid var(--line);border-radius:999px;padding:3px 12px}
.facts li:nth-child(odd){background:#cfe8ff}.facts li:nth-child(even){background:#d4f5e6}.facts li:last-child{background:var(--p);color:#fff}
.facts a{text-decoration:none}
@media(max-width:820px){.guide{grid-template-columns:1fr}.guide .card{padding:22px 18px}}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.steps li{border:3px solid var(--line);border-radius:22px;padding:22px;background:#fff}
.steps .n{display:inline-flex;width:46px;height:46px;border-radius:14px;background:var(--b);color:#fff;border:3px solid var(--line);align-items:center;justify-content:center;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:22px}
.steps li:nth-child(2) .n{background:var(--p)}.steps li:nth-child(3) .n{background:var(--g)}
.steps h3{font-size:21px;margin:10px 0 4px}.steps p{font-size:14.5px}
@media(max-width:760px){.steps{grid-template-columns:1fr}}
.cta{margin-top:56px;background:var(--y);border:3px solid var(--line);border-radius:30px;box-shadow:8px 8px 0 var(--line);padding:44px 22px;text-align:center}
.cta h2{font-size:min(48px,8.6cqi);white-space:nowrap}
.cta p{max-width:32em;margin:10px auto 22px}
.btn{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:13px 30px}
.cta small{display:block;margin-top:14px;font-weight:700}
.cta .pr{display:inline-block;background:#fff;border:2px solid var(--line);border-radius:999px;padding:3px 14px;font-weight:800;font-size:14px;margin-bottom:12px}
.foot{max-width:1080px;margin:56px auto 0;padding:22px 20px 40px;font-size:12.5px;color:var(--mut);display:flex;flex-direction:column;gap:4px}
"""
    T = TOURS
    h = head("Bright & playful", "family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Figtree:wght@500;700;800&family=Zen+Kaku+Gothic+New:wght@700", css, "")
    k = KEY
    h += f"""<div class="w">
<nav class="top"><a class="logo" href="#"><span>Yuri</span> in Tokyo</a><div class="links"><a href="#tours">Tours</a><a href="#guide">Yuri</a><a href="#area">Map</a></div></nav>
<header class="hero">
 <div class="cq"><h1>Tokyo days<br>with a <span class="hl">friend</span></h1>
 <p>Not just famous spots, but the small moments of everyday life. Shimbashi at night, art by day, and plenty of places to sit.</p>
 <ul class="stk"><li>Guide is a nurse</li><li>Sit-down spots</li><li>Small groups</li><li>In kimono</li></ul></div>
 <div class="collage"><img src="img/yuri-sakura-arms.jpg" alt="Yuri with both hands up under cherry blossoms" style="object-position:38% 50%"><img src="img/yuri-izakaya-fan.jpg" alt="Yuri with a fan and a drink at an izakaya" style="object-position:50% 40%"><img src="img/yuri-tower-view.jpg" alt="Yuri posing at a city viewpoint" style="object-position:50% 30%"></div>
</header>
<dl class="bento">
<div class="bx b1"><dt>{k[0][0]}</dt><dd>{k[0][1]}</dd></div><div class="bx b2"><dt>{k[1][0]}</dt><dd>{k[1][1]}</dd></div><div class="bx b3"><dt>{k[2][0]}</dt><dd>{k[2][1]}</dd></div>
<div class="bx b4"><dt>{k[3][0]}</dt><dd>{k[3][1]}</dd></div><div class="bx b5"><dt>{k[4][0]}</dt><dd>{k[4][1]}</dd></div>
<div class="bx care"><div class="cq"><div class="jp" style="color:#ffd0de">ゆっくり、座れる</div><h2>{CARE_SHORT}</h2><p style="font-size:14px;opacity:.85">{CARE_T}.</p></div>{care_list()}</div>
</dl>

<section id="tours"><div class="sh"><div class="jp">Tours · ツアー</div><h2>Pick your day</h2></div><div class="tours">
""" + "".join(f"""<article class="tour" id="{t['id']}"><div class="ph">{timg(t,{"t1":("img/yuri-izakaya-beer.jpg","Yuri raising a glass of beer at an izakaya"),"t2":("img/yuri-green-smile.jpg","Yuri smiling in the greenery by a river")})}<span class="no">{i+1}</span></div><div class="tx"><h3>{t['t']}</h3><div class="sub">{t['s']}</div><p class="lead">{t['lead']}</p>{chips(t)}{meta(t)}<details><summary>Read the details</summary>{tour_body(t)}</details></div></article>""" for i, t in enumerate(T)) + f"""</div></section>

<section id="guide"><div class="sh"><div class="jp">Your guide · ガイド</div><h2>Say hi to Yuri</h2></div>
<div class="guide"><div class="pics"><img src="img/yuri-yukata-fan.jpg" alt="Yuri in a yukata with a fan near Tokyo Skytree" loading="lazy" style="object-position:50% 30%"><img src="img/yuri-sakura-wave.jpg" alt="Yuri waving under cherry blossoms" loading="lazy"><img src="img/yuri-cheesecake.jpg" alt="Yuri with a slice of cheesecake" loading="lazy"><img src="img/yuri-street-wave.jpg" alt="Yuri waving on a street" loading="lazy"></div>
<div class="card"><h3>Hi, I'm <span>Yuri</span></h3><div class="msg">{bio()}</div>{facts()}</div></div></section>

<section id="area"><div class="sh"><div class="jp">Area · エリア</div><h2>Where we'll go</h2></div><div id="map"></div></section>
<section id="food"><div class="sh"><div class="jp">Food · 寄る店</div><h2>Yummy stops</h2></div>{food_tiles()}</section>
<section id="how"><div class="sh"><div class="jp">How it works · 流れ</div><h2>Easy as 1, 2, 3</h2></div>{steps()}
<div class="cta"><div class="pr">Price on request</div><h2>{CTA_T}</h2><p>{CTA_P}</p><a class="btn" href="#tours">See the tours</a><small>{CTA_NOTE}</small></div></section>
</div>
{footer()}
"""
    return h + map_js("sepia(.3) hue-rotate(10deg) saturate(1.6) brightness(1.04)", "#ff5d8f")

# ============ board ============
VARS = [
    ("v1", "Warm cream × coral", "Fraunces (soft) / Caveat / Work Sans", "#ee6c58", "#fff7ee", "img/yuri-yukata-fan.jpg",
     "クリーム地にコーラル。手書き英字（Caveat）の吹き出しとアーチ型の写真で『友だちからの手紙』の温度に。"),
    ("v2", "Photo-forward magazine", "Lora / Great Vibes / Manrope", "#8f5f6e", "#fbf6ee", "img/yuri-yukata-river.jpg",
     "金沢サイトと同じ Lora＋Great Vibes＋モーヴ。全面写真のヒーローと『Small moments』写真グリッドで本人推し。いちばん金沢に近い案。"),
    ("v3", "Gentle wa-modern", "Lora / Source Sans 3 / Zen Old Mincho", "#4b6c8f", "#fbf9f4", "img/yuri-kimono-window.jpg",
     "温かい白に柔らかい藍と抹茶。中央の丸い着物ポートレートから始まる、静かで上品な縦一列。"),
    ("v4", "Café-style cozy", "Young Serif / Courier Prime / Libre Franklin", "#9a5b2e", "#e8d9bf", "img/yuri-cafe-cake.jpg",
     "クラフト紙色＋スタンプ風チップ。ツアーを喫茶店の『本日のメニュー』に見立て、自己紹介は罫線の便箋。"),
    ("v5", "Bright & playful", "Bricolage Grotesque / Figtree", "#ff5d8f", "#ffd23f", "img/yuri-sakura-arms.jpg",
     "黄・ピンク・水色のステッカー風。要点はベントー型の箱、ツアーは3枚並びのカードで詳細は開閉式。"),
]
def board():
    cards = "".join(f"""<a class="c" href="{f}.html"><div class="ph"><img src="{img}" alt=""><span class="sw" style="background:{c1}"></span><span class="sw s2" style="background:{c2}"></span></div><div class="tx"><div class="no">{f.upper()}</div><h2>{n}</h2><p class="jp">{note}</p><p class="ft">{fonts}<br>Main color {c1}</p></div></a>""" for f, n, fonts, c1, c2, img, note in VARS)
    return f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tokyo with Yuri — 5 friendly drafts (English editions)</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="../favicon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="Tokyo with Yuri — 5 friendly drafts">
<meta property="og:description" content="English editions — all five variants are in English, for overseas guests. Warm cream, magazine, wa-modern, café and playful.">
<meta property="og:image" content="https://yukitchy.github.io/yuri-tokyo-tours/ogp/og1.jpg">
<meta name="twitter:card" content="summary_large_image">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font:15px/1.7 -apple-system,"Hiragino Sans","Helvetica Neue",sans-serif;background:#f6f3ee;color:#2a2622;overflow-x:hidden}}
.w{{max-width:1180px;margin:0 auto;padding:34px 20px 60px}}
h1{{font-size:clamp(20px,5vw,30px);white-space:nowrap}}
.en{{display:inline-block;margin:10px 0 6px;background:#2a2622;color:#fff;border-radius:999px;padding:4px 14px;font-size:13px;font-weight:600}}
.lead{{color:#6c635a;font-size:13.5px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;margin-top:26px}}
@media(max-width:360px){{.grid{{grid-template-columns:1fr}}}}
.c{{background:#fff;border-radius:16px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.c .ph{{position:relative;aspect-ratio:4/3}}.c img{{width:100%;height:100%;object-fit:cover;object-position:50% 30%}}
.sw{{position:absolute;right:12px;bottom:12px;width:30px;height:30px;border-radius:50%;border:3px solid #fff}}.sw.s2{{right:46px}}
.tx{{padding:16px 18px 18px}}.no{{font-size:12px;font-weight:700;letter-spacing:.14em;color:#9a8f84}}
.c h2{{font-size:min(19px,7cqi);white-space:nowrap;margin:2px 0 6px}}.tx{{container-type:inline-size}}.c .jp{{font-size:13.5px}}.c .ft{{font-size:12px;color:#8a8077;margin-top:10px}}
.foot{{margin-top:30px;font-size:12px;color:#8a8077}}
</style></head><body><div class="w">
<h1>ゆりの東京ツアー 第2ラウンド</h1>
<div class="en">English editions — all five variants are in English, for overseas guests</div>
<p class="lead">テーマ：親しみやすさ。5案で書体・メインカラー・骨格をすべて変えています。写真は Immich のゆりっぺ本人クラスタから。料金は全案 Price on request、予約は準備中の注記のみ。</p>
<div class="grid">{cards}</div>
<p class="foot">各案はスマホ幅 390px / 320px で横スクロールなし・見出し1行を確認済み。</p>
</div></body></html>
"""

if __name__ == "__main__":
    for name, fn in [("v1", v1), ("v2", v2), ("v3", v3), ("v4", v4), ("v5", v5)]:
        (HERE / f"{name}.html").write_text(fn(), encoding="utf-8")
    (HERE / "index.html").write_text(board(), encoding="utf-8")
    print("built")
