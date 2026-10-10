#!/usr/bin/env python3
"""Generates the animated SVG assets for the GitHub profile README."""
import os, textwrap
from xml.sax.saxutils import escape

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(os.path.join(ROOT, "cards"), exist_ok=True)

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
BG, PANEL, LINE = "#070b10", "#0c131b", "#1d2a38"
BLUE, YELLOW, GREEN, DIM, TEXT = "#2f7cff", "#ffd500", "#3ef08f", "#5b6b7d", "#d6e2ee"

BANNER = [
    "██╗   ██╗ ██╗██████╗ ██╗   ██╗███████╗ █████╗  ██╗",
    "██║   ██║███║██╔══██╗██║   ██║██╔════╝██╔══██╗███║",
    "██║   ██║╚██║██████╔╝██║   ██║███████╗╚██████║╚██║",
    "╚██╗ ██╔╝ ██║██╔══██╗██║   ██║╚════██║ ╚═══██║ ██║",
    " ╚████╔╝  ██║██║  ██║╚██████╔╝███████║ █████╔╝ ██║",
    "  ╚═══╝   ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚════╝  ╚═╝",
]


def typed(lines, x, y0, size, step, start, cps=0.035, gap=0.35):
    """Lines that type themselves in, char by char (SMIL, works inside <img>)."""
    cw = size * 0.61
    out, t = [], start
    for i, (parts, pause) in enumerate(lines):
        y = y0 + i * step
        n = sum(len(p[0]) for p in parts)
        cid = f"tl{i}"
        values = ";".join(f"{k * cw:.1f}" for k in range(n + 1))
        dur = max(n * cps, 0.05)
        out.append(
            f'<clipPath id="{cid}"><rect x="{x}" y="{y - size}" width="0" height="{size * 1.5}">'
            f'<animate attributeName="width" values="{values}" begin="{t:.2f}s" dur="{dur:.2f}s" '
            f'calcMode="discrete" fill="freeze"/></rect></clipPath>'
        )
        spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in parts)
        out.append(f'<text x="{x}" y="{y}" font-size="{size}" clip-path="url(#{cid})" xml:space="preserve">{spans}</text>')
        t += dur + pause
    return "\n".join(out), t


def header():
    W, H = 1000, 380
    s = []
    s.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}">
<defs>
  <linearGradient id="flag" gradientUnits="userSpaceOnUse" x1="0" y1="64" x2="0" y2="170">
    <stop offset="0" stop-color="{BLUE}"/><stop offset="0.5" stop-color="#5aa0ff"/>
    <stop offset="0.5" stop-color="{YELLOW}"/><stop offset="1" stop-color="#ffb800"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity=".55"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{GREEN}" stop-opacity=".18"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".55"/>
  </linearGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#fff" opacity=".035"/>
  </pattern>
  <clipPath id="win"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14"/></clipPath>
  <clipPath id="banner"><rect x="40" y="62" width="0" height="120">
    <animate attributeName="width" from="0" to="560" begin="0.2s" dur="0.9s" fill="freeze" calcMode="spline" keySplines=".2 .7 .3 1" keyTimes="0;1"/>
  </rect></clipPath>
</defs>
<g clip-path="url(#win)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="36" fill="{PANEL}"/>
<line x1="0" y1="36" x2="{W}" y2="36" stroke="{LINE}"/>
<circle cx="22" cy="18" r="6" fill="#ff5f57"/><circle cx="42" cy="18" r="6" fill="#febc2e"/><circle cx="62" cy="18" r="6" fill="#28c840"/>
<text x="{W / 2}" y="23" text-anchor="middle" font-size="12" fill="{DIM}">v1rus91@cherkasy: ~ — zsh — 120×38</text>
''')
    # ASCII banner with a flag gradient and a passing shine
    s.append('<g clip-path="url(#banner)">')
    for i, line in enumerate(BANNER):
        s.append(f'<text x="40" y="{80 + i * 17}" font-size="15.5" fill="url(#flag)" xml:space="preserve">{escape(line)}</text>')
    s.append(f'''<rect x="-200" y="62" width="160" height="110" fill="url(#shine)" opacity=".5">
  <animate attributeName="x" values="-200;700" dur="3.2s" begin="1.4s" repeatCount="indefinite"/>
</rect></g>''')

    lines = [
        ([("❯ ", YELLOW), ("whoami", TEXT)], 0.25),
        ([("Andrii Kaznachei", GREEN), (" · Defense-Tech Front-End Developer · Ukraine", TEXT)], 0.4),
        ([("❯ ", YELLOW), ("cat ", TEXT), ("stack.ts", BLUE)], 0.25),
        ([("[", DIM), ("Next.js", TEXT), (", ", DIM), ("TypeScript", TEXT), (", ", DIM), ("React", TEXT), (", ", DIM),
          ("Python", TEXT), (", ", DIM), ("Swift", TEXT), ("]", DIM)], 0.4),
        ([("❯ ", YELLOW), ("echo ", TEXT), ("$MISSION", GREEN)], 0.25),
        ([("Building the digital infrastructure for modern defense.", YELLOW)], 0.3),
    ]
    body, end = typed(lines, 40, 208, 14, 25, start=1.3)
    s.append(body)
    cw = 14 * 0.61
    s.append(f'''<text x="40" y="{208 + len(lines) * 25}" font-size="14" fill="{YELLOW}" opacity="0">❯
  <animate attributeName="opacity" values="0;1" begin="{end:.2f}s" dur="0.01s" fill="freeze"/></text>
<rect x="{40 + 2 * cw:.1f}" y="{208 + len(lines) * 25 - 13}" width="{cw:.1f}" height="16" fill="{GREEN}" opacity="0">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="{end:.2f}s" repeatCount="indefinite"/>
</rect>''')

    # Radar
    cx, cy, r = 830, 205, 120
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="url(#glow)"/>')
    for k in (1, 2 / 3, 1 / 3):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r * k:.1f}" fill="none" stroke="{GREEN}" stroke-opacity=".28"/>')
    s.append(f'<line x1="{cx - r}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="{GREEN}" stroke-opacity=".18"/>')
    s.append(f'<line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}" stroke="{GREEN}" stroke-opacity=".18"/>')
    for a in range(0, 360, 10):
        import math
        L = 6 if a % 30 == 0 else 3
        x1, y1 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        x2, y2 = cx + (r - L) * math.cos(math.radians(a)), cy + (r - L) * math.sin(math.radians(a))
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GREEN}" stroke-opacity=".45"/>')
    # 50° sweep wedge rotating around the centre
    import math
    a0 = math.radians(-50)
    s.append(f'''<g><path d="M{cx},{cy} L{cx + r},{cy} A{r},{r} 0 0,0 {cx + r * math.cos(a0):.1f},{cy + r * math.sin(a0):.1f} Z" fill="url(#sweep)" opacity=".7"/>
<line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="{GREEN}" stroke-width="1.6"/>
<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="4s" repeatCount="indefinite"/></g>''')
    # blips light up when the beam passes (beam angle = 90°/s)
    for ang, dist, label in [(35, .55, "UI"), (140, .8, "API"), (215, .4, "SWIFT"), (300, .7, "PY")]:
        bx, by = cx + r * dist * math.cos(math.radians(ang)), cy + r * dist * math.sin(math.radians(ang))
        begin = ang / 360 * 4
        s.append(f'''<g opacity=".15"><circle cx="{bx:.1f}" cy="{by:.1f}" r="4" fill="{GREEN}"/>
<text x="{bx + 7:.1f}" y="{by - 6:.1f}" font-size="9" fill="{GREEN}">{label}</text>
<animate attributeName="opacity" values="1;.15" dur="4s" begin="{begin:.2f}s" repeatCount="indefinite"/></g>''')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{YELLOW}"/>')
    s.append(f'<text x="{cx}" y="{cy - r - 10}" text-anchor="middle" font-size="10" fill="{GREEN}" opacity=".8">N</text>')
    s.append(f'<text x="{cx}" y="{cy + r + 22}" text-anchor="middle" font-size="10.5" fill="{DIM}">49.44°N  32.06°E · CHERKASY</text>')
    s.append(f'<text x="{cx - r - 10}" y="{cy - r + 4}" font-size="10" fill="{GREEN}">● TRACKING<animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></text>')

    s.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    s.append('</g>')
    s.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{LINE}" stroke-width="2"/>')
    s.append('</svg>')
    return "\n".join(s)


PROJECTS = [
    ("Stezha", "Air raid alerts in the MacBook notch: hover to see a live map of Ukraine, raion-level status for your area, stats and notifications.", "Swift", "macOS · Notch · alerts.in.ua"),
    ("Void", "Mac cleaner and live system monitor: smart cleanup, disk analyzer, duplicates, uninstaller, startup items, menu bar.", "Swift", "macOS · SwiftUI · Liquid Glass"),
    ("UniLoader", "Native media downloader: YouTube, Instagram, TikTok and 1000+ sites via yt-dlp, plus Spotify / Apple Music links to tagged audio.", "Swift", "macOS · SwiftUI · yt-dlp"),
    ("ClipGlass", "Smart clipboard manager: card tray, pinboards, type-aware actions, OCR, snippets with placeholders, secret filtering.", "Swift", "macOS · SwiftUI · Liquid Glass"),
    ("ServerPulse", "Menu-bar server monitor: agentless over SSH, Docker and systemd checks, alerts.", "Swift", "macOS · SSH · Liquid Glass"),
    ("WinForge", "Windows 11 optimizer that knows exactly what it changed: 145 declarative tweaks, journaled undo, live state detection.", "PowerShell", "Windows 11 · GUI / TUI / CLI"),
]
LANG = {"Swift": "#F05138", "PowerShell": "#2f7cff"}


def card(i, name, desc, lang, tags):
    W, H = 490, 170
    lines = textwrap.wrap(desc, 58)[:3]
    c = LANG.get(lang, GREEN)
    corner = lambda x, y, dx, dy: f'<path d="M{x},{y + 14 * dy} L{x},{y} L{x + 14 * dx},{y}" fill="none" stroke="{YELLOW}" stroke-width="2"/>'
    body = "".join(f'<text x="24" y="{86 + k * 19}" font-size="13" fill="{TEXT}" opacity=".85">{escape(l)}</text>' for k, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}">
<defs><pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{YELLOW}"/></linearGradient></defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="{LINE}" stroke-width="1.5"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="url(#g)"/>
<rect x="24" y="1" width="80" height="3" fill="url(#edge)"/>
{corner(8, 8, 1, 1)}{corner(W - 8, 8, -1, 1)}{corner(8, H - 8, 1, -1)}{corner(W - 8, H - 8, -1, -1)}
<text x="24" y="34" font-size="11" fill="{DIM}">// UNIT {i:02d}</text>
<text x="{W - 24}" y="34" font-size="11" fill="{GREEN}" text-anchor="end">● ONLINE<animate attributeName="opacity" values="1;.35;1" dur="2s" begin="{i * 0.3:.1f}s" repeatCount="indefinite"/></text>
<text x="24" y="62" font-size="22" font-weight="700" fill="#fff">{escape(name)}</text>
{body}
<circle cx="29" cy="{H - 24}" r="5" fill="{c}"/>
<text x="40" y="{H - 20}" font-size="12" fill="{TEXT}">{lang}</text>
<text x="{W - 24}" y="{H - 20}" font-size="11.5" fill="{DIM}" text-anchor="end">{escape(tags)}</text>
</svg>'''


def footer():
    W, H = 1000, 70
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}">
<defs><linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
<stop offset=".5" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H / 2}" fill="{BLUE}"/><rect y="{H / 2}" width="{W}" height="{H / 2}" fill="{YELLOW}"/>
<rect x="-300" width="260" height="{H}" fill="url(#s)"><animate attributeName="x" values="-300;{W + 40}" dur="4s" repeatCount="indefinite"/></rect>
</g>
<text x="{W / 2}" y="{H / 2 - 9}" text-anchor="middle" font-size="15" font-weight="700" fill="#fff" letter-spacing="4">СЛАВА УКРАЇНІ</text>
<text x="{W / 2}" y="{H / 2 + 22}" text-anchor="middle" font-size="15" font-weight="700" fill="#0b2a5c" letter-spacing="4">ГЕРОЯМ СЛАВА</text>
</svg>'''


with open(os.path.join(ROOT, "header.svg"), "w") as f: f.write(header())
with open(os.path.join(ROOT, "footer.svg"), "w") as f: f.write(footer())
for i, p in enumerate(PROJECTS, 1):
    with open(os.path.join(ROOT, "cards", p[0].lower() + ".svg"), "w") as f: f.write(card(i, *p))
print("ok")
