import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
from collections import defaultdict

st.set_page_config(
    page_title="AptitudePro — Graduate Psychometric Suite",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Global ─────────────────────────────── */
:root {
    --navy:   #0f1a2e;
    --blue:   #1a56db;
    --sky:    #3b82f6;
    --teal:   #0d9488;
    --gold:   #f59e0b;
    --green:  #059669;
    --red:    #dc2626;
    --paper:  #f8f9fc;
    --white:  #ffffff;
    --border: #e5e7eb;
    --mid:    #6b7280;
    --ink:    #111827;
}

.main { background: var(--paper); }
#MainMenu, footer, header { visibility: hidden; }

/* ── App Header ─────────────────────────── */
.app-header {
    background: linear-gradient(135deg, #0f1a2e 0%, #1a3a6b 100%);
    padding: 1.25rem 2rem;
    border-radius: 14px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 32px rgba(15,26,46,0.18);
}
.app-header-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.75rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.02em;
}
.app-header-title span { color: #f59e0b; }
.app-header-sub {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.6);
    margin-top: 0.15rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.header-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.85);
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.03em;
}

/* ── Stat Cards ─────────────────────────── */
.stat-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    border-left: 4px solid var(--blue);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s;
}
.stat-card:hover { box-shadow: 0 6px 20px rgba(26,86,219,0.1); }
.stat-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.stat-label { font-size: 0.78rem; color: var(--mid); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.stat-value { font-size: 1.75rem; font-weight: 700; color: var(--navy); margin-top: 0.1rem; }

/* ── Category Cards ─────────────────────── */
.cat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem; }
.cat-card {
    background: var(--white);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    transition: all 0.22s;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.cat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--blue), var(--sky));
    opacity: 0;
    transition: opacity 0.22s;
}
.cat-card:hover { border-color: var(--blue); transform: translateY(-3px); box-shadow: 0 10px 28px rgba(26,86,219,0.12); }
.cat-card:hover::before { opacity: 1; }
.cat-icon { font-size: 1.75rem; margin-bottom: 0.6rem; }
.cat-name { font-weight: 700; color: var(--navy); font-size: 0.95rem; margin-bottom: 0.25rem; }
.cat-desc { font-size: 0.78rem; color: var(--mid); line-height: 1.5; }
.cat-badge {
    display: inline-block;
    margin-top: 0.6rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-green { background: #d1fae5; color: #065f46; }
.badge-yellow { background: #fef3c7; color: #92400e; }
.badge-red { background: #fee2e2; color: #991b1b; }

/* ── FEATURED: Full Blend Card ──────────── */
.blend-card {
    background: linear-gradient(135deg, #0f1a2e 0%, #1e3a6e 50%, #0d7a6f 100%);
    border-radius: 16px;
    padding: 2rem;
    color: white;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(15,26,46,0.25);
}
.blend-card::after {
    content: '⚡';
    position: absolute;
    right: 2rem; top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.08;
}
.blend-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
}
.blend-subtitle { color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-bottom: 1.25rem; }
.blend-chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1.25rem; }
.blend-chip {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    padding: 0.2rem 0.65rem;
    border-radius: 100px;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.9);
}

/* ── Question Interface ──────────────────── */
.q-header {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.q-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}
.q-tag {
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.q-tag-num  { background: #dbeafe; color: #1e40af; }
.q-tag-verb { background: #ede9fe; color: #5b21b6; }
.q-tag-log  { background: #d1fae5; color: #065f46; }
.q-tag-mech { background: #ffedd5; color: #9a3412; }
.q-tag-sjt  { background: #fce7f3; color: #9d174d; }
.q-tag-wg   { background: #cffafe; color: #164e63; }
.q-tag-abs  { background: #f3e8ff; color: #6b21a8; }
.q-tag-iq   { background: #fef9c3; color: #713f12; }
.q-tag-sp   { background: #e0f2fe; color: #075985; }
.q-tag-err  { background: #fef2f2; color: #991b1b; }
.q-tag-cr   { background: #ecfdf5; color: #14532d; }
.q-tag-diag { background: #f0fdf4; color: #166534; }

.q-difficulty-easy   { background: #d1fae5; color: #059669; }
.q-difficulty-medium { background: #fef3c7; color: #b45309; }
.q-difficulty-hard   { background: #fee2e2; color: #dc2626; }

.q-text {
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--ink);
    font-weight: 500;
}

.passage-box {
    background: #f0f7ff;
    border-left: 4px solid var(--blue);
    padding: 1rem 1.25rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.9rem;
    line-height: 1.7;
    color: #1e3a5f;
    margin-bottom: 1rem;
}

/* ── Answer Options ─────────────────────── */
.opt-btn {
    display: block;
    width: 100%;
    padding: 0.9rem 1.25rem;
    margin: 0.4rem 0;
    border: 2px solid var(--border);
    border-radius: 10px;
    background: var(--white);
    text-align: left;
    cursor: pointer;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: var(--ink);
    transition: all 0.18s;
    line-height: 1.5;
}
.opt-btn:hover { border-color: var(--blue); background: #eff6ff; }
.opt-selected {
    border-color: var(--blue) !important;
    background: #eff6ff !important;
    color: var(--blue) !important;
    font-weight: 600;
    box-shadow: 0 0 0 3px rgba(26,86,219,0.12);
}
/* Review mode */
.opt-correct { border-color: var(--green) !important; background: #d1fae5 !important; color: #065f46 !important; font-weight: 600; }
.opt-wrong   { border-color: var(--red) !important;   background: #fee2e2 !important; color: #991b1b !important; }

/* ── Timer ──────────────────────────────── */
.timer-display {
    background: var(--navy);
    color: white;
    padding: 0.6rem 1.5rem;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 12px rgba(15,26,46,0.2);
}
.timer-warn { background: #b45309 !important; }
.timer-danger { background: var(--red) !important; animation: pulse 1s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.7} }

/* ── Progress ───────────────────────────── */
.prog-bar-wrap { background: #e5e7eb; border-radius: 999px; height: 8px; overflow: hidden; }
.prog-bar-fill { background: linear-gradient(90deg, var(--blue), var(--sky)); height: 100%; border-radius: 999px; transition: width 0.3s; }

/* ── Q Navigator ────────────────────────── */
.q-nav-wrap { display: flex; flex-wrap: wrap; gap: 4px; justify-content: center; margin: 0.75rem 0; }
.q-nav-dot {
    width: 34px; height: 34px;
    border-radius: 7px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 600;
    cursor: pointer;
    border: 2px solid var(--border);
    background: white;
    color: var(--mid);
    transition: all 0.15s;
}
.q-nav-dot:hover  { border-color: var(--blue); color: var(--blue); }
.q-nav-answered   { background: var(--green) !important; border-color: var(--green) !important; color: white !important; }
.q-nav-current    { border-color: var(--blue) !important; color: var(--blue) !important; font-weight: 700 !important; box-shadow: 0 0 0 3px rgba(26,86,219,0.2); }
.q-nav-flagged    { border-color: var(--gold) !important; color: var(--gold) !important; }

/* ── Results ────────────────────────────── */
.result-hero {
    background: linear-gradient(135deg, #0f1a2e, #1a3a6b);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    color: white;
    margin-bottom: 1.5rem;
}
.result-score {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    color: #f59e0b;
}
.result-grade { font-size: 1.2rem; color: rgba(255,255,255,0.85); margin-top: 0.5rem; }

.result-stat {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.result-stat-val { font-size: 1.75rem; font-weight: 700; }
.result-stat-lbl { font-size: 0.78rem; color: var(--mid); margin-top: 0.2rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }

/* ── Explanation ────────────────────────── */
.exp-box {
    background: #f0f7ff;
    border-left: 4px solid var(--blue);
    padding: 1rem 1.25rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.9rem;
    color: #1e3a5f;
    margin-top: 0.75rem;
    line-height: 1.6;
}

/* ── SVG diagrams ───────────────────────── */
.diagram-box {
    background: white;
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.75rem 0;
    display: flex;
    justify-content: center;
}

/* ── Misc ───────────────────────────────── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--navy);
    margin: 1.5rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.divider { border: none; border-top: 1px solid var(--border); margin: 1.25rem 0; }
.info-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    font-size: 0.875rem;
    color: #1e3a5f;
    margin: 0.75rem 0;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# SVG DIAGRAM HELPERS
# ═══════════════════════════════════════════════════════

def svg_gears(a_teeth=20, b_teeth=40, a_rpm=200):
    b_rpm = round(a_teeth * a_rpm / b_teeth)
    ra, rb = 40, 80
    return f"""
<svg width="260" height="160" viewBox="0 0 260 160" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <path d="M0,0 L0,8 L8,4 z" fill="#1a56db"/>
    </marker>
  </defs>
  <!-- Gear A -->
  <circle cx="70" cy="80" r="{ra}" fill="#e0edff" stroke="#1a56db" stroke-width="2"/>
  <circle cx="70" cy="80" r="{ra-10}" fill="none" stroke="#1a56db" stroke-width="1.5" stroke-dasharray="4,3"/>
  <circle cx="70" cy="80" r="8" fill="#1a56db"/>
  <text x="70" y="84" text-anchor="middle" fill="#1a56db" font-size="10" font-weight="700">{a_teeth}T</text>
  <text x="70" y="136" text-anchor="middle" fill="#1a56db" font-size="10" font-weight="600">{a_rpm} RPM →</text>
  <!-- Gear B -->
  <circle cx="190" cy="80" r="{rb}" fill="#fff3e0" stroke="#f59e0b" stroke-width="2"/>
  <circle cx="190" cy="80" r="{rb-10}" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,4"/>
  <circle cx="190" cy="80" r="10" fill="#f59e0b"/>
  <text x="190" y="84" text-anchor="middle" fill="#92400e" font-size="10" font-weight="700">{b_teeth}T</text>
  <text x="190" y="136" text-anchor="middle" fill="#f59e0b" font-size="10" font-weight="600">? RPM</text>
  <!-- Mesh point -->
  <circle cx="110" cy="80" r="4" fill="#059669"/>
  <text x="130" y="20" text-anchor="middle" fill="#374151" font-size="9">Gear A drives Gear B</text>
</svg>"""


def svg_lever(load_dist=2, effort_dist=4, load=100):
    # Fulcrum at x=130, beam from 20 to 240
    total = load_dist + effort_dist
    frac = load_dist / total
    load_x = int(130 - frac * 110)
    effort_x = int(130 + (1 - frac) * 110)
    return f"""
<svg width="300" height="130" viewBox="0 0 300 130" xmlns="http://www.w3.org/2000/svg">
  <!-- Beam -->
  <line x1="20" y1="70" x2="280" y2="70" stroke="#374151" stroke-width="6" stroke-linecap="round"/>
  <!-- Fulcrum triangle -->
  <polygon points="130,70 115,100 145,100" fill="#1a56db"/>
  <line x1="110" y1="100" x2="150" y2="100" stroke="#1a56db" stroke-width="3"/>
  <!-- Load (down arrow) -->
  <line x1="{load_x}" y1="40" x2="{load_x}" y2="68" stroke="#dc2626" stroke-width="3" marker-end="url(#arrd)"/>
  <text x="{load_x}" y="32" text-anchor="middle" fill="#dc2626" font-size="11" font-weight="700">{load}N</text>
  <text x="{load_x}" y="22" text-anchor="middle" fill="#dc2626" font-size="9">{load_dist}m</text>
  <!-- Effort (up arrow) -->
  <line x1="{effort_x}" y1="95" x2="{effort_x}" y2="73" stroke="#059669" stroke-width="3" marker-end="url(#arru)"/>
  <text x="{effort_x}" y="112" text-anchor="middle" fill="#059669" font-size="11" font-weight="700">E = ?</text>
  <text x="{effort_x}" y="122" text-anchor="middle" fill="#059669" font-size="9">{effort_dist}m</text>
  <!-- Labels -->
  <text x="130" y="115" text-anchor="middle" fill="#1a56db" font-size="9" font-weight="600">FULCRUM</text>
  <defs>
    <marker id="arrd" markerWidth="8" markerHeight="8" refX="4" refY="8" orient="auto">
      <path d="M0,0 L8,0 L4,8 z" fill="#dc2626"/>
    </marker>
    <marker id="arru" markerWidth="8" markerHeight="8" refX="4" refY="0" orient="auto">
      <path d="M0,8 L8,8 L4,0 z" fill="#059669"/>
    </marker>
  </defs>
</svg>"""


def svg_pulley(ropes=4, load=400):
    effort = load // ropes
    return f"""
<svg width="220" height="170" viewBox="0 0 220 170" xmlns="http://www.w3.org/2000/svg">
  <!-- Fixed pulley -->
  <circle cx="110" cy="30" r="22" fill="#e0edff" stroke="#1a56db" stroke-width="2"/>
  <circle cx="110" cy="30" r="8" fill="#1a56db"/>
  <text x="110" y="10" text-anchor="middle" fill="#374151" font-size="9">Fixed Pulley</text>
  <!-- Movable pulley -->
  <circle cx="110" cy="100" r="20" fill="#fff3e0" stroke="#f59e0b" stroke-width="2"/>
  <circle cx="110" cy="100" r="7" fill="#f59e0b"/>
  <!-- Ropes -->
  <line x1="91" y1="100" x2="91" y2="30" stroke="#374151" stroke-width="1.5" stroke-dasharray="3,2"/>
  <line x1="102" y1="100" x2="102" y2="30" stroke="#374151" stroke-width="1.5" stroke-dasharray="3,2"/>
  <line x1="118" y1="100" x2="118" y2="30" stroke="#374151" stroke-width="1.5" stroke-dasharray="3,2"/>
  <line x1="129" y1="100" x2="160" y2="30" stroke="#374151" stroke-width="1.5" stroke-dasharray="3,2"/>
  <!-- Load -->
  <rect x="85" y="120" width="50" height="30" fill="#dc2626" rx="4"/>
  <text x="110" y="140" text-anchor="middle" fill="white" font-size="11" font-weight="700">{load}N</text>
  <!-- Effort -->
  <line x1="160" y1="30" x2="160" y2="60" stroke="#059669" stroke-width="2.5"/>
  <text x="175" y="50" fill="#059669" font-size="10" font-weight="700">E={effort}N</text>
  <text x="110" y="165" text-anchor="middle" fill="#374151" font-size="9">MA = {ropes} rope(s) support load</text>
</svg>"""


def svg_cube_net():
    """Show a standard cube net with labeled faces"""
    return """
<svg width="280" height="200" viewBox="0 0 280 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="80" y="10" width="60" height="60" fill="#dbeafe" stroke="#1a56db" stroke-width="2" rx="2"/>
  <text x="110" y="46" text-anchor="middle" fill="#1e40af" font-size="13" font-weight="700">Top</text>

  <rect x="20" y="70" width="60" height="60" fill="#fef3c7" stroke="#f59e0b" stroke-width="2" rx="2"/>
  <text x="50" y="106" text-anchor="middle" fill="#92400e" font-size="13" font-weight="700">Left</text>

  <rect x="80" y="70" width="60" height="60" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="2"/>
  <text x="110" y="106" text-anchor="middle" fill="#065f46" font-size="13" font-weight="700">Front</text>

  <rect x="140" y="70" width="60" height="60" fill="#ede9fe" stroke="#7c3aed" stroke-width="2" rx="2"/>
  <text x="170" y="106" text-anchor="middle" fill="#5b21b6" font-size="13" font-weight="700">Right</text>

  <rect x="200" y="70" width="60" height="60" fill="#fce7f3" stroke="#db2777" stroke-width="2" rx="2"/>
  <text x="230" y="106" text-anchor="middle" fill="#9d174d" font-size="13" font-weight="700">Back</text>

  <rect x="80" y="130" width="60" height="60" fill="#ffedd5" stroke="#ea580c" stroke-width="2" rx="2"/>
  <text x="110" y="166" text-anchor="middle" fill="#9a3412" font-size="13" font-weight="700">Bottom</text>

  <text x="140" y="195" text-anchor="middle" fill="#6b7280" font-size="9">Standard cross-shaped cube net — 6 faces</text>
</svg>"""


def svg_cube_rotation():
    """Shows a 3D cube and its rotated version"""
    return """
<svg width="300" height="130" viewBox="0 0 300 130" xmlns="http://www.w3.org/2000/svg">
  <!-- Cube 1 -->
  <polygon points="30,90 80,90 80,40 30,40" fill="#dbeafe" stroke="#1a56db" stroke-width="2"/>
  <polygon points="80,40 110,20 110,70 80,90" fill="#bfdbfe" stroke="#1a56db" stroke-width="2"/>
  <polygon points="30,40 80,40 110,20 60,20" fill="#eff6ff" stroke="#1a56db" stroke-width="2"/>
  <text x="55" y="70" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="700">A</text>
  <text x="55" y="115" text-anchor="middle" fill="#374151" font-size="10">Original</text>

  <!-- Arrow -->
  <text x="150" y="65" text-anchor="middle" fill="#374151" font-size="18">→</text>
  <text x="150" y="82" text-anchor="middle" fill="#6b7280" font-size="8">90° CW</text>

  <!-- Cube 2 rotated appearance -->
  <polygon points="190,90 240,90 240,40 190,40" fill="#d1fae5" stroke="#059669" stroke-width="2"/>
  <polygon points="240,40 270,20 270,70 240,90" fill="#a7f3d0" stroke="#059669" stroke-width="2"/>
  <polygon points="190,40 240,40 270,20 220,20" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="220" y="70" text-anchor="middle" fill="#065f46" font-size="10" font-weight="700">A</text>
  <text x="220" y="115" text-anchor="middle" fill="#374151" font-size="10">Rotated</text>
</svg>"""


def svg_hydraulic(a_area=5, b_area=25, force_a=100):
    force_b = force_a * b_area // a_area
    w_a = 40; w_b = int(40 * (b_area / a_area) ** 0.5)
    return f"""
<svg width="300" height="150" viewBox="0 0 300 150" xmlns="http://www.w3.org/2000/svg">
  <!-- Cylinder A -->
  <rect x="30" y="60" width="{w_a}" height="70" fill="#dbeafe" stroke="#1a56db" stroke-width="2" rx="3"/>
  <rect x="30" y="50" width="{w_a}" height="18" fill="#1a56db" rx="2"/>
  <text x="{30+w_a//2}" y="32" text-anchor="middle" fill="#dc2626" font-size="11" font-weight="700">{force_a}N ↓</text>
  <text x="{30+w_a//2}" y="142" text-anchor="middle" fill="#374151" font-size="9">{a_area} cm²</text>
  <!-- Fluid pipe -->
  <rect x="{30+w_a}" y="110" width="{160-w_a}" height="14" fill="#bfdbfe" stroke="#1a56db" stroke-width="1.5"/>
  <!-- Cylinder B -->
  <rect x="190" y="40" width="{w_b}" height="90" fill="#fef3c7" stroke="#f59e0b" stroke-width="2" rx="3"/>
  <rect x="190" y="26" width="{w_b}" height="22" fill="#f59e0b" rx="2"/>
  <text x="{190+w_b//2}" y="14" text-anchor="middle" fill="#059669" font-size="11" font-weight="700">{force_b}N ↑</text>
  <text x="{190+w_b//2}" y="142" text-anchor="middle" fill="#374151" font-size="9">{b_area} cm²</text>
  <text x="140" y="155" text-anchor="middle" fill="#374151" font-size="8">Pascal's Law: P = F/A is constant</text>
</svg>"""


def svg_pipe_flow():
    return """
<svg width="300" height="100" viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Wide pipe -->
  <rect x="10" y="30" width="110" height="40" fill="#dbeafe" stroke="#1a56db" stroke-width="2" rx="2"/>
  <!-- Arrow in wide -->
  <text x="65" y="55" text-anchor="middle" fill="#1a56db" font-size="11" font-weight="700">→ 2 m/s</text>
  <text x="65" y="22" text-anchor="middle" fill="#374151" font-size="9">Area = A</text>
  <!-- Narrow section -->
  <polygon points="120,30 160,38 160,62 120,70" fill="#bfdbfe" stroke="#1a56db" stroke-width="2"/>
  <!-- Narrow pipe -->
  <rect x="160" y="38" width="120" height="24" fill="#eff6ff" stroke="#1a56db" stroke-width="2" rx="2"/>
  <text x="220" y="54" text-anchor="middle" fill="#1a56db" font-size="11" font-weight="700">→ ? m/s</text>
  <text x="220" y="30" text-anchor="middle" fill="#374151" font-size="9">Area = A/2</text>
  <text x="150" y="92" text-anchor="middle" fill="#374151" font-size="8">Continuity: A₁v₁ = A₂v₂</text>
</svg>"""


def svg_abstract_matrix():
    """3x2 matrix pattern for abstract reasoning"""
    return """
<svg width="280" height="200" viewBox="0 0 280 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Row 1 -->
  <rect x="10" y="10" width="70" height="70" fill="#f9fafb" stroke="#d1d5db" stroke-width="1.5" rx="4"/>
  <circle cx="45" cy="30" r="12" fill="#dc2626"/>
  <circle cx="30" cy="55" r="10" fill="#1a56db" opacity="0.3"/>
  <circle cx="60" cy="55" r="10" fill="#1a56db" opacity="0.3"/>

  <rect x="105" y="10" width="70" height="70" fill="#f9fafb" stroke="#d1d5db" stroke-width="1.5" rx="4"/>
  <circle cx="140" cy="30" r="12" fill="#dc2626"/>
  <circle cx="125" cy="55" r="12" fill="#dc2626"/>
  <circle cx="155" cy="55" r="10" fill="#1a56db" opacity="0.3"/>

  <rect x="200" y="10" width="70" height="70" fill="#f9fafb" stroke="#d1d5db" stroke-width="1.5" rx="4"/>
  <circle cx="235" cy="30" r="12" fill="#dc2626"/>
  <circle cx="220" cy="55" r="12" fill="#dc2626"/>
  <circle cx="250" cy="55" r="12" fill="#dc2626"/>

  <!-- Row 2 -->
  <rect x="10" y="110" width="70" height="70" fill="#f9fafb" stroke="#d1d5db" stroke-width="1.5" rx="4"/>
  <rect x="28" y="128" width="18" height="18" fill="#059669" rx="2"/>
  <rect x="53" y="128" width="18" height="18" fill="#6b7280" rx="2" opacity="0.3"/>
  <rect x="28" y="152" width="18" height="18" fill="#6b7280" rx="2" opacity="0.3"/>
  <rect x="53" y="152" width="18" height="18" fill="#6b7280" rx="2" opacity="0.3"/>

  <rect x="105" y="110" width="70" height="70" fill="#f9fafb" stroke="#d1d5db" stroke-width="1.5" rx="4"/>
  <rect x="123" y="128" width="18" height="18" fill="#059669" rx="2"/>
  <rect x="148" y="128" width="18" height="18" fill="#059669" rx="2"/>
  <rect x="123" y="152" width="18" height="18" fill="#6b7280" rx="2" opacity="0.3"/>
  <rect x="148" y="152" width="18" height="18" fill="#6b7280" rx="2" opacity="0.3"/>

  <!-- ??? box -->
  <rect x="200" y="110" width="70" height="70" fill="#eff6ff" stroke="#1a56db" stroke-width="2" stroke-dasharray="5,3" rx="4"/>
  <text x="235" y="152" text-anchor="middle" fill="#1a56db" font-size="22" font-weight="800">?</text>

  <text x="140" y="196" text-anchor="middle" fill="#6b7280" font-size="9">Find the pattern — what completes the bottom-right?</text>
</svg>"""


def svg_spatial_l_rotation():
    return """
<svg width="300" height="120" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
  <!-- L shape original -->
  <rect x="20" y="20" width="25" height="70" fill="#dbeafe" stroke="#1a56db" stroke-width="2" rx="2"/>
  <rect x="20" y="65" width="60" height="25" fill="#dbeafe" stroke="#1a56db" stroke-width="2" rx="2"/>
  <text x="52" y="108" text-anchor="middle" fill="#374151" font-size="9">Original ┗</text>

  <text x="115" y="62" text-anchor="middle" fill="#374151" font-size="16">→</text>
  <text x="115" y="76" text-anchor="middle" fill="#6b7280" font-size="8">90° CW</text>

  <!-- 90° CW: L becomes ┏ shape -->
  <rect x="145" y="20" width="70" height="25" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="2"/>
  <rect x="145" y="20" width="25" height="70" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="2"/>
  <text x="180" y="108" text-anchor="middle" fill="#374151" font-size="9">Result ┏</text>

  <text x="255" y="62" text-anchor="middle" fill="#374151" font-size="9">Options:</text>
  <text x="255" y="77" text-anchor="middle" fill="#059669" font-size="18" font-weight="700">┏</text>
</svg>"""

# ═══════════════════════════════════════════════════════
# QUESTION BANK — CLEANED & EXPANDED
# ═══════════════════════════════════════════════════════

def build_question_bank():
    bank = {}

    # ── NUMERICAL ─────────────────────────────────────
    bank["numerical"] = [
        {"id":"N001","cat":"numerical","sub":"Percentages","diff":"medium",
         "text":"A company's revenue increased by 15% from £2.4 million. What is the new revenue?",
         "opts":["£2.76m","£2.64m","£2.88m","£2.52m"],"ans":0,
         "exp":"£2.4m × 1.15 = <strong>£2.76m</strong>"},

        {"id":"N002","cat":"numerical","sub":"Percentages","diff":"medium",
         "text":"After a 12% discount, an item costs £308. What was the original price?",
         "opts":["£350","£340","£360","£345"],"ans":0,
         "exp":"88% × original = £308 → original = 308 ÷ 0.88 = <strong>£350</strong>"},

        {"id":"N003","cat":"numerical","sub":"Ratios","diff":"easy",
         "text":"Divide £720 in the ratio 5:3:4.",
         "opts":["£300 : £180 : £240","£360 : £180 : £180","£250 : £150 : £320","£400 : £240 : £320"],"ans":0,
         "exp":"Total parts = 12. Unit = £60. Parts: 5×60=<strong>£300</strong>, 3×60=<strong>£180</strong>, 4×60=<strong>£240</strong>"},

        {"id":"N004","cat":"numerical","sub":"Currency","diff":"medium",
         "text":"If £1 = $1.25 and €1 = $1.10, approximately how many euros equal £500?",
         "opts":["€568","€550","€625","€575"],"ans":0,
         "exp":"£500 → $625 → $625 ÷ 1.10 = <strong>€568</strong>"},

        {"id":"N005","cat":"numerical","sub":"Data Table","diff":"medium",
         "text":"""<table style='width:100%;border-collapse:collapse;margin:0.75rem 0;font-size:0.9rem;'>
<tr style='background:#1a56db;color:white;'><th style='padding:6px 10px;'>Quarter</th><th style='padding:6px 10px;'>Sales (£k)</th><th style='padding:6px 10px;'>Costs (£k)</th></tr>
<tr style='background:#f9fafb;'><td style='padding:6px 10px;text-align:center;'>Q1</td><td style='padding:6px 10px;text-align:center;'>450</td><td style='padding:6px 10px;text-align:center;'>320</td></tr>
<tr><td style='padding:6px 10px;text-align:center;'>Q2</td><td style='padding:6px 10px;text-align:center;'>520</td><td style='padding:6px 10px;text-align:center;'>380</td></tr>
<tr style='background:#f9fafb;'><td style='padding:6px 10px;text-align:center;'>Q3</td><td style='padding:6px 10px;text-align:center;'>480</td><td style='padding:6px 10px;text-align:center;'>350</td></tr>
<tr><td style='padding:6px 10px;text-align:center;'>Q4</td><td style='padding:6px 10px;text-align:center;'>610</td><td style='padding:6px 10px;text-align:center;'>420</td></tr>
</table>
What was the average quarterly profit (£k)?""",
         "opts":["£147.5k","£150k","£145k","£152.5k"],"ans":0,
         "exp":"Profits: Q1=130, Q2=140, Q3=130, Q4=190. Average = 590÷4 = <strong>£147.5k</strong>"},

        {"id":"N006","cat":"numerical","sub":"Data Table","diff":"hard",
         "text":"""<table style='width:100%;border-collapse:collapse;margin:0.75rem 0;font-size:0.9rem;'>
<tr style='background:#1a56db;color:white;'><th style='padding:6px 8px;'>Product</th><th style='padding:6px 8px;'>Units</th><th style='padding:6px 8px;'>Price</th><th style='padding:6px 8px;'>Discount</th></tr>
<tr style='background:#f9fafb;'><td style='padding:6px 8px;text-align:center;'>A</td><td style='padding:6px 8px;text-align:center;'>1,200</td><td style='padding:6px 8px;text-align:center;'>£45</td><td style='padding:6px 8px;text-align:center;'>10%</td></tr>
<tr><td style='padding:6px 8px;text-align:center;'>B</td><td style='padding:6px 8px;text-align:center;'>800</td><td style='padding:6px 8px;text-align:center;'>£60</td><td style='padding:6px 8px;text-align:center;'>15%</td></tr>
<tr style='background:#f9fafb;'><td style='padding:6px 8px;text-align:center;'>C</td><td style='padding:6px 8px;text-align:center;'>1,500</td><td style='padding:6px 8px;text-align:center;'>£35</td><td style='padding:6px 8px;text-align:center;'>5%</td></tr>
</table>
What is the total revenue after discounts?""",
         "opts":["£139,275","£142,500","£135,000","£145,250"],"ans":0,
         "exp":"A: 1200×45×0.9=£48,600 | B: 800×60×0.85=£40,800 | C: 1500×35×0.95=£49,875 | Total=<strong>£139,275</strong>"},

        {"id":"N007","cat":"numerical","sub":"Finance","diff":"hard",
         "text":"An investment of £5,000 grows at 8% compound interest for 3 years. What is the final value (nearest £)?",
         "opts":["£6,299","£6,200","£6,400","£6,500"],"ans":0,
         "exp":"5000 × (1.08)³ = 5000 × 1.2597 = <strong>£6,299</strong>"},

        {"id":"N008","cat":"numerical","sub":"Finance","diff":"medium",
         "text":"A share price drops 20% then rises 25%. What is the net percentage change?",
         "opts":["0% (no change)","5% gain","5% loss","2% gain"],"ans":0,
         "exp":"Start 100 → ×0.8 = 80 → ×1.25 = 100. Net change = <strong>0%</strong>"},

        {"id":"N009","cat":"numerical","sub":"Speed/Distance","diff":"medium",
         "text":"A train travels 360 km in 2 hours 24 minutes. What is its average speed?",
         "opts":["150 km/h","144 km/h","160 km/h","140 km/h"],"ans":0,
         "exp":"2h 24min = 2.4h. Speed = 360 ÷ 2.4 = <strong>150 km/h</strong>"},

        {"id":"N010","cat":"numerical","sub":"Rates","diff":"hard",
         "text":"Machine A produces 240 units/hr; Machine B produces 180 units/hr. Together for 6 hours, how many units total?",
         "opts":["2,520","2,400","2,640","2,340"],"ans":0,
         "exp":"Combined rate = 420 units/hr. Total = 420 × 6 = <strong>2,520 units</strong>"},

        {"id":"N011","cat":"numerical","sub":"Statistics","diff":"medium",
         "text":"The average of 5 numbers is 24. Four are: 18, 22, 28, 30. What is the fifth?",
         "opts":["22","20","24","26"],"ans":0,
         "exp":"Sum = 5×24 = 120. Known sum = 98. Fifth = 120 − 98 = <strong>22</strong>"},

        {"id":"N012","cat":"numerical","sub":"Statistics","diff":"hard",
         "text":"A normally-distributed dataset has mean 50 and standard deviation 10. Approximately what % of values fall between 40 and 60?",
         "opts":["68%","95%","50%","75%"],"ans":0,
         "exp":"40–60 = ±1σ from mean → empirical rule gives <strong>≈68%</strong>"},

        {"id":"N013","cat":"numerical","sub":"Percentages","diff":"easy",
         "text":"What is 15% of 80 plus 25% of 120?",
         "opts":["42","45","40","48"],"ans":0,
         "exp":"15%×80=12, 25%×120=30. Total = <strong>42</strong>"},

        {"id":"N014","cat":"numerical","sub":"Ratios","diff":"medium",
         "text":"If 3:5 = x:35, find x.",
         "opts":["21","20","25","18"],"ans":0,
         "exp":"x = (3 × 35) ÷ 5 = <strong>21</strong>"},

        {"id":"N015","cat":"numerical","sub":"Data Table","diff":"medium",
         "text":"""<table style='width:100%;border-collapse:collapse;margin:0.75rem 0;font-size:0.9rem;'>
<tr style='background:#1a56db;color:white;'><th style='padding:6px 10px;'>Month</th><th style='padding:6px 10px;'>Revenue</th><th style='padding:6px 10px;'>Target</th></tr>
<tr style='background:#f9fafb;'><td style='padding:6px 10px;text-align:center;'>Jan</td><td style='padding:6px 10px;text-align:center;'>£125k</td><td style='padding:6px 10px;text-align:center;'>£120k</td></tr>
<tr><td style='padding:6px 10px;text-align:center;'>Feb</td><td style='padding:6px 10px;text-align:center;'>£110k</td><td style='padding:6px 10px;text-align:center;'>£115k</td></tr>
<tr style='background:#f9fafb;'><td style='padding:6px 10px;text-align:center;'>Mar</td><td style='padding:6px 10px;text-align:center;'>£135k</td><td style='padding:6px 10px;text-align:center;'>£130k</td></tr>
</table>
Overall target achievement %?""",
         "opts":["101.4%","100%","105%","98%"],"ans":0,
         "exp":"Total revenue £370k vs target £365k. (370÷365)×100 = <strong>101.4%</strong>"},

        {"id":"N016","cat":"numerical","sub":"Percentages","diff":"medium",
         "text":"A salary of £45,000 receives a 7.5% raise. What is the new salary?",
         "opts":["£48,375","£47,500","£49,000","£48,000"],"ans":0,
         "exp":"£45,000 × 1.075 = <strong>£48,375</strong>"},

        {"id":"N017","cat":"numerical","sub":"Ratios","diff":"hard",
         "text":"In a team of 35, the ratio of managers to analysts to engineers is 2:3:2. How many analysts are there?",
         "opts":["15","10","12","14"],"ans":0,
         "exp":"Total parts=7. Each part=35÷7=5. Analysts=3×5=<strong>15</strong>"},

        {"id":"N018","cat":"numerical","sub":"Algebra","diff":"medium",
         "text":"If 4x + 7 = 39, what is x?",
         "opts":["8","7","9","6"],"ans":0,
         "exp":"4x = 32 → x = <strong>8</strong>"},

        {"id":"N019","cat":"numerical","sub":"Finance","diff":"medium",
         "text":"VAT at 20% is added to a £320 item. What is the final price?",
         "opts":["£384","£380","£400","£370"],"ans":0,
         "exp":"£320 × 1.20 = <strong>£384</strong>"},

        {"id":"N020","cat":"numerical","sub":"Speed/Distance","diff":"hard",
         "text":"Two cars start 300 km apart, driving toward each other. Car A travels 80 km/h, Car B 70 km/h. In how many hours do they meet?",
         "opts":["2 hours","2.5 hours","3 hours","1.5 hours"],"ans":0,
         "exp":"Combined speed = 150 km/h. Time = 300÷150 = <strong>2 hours</strong>"},
    ]

    # ── VERBAL ────────────────────────────────────────
    cloud_passage = ("Cloud computing has revolutionised enterprise IT over the past decade. "
        "Organisations have shifted from capital-intensive on-premise data centres to operational "
        "expenditure models. This enables elastic scaling and managed services that would be "
        "prohibitively expensive to build internally. However, concerns persist around data sovereignty, "
        "vendor lock-in, and the environmental impact of energy-intensive data centres. "
        "GDPR has introduced complexity in cross-border data flows, forcing providers to invest "
        "in regional infrastructure and compliance certifications.")

    qe_passage = ("Quantitative easing (QE) implemented by central banks after the 2008 crisis "
        "expanded balance sheets to unprecedented levels. The Bank of England's asset purchases "
        "reached £895 billion by 2022. While QE stabilised financial markets and lowered borrowing "
        "costs, critics argue it exacerbated wealth inequality by inflating asset prices that "
        "disproportionately benefited existing asset holders. Transmission through financial markets "
        "rather than direct fiscal transfers meant households without significant portfolios saw "
        "limited direct benefit, while facing higher housing costs.")

    remote_passage = ("Remote work policies implemented during the pandemic have permanently altered "
        "workplace dynamics. Studies indicate hybrid models yield higher employee satisfaction while "
        "maintaining productivity. However, challenges include reduced spontaneous collaboration, "
        "difficulties onboarding junior staff, and blurred work-life boundaries. Organisations must "
        "balance individual flexibility with team cohesion and cultural transmission.")

    bank["verbal"] = [
        {"id":"V001","cat":"verbal","sub":"Comprehension","diff":"medium",
         "passage": cloud_passage,
         "text":"Cloud computing eliminates all IT infrastructure costs for organisations.",
         "opts":["True","False","Cannot Say"],"ans":1,
         "exp":"The passage describes a shift from capital to <em>operational</em> expenditure — costs still exist. <strong>False</strong>."},

        {"id":"V002","cat":"verbal","sub":"Comprehension","diff":"medium",
         "passage": cloud_passage,
         "text":"GDPR has required cloud providers to invest in regional infrastructure.",
         "opts":["True","False","Cannot Say"],"ans":0,
         "exp":"The passage explicitly states GDPR forced providers to invest in regional infrastructure. <strong>True</strong>."},

        {"id":"V003","cat":"verbal","sub":"Comprehension","diff":"hard",
         "passage": qe_passage,
         "text":"QE programs directly transferred money to all UK households equally.",
         "opts":["True","False","Cannot Say"],"ans":1,
         "exp":"The passage states transmission was through financial markets, not direct fiscal transfers, and benefits were disproportionate. <strong>False</strong>."},

        {"id":"V004","cat":"verbal","sub":"Comprehension","diff":"hard",
         "passage": qe_passage,
         "text":"The Bank of England's QE program exceeded £1 trillion.",
         "opts":["True","False","Cannot Say"],"ans":1,
         "exp":"The passage states £895 billion — less than £1 trillion. <strong>False</strong>."},

        {"id":"V005","cat":"verbal","sub":"Comprehension","diff":"medium",
         "passage": remote_passage,
         "text":"Hybrid work models consistently reduce productivity compared to full office attendance.",
         "opts":["True","False","Cannot Say"],"ans":1,
         "exp":"The passage says hybrid models maintain productivity (not reduce it). <strong>False</strong>."},

        {"id":"V006","cat":"verbal","sub":"Comprehension","diff":"medium",
         "passage": remote_passage,
         "text":"Onboarding junior staff is identified as a challenge of hybrid working.",
         "opts":["True","False","Cannot Say"],"ans":0,
         "exp":"Explicitly stated in the passage. <strong>True</strong>."},

        {"id":"V007","cat":"verbal","sub":"Synonym","diff":"medium",
         "text":"Choose the word most similar in meaning to: <strong>ABSTEMIOUS</strong>",
         "opts":["Temperate","Gluttonous","Extravagant","Loud"],"ans":0,
         "exp":"Abstemious = restrained in eating/drinking. Best synonym: <strong>Temperate</strong>."},

        {"id":"V008","cat":"verbal","sub":"Synonym","diff":"hard",
         "text":"Choose the word most similar in meaning to: <strong>ESCHEW</strong>",
         "opts":["Avoid","Pursue","Embrace","Welcome"],"ans":0,
         "exp":"Eschew = deliberately avoid. Synonym: <strong>Avoid</strong>."},

        {"id":"V009","cat":"verbal","sub":"Synonym","diff":"medium",
         "text":"Choose the word most similar in meaning to: <strong>PROPITIOUS</strong>",
         "opts":["Favourable","Unlucky","Hostile","Unpromising"],"ans":0,
         "exp":"Propitious = giving a good chance of success. Synonym: <strong>Favourable</strong>."},

        {"id":"V010","cat":"verbal","sub":"Synonym","diff":"medium",
         "text":"Choose the word most similar in meaning to: <strong>PRAGMATIC</strong>",
         "opts":["Practical","Idealistic","Theoretical","Impractical"],"ans":0,
         "exp":"Pragmatic = dealing with things sensibly and realistically. Synonym: <strong>Practical</strong>."},

        {"id":"V011","cat":"verbal","sub":"Synonym","diff":"hard",
         "text":"Choose the word most similar in meaning to: <strong>TACITURN</strong>",
         "opts":["Reserved","Talkative","Friendly","Outgoing"],"ans":0,
         "exp":"Taciturn = habitually silent. Synonym: <strong>Reserved</strong>."},

        {"id":"V012","cat":"verbal","sub":"Antonym","diff":"medium",
         "text":"Choose the word most <em>opposite</em> in meaning to: <strong>VENERATE</strong>",
         "opts":["Despise","Respect","Worship","Honour"],"ans":0,
         "exp":"Venerate = regard with great respect. Antonym: <strong>Despise</strong>."},

        {"id":"V013","cat":"verbal","sub":"Antonym","diff":"hard",
         "text":"Choose the word most <em>opposite</em> in meaning to: <strong>UBIQUITOUS</strong>",
         "opts":["Rare","Common","Widespread","Universal"],"ans":0,
         "exp":"Ubiquitous = present everywhere. Antonym: <strong>Rare</strong>."},

        {"id":"V014","cat":"verbal","sub":"Antonym","diff":"medium",
         "text":"Choose the word most <em>opposite</em> in meaning to: <strong>BENIGN</strong>",
         "opts":["Malignant","Harmless","Kind","Gentle"],"ans":0,
         "exp":"Benign = harmless. Antonym: <strong>Malignant</strong>."},

        {"id":"V015","cat":"verbal","sub":"Antonym","diff":"medium",
         "text":"Choose the word most <em>opposite</em> in meaning to: <strong>ZEALOUS</strong>",
         "opts":["Apathetic","Enthusiastic","Passionate","Fervent"],"ans":0,
         "exp":"Zealous = enthusiastic. Antonym: <strong>Apathetic</strong>."},

        {"id":"V016","cat":"verbal","sub":"Sentence Completion","diff":"medium",
         "text":"The CEO's _______ approach to risk management prevented the company from pursuing aggressive expansion.",
         "opts":["cautious","reckless","innovative","aggressive"],"ans":0,
         "exp":"'Prevented aggressive expansion' implies a <strong>cautious</strong> approach."},

        {"id":"V017","cat":"verbal","sub":"Sentence Completion","diff":"medium",
         "text":"Despite the project's complexity, the team managed to deliver it _______ ahead of schedule.",
         "opts":["impressively","poorly","barely","unsuccessfully"],"ans":0,
         "exp":"Positive outcome ('delivered ahead') pairs with <strong>impressively</strong>."},
    ]

    # ── LOGICAL ───────────────────────────────────────
    bank["logical"] = [
        {"id":"L001","cat":"logical","sub":"Number Sequence","diff":"easy",
         "text":"What comes next? &nbsp; 2, 5, 11, 23, 47, ___",
         "opts":["95","94","96","93"],"ans":0,
         "exp":"Rule: ×2 + 1. &nbsp; 47×2+1 = <strong>95</strong>"},

        {"id":"L002","cat":"logical","sub":"Letter Sequence","diff":"medium",
         "text":"What comes next? &nbsp; Z, X, V, T, R, ___",
         "opts":["P","Q","S","O"],"ans":0,
         "exp":"Skip one letter each time (−2). R(18)→<strong>P(16)</strong>"},

        {"id":"L003","cat":"logical","sub":"Number Sequence","diff":"easy",
         "text":"What comes next? &nbsp; 1, 4, 9, 16, 25, 36, ___",
         "opts":["49","48","50","47"],"ans":0,
         "exp":"Square numbers: 7² = <strong>49</strong>"},

        {"id":"L004","cat":"logical","sub":"Number Sequence","diff":"medium",
         "text":"What comes next? &nbsp; 3, 6, 12, 24, 48, ___",
         "opts":["96","72","64","108"],"ans":0,
         "exp":"Each term doubles: 48×2 = <strong>96</strong>"},

        {"id":"L005","cat":"logical","sub":"Number Sequence","diff":"medium",
         "text":"What comes next? &nbsp; 1, 1, 2, 3, 5, 8, 13, ___",
         "opts":["21","19","22","20"],"ans":0,
         "exp":"Fibonacci: 8+13 = <strong>21</strong>"},

        {"id":"L006","cat":"logical","sub":"Number Sequence","diff":"hard",
         "text":"What comes next? &nbsp; 2, 6, 12, 20, 30, ___",
         "opts":["42","40","44","38"],"ans":0,
         "exp":"n(n+1): 6×7 = <strong>42</strong>"},

        {"id":"L007","cat":"logical","sub":"Analogy","diff":"medium",
         "text":"Book : Read &nbsp;::&nbsp; Piano : ___",
         "opts":["Play","Listen","Write","Sing"],"ans":0,
         "exp":"You read a book; you <strong>play</strong> a piano."},

        {"id":"L008","cat":"logical","sub":"Analogy","diff":"hard",
         "text":"Carpenter : Wood &nbsp;::&nbsp; Mason : ___",
         "opts":["Stone","Clay","Metal","Concrete"],"ans":0,
         "exp":"A carpenter works with wood; a mason works with <strong>stone</strong>."},

        {"id":"L009","cat":"logical","sub":"Analogy","diff":"medium",
         "text":"Doctor : Patient &nbsp;::&nbsp; Teacher : ___",
         "opts":["Student","School","Book","Class"],"ans":0,
         "exp":"A doctor serves a patient; a teacher serves a <strong>student</strong>."},

        {"id":"L010","cat":"logical","sub":"Analogy","diff":"medium",
         "text":"Sheep : Flock &nbsp;::&nbsp; Wolf : ___",
         "opts":["Pack","Herd","School","Pride"],"ans":0,
         "exp":"Collective noun for wolves is a <strong>pack</strong>."},

        {"id":"L011","cat":"logical","sub":"Syllogism","diff":"hard",
         "text":"All managers are graduates. Some graduates are accountants. Therefore:",
         "opts":["Some managers may be accountants","All accountants are managers","No managers are accountants","All managers are accountants"],"ans":0,
         "exp":"The overlap between 'managers' and 'accountants' cannot be determined fully. <strong>Some managers may be accountants</strong> is the valid, cautious conclusion."},

        {"id":"L012","cat":"logical","sub":"Syllogism","diff":"medium",
         "text":"All team leaders hold PMP certification. James is a team leader. Therefore:",
         "opts":["James holds PMP certification","James may hold PMP certification","James does not hold PMP certification","Cannot be determined"],"ans":0,
         "exp":"Universal affirmative applied directly: <strong>James holds PMP certification</strong>."},

        {"id":"L013","cat":"logical","sub":"Diagrammatic Flow","diff":"medium",
         "text":"Input: 8 → [×3] → [−4] → [÷2] → Output = ?",
         "opts":["10","12","8","14"],"ans":0,
         "exp":"8×3=24 → 24−4=20 → 20÷2 = <strong>10</strong>"},

        {"id":"L014","cat":"logical","sub":"Diagrammatic Flow","diff":"medium",
         "text":"Input: 5 → [×2] → [+3] → [÷2] → Output = ?",
         "opts":["6.5","7","8","5.5"],"ans":0,
         "exp":"5×2=10 → 10+3=13 → 13÷2 = <strong>6.5</strong>"},

        {"id":"L015","cat":"logical","sub":"Code Pattern","diff":"hard",
         "text":"If KING = 11-9-14-7, what does QUEEN =?",
         "opts":["17-21-5-5-14","16-21-5-5-14","17-20-5-5-14","16-20-5-5-13"],"ans":0,
         "exp":"A=1, B=2…Z=26. Q=17, U=21, E=5, E=5, N=14 → <strong>17-21-5-5-14</strong>"},
    ]

    # ── MECHANICAL ────────────────────────────────────
    bank["mechanical"] = [
        {"id":"M001","cat":"mechanical","sub":"Gears","diff":"medium",
         "diagram": svg_gears(20, 40, 200),
         "text":"Gear A has 20 teeth and rotates at 200 RPM. It meshes with Gear B which has 40 teeth. What is Gear B's rotational speed?",
         "opts":["100 RPM","200 RPM","400 RPM","50 RPM"],"ans":0,
         "exp":"Gear ratio = 20:40 = 1:2. Speed of B = 200 ÷ 2 = <strong>100 RPM</strong> (larger gear = slower speed)"},

        {"id":"M002","cat":"mechanical","sub":"Levers","diff":"medium",
         "diagram": svg_lever(2, 4, 100),
         "text":"A lever has a 100N load positioned 2m from the fulcrum. The effort is applied 4m from the fulcrum. What effort is required to balance the load?",
         "opts":["50N","100N","25N","200N"],"ans":0,
         "exp":"Moments: Load × distance = Effort × distance → 100×2 = E×4 → E = <strong>50N</strong>"},

        {"id":"M003","cat":"mechanical","sub":"Hydraulics","diff":"hard",
         "diagram": svg_hydraulic(5, 25, 100),
         "text":"A hydraulic piston A has an area of 5 cm² and a force of 100N applied to it. Piston B has an area of 25 cm². What force does piston B exert?",
         "opts":["500N","100N","250N","50N"],"ans":0,
         "exp":"Pascal's Law: Pressure = F/A is constant. Pressure = 100/5 = 20 N/cm². Force B = 20 × 25 = <strong>500N</strong>"},

        {"id":"M004","cat":"mechanical","sub":"Fluid Flow","diff":"medium",
         "diagram": svg_pipe_flow(),
         "text":"Water flows at 2 m/s through a pipe. The pipe then narrows to half its cross-sectional area. What is the water's velocity in the narrow section?",
         "opts":["4 m/s","2 m/s","1 m/s","8 m/s"],"ans":0,
         "exp":"Continuity equation: A₁v₁ = A₂v₂. A × 2 = (A/2) × v → v = <strong>4 m/s</strong>"},

        {"id":"M005","cat":"mechanical","sub":"Pulleys","diff":"medium",
         "diagram": svg_pulley(4, 400),
         "text":"A pulley system has 4 ropes supporting a movable pulley. The load is 400N. What ideal effort force is needed?",
         "opts":["100N","200N","400N","50N"],"ans":0,
         "exp":"Mechanical advantage = number of supporting rope sections = 4. Effort = 400 ÷ 4 = <strong>100N</strong>"},

        {"id":"M006","cat":"mechanical","sub":"Gears","diff":"hard",
         "diagram": svg_gears(15, 45, 300),
         "text":"Gear A (15 teeth, 300 RPM) drives Gear B (45 teeth). What is Gear B's speed?",
         "opts":["100 RPM","150 RPM","200 RPM","300 RPM"],"ans":0,
         "exp":"Ratio 15:45 = 1:3. Speed B = 300 ÷ 3 = <strong>100 RPM</strong>"},

        {"id":"M007","cat":"mechanical","sub":"Levers","diff":"hard",
         "diagram": svg_lever(3, 6, 180),
         "text":"Load = 180N at 3m from fulcrum; effort applied at 6m from fulcrum. What effort is needed?",
         "opts":["90N","60N","120N","180N"],"ans":0,
         "exp":"180×3 = E×6 → E = 540÷6 = <strong>90N</strong>"},

        {"id":"M008","cat":"mechanical","sub":"Hydraulics","diff":"medium",
         "diagram": svg_hydraulic(10, 50, 200),
         "text":"Hydraulic piston A: area 10 cm², force 200N. Piston B: area 50 cm². What is the output force?",
         "opts":["1,000N","500N","2,000N","250N"],"ans":0,
         "exp":"Pressure = 200/10 = 20 N/cm². Output = 20 × 50 = <strong>1,000N</strong>"},
    ]

    # ── SPATIAL ───────────────────────────────────────
    bank["spatial"] = [
        {"id":"SP001","cat":"spatial","sub":"2D Rotation","diff":"medium",
         "diagram": svg_spatial_l_rotation(),
         "text":"An L-shaped piece (┗) is rotated 90° clockwise. Which shape does it become?",
         "opts":["┏ (top-left corner)","┛ (bottom-right corner)","┓ (top-right corner)","━ (horizontal bar)"],"ans":0,
         "exp":"Rotating ┗ by 90° clockwise gives <strong>┏</strong>. The foot of the L swings to become the top."},

        {"id":"SP002","cat":"spatial","sub":"Cube Nets","diff":"hard",
         "diagram": svg_cube_net(),
         "text":"The diagram shows a standard cross-shaped cube net. How many faces does a cube have?",
         "opts":["6","4","5","8"],"ans":0,
         "exp":"A cube always has exactly <strong>6 faces</strong> (top, bottom, front, back, left, right)."},

        {"id":"SP003","cat":"spatial","sub":"Cube Nets","diff":"hard",
         "diagram": svg_cube_net(),
         "text":"Which face is opposite the 'Front' face when this net is folded into a cube?",
         "opts":["Back","Top","Left","Right"],"ans":0,
         "exp":"In a standard cross net, Front and <strong>Back</strong> are opposite faces."},

        {"id":"SP004","cat":"spatial","sub":"Mirror Image","diff":"easy",
         "text":"The mirror image of the letter 'b' is:",
         "opts":["d","p","q","b"],"ans":0,
         "exp":"Reflecting 'b' horizontally gives <strong>'d'</strong>"},

        {"id":"SP005","cat":"spatial","sub":"Mirror Image","diff":"medium",
         "text":"The mirror image of the number '9' is:",
         "opts":["Reversed 9","6","9 unchanged","b"],"ans":0,
         "exp":"A horizontal mirror of '9' gives a <strong>reversed/flipped 9</strong> (like a backwards 9)."},

        {"id":"SP006","cat":"spatial","sub":"3D Rotation","diff":"hard",
         "diagram": svg_cube_rotation(),
         "text":"A cube has face 'A' on the front. After a 90° clockwise rotation (when viewed from above), where is face 'A'?",
         "opts":["On the right side","On the left side","On the back","On the top"],"ans":0,
         "exp":"Rotating 90° clockwise (top view) moves front face → <strong>right side</strong>."},

        {"id":"SP007","cat":"spatial","sub":"Cube Nets","diff":"hard",
         "diagram": svg_cube_net(),
         "text":"When the net is folded, which face is opposite 'Top'?",
         "opts":["Bottom","Front","Left","Right"],"ans":0,
         "exp":"In the cross net shown, Top and <strong>Bottom</strong> are directly opposite."},

        {"id":"SP008","cat":"spatial","sub":"2D Rotation","diff":"medium",
         "text":"The letter 'N' is rotated 180°. Which letter does it most resemble?",
         "opts":["N","Z","S","W"],"ans":0,
         "exp":"'N' rotated 180° still resembles <strong>N</strong> due to its rotational symmetry under 180°."},
    ]

    # ── ABSTRACT ──────────────────────────────────────
    bank["abstract"] = [
        {"id":"A001","cat":"abstract","sub":"Pattern Series","diff":"medium",
         "diagram": svg_abstract_matrix(),
         "text":"The matrix above shows patterns of circles (row 1) and squares (row 2). Looking at row 2: 1 green square, then 2 green squares — what completes the bottom-right cell?",
         "opts":["3 green squares + 1 grey","2 green squares","4 green squares","1 green + 2 grey"],"ans":0,
         "exp":"Row 2 adds one green square each cell (1→2→?). Pattern: <strong>3 green squares + 1 grey</strong>"},

        {"id":"A002","cat":"abstract","sub":"Pattern Series","diff":"easy",
         "text":"🔵 → 🔵🔵 → 🔵🔵🔵 → ? (What comes next?)",
         "opts":["🔵🔵🔵🔵","🔵🔵","🔵🔵🔵🔵🔵","🔵"],"ans":0,
         "exp":"Pattern adds one circle each step. Next = <strong>4 circles</strong>."},

        {"id":"A003","cat":"abstract","sub":"Rotation","diff":"medium",
         "text":"Arrow direction sequence: ➡️ → ↘️ → ⬇️ → ↙️ → ⬅️ → ? (continuing clockwise rotation of 45° each step)",
         "opts":["↖️","⬆️","↗️","➡️"],"ans":0,
         "exp":"Rotating 45° clockwise: ⬅️ → <strong>↖️</strong>"},

        {"id":"A004","cat":"abstract","sub":"Odd One Out","diff":"medium",
         "text":"Which does not belong? &nbsp; △ &nbsp; ○ &nbsp; ▷ &nbsp; ◇ &nbsp; ★",
         "opts":["★ (has 5 sides/points unlike the others)","○","△","▷"],"ans":0,
         "exp":"All others are simple geometric shapes (triangle, circle, arrow, diamond). ★ is a <strong>complex star shape</strong> — it doesn't belong."},

        {"id":"A005","cat":"abstract","sub":"Pattern Series","diff":"hard",
         "text":"Shape sides: △(3) → ◇(4) → ⬠(5) → ⬡(6) → ?",
         "opts":["Heptagon (7 sides)","Circle","Square","Pentagon"],"ans":0,
         "exp":"Each shape adds one side: 3→4→5→6→<strong>7 (heptagon)</strong>"},

        {"id":"A006","cat":"abstract","sub":"Matrix Pattern","diff":"hard",
         "text":"""Matrix (each row, shapes rotate 90° clockwise):
Row 1: ▶ | ▼ | ◀
Row 2: ▶ | ▼ | ?""",
         "opts":["◀","▲","▶","▼"],"ans":0,
         "exp":"Row 2 follows same 90° CW rotation: ▶→▼→<strong>◀</strong>"},
    ]

    # ── SJT ───────────────────────────────────────────
    bank["sjt"] = [
        {"id":"S001","cat":"sjt","sub":"Workplace Conflict","diff":"medium",
         "text":"You notice a colleague consistently arriving 30 minutes late, affecting team deadlines. What do you do first?",
         "opts":["Speak privately with them to understand the situation","Report them to HR immediately","Tell other team members","Ignore it — not your responsibility"],"ans":0,
         "exp":"<strong>Speak privately first.</strong> Direct, empathetic communication before escalation is always the professional approach."},

        {"id":"S002","cat":"sjt","sub":"Client Pressure","diff":"hard",
         "text":"A major client demands a feature requiring you to bypass security protocols. Your manager is on leave. What do you do?",
         "opts":["Explain security risks and propose compliant alternatives","Implement it to keep the client happy","Refuse all contact with the client","Wait for manager to return without responding"],"ans":0,
         "exp":"<strong>Explain risks and propose alternatives.</strong> Integrity and client service are not mutually exclusive."},

        {"id":"S003","cat":"sjt","sub":"Team Leadership","diff":"medium",
         "text":"Two team members have incompatible but both valid approaches to a project. As project lead, you should:",
         "opts":["Facilitate a discussion to find an integrated solution","Choose one approach arbitrarily","Split the team to pursue both","Escalate to senior management immediately"],"ans":0,
         "exp":"<strong>Facilitate discussion.</strong> Collaborative problem-solving is a core leadership competency."},

        {"id":"S004","cat":"sjt","sub":"Ethics","diff":"hard",
         "text":"You discover a minor error in a report already sent to a client. It doesn't affect the conclusions. You should:",
         "opts":["Notify client promptly with corrected information","Say nothing — conclusions are unaffected","Wait to see if client notices","Mark it as a system error"],"ans":0,
         "exp":"<strong>Notify client promptly.</strong> Transparency and honesty build long-term trust even when errors are minor."},

        {"id":"S005","cat":"sjt","sub":"Workload","diff":"medium",
         "text":"You are overwhelmed with deadlines and one task will clearly be late. Best action?",
         "opts":["Proactively discuss priorities and timeline with your manager","Work overtime without telling anyone","Miss the deadline and explain afterwards","Delegate to a colleague without telling them why"],"ans":0,
         "exp":"<strong>Proactive communication with manager</strong> enables informed decisions about priorities."},

        {"id":"S006","cat":"sjt","sub":"Disagreement","diff":"medium",
         "text":"You genuinely believe your manager has made a poor strategic decision. You should:",
         "opts":["Request a private meeting and present your concerns with evidence","Post your concerns in a team channel","Complain to HR","Comply without comment"],"ans":0,
         "exp":"<strong>Private meeting with evidence.</strong> Professional challenge is appropriate when done respectfully and constructively."},

        {"id":"S007","cat":"sjt","sub":"Credit","diff":"medium",
         "text":"A colleague presents your idea to senior leadership without crediting you. First step?",
         "opts":["Speak with your colleague privately and calmly","Interrupt the presentation to claim credit","Email your manager immediately","Say nothing and accept it"],"ans":0,
         "exp":"<strong>Private, calm conversation first.</strong> It may have been unintentional; escalation should follow only if needed."},

        {"id":"S008","cat":"sjt","sub":"New Information","diff":"hard",
         "text":"Midway through a project, you discover data suggesting the approach may not achieve the intended outcome. You should:",
         "opts":["Flag it immediately to stakeholders with evidence and options","Continue anyway — too late to change","Delete the contradictory data","Wait until the project ends before raising it"],"ans":0,
         "exp":"<strong>Flag immediately.</strong> Early transparency allows course correction. Hiding issues leads to much larger failures."},
    ]

    # ── WATSON-GLASER ─────────────────────────────────
    wg_passage1 = ("A study found 70% of Fortune 500 companies offer flexible working. "
        "Employee satisfaction at these companies averages 15% above industry norms. "
        "However, 40% of managers report difficulty coordinating team activities.")

    wg_passage2 = ("Research across 12 countries shows remote workers are 13% more productive "
        "and 68% report higher satisfaction. However, 25% feel isolated, and junior employees "
        "show slower career development compared to office-based peers.")

    bank["watson_glaser"] = [
        {"id":"W001","cat":"watson_glaser","sub":"Inference","diff":"hard",
         "passage": wg_passage1,
         "text":"Flexible working <em>always</em> improves company performance.",
         "opts":["True","Probably True","Insufficient Data","Probably False","False"],"ans":4,
         "exp":"The passage notes coordination difficulties and does not establish universal improvement. 'Always' is too absolute. <strong>False</strong>."},

        {"id":"W002","cat":"watson_glaser","sub":"Inference","diff":"medium",
         "passage": wg_passage1,
         "text":"Some managers find flexible work arrangements challenging to manage.",
         "opts":["True","Probably True","Insufficient Data","Probably False","False"],"ans":0,
         "exp":"40% of managers report coordination difficulty — this is directly stated. <strong>True</strong>."},

        {"id":"W003","cat":"watson_glaser","sub":"Inference","diff":"hard",
         "passage": wg_passage2,
         "text":"Remote work benefits all employees equally.",
         "opts":["True","Probably True","Insufficient Data","Probably False","False"],"ans":4,
         "exp":"25% feel isolated and junior employees develop more slowly — clearly not equal benefit. <strong>False</strong>."},

        {"id":"W004","cat":"watson_glaser","sub":"Inference","diff":"medium",
         "passage": wg_passage2,
         "text":"Remote workers report higher job satisfaction on average.",
         "opts":["True","Probably True","Insufficient Data","Probably False","False"],"ans":0,
         "exp":"68% report higher satisfaction — directly stated. <strong>True</strong>."},

        {"id":"W005","cat":"watson_glaser","sub":"Assumption","diff":"hard",
         "text":"Statement: 'We should invest in AI training for all staff to remain competitive.'\n\nWhich assumption is made?",
         "opts":["AI skills will be essential across all roles","AI training is inexpensive","Most staff already have some AI skills","Competitors are not investing in AI"],"ans":0,
         "exp":"Recommending training for <em>all staff</em> assumes AI will be relevant to all roles. <strong>AI skills will be essential across all roles</strong>."},

        {"id":"W006","cat":"watson_glaser","sub":"Deduction","diff":"medium",
         "text":"Premises: All team leaders must have PMP certification. Sarah is a team leader.\n\nConclusion: Sarah has PMP certification.",
         "opts":["Conclusion follows","Conclusion does not follow"],"ans":0,
         "exp":"Direct syllogistic deduction: All TLs → PMP. Sarah is TL. Therefore Sarah has PMP. <strong>Conclusion follows</strong>."},

        {"id":"W007","cat":"watson_glaser","sub":"Evaluation of Arguments","diff":"medium",
         "text":"Question: Should companies ban social media during work hours?\n\nArgument: No — employees need breaks to maintain productivity.",
         "opts":["Strong argument","Weak argument"],"ans":1,
         "exp":"The argument conflates <em>work hours</em> with <em>break times</em> and doesn't address the core question. <strong>Weak argument</strong>."},

        {"id":"W008","cat":"watson_glaser","sub":"Evaluation of Arguments","diff":"hard",
         "text":"Question: Should graduate recruitment use blind CV screening?\n\nArgument: Yes — removing names and university names reduces unconscious bias and creates more meritocratic outcomes.",
         "opts":["Strong argument","Weak argument"],"ans":0,
         "exp":"The argument is directly relevant, specific, and evidence-based. <strong>Strong argument</strong>."},
    ]

    # ── IQ & APTITUDE ─────────────────────────────────
    bank["iq"] = [
        {"id":"I001","cat":"iq","sub":"Number Pattern","diff":"medium",
         "text":"What replaces the ? &nbsp; 2, 6, 12, 20, 30, ?",
         "opts":["42","40","44","36"],"ans":0,
         "exp":"Pattern n(n+1): 1×2=2, 2×3=6…6×7=<strong>42</strong>"},

        {"id":"I002","cat":"iq","sub":"Odd One Out","diff":"easy",
         "text":"Which does not belong? &nbsp; Apple, Banana, Carrot, Cherry",
         "opts":["Carrot","Apple","Banana","Cherry"],"ans":0,
         "exp":"<strong>Carrot</strong> is a vegetable; the others are fruits."},

        {"id":"I003","cat":"iq","sub":"Logic","diff":"hard",
         "text":"All Bloops are Razzies. All Razzies are Lazzies. Are all Bloops definitely Lazzies?",
         "opts":["Yes","No","Cannot tell","Only some"],"ans":0,
         "exp":"Transitive: Bloops→Razzies→Lazzies. All Bloops are Lazzies. <strong>Yes</strong>."},

        {"id":"I004","cat":"iq","sub":"Trick Calculation","diff":"medium",
         "text":"A bat and a ball cost £11 in total. The bat costs £10 more than the ball. How much is the ball?",
         "opts":["50p","£1.00","£1.50","£0.10"],"ans":0,
         "exp":"Let ball = x. Bat = x+10. x+(x+10)=11 → 2x=1 → x=<strong>50p</strong>"},

        {"id":"I005","cat":"iq","sub":"Sequence","diff":"medium",
         "text":"What comes next in this sequence? &nbsp; J, F, M, A, M, ?",
         "opts":["J","A","S","O"],"ans":0,
         "exp":"Initial letters of months: Jan, Feb, Mar, Apr, May → <strong>J</strong>une"},

        {"id":"I006","cat":"iq","sub":"Lateral Thinking","diff":"hard",
         "text":"I am lighter than a feather but the strongest person cannot hold me for more than a few minutes. What am I?",
         "opts":["Breath","Thought","Shadow","Sound"],"ans":0,
         "exp":"You cannot hold your <strong>breath</strong> indefinitely."},

        {"id":"I007","cat":"iq","sub":"Number Pattern","diff":"hard",
         "text":"If 2+3=25, 4+5=41, 6+7=85, then 8+9=?",
         "opts":["145","130","160","120"],"ans":0,
         "exp":"Pattern: (a²)+(b²). 2²+3²=4+9=13… Hmm. Try a+b=sum, product + sum²: 8+9=17, 72=product; 17²=289… Let's verify pattern: (a+b)²−a×b: 5²−6=19 ≠ 25. Correct pattern here is a²+b²+... recalculate: actually 2²+3²=13, ×2=26−1=25✓. 4²+5²=41✓. 6²+7²=85✓. 8²+9²=64+81=<strong>145</strong>"},

        {"id":"I008","cat":"iq","sub":"Spatial Logic","diff":"medium",
         "text":"You have 3 boxes: one contains only apples, one only oranges, one mixed. All labels are wrong. You pick one fruit from one box. What is the minimum draws to correctly label all boxes?",
         "opts":["1","2","3","Cannot be done"],"ans":0,
         "exp":"Draw from 'Mixed' box (label is wrong, so it's pure). That one fruit reveals its content. The other two boxes can then be logically deduced. <strong>1 draw</strong>."},
    ]

    # ── ERROR CHECKING ────────────────────────────────
    bank["error_checking"] = [
        {"id":"E001","cat":"error_checking","sub":"Data Checking","diff":"easy",
         "text":"Compare these two references:<br><code>ACME Corp, 123 Main St, London, EC1A 1BB</code><br><code>ACME Corp, 123 Main St, London, EC1A 1BB</code><br>Are there any errors?",
         "opts":["No errors — identical","Postcode error","Street number error","Company name error"],"ans":0,
         "exp":"The strings are <strong>identical</strong> — no errors."},

        {"id":"E002","cat":"error_checking","sub":"Data Checking","diff":"medium",
         "text":"Compare these reference numbers:<br><code>Ref: 883921-A</code><br><code>Ref: 883912-A</code><br>What type of error exists?",
         "opts":["Transposed digits (21 vs 12)","Missing digit","Extra character","Letter error"],"ans":0,
         "exp":"Digits '21' and '12' are transposed. <strong>Transposed digits</strong>."},

        {"id":"E003","cat":"error_checking","sub":"Data Checking","diff":"medium",
         "text":"Compare:<br><code>Invoice: £14,750.00 — Date: 14/03/2024</code><br><code>Invoice: £14,570.00 — Date: 14/03/2024</code><br>What is wrong?",
         "opts":["Amount error (£14,750 vs £14,570)","Date error","Both correct","Currency symbol error"],"ans":0,
         "exp":"£14,750 ≠ £14,570. The <strong>amount differs by £180</strong> — transposed digits in hundreds column."},

        {"id":"E004","cat":"error_checking","sub":"Data Checking","diff":"hard",
         "text":"Compare these account numbers:<br><code>ACC-2024-00847-X</code><br><code>ACC-2024-00874-X</code><br>What error is present?",
         "opts":["Transposed digits in sequence (847 vs 874)","Letter code error","Year error","No error"],"ans":0,
         "exp":"847 vs 874 — digits 4 and 7 are transposed. <strong>Transposed digits</strong>."},
    ]

    # ── CRITICAL THINKING ─────────────────────────────
    bank["critical"] = [
        {"id":"C001","cat":"critical","sub":"Analysis","diff":"hard",
         "text":"A survey shows 80% of CEOs believe AI will transform their industry within 5 years. Does this prove AI will definitely transform all industries?",
         "opts":["No — belief is not the same as evidence or guaranteed outcome","Yes — CEOs are domain experts","Yes — 80% is a strong majority","Cannot determine"],"ans":0,
         "exp":"<strong>No.</strong> CEO beliefs are predictions, not facts. Surveys of opinion cannot establish future certainty."},

        {"id":"C002","cat":"critical","sub":"Causation vs Correlation","diff":"hard",
         "text":"A study finds that cities with more libraries have lower crime rates. A politician concludes: 'Building more libraries reduces crime.' What is wrong with this conclusion?",
         "opts":["Confusing correlation with causation — a third factor (e.g. wealth) likely explains both","Nothing — the data clearly supports it","The sample size is too small","Libraries are irrelevant to crime"],"ans":0,
         "exp":"<strong>Correlation ≠ causation.</strong> Wealthier cities tend to have both more libraries and lower crime — the libraries may not be the causal factor."},

        {"id":"C003","cat":"critical","sub":"Logical Fallacy","diff":"medium",
         "text":"'Our product has been used for 50 years, so it must be safe and effective.' This argument commits which fallacy?",
         "opts":["Appeal to tradition / age","Ad hominem","False dilemma","Slippery slope"],"ans":0,
         "exp":"Longevity alone does not prove safety or efficacy. This is the <strong>appeal to tradition</strong> fallacy."},
    ]

    return bank


@st.cache_data
def get_question_bank():
    return build_question_bank()


BANK = get_question_bank()

CATEGORIES = {
    "numerical":      ("Numerical Reasoning",       "📊", "Percentages, ratios, data tables, finance"),
    "verbal":         ("Verbal Reasoning",           "📖", "Comprehension, synonyms, antonyms, T/F/CS"),
    "logical":        ("Logical Reasoning",          "🔷", "Sequences, analogies, syllogisms, flow"),
    "mechanical":     ("Mechanical Reasoning",       "⚙️", "Gears, levers, hydraulics, pulleys (with diagrams)"),
    "spatial":        ("Spatial Reasoning",          "📐", "Cube nets, rotations, mirror images (with diagrams)"),
    "abstract":       ("Abstract Reasoning",         "🔺", "Matrix patterns, shape series, rotations"),
    "watson_glaser":  ("Watson-Glaser",              "🎯", "Inference, assumption, deduction, evaluation"),
    "sjt":            ("Situational Judgement",      "🤝", "Workplace scenarios, ethics, leadership"),
    "iq":             ("IQ & Aptitude",              "🧩", "Logic puzzles, lateral thinking, patterns"),
    "error_checking": ("Error Checking",             "🔍", "Spot differences in data, codes, figures"),
    "critical":       ("Critical Thinking",          "💡", "Fallacies, causation, argument evaluation"),
}

TAG_CLASSES = {
    "numerical":"q-tag-num","verbal":"q-tag-verb","logical":"q-tag-log",
    "mechanical":"q-tag-mech","spatial":"q-tag-sp","abstract":"q-tag-abs",
    "watson_glaser":"q-tag-wg","sjt":"q-tag-sjt","iq":"q-tag-iq",
    "error_checking":"q-tag-err","critical":"q-tag-cr","diagrammatic":"q-tag-diag",
}

# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════

def init_state():
    defaults = {
        "page": "home",
        "test_history": [],
        "current_test": None,
        "selected_cat": None,
        "answers": {},
        "flagged": set(),
        "current_q": 0,
        "time_remaining": 3000,
        "test_start": None,
        "last_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ═══════════════════════════════════════════════════════
# HEADER (rendered on every page)
# ═══════════════════════════════════════════════════════

def render_header():
    st.markdown("""
    <div class="app-header">
        <div>
            <div class="app-header-title">Aptitude<span>Pro</span></div>
            <div class="app-header-sub">Graduate Psychometric Test Suite</div>
        </div>
        <div class="header-badges">
            <span class="badge">SHL</span>
            <span class="badge">Kenexa</span>
            <span class="badge">Cubiks</span>
            <span class="badge">Watson-Glaser</span>
            <span class="badge">CEB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# NAV BAR
# ═══════════════════════════════════════════════════════

def render_nav():
    if st.session_state.page == "active_test":
        return  # No nav during active test

    cols = st.columns(5)
    pages = [
        ("🏠 Home", "home"),
        ("📝 Practice Tests", "tests"),
        ("📈 Analytics", "analytics"),
        ("ℹ️ Guide", "guide"),
    ]
    with cols[0]:
        st.write("")  # spacer
    for col, (label, pg) in zip(cols[1:], pages):
        with col:
            is_active = st.session_state.page == pg
            if st.button(label, key=f"nav_{pg}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.page = pg
                st.rerun()

# ═══════════════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════════════

def render_home():
    history = st.session_state.test_history

    # Stats
    total_tests = len(history)
    avg_score = round(sum(t["score"] for t in history) / total_tests) if history else 0
    best_score = max(t["score"] for t in history) if history else 0
    total_qs = sum(t["total_q"] for t in history)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, label, val in [
        (c1,"📝","Tests Completed", total_tests),
        (c2,"📊","Average Score", f"{avg_score}%" if history else "—"),
        (c3,"🏆","Best Score", f"{best_score}%" if history else "—"),
        (c4,"❓","Questions Answered", total_qs),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-label">{label}</div>
                <div class="stat-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    # ── FULL BLEND TEST (featured) ──────────────────
    st.markdown('<div class="section-title">⚡ Featured</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="blend-card">
        <div class="blend-title">Full Graduate Aptitude Test — All Types Blended</div>
        <div class="blend-subtitle">The most realistic test experience: 60 questions drawn from all 11 categories, just like real employer assessments from SHL, Kenexa, and Cubiks.</div>
        <div class="blend-chips">
            <span class="blend-chip">Numerical</span>
            <span class="blend-chip">Verbal</span>
            <span class="blend-chip">Logical</span>
            <span class="blend-chip">Mechanical</span>
            <span class="blend-chip">Spatial</span>
            <span class="blend-chip">Abstract</span>
            <span class="blend-chip">Watson-Glaser</span>
            <span class="blend-chip">SJT</span>
            <span class="blend-chip">IQ</span>
            <span class="blend-chip">Error Checking</span>
            <span class="blend-chip">Critical Thinking</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Full Blended Test (60 Questions · 50 min)", type="primary", use_container_width=True):
        start_test("BLEND")

    st.markdown('<div class="section-title">📚 Practice by Category</div>', unsafe_allow_html=True)

    # Category grid 3 columns
    cat_keys = list(CATEGORIES.keys())
    rows = [cat_keys[i:i+3] for i in range(0, len(cat_keys), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, key in zip(cols, row):
            name, icon, desc = CATEGORIES[key]
            cat_hist = [t for t in history if t["category"] == key]
            best = max((t["score"] for t in cat_hist), default=None)
            badge_html = ""
            if best is not None:
                cls = "badge-green" if best >= 70 else "badge-yellow" if best >= 50 else "badge-red"
                badge_html = f'<span class="cat-badge {cls}">Best: {best}%</span>'
            with col:
                st.markdown(f"""
                <div class="cat-card">
                    <div class="cat-icon">{icon}</div>
                    <div class="cat-name">{name}</div>
                    <div class="cat-desc">{desc}</div>
                    {badge_html}
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Start {name}", key=f"start_{key}", use_container_width=True):
                    start_test(key)

# ═══════════════════════════════════════════════════════
# TEST LOGIC
# ═══════════════════════════════════════════════════════

def build_blended_test(n=60):
    all_qs = []
    for qs in BANK.values():
        all_qs.extend(qs)
    random.shuffle(all_qs)
    return all_qs[:n]


def start_test(category: str):
    if category == "BLEND":
        questions = build_blended_test(60)
    else:
        pool = BANK.get(category, [])
        n = min(len(pool), 60)
        questions = random.sample(pool, n)

    st.session_state.current_test = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "category": category,
        "questions": questions,
    }
    st.session_state.answers = {}
    st.session_state.flagged = set()
    st.session_state.current_q = 0
    st.session_state.time_remaining = 50 * 60
    st.session_state.test_start = time.time()
    st.session_state.page = "active_test"
    st.rerun()

# ═══════════════════════════════════════════════════════
# ACTIVE TEST PAGE
# ═══════════════════════════════════════════════════════

def render_active_test():
    test = st.session_state.current_test
    if not test:
        st.session_state.page = "home"
        st.rerun()
        return

    questions = test["questions"]
    n = len(questions)
    q_idx = st.session_state.current_q

    # Update timer
    elapsed = int(time.time() - st.session_state.test_start)
    remaining = max(0, 50 * 60 - elapsed)
    st.session_state.time_remaining = remaining

    if remaining <= 0:
        submit_test()
        return

    mins, secs = divmod(remaining, 60)
    timer_cls = "timer-display"
    if remaining < 300: timer_cls += " timer-warn"
    if remaining < 60:  timer_cls += " timer-danger"

    question = questions[q_idx]
    cat = question.get("cat", "numerical")
    sub = question.get("sub", "")
    diff = question.get("diff", "medium")

    # ── TOP ROW ──────────────────────────────────────
    r1c1, r1c2, r1c3 = st.columns([3, 2, 2])
    with r1c1:
        render_header()
    with r1c2:
        st.markdown(f'<div class="{timer_cls}">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        answered = len(st.session_state.answers)
        st.markdown(f"""
        <div class="prog-bar-wrap" style="margin-top:0.5rem;">
            <div class="prog-bar-fill" style="width:{answered/n*100:.0f}%"></div>
        </div>
        <div style="text-align:center;font-size:0.75rem;color:#6b7280;margin-top:0.25rem;">{answered}/{n} answered</div>
        """, unsafe_allow_html=True)
    with r1c3:
        st.write("")
        if st.button("🏁 Submit Test", type="primary", use_container_width=True):
            submit_test()
            return
        flag_label = "🚩 Flagged" if q_idx in st.session_state.flagged else "⚑ Flag Question"
        if st.button(flag_label, use_container_width=True):
            if q_idx in st.session_state.flagged:
                st.session_state.flagged.discard(q_idx)
            else:
                st.session_state.flagged.add(q_idx)
            st.rerun()

    # ── Q NAVIGATOR ──────────────────────────────────
    dots = ""
    for i in range(n):
        cls = "q-nav-dot"
        if i in st.session_state.answers:   cls += " q-nav-answered"
        if i == q_idx:                       cls += " q-nav-current"
        if i in st.session_state.flagged:   cls += " q-nav-flagged"
        dots += f'<span class="{cls}">{i+1}</span>'
    st.markdown(f'<div class="q-nav-wrap">{dots}</div>', unsafe_allow_html=True)

    # ── QUESTION CARD ─────────────────────────────────
    tag_cls = TAG_CLASSES.get(cat, "q-tag-num")
    diff_cls = f"q-difficulty-{diff}"

    with st.container():
        st.markdown(f"""
        <div class="q-header">
            <div class="q-meta">
                <span class="q-tag {tag_cls}">{CATEGORIES.get(cat,(cat,'',''))[0] if cat in CATEGORIES else cat.replace('_',' ').title()}</span>
                <span class="q-tag {tag_cls}" style="opacity:0.8">{sub}</span>
                <span class="q-tag {diff_cls}">{diff.capitalize()}</span>
                <span style="margin-left:auto;font-size:0.8rem;color:#6b7280;font-weight:500;">Q{q_idx+1} of {n}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Passage
        if "passage" in question and question["passage"]:
            with st.expander("📖 Read Passage", expanded=True):
                st.markdown(f'<div class="passage-box">{question["passage"]}</div>', unsafe_allow_html=True)

        # Diagram
        if "diagram" in question and question["diagram"]:
            st.markdown(f'<div class="diagram-box">{question["diagram"]}</div>', unsafe_allow_html=True)

        # Question text
        st.markdown(f'<div class="q-text">{question["text"]}</div>', unsafe_allow_html=True)
        st.write("")

        # ── ANSWER OPTIONS ─────────────────────────────
        current_ans = st.session_state.answers.get(q_idx)

        for i, opt in enumerate(question["opts"]):
            label = chr(65 + i)
            is_selected = current_ans == i
            style = "opt-selected" if is_selected else ""
            # Render styled HTML button via Streamlit button
            btn_label = f"**{label}.** {opt}" if is_selected else f"{label}. {opt}"
            if st.button(btn_label, key=f"opt_{q_idx}_{i}", use_container_width=True,
                         type="primary" if is_selected else "secondary"):
                st.session_state.answers[q_idx] = i
                st.rerun()

    # ── NAV BUTTONS ─────────────────────────────────
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
    nc1, nc2, nc3 = st.columns([1, 2, 1])
    with nc1:
        if q_idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()
    with nc3:
        if q_idx < n - 1:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("Finish ✓", type="primary", use_container_width=True):
                submit_test()
                return

    # Auto-refresh for timer
    time.sleep(0.05)
    st.rerun()

# ═══════════════════════════════════════════════════════
# SUBMIT & RESULTS
# ═══════════════════════════════════════════════════════

def submit_test():
    test = st.session_state.current_test
    if not test:
        return

    questions = test["questions"]
    n = len(questions)
    correct = wrong = unanswered = 0

    for i, q in enumerate(questions):
        ua = st.session_state.answers.get(i)
        if ua is None:
            unanswered += 1
        elif ua == q["ans"]:
            correct += 1
        else:
            wrong += 1

    time_taken = int(time.time() - st.session_state.test_start)
    score = round(correct / n * 100)

    result = {
        "id": test["id"],
        "category": test["category"],
        "score": score,
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "total_q": n,
        "date": datetime.now().isoformat(),
        "time_taken": time_taken,
        "answers": dict(st.session_state.answers),
        "questions": questions,
    }

    st.session_state.test_history.append(result)
    st.session_state.last_result = result
    st.session_state.current_test = None
    st.session_state.page = "results"
    st.rerun()


def get_grade(score):
    if score >= 90: return ("🏆 Outstanding", "#059669", "Top 5% — Excellent candidacy")
    if score >= 80: return ("⭐ Excellent",    "#0d9488", "Top 15% — Strong performance")
    if score >= 70: return ("✅ Good",          "#2563eb", "Above average — Well placed")
    if score >= 60: return ("📈 Satisfactory",  "#7c3aed", "Average — More practice recommended")
    if score >= 50: return ("⚠️ Below Average", "#b45309", "Below average — Focus on weak areas")
    return ("📚 Needs Work", "#dc2626", "Significant practice needed")


def render_results():
    result = st.session_state.last_result
    if not result:
        st.session_state.page = "home"
        st.rerun()
        return

    render_header()
    render_nav()

    grade, color, detail = get_grade(result["score"])
    cat_name = "Full Blended Test" if result["category"] == "BLEND" else CATEGORIES.get(result["category"], (result["category"],))[0]

    st.markdown(f"""
    <div class="result-hero">
        <div style="font-size:0.85rem;opacity:0.65;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.1em;">{cat_name}</div>
        <div class="result-score">{result['score']}%</div>
        <div class="result-grade" style="color:{color};">{grade}</div>
        <div style="color:rgba(255,255,255,0.55);font-size:0.85rem;margin-top:0.25rem;">{detail}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, clr in [
        (c1, result["correct"],   "✅ Correct",    "#059669"),
        (c2, result["wrong"],     "❌ Incorrect",  "#dc2626"),
        (c3, result["unanswered"],"⚪ Unanswered", "#6b7280"),
        (c4, f"{result['time_taken']//60}m {result['time_taken']%60}s", "⏱ Time Used", "#f59e0b"),
    ]:
        with col:
            st.markdown(f"""
            <div class="result-stat">
                <div class="result-stat-val" style="color:{clr};">{val}</div>
                <div class="result-stat-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    # ── ACTION BUTTONS ──────────────────────────────
    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        if st.button("🔄 Retake This Test", type="primary", use_container_width=True):
            start_test(result["category"])
    with bc2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with bc3:
        if st.button("📈 View Analytics", use_container_width=True):
            st.session_state.page = "analytics"
            st.rerun()

    # ── REVIEW ANSWERS ──────────────────────────────
    st.markdown('<div class="section-title">📋 Review Your Answers</div>', unsafe_allow_html=True)

    for i, q in enumerate(result["questions"]):
        ua = result["answers"].get(i)
        ca = q["ans"]
        status = "✅" if ua == ca else "❌" if ua is not None else "⚪"

        with st.expander(f"{status} Q{i+1}: {str(q['text'])[:80].replace('<br>','').replace('<strong>','').replace('</strong>','')}…"):

            if "passage" in q and q["passage"]:
                st.markdown(f'<div class="passage-box">{q["passage"]}</div>', unsafe_allow_html=True)

            if "diagram" in q and q["diagram"]:
                st.markdown(f'<div class="diagram-box">{q["diagram"]}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="q-text" style="margin-bottom:0.75rem;">{q["text"]}</div>', unsafe_allow_html=True)

            for j, opt in enumerate(q["opts"]):
                if j == ca:
                    st.markdown(f'<div class="opt-btn opt-correct">✅ {chr(65+j)}. {opt} — Correct answer</div>', unsafe_allow_html=True)
                elif j == ua and j != ca:
                    st.markdown(f'<div class="opt-btn opt-wrong">❌ {chr(65+j)}. {opt} — Your answer</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="opt-btn">{chr(65+j)}. {opt}</div>', unsafe_allow_html=True)

            if ua is None:
                st.markdown('<div style="color:#6b7280;font-size:0.85rem;padding:0.5rem 0;">⚪ Not answered</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="exp-box"><strong>💡 Explanation:</strong><br>{q["exp"]}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# ANALYTICS
# ═══════════════════════════════════════════════════════

def render_analytics():
    st.markdown('<div class="section-title">📈 Performance Analytics</div>', unsafe_allow_html=True)
    history = st.session_state.test_history

    if not history:
        st.markdown('<div class="info-box">Complete some tests to see your analytics here.</div>', unsafe_allow_html=True)
        if st.button("Start a Test", type="primary"):
            st.session_state.page = "home"
            st.rerun()
        return

    # Score trend
    df = pd.DataFrame([
        {"Test": i+1, "Score": t["score"],
         "Category": "Full Blend" if t["category"]=="BLEND" else CATEGORIES.get(t["category"], (t["category"],))[0]}
        for i, t in enumerate(history[-15:])
    ])
    fig = px.line(df, x="Test", y="Score", color="Category", markers=True,
                  range_y=[0, 100], title="Score Trend (last 15 tests)",
                  color_discrete_sequence=["#1a56db","#0d9488","#f59e0b","#dc2626","#7c3aed"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                      yaxis_gridcolor="#e5e7eb", font_family="Inter")
    st.plotly_chart(fig, use_container_width=True)

    # Category bar
    cat_scores = defaultdict(list)
    for t in history:
        cat_scores[t["category"]].append(t["score"])
    rows = [{"Category": "Full Blend" if k=="BLEND" else CATEGORIES.get(k,(k,))[0],
             "Average": round(sum(v)/len(v), 1), "Tests": len(v)}
            for k, v in cat_scores.items()]
    df2 = pd.DataFrame(rows)
    fig2 = px.bar(df2, x="Category", y="Average", color="Tests",
                  text="Average", range_y=[0,100],
                  color_continuous_scale="Blues", title="Average Score by Category")
    fig2.update_traces(texttemplate="%{text}%", textposition="outside")
    fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                       yaxis_gridcolor="#e5e7eb", font_family="Inter")
    st.plotly_chart(fig2, use_container_width=True)

    # Table
    st.markdown('<div class="section-title">📋 Recent Tests</div>', unsafe_allow_html=True)
    tbl = pd.DataFrame([{
        "Date": datetime.fromisoformat(t["date"]).strftime("%d %b %Y %H:%M"),
        "Category": "Full Blend" if t["category"]=="BLEND" else CATEGORIES.get(t["category"],(t["category"],))[0],
        "Score": f"{t['score']}%",
        "Correct": f"{t['correct']}/{t['total_q']}",
        "Time": f"{t['time_taken']//60}m {t['time_taken']%60}s",
    } for t in reversed(history[-15:])])
    st.dataframe(tbl, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════
# GUIDE
# ═══════════════════════════════════════════════════════

def render_guide():
    st.markdown('<div class="section-title">📖 How to Use AptitudePro</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <strong>🎯 Start with the Full Blended Test</strong> on the Home page — this gives you the most realistic experience,
    mixing all 11 question types just like real SHL, Kenexa, and Cubiks assessments.
    </div>

    <br>

    **Test Categories & What to Expect:**

    | Category | Format | Key Skills |
    |----------|--------|------------|
    | Numerical | Tables, calculations | Mental arithmetic, data extraction |
    | Verbal | Passage → True/False/Cannot Say | Careful reading, inference |
    | Logical | Sequences, analogies, flow diagrams | Pattern recognition |
    | Mechanical | Diagrams with gears/levers | Physics principles |
    | Spatial | Cube nets, rotations | 3D visualisation |
    | Watson-Glaser | 5-option inference/assumption | Critical reasoning |
    | SJT | Workplace scenarios | Professional judgement |
    | IQ & Aptitude | Logic puzzles, lateral thinking | Reasoning breadth |
    | Error Checking | Compare data strings | Accuracy and attention |

    **Test Conditions:**
    - ⏱ 50 minutes for 60 questions (≈50 seconds each)
    - 🚩 Flag difficult questions and return to them
    - ✅ No penalty for guessing — answer everything
    - 💡 Full explanations provided after each test

    **Scoring Benchmarks:**
    - 90–100% → Outstanding (top 5%)
    - 80–89% → Excellent (top 15%)
    - 70–79% → Good (above average)
    - 60–69% → Satisfactory (average pass zone)
    - Below 60% → Needs practice
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# MAIN ROUTER
# ═══════════════════════════════════════════════════════

def main():
    page = st.session_state.page

    if page == "active_test":
        render_active_test()
        return

    render_header()
    render_nav()

    if page == "home":
        render_home()
    elif page == "tests":
        render_home()
    elif page == "results":
        render_results()
    elif page == "analytics":
        render_analytics()
    elif page == "guide":
        render_guide()
    else:
        render_home()


main()
