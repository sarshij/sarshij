import os, math, re, sys, zipfile
from xml.sax.saxutils import escape

STATIC = len(sys.argv) > 1 and sys.argv[1] == "static"   # preview mode: no animation state
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
A = OUT + "/assets"
os.makedirs(A, exist_ok=True)
os.makedirs(OUT + "/.github/workflows", exist_ok=True)

FONT = "'Fira Code','JetBrains Mono',Consolas,Menlo,'Courier New',monospace"
BG, BG2 = "#0d0b16", "#15122a"
PUR, LIL, CYA = "#8A2BE2", "#b47cff", "#19e3e6"
DIM, INK, GRN, PINK = "#7b7399", "#e8e4f5", "#4ade80", "#ff2bd6"
NB = "\u00a0"


def w(path, txt):
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)


# ------------------------------------------------------------------ HEADER
def header():
    W, H, ax = 1000, 320, 240
    pts = []
    for x in range(0, W + 1, 2):
        env = 0.5 + 0.5 * math.sin(x / 140 + 1.0)
        y = ax - 26 * env * math.sin(x / 11.5) - 4 * env * math.sin(x / 3.1)
        pts.append(f"{x},{y:.1f}")
    d = "M" + " L".join(pts)
    ticks = "".join(
        f"M{x} {ax - (7 if x % 50 == 0 else 3)}V{ax + (7 if x % 50 == 0 else 3)}"
        for x in range(0, W + 1, 10)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Sarshij Karn, electronics engineer. AI and cybersecurity.">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d0b16"/><stop offset="1" stop-color="#171030"/></linearGradient>
  <linearGradient id="gn" x1="0" x2="1"><stop offset="0" stop-color="{LIL}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>
  <linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{PUR}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>
  <linearGradient id="sc" x1="0" x2="1"><stop offset="0" stop-color="{CYA}" stop-opacity="0"/><stop offset="1" stop-color="{CYA}" stop-opacity=".16"/></linearGradient>
  <pattern id="g" width="50" height="40" patternUnits="userSpaceOnUse"><path d="M50 0H0V40" fill="none" stroke="#2a2346" stroke-width="1"/></pattern>
  <filter id="gl" x="-5%" y="-60%" width="110%" height="220%"><feGaussianBlur stdDeviation="3.5"/></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)" font-family="{FONT}">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#g)" opacity=".6"/>
  <path d="M500 0V{H}M0 160H{W}" stroke="#3a3160" stroke-dasharray="2 5" fill="none"/>
  <path d="{ticks}" stroke="#4a4075" stroke-width="1" fill="none"/>

  <!-- the signal: dim trace + travelling pulse -->
  <path d="{d}" fill="none" stroke="{CYA}" stroke-opacity=".22" stroke-width="1.5"/>
  <path d="{d}" pathLength="1" fill="none" stroke="{CYA}" stroke-width="5" stroke-linecap="round" stroke-dasharray="0.16 0.84" filter="url(#gl)" opacity=".85">
    <animate attributeName="stroke-dashoffset" from="0" to="-1" dur="5s" repeatCount="indefinite"/>
  </path>
  <path d="{d}" pathLength="1" fill="none" stroke="#c9fbff" stroke-width="2" stroke-linecap="round" stroke-dasharray="0.16 0.84">
    <animate attributeName="stroke-dashoffset" from="0" to="-1" dur="5s" repeatCount="indefinite"/>
  </path>

  <!-- sweep bar -->
  <rect x="-70" y="0" width="70" height="{H}" fill="url(#sc)">
    <animateTransform attributeName="transform" type="translate" from="0 0" to="{W + 70} 0" dur="7s" repeatCount="indefinite"/>
  </rect>

  <!-- name with a rare glitch -->
  <g font-weight="800" font-size="64" text-anchor="middle">
    <text x="500" y="128" fill="{CYA}" opacity="0" textLength="640" lengthAdjust="spacing">SARSHIJ KARN
      <animate attributeName="opacity" values="0;0;.75;0;.75;0;0" keyTimes="0;.88;.89;.91;.92;.94;1" dur="7s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0 0;0 0;-5 0;3 -1;-3 1;0 0;0 0" keyTimes="0;.88;.89;.91;.92;.94;1" dur="7s" repeatCount="indefinite"/>
    </text>
    <text x="500" y="128" fill="{PINK}" opacity="0" textLength="640" lengthAdjust="spacing">SARSHIJ KARN
      <animate attributeName="opacity" values="0;0;.7;0;.7;0;0" keyTimes="0;.88;.89;.91;.92;.94;1" dur="7s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0 0;0 0;5 0;-3 1;3 -1;0 0;0 0" keyTimes="0;.88;.89;.91;.92;.94;1" dur="7s" repeatCount="indefinite"/>
    </text>
    <text x="500" y="128" fill="url(#gn)" textLength="640" lengthAdjust="spacing">SARSHIJ KARN</text>
  </g>
  <text x="500" y="172" text-anchor="middle" font-size="17" fill="#cfc8e8" textLength="700" lengthAdjust="spacing">Electronics engineer. Teaching circuits to think, and keeping them secure.</text>

  <!-- instrument readouts -->
  <g font-size="11" fill="{DIM}" letter-spacing="1">
    <text x="34" y="36">ch1   2V/div   1ms/div</text>
    <text x="966" y="36" text-anchor="end">sys_core 0x8f2a   link active</text>
    <text x="34" y="300">BEI   NCE   T.U.</text>
    <text x="966" y="300" text-anchor="end">27.66°N  85.32°E</text>
  </g>

  <!-- corner brackets -->
  <path d="M14 34V14H34M966 14H986V34M986 286V306H966M34 306H14V286" fill="none" stroke="{PUR}" stroke-width="2" opacity=".85"/>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="url(#bd)" stroke-width="1.5"/>
</svg>
'''


# ---------------------------------------------------------------- TERMINAL
def json_segs(line):
    segs = []
    for m in re.finditer(r'"[^"]*"|[^"]+', line):
        tok = m.group(0)
        if tok.startswith('"'):
            col = CYA if line[m.end():m.end() + 1] == ":" else "#d9c2ff"
        else:
            col = DIM
        segs.append((tok, col))
    return segs


def terminal():
    cw, fs, lh = 8.4, 14, 23
    W, x0, top = 900, 30, 40
    yf = top + 38

    def prompt(cmd):
        return [("sarshij", LIL), ("@", DIM), ("nepal", CYA), (":~$ ", DIM), (cmd, INK)]

    JSON = [
        "{",
        '  "studying":  "BEI @ National College of Engineering (T.U.)",',
        '  "based_in":  "Kathmandu, Nepal",',
        '  "building":  ["AI/ML tools", "security utilities", "embedded systems"],',
        '  "exploring": ["quantum computing", "semiconductors", "space tech"],',
        '  "off_duty":  ["books", "sports", "markets", "making videos"],',
        '  "open_to":   ["internships", "freelance", "collabs"]',
        "}",
    ]
    dirs = ["faceshield", "clearhire", "medassist", "smartvault", "hyperqr", "gesture-calc"]
    ok = lambda msg: [("[", DIM), ("  OK  ", GRN), ("] ", DIM), (msg, INK)]

    L = [(prompt("whoami"), "cmd"),
         ([("Sarshij Karn: electronics engineer, builder, perpetual learner", INK)], "out"),
         ([], "blank"),
         (prompt("cat about.json"), "cmd")]
    L += [(json_segs(j), "out") for j in JSON]
    L += [([], "blank"), (prompt("ls ~/projects"), "cmd"),
          ([(d + "/  ", CYA) for d in dirs] + [("+4 more", DIM)], "out"),
          ([], "blank"), (prompt("./start_transmission.sh"), "cmd"),
          (ok("uplink established"), "out"),
          (ok("inbox open: sarshijkarn.com.np/#contact"), "out"),
          (prompt(""), "cursor")]

    t, tl = 0.8, []
    for segs, kind in L:
        n = sum(len(s) for s, _ in segs) + (1 if kind == "cursor" else 0)
        if kind == "blank":
            t += 0.15
            tl.append(None)
            continue
        ct = 0.05 if kind in ("cmd", "cursor") else 0.007
        tl.append((t, ct, n))
        t += n * ct + (0.55 if kind == "cmd" else 0.12)
    T = t + 6

    H = yf + (len(L) - 1) * lh + 34
    defs, body = [], []
    for i, ((segs, kind), info) in enumerate(zip(L, tl)):
        if info is None:
            continue
        start, ct, n = info
        y = yf + i * lh
        if STATIC:
            defs.append(f'<clipPath id="c{i}"><rect x="{x0}" y="{y - fs}" width="{n * cw + 4:.1f}" height="{lh}"/></clipPath>')
        else:
            kts = ["0"] + [f"{(start + k * ct) / T:.6f}" for k in range(n)]
            vals = ["0"] + [f"{(k + 1) * cw:.1f}" for k in range(n)]
            defs.append(
                f'<clipPath id="c{i}"><rect x="{x0}" y="{y - fs}" width="0" height="{lh}">'
                f'<animate attributeName="width" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="{";".join(kts)}" values="{";".join(vals)}"/></rect></clipPath>')
        x = x0
        parts = []
        for s, col in segs:
            if not s:
                continue
            tl_attr = f' textLength="{len(s) * cw:.1f}" lengthAdjust="spacing"' if len(s) > 1 else ""
            parts.append(f'<text x="{x:.1f}" y="{y}" fill="{col}"{tl_attr}>{escape(s.replace(" ", NB))}</text>')
            x += len(s) * cw
        if kind == "cursor":
            parts.append(f'<rect class="cur" x="{x:.1f}" y="{y - fs + 2}" width="8" height="17" fill="{CYA}"/>')
        body.append(f'<g clip-path="url(#c{i})">{"".join(parts)}</g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal session: whoami, cat about.json, ls projects, start_transmission">
<defs>
  <linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{PUR}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>
  <clipPath id="win"><rect width="{W}" height="{H}" rx="12"/></clipPath>
  {"".join(defs)}
  <style>@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}} .cur{{animation:blink 1s steps(1) infinite}}</style>
</defs>
<g clip-path="url(#win)" font-family="{FONT}" font-size="{fs}">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{top}" fill="{BG2}"/>
  <circle cx="24" cy="20" r="6" fill="#ff5f57" opacity=".85"/><circle cx="44" cy="20" r="6" fill="#febc2e" opacity=".85"/><circle cx="64" cy="20" r="6" fill="#28c840" opacity=".85"/>
  <text x="{W / 2}" y="25" text-anchor="middle" font-size="12" fill="{DIM}">sarshij@nepal: ~</text>
  {"".join(body)}
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="12" fill="none" stroke="url(#bd)" stroke-width="1.5"/>
</svg>
'''


# ----------------------------------------------------------------- WAVES
def wave_open(y, amp, period, width):
    h = period / 2
    n = int(width / h) + 3
    d = f"M0 {y} Q {h / 2:g} {y - 2 * amp:g} {h:g} {y}"
    for k in range(2, n + 1):
        d += f" T {k * h:g} {y}"
    return d, n * h


def divider():
    W, H = 1000, 36
    d1, _ = wave_open(18, 8, 100, W + 100)
    d2, _ = wave_open(18, 6, 160, W + 160)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation" aria-hidden="true">
<defs>
  <linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="{PUR}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>
  <linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset=".18" stop-color="#fff"/><stop offset=".82" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#f)"/></mask>
</defs>
<g mask="url(#m)" fill="none" stroke-linecap="round">
  <path d="{d2}" stroke="{PUR}" stroke-width="1.6" opacity=".7">
    <animateTransform attributeName="transform" type="translate" from="0 0" to="-160 0" dur="7s" repeatCount="indefinite"/>
  </path>
  <path d="{d1}" stroke="url(#s)" stroke-width="2">
    <animateTransform attributeName="transform" type="translate" from="0 0" to="-100 0" dur="3.5s" repeatCount="indefinite"/>
  </path>
</g>
</svg>
'''


def footer():
    W, H = 1000, 150
    layers = [(104, 10, 250, 11, "-250 0", 0.34), (112, 8, 180, 8, "-180 0", 0.26), (120, 6, 320, 14, "-320 0", 0.2)]
    ws = ""
    for y, amp, per, dur, to, op in layers:
        d, _ = wave_open(y, amp, per, W + per)
        d += f" L{W + 2 * per} {H} L0 {H} Z"
        ws += (f'<path d="{d}" fill="url(#wg)" opacity="{op}">'
               f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{to}" dur="{dur}s" repeatCount="indefinite"/></path>\n  ')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Built with passion and futuristic vision in Nepal">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d0b16"/><stop offset="1" stop-color="#171030"/></linearGradient>
  <linearGradient id="wg" x1="0" x2="1"><stop offset="0" stop-color="{PUR}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>
  <linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{PUR}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>
  <clipPath id="fr"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#fr)" font-family="{FONT}" text-anchor="middle">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {ws}
  <text x="500" y="44" font-size="12" fill="{CYA}" letter-spacing="2">// end of transmission</text>
  <text x="500" y="74" font-size="17" fill="{INK}">Built with passion and futuristic vision in Nepal</text>
  <text x="500" y="96" font-size="11" fill="{DIM}">© 2026 Sarshij Karn   ·   sarshijkarn.com.np</text>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="url(#bd)" stroke-width="1.5"/>
</svg>
'''


# ----------------------------------------------------------------- NEOFETCH
def neofetch():
    Wd = 21
    top_pins = "".join("╷" if (3 <= i <= Wd - 4 and i % 2 == 1) else " " for i in range(Wd))
    top = "".join("┴" if (3 <= i <= Wd - 4 and i % 2 == 1) else "─" for i in range(Wd))
    bot = "".join("┬" if (3 <= i <= Wd - 4 and i % 2 == 1) else "─" for i in range(Wd))
    bot_pins = "".join("╵" if (3 <= i <= Wd - 4 and i % 2 == 1) else " " for i in range(Wd))
    row = lambda s: "──┤" + s.center(Wd) + "├──"
    art = [
        "   " + top_pins,
        "  ┌" + top + "┐",
        row(""),
        row("S A R S H I J"),
        row("░▒▓█ 0x8F2A █▓▒░"),
        row("BEI · NCE · T.U."),
        row(""),
        "  └" + bot + "┘",
        "   " + bot_pins,
    ]
    art = [a.ljust(30) for a in art]
    info = [
        "sarshij@nepal",
        "─────────────",
        "Languages  Python · C/C++ · JavaScript · TypeScript",
        "Frontend   React · Next.js · Vite · HTML/CSS",
        "AI/ML      TensorFlow · PyTorch · OpenCV · MediaPipe",
        "Embedded   Arduino · MCUs · circuit sim · PCB design",
        "Security   Linux · Kali · networking · automation",
        "Shell      Bash · PowerShell",
        "Host       Acer Nitro V 16 · Ryzen 7 8845HS · RTX 4050",
    ]
    return "\n".join(a + "  " + i for a, i in zip(art, info))


# ------------------------------------------------------------------ README
README = r'''<div align="center">

<a href="https://sarshijkarn.com.np"><img src="assets/header.svg" alt="Sarshij Karn, electronics engineer. AI and cybersecurity." width="100%"></a>

<br>

<a href="https://sarshijkarn.com.np"><img src="https://img.shields.io/badge/Website-sarshijkarn.com.np-8A2BE2?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Website"></a>
<a href="https://sarshijkarn.com.np/assets/Sarshij-Karn-Resume.pdf"><img src="https://img.shields.io/badge/Resume-PDF-19e3e6?style=for-the-badge&logo=readthedocs&logoColor=0d0b16" alt="Resume"></a>
<a href="https://www.linkedin.com/in/sarshij-karn-1a7766236/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://youtube.com/@sarshijkarn"><img src="https://img.shields.io/badge/YouTube-Sarshij-FF0033?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://x.com/realsarshijkarn"><img src="https://img.shields.io/badge/X-realsarshijkarn-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.instagram.com/sarshijkarn"><img src="https://img.shields.io/badge/Instagram-sarshijkarn-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"></a>

<br><br>

<a href="#about"><kbd> about </kbd></a>
<a href="#stack"><kbd> stack </kbd></a>
<a href="#projects"><kbd> projects </kbd></a>
<a href="#now"><kbd> now </kbd></a>
<a href="#telemetry"><kbd> telemetry </kbd></a>
<a href="#connect"><kbd> connect </kbd></a>

<br><br>

<img src="https://komarev.com/ghpvc/?username=SarshijKarn&label=Visitors&color=8A2BE2&style=flat-square" alt="Profile views">

</div>

<img src="assets/divider.svg" width="100%" alt="">

<h2 align="center">About</h2>

<img src="assets/terminal.svg" alt="Terminal session: whoami, cat about.json, ls ~/projects, ./start_transmission.sh" width="100%">

<br>

I'm an electronics engineering student in Kathmandu who likes the spot where hardware meets software. I build things that see, decide and protect: computer vision tools, AI screeners, privacy utilities, and the occasional circuit. Hackathons, books, sports and the markets keep the rest of me busy.

<img src="assets/divider.svg" width="100%" alt="">

<h2 align="center">Stack</h2>

```text
@@NEOFETCH@@
```

How I think about building anything:

```mermaid
flowchart LR
    A["<b>Sense</b><br/>sensors · MCUs · cameras"] --> B["<b>Think</b><br/>ML · CV · LLM agents"]
    B --> C["<b>Act</b><br/>automation · apps · UIs"]
    C --> D["<b>Defend</b><br/>Linux · networks · hardening"]
    D -.->|feedback| A
    classDef n fill:#0d0b16,stroke:#8A2BE2,stroke-width:2px,color:#e8e4f5;
    class A,B,C,D n;
```

<table>
<tr>
<td><b>Languages</b></td>
<td><img src="https://skillicons.dev/icons?i=python,c,cpp,js,ts,bash,powershell" alt="Languages"></td>
</tr>
<tr>
<td><b>Web</b></td>
<td><img src="https://skillicons.dev/icons?i=html,css,react,nextjs,vite,nodejs,vercel,cloudflare" alt="Web"></td>
</tr>
<tr>
<td><b>AI / ML</b></td>
<td><img src="https://skillicons.dev/icons?i=tensorflow,pytorch,opencv" alt="AI and ML"> <img src="https://img.shields.io/badge/MediaPipe-0097A7?style=flat-square" alt="MediaPipe"> <img src="https://img.shields.io/badge/SBERT-8A2BE2?style=flat-square" alt="SBERT"> <img src="https://img.shields.io/badge/n8n-EA4B71?style=flat-square" alt="n8n"></td>
</tr>
<tr>
<td><b>Embedded</b></td>
<td><img src="https://skillicons.dev/icons?i=arduino" alt="Arduino"> <img src="https://img.shields.io/badge/PCB%20design-1f6f43?style=flat-square" alt="PCB design"> <img src="https://img.shields.io/badge/Circuit%20simulation-6a35b0?style=flat-square" alt="Circuit simulation"></td>
</tr>
<tr>
<td><b>Security + OS</b></td>
<td><img src="https://skillicons.dev/icons?i=linux,kali,bash" alt="Linux and Kali"></td>
</tr>
<tr>
<td><b>Workflow</b></td>
<td><img src="https://skillicons.dev/icons?i=git,github,githubactions,vscode" alt="Git, GitHub, Actions, VS Code"></td>
</tr>
</table>

<img src="assets/divider.svg" width="100%" alt="">

<h2 align="center">Projects</h2>

<table>
<tr>
<td width="50%" valign="top">

### [ClearHire](https://github.com/SarshijKarn/ClearHire-AI-Resume-Screener)
AI resume screener. Matches candidates to roles with SBERT, handles bulk screening for multiple recruiters, and flags fake or AI-written resumes.

`Python` `SBERT` `NLP`

</td>
<td width="50%" valign="top">

### [FaceShield](https://github.com/SarshijKarn/Faceshield)
Privacy tool that detects, tracks and blurs faces in video. Runs fully on your own machine, so footage never leaves it.

`MediaPipe` `DeepSORT` `Web app`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [MedAssist](https://github.com/SarshijKarn/medassist)
Medical assistant for rural communities. Symptom analysis, voice interaction, English and Nepali, report analysis and offline first-aid guides.

`Python` `Voice` `Offline-first`

</td>
<td width="50%" valign="top">

### [SmartVault](https://github.com/SarshijKarn/smart-vault-text-and-photo-notes-app)
Private notes for text and photos behind a local PIN vault, with optional AI image enhancement through Gemini.

`React` `TypeScript` `Vite`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [HyperQR](https://github.com/SarshijKarn/hyperqr-all-in-one-qr-code-utility)
QR toolkit. Create or scan from camera and images, auto-connect to WiFi, batch-process hundreds of files, export history to CSV.

`Python` `Desktop UI`

</td>
<td width="50%" valign="top">

### [Sync](https://lnkd.in/p/g-pPifWb)
Self-hosted Android fleet management for authorised MDM setups. Live location, device diagnostics and secure file sync, deployed with zero-touch setup.

`Android` `Self-hosted` `MDM`

</td>
</tr>
</table>

<details>
<summary><code>ls -a ~/projects</code>   (4 more)</summary>
<br>

| Project | What it does |
|---|---|
| [Gesture Calculator](https://github.com/SarshijKarn/gesture-based-calculator) | Do arithmetic with your hand in front of a webcam. Fingers pick numbers, thumb distance picks the operator, and it speaks the answer. |
| [Emotion Detection](https://github.com/SarshijKarn/emotion-detection-model) | Reads facial expressions in real time with OpenCV and deep learning. |
| [Reddit Data Scraper](https://github.com/SarshijKarn/reddit-data-scraper) | Pulls posts and comments from a subreddit starting at any year. Fast with API keys (PRAW), slower but keyless without them. |
| [WhatsApp Automation Tool](https://github.com/SarshijKarn/whatsapp-automation-king-pro) | Desktop app for bulk and scheduled messaging from Excel lists, with attachments and group support. |

</details>

<details>
<summary><code>./achievements.sh</code></summary>
<br>

- Startup Hackathon 2025, theme "AI for Social Impact and Scale" (The Startup Network, Embark College and PHDCCI)
- Full merit scholarship at National College of Engineering
- Merit-based scholarship at Liverpool International College
- Grade X: GPA 4.00
- Cracked the engineering entrance exam on the first attempt
- Cloud Computing and Python Programming trainings at NCE

</details>

<img src="assets/divider.svg" width="100%" alt="">

<h2 align="center">Now</h2>

```text
[~] rebuilding sarshijkarn.com.np into an interactive, multi-world portal
[~] a JARVIS-style local assistant that runs on my own machine
[~] a stock-market bot for NEPSE
[~] a free streaming platform for Nepali films, and ways to back indie filmmakers
[~] new videos on the Sarshij YouTube channel
[ ] your idea here
```

<img src="assets/divider.svg" width="100%" alt="">

<h2 align="center">Telemetry</h2>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SarshijKarn/SarshijKarn/output/github-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/SarshijKarn/SarshijKarn/output/github-snake.svg">
  <img alt="Contribution graph eaten by a snake" src="https://raw.githubusercontent.com/SarshijKarn/SarshijKarn/output/github-snake.svg" width="100%">
</picture>

<br>

<img height="170" src="https://github-readme-stats.vercel.app/api?username=SarshijKarn&show_icons=true&hide_border=true&bg_color=0d0b16&title_color=b47cff&text_color=d9d4ee&icon_color=19e3e6&ring_color=8A2BE2" alt="GitHub stats">
<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=SarshijKarn&layout=compact&hide_border=true&bg_color=0d0b16&title_color=b47cff&text_color=d9d4ee" alt="Top languages">

<img src="https://streak-stats.demolab.com/?user=SarshijKarn&hide_border=true&background=0d0b16&ring=8A2BE2&fire=19e3e6&currStreakNum=d9d4ee&sideNums=d9d4ee&currStreakLabel=b47cff&sideLabels=b47cff&dates=7b7399" alt="Contribution streak">

</div>

<img src="assets/divider.svg" width="100%" alt="">

<h2 align="center">Connect</h2>

<div align="center">

Collabs, internships, freelance work, or just a good book recommendation: the fastest way to reach me is the contact form on my site.

<a href="https://sarshijkarn.com.np/#contact"><img src="https://img.shields.io/badge/Open%20the%20terminal%20form-sarshijkarn.com.np-8A2BE2?style=for-the-badge&logo=gnometerminal&logoColor=white" alt="Contact form"></a>

</div>

<details>
<summary><code>cat secret.txt</code></summary>
<br>

If you scrolled this far, you read READMEs for fun. We'll get along.

</details>

<br>

<img src="assets/footer.svg" width="100%" alt="Built with passion and futuristic vision in Nepal">
'''

SNAKE = '''name: Generate snake

on:
  schedule:
    - cron: "0 */12 * * *"
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-snake.svg
            dist/github-snake-dark.svg?palette=github-dark&color_snake=#19e3e6&color_dots=#161b22,#3b1d63,#5b2a99,#8A2BE2,#b47cff

      - uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''

w(A + "/header.svg", header())
w(A + "/terminal.svg", terminal())
w(A + "/divider.svg", divider())
w(A + "/footer.svg", footer())
if False:  # README and workflow are edited by hand now
    w(OUT + "/README.md", README.replace("@@NEOFETCH@@", neofetch()))
    w(OUT + "/.github/workflows/snake.yml", SNAKE)
    print(neofetch())
