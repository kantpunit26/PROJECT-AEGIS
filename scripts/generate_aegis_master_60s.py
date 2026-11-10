import os
import sys
import time
import math
import subprocess
import asyncio
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts
import imageio_ffmpeg

ROOT_DIR = Path(__file__).resolve().parent.parent
PROD_DIR = ROOT_DIR / "master_60s_production"
PROD_DIR.mkdir(exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

VOICE = "en-US-ChristopherNeural"

# Exactly 60.0 Seconds Timeline: 6 High-Impact Scenes
SCENES = [
    {
        "id": "scene_01",
        "title": "THE HOOK & PROBLEM",
        "duration": 10.0,
        "frames": 600,
        "voice_text": "The threats are evolving. The perimeter is breached. Until now.",
        "caption": [
            ("The threats are evolving. The perimeter is breached. ", False),
            ("Until now.", True)
        ]
    },
    {
        "id": "scene_02",
        "title": "THE REVEAL & IDENTITY",
        "duration": 7.0,
        "frames": 420,
        "voice_text": "Introducing AEGIS 2.0. Autonomous. Intelligent. Impenetrable.",
        "caption": [
            ("Introducing ", False),
            ("AEGIS 2.0", True),
            (". Autonomous. Intelligent. Impenetrable.", False)
        ]
    },
    {
        "id": "scene_03",
        "title": "UI/UX & GLOBAL DASHBOARD",
        "duration": 18.0,
        "frames": 1080,
        "voice_text": "Total visibility. Zero friction. Command your entire infrastructure from a single pane of glass.",
        "caption": [
            ("Total visibility. Zero friction. ", True),
            ("Command your entire infrastructure from a ", False),
            ("single pane of glass.", True)
        ]
    },
    {
        "id": "scene_04",
        "title": "CORE ENGINE & 3D THREAT ISOLATION",
        "duration": 10.0,
        "frames": 600,
        "voice_text": "Powered by predictive AI architecture. Real-Time Detection. Instant Isolation. Automated Neutralization.",
        "caption": [
            ("Powered by predictive AI architecture. ", False),
            ("Real-Time Detection. Instant Isolation. Automated Neutralization.", True)
        ]
    },
    {
        "id": "scene_05",
        "title": "REAL-WORLD APPLICATION & IMPACT",
        "duration": 7.0,
        "frames": 420,
        "voice_text": "Bridging the gap between raw threat data and real-world continuity. Designed for absolute security.",
        "caption": [
            ("Bridging the gap between raw threat data and real-world continuity. ", False),
            ("Designed for absolute security.", True)
        ]
    },
    {
        "id": "scene_06",
        "title": "OUTRO & CALL TO ACTION",
        "duration": 8.0,
        "frames": 480,
        "voice_text": "Experience the future of digital defense. Secure your network with AEGIS 2.0 today.",
        "caption": [
            ("Experience the future of digital defense. Secure your network with ", False),
            ("AEGIS 2.0", True),
            (" today.", False)
        ]
    }
]

def get_font(size: int, bold: bool = False, mono: bool = False):
    font_paths = []
    if mono:
        font_paths = ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/lucon.ttf"]
    elif bold:
        font_paths = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    else:
        font_paths = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def synthesize_audio():
    print("[AEGIS 60s] Synthesizing high-tension driving electro-synth soundtrack & cinematic SFX...")
    sr = 44100
    total_dur = 60.0
    t = np.linspace(0, total_dur, int(sr * total_dur), endpoint=False)
    
    music = np.zeros_like(t)
    sfx = np.zeros_like(t)

    # 1. SCENE 1 (0:00 - 0:10): Rhythmic Ticking Urgency & Tension Drone
    idx_s1 = (t >= 0.0) & (t < 10.0)
    t_s1 = t[idx_s1]
    
    # 4 Hz Ticking clock urgency
    tick_phase = (t_s1 * 4.0) % 1.0
    tick_env = np.exp(-50.0 * tick_phase)
    tick = 0.25 * np.sin(2 * np.pi * 1800 * tick_phase) * tick_env
    # Low tension rumble
    drone_s1 = 0.35 * np.sin(2 * np.pi * 55 * t_s1) + 0.20 * np.sin(2 * np.pi * 110 * t_s1 + 0.1 * np.sin(2 * np.pi * 0.5 * t_s1))
    # Riser at 7.0 - 9.0s
    riser_mask = (t_s1 >= 7.0) & (t_s1 < 9.0)
    riser_t = t_s1[riser_mask] - 7.0
    riser_freq = np.geomspace(120, 950, len(riser_t))
    riser_phase = 2 * np.pi * np.cumsum(riser_freq) / sr
    riser = 0.40 * np.sin(riser_phase) * (riser_t / 2.0)**2
    drone_s1[riser_mask] += riser
    
    music[idx_s1] = drone_s1 + tick

    # Digital Shockwave freeze impact at 9.0s
    sw_mask = (t >= 9.0) & (t < 10.0)
    sw_t = t[sw_mask] - 9.0
    sw_boom = 0.85 * np.sin(2 * np.pi * 48 * np.exp(-1.5 * sw_t) * sw_t) * np.exp(-3.0 * sw_t)
    sw_noise = np.random.normal(0, 0.2, len(sw_t)) * np.exp(-8.0 * sw_t)
    sfx[sw_mask] += (sw_boom + sw_noise)

    # 2. SCENE 2 through SCENE 6 (0:10 - 0:58): Driving 128 BPM Electro-Synth Beat
    # 128 BPM = 2.1333 beats per second = period 0.46875s
    idx_beat = (t >= 10.0) & (t < 58.0)
    t_beat = t[idx_beat] - 10.0
    
    bpm = 128.0
    beat_dur = 60.0 / bpm
    beat_phase = (t_beat % beat_dur) / beat_dur
    
    # 4-on-the-floor Punchy Kick Drum
    kick_env = np.exp(-14.0 * beat_phase)
    kick_freq = 50 + 110 * np.exp(-25.0 * beat_phase)
    kick = 0.55 * np.sin(2 * np.pi * kick_freq * beat_phase * beat_dur) * kick_env
    
    # 16th-note rolling electro bassline
    sub_16 = (t_beat % (beat_dur / 4)) / (beat_dur / 4)
    bass_env = np.exp(-8.0 * sub_16)
    # Bass progression in A minor (A, F, C, G)
    chord_len = beat_dur * 16 # 4 bars
    prog_phase = (t_beat % chord_len) / chord_len
    bass_freq = np.where(prog_phase < 0.25, 55.0,
                np.where(prog_phase < 0.50, 43.65, # F
                np.where(prog_phase < 0.75, 65.41, # C
                                            49.0))) # G
    bass = 0.35 * np.sin(2 * np.pi * bass_freq * t_beat) * bass_env
    
    # Off-beat Hi-Hat
    hh_phase = ((t_beat + beat_dur / 2) % beat_dur) / beat_dur
    hh_env = np.exp(-35.0 * hh_phase)
    hh = np.random.normal(0, 0.12, len(t_beat)) * hh_env
    
    # Synth Arp Lead
    arp_sub = (t_beat % (beat_dur / 2)) / (beat_dur / 2)
    arp_env = np.exp(-6.0 * arp_sub)
    arp_lead = 0.18 * np.sin(2 * np.pi * (bass_freq * 4.0) * t_beat) * arp_env
    
    music[idx_beat] = kick + bass + hh + arp_lead

    # Specific SFX Hits
    # a) Shield Slam & Sub-Bass Drop at 10.0s
    slam_mask = (t >= 10.0) & (t < 12.0)
    st = t[slam_mask] - 10.0
    sfx[slam_mask] += 0.8 * np.sin(2 * np.pi * 42 * np.exp(-1.0 * st) * st) * np.exp(-2.5 * st)
    
    # b) Click SFX at 26.0s (Scene 3 Cursor Tab Click)
    clk_mask = (t >= 26.0) & (t < 26.2)
    ct = t[clk_mask] - 26.0
    sfx[clk_mask] += 0.4 * np.sin(2 * np.pi * 2400 * ct) * np.exp(-60.0 * ct)
    
    # c) Threat Neutralization ZAP & Chime at 41.5s (Scene 4 Emerald Shift)
    chm_mask = (t >= 41.5) & (t < 43.5)
    cht = t[chm_mask] - 41.5
    sfx[chm_mask] += 0.35 * (np.sin(2 * np.pi * 1046.5 * cht) + 0.6 * np.sin(2 * np.pi * 1318.5 * cht) + 0.4 * np.sin(2 * np.pi * 1567.98 * cht)) * np.exp(-3.5 * cht)
    
    # d) Final Resonant Synthetic Bass Drop at 58.0s (Scene 6 Fade)
    end_mask = (t >= 58.0) & (t < 60.0)
    et = t[end_mask] - 58.0
    sfx[end_mask] += 0.9 * np.sin(2 * np.pi * 38 * np.exp(-0.8 * et) * et) * np.exp(-1.8 * et)

    # Master Track Normalization
    music = music / np.max(np.abs(music) + 1e-6) * 0.32
    sfx = sfx / np.max(np.abs(sfx) + 1e-6) * 0.50
    master_audio = music + sfx
    master_audio = master_audio / np.max(np.abs(master_audio) + 1e-6) * 0.85
    
    audio_path = PROD_DIR / "master_soundtrack_60s.wav"
    wavfile.write(str(audio_path), sr, (master_audio * 32767).astype(np.int16))
    print(f"  Soundtrack & SFX generated: {audio_path.name}")
    return audio_path

async def generate_voiceovers():
    print("[AEGIS 60s] Generating crisp neural voiceovers via edge-tts...")
    audio_files = []
    for scene in SCENES:
        audio_path = PROD_DIR / f"{scene['id']}_voice.mp3"
        print(f"  Synthesizing voice: {scene['id']} ({scene['voice_text'][:35]}...)...")
        # Paced for high energy and impact
        communicate = edge_tts.Communicate(scene['voice_text'], VOICE, rate="+8%", pitch="+0Hz")
        await communicate.save(str(audio_path))
        audio_files.append(audio_path)
    return audio_files

def render_kinetic_subtitle(draw: ImageDraw.Draw, caption_parts: list, width: int = 1920, height: int = 1080):
    """Renders lower-center kinetic subtitles with glassmorphic pill and emerald accent."""
    cx = width // 2
    cy = height - 70
    
    # Measure text
    font_reg = get_font(21, bold=False)
    font_bold = get_font(22, bold=True)
    
    total_text = "".join([part[0] for part in caption_parts])
    full_w = font_bold.getlength(total_text)
    
    pill_w = min(width - 80, max(680, int(full_w + 120)))
    pill_h = 56
    x1, y1 = cx - pill_w // 2, cy - pill_h // 2
    x2, y2 = cx + pill_w // 2, cy + pill_h // 2
    
    # Glassmorphism Pill (Obsidian Slate with Neon Emerald border)
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=(7, 11, 20), outline=(16, 185, 129), width=1)
    # Glowing Emerald Top Accent Line
    draw.line([(x1 + 12, y1 + 1), (x2 - 12, y1 + 1)], fill=(5, 242, 146), width=2)
    
    # Status Tag Pill
    tag_w = 82
    draw.rounded_rectangle([(x1 + 12, cy - 13), (x1 + 12 + tag_w, cy + 13)], radius=4, fill=(6, 78, 59), outline=(16, 185, 129))
    draw.text((x1 + 12 + tag_w // 2, cy), "AEGIS 2.0", fill=(167, 243, 208), font=get_font(10, bold=True), anchor="mm")
    
    # Text Positioning
    start_x = x1 + tag_w + 30
    curr_x = start_x
    for text, is_bold in caption_parts:
        f = font_bold if is_bold else font_reg
        col = (255, 255, 255) if is_bold else (203, 213, 225)
        # Drop shadow
        draw.text((curr_x + 1, cy + 1), text, fill=(0, 0, 0), font=f, anchor="lm")
        draw.text((curr_x, cy), text, fill=col, font=f, anchor="lm")
        curr_x += f.getlength(text)

# ----------------- SCENE RENDERERS (60 FPS) ----------------- #

def render_scene_1_frame(f_idx: int, total_f: int = 600) -> Image.Image:
    """Scene 1: Hook & Problem - Red data streams, 3D wireframe threat globe, freezing shockwave."""
    t_sec = f_idx / 60.0
    img = Image.new("RGB", (1920, 1080), color=(3, 7, 18))
    draw = ImageDraw.Draw(img)
    
    # Ambient grid
    for x in range(0, 1920, 80):
        draw.line([(x, 0), (x, 1080)], fill=(11, 18, 33), width=1)
    for y in range(0, 1080, 80):
        draw.line([(0, y), (1920, y)], fill=(11, 18, 33), width=1)
        
    # Cascading Red Data Streams
    np.random.seed(42)
    cols = 24
    is_frozen = t_sec >= 8.5
    
    for c in range(cols):
        col_x = 40 + c * 78
        speed = 18 + (c % 5) * 8
        offset_y = int((f_idx * speed) if not is_frozen else (8.5 * 60 * speed)) % 1080
        
        # Draw streaming hex threat packets
        for r in range(12):
            char_y = (offset_y + r * 38) % 1080
            alpha = int(255 * (r / 12.0))
            threat_color = (239, 68, 68) if not is_frozen else (148, 163, 184)
            hex_text = f"0x{((c * 17 + r * 13 + f_idx) % 255):02X}"
            draw.text((col_x, char_y), hex_text, fill=threat_color, font=get_font(12, mono=True))

    # Center Wireframe 3D Threat Globe
    cx, cy = 960, 480
    r_globe = 220
    rot = f_idx * 0.02 if not is_frozen else (8.5 * 60 * 0.02)
    
    # Latitude rings
    for lat in range(-60, 70, 30):
        r_lat = int(r_globe * math.cos(math.radians(lat)))
        y_lat = int(cy + r_globe * math.sin(math.radians(lat)))
        if r_lat > 0:
            draw.ellipse([(cx - r_lat, y_lat - r_lat // 5), (cx + r_lat, y_lat + r_lat // 5)], outline=(60, 15, 25), width=1)
            
    # Longitude rings with 3D rotation
    for lon in range(0, 180, 30):
        eff_w = int(r_globe * math.sin(math.radians(lon) + rot))
        draw.ellipse([(cx - abs(eff_w), cy - r_globe), (cx + abs(eff_w), cy + r_globe)], outline=(185, 28, 28), width=1)
        
    # Chaotic Crimson Warning Nodes on Globe
    threat_nodes = [
        (0.4, 0.2, "CRITICAL ZERO-DAY: NODE 7"),
        (-0.5, -0.3, "EXFILTRATION DETECTED"),
        (0.2, -0.5, "PORT 443 BUFFER OVERFLOW"),
        (-0.3, 0.4, "ROOTKIT CASSETTE SPREADING")
    ]
    pulse = 1.0 + 0.3 * math.sin(f_idx * 0.2)
    for nx, ny, label in threat_nodes:
        px = int(cx + nx * r_globe * math.cos(rot) - ny * r_globe * math.sin(rot))
        py = int(cy + nx * r_globe * math.sin(rot) + ny * r_globe * math.cos(rot))
        rad = int(8 * pulse)
        draw.ellipse([(px - rad, py - rad), (px + rad, py + rad)], fill=(239, 68, 68))
        draw.ellipse([(px - rad - 6, py - rad - 6), (px + rad + 6, py + rad + 6)], outline=(220, 38, 38), width=1)
        if px > cx:
            draw.text((px + 14, py - 6), label, fill=(248, 113, 113), font=get_font(10, bold=True))

    # HUD Alert Overlay
    draw.rounded_rectangle([(60, 60), (450, 120)], radius=6, fill=(20, 5, 10), outline=(220, 38, 38))
    draw.text((80, 75), "⚠️ PERIMETER BREACH ACTIVE", fill=(239, 68, 68), font=get_font(14, bold=True))
    draw.text((80, 96), "SEVERITY: 9.8 CRITICAL | MULTIPLE VECTOR THREATS", fill=(248, 113, 113), font=get_font(10, bold=True))

    # Shockwave Freeze Ripple at 8.5s - 10.0s (frames 510 to 600)
    if t_sec >= 8.5:
        sw_progress = (t_sec - 8.5) / 1.5 # 0.0 to 1.0
        sw_rad = int(sw_progress * 1400)
        sw_alpha = int(255 * (1.0 - sw_progress))
        if sw_rad > 0:
            draw.ellipse([(cx - sw_rad, cy - sw_rad), (cx + sw_rad, cy + sw_rad)], outline=(5, 242, 146), width=6)
        if sw_rad > 12:
            draw.ellipse([(cx - sw_rad + 8, cy - sw_rad + 8), (cx + sw_rad - 8, cy + sw_rad - 8)], outline=(255, 255, 255), width=2)
        draw.text((cx, cy), "PERIMETER FROZEN — INITIALIZING AEGIS DEFENSE", fill=(5, 242, 146), font=get_font(20, bold=True), anchor="mm")

    render_kinetic_subtitle(draw, SCENES[0]["caption"])
    return img

def render_scene_2_frame(f_idx: int, total_f: int = 420) -> Image.Image:
    """Scene 2: The Reveal - Red data shatters, glowing emerald 3D shield logo slams onto screen."""
    t_sec = f_idx / 60.0
    img = Image.new("RGB", (1920, 1080), color=(3, 7, 18))
    draw = ImageDraw.Draw(img)
    
    cx, cy = 960, 460
    
    # Shattered particles dispersing outward
    np.random.seed(99)
    if t_sec < 2.5:
        part_progress = t_sec / 2.5
        for p in range(120):
            ang = (p * 2 * math.pi) / 120
            spd = 200 + (p % 10) * 80
            px = int(cx + math.cos(ang) * spd * part_progress)
            py = int(cy + math.sin(ang) * spd * part_progress)
            alpha_col = (int(220 * (1 - part_progress)), 38, 38)
            draw.rectangle([(px, py), (px + 4, py + 4)], fill=alpha_col)

    # Volumetric Emerald Light Rays
    for ray in range(8):
        ang_r = (ray * math.pi / 4) + (f_idx * 0.01)
        rx = cx + int(600 * math.cos(ang_r))
        ry = cy + int(400 * math.sin(ang_r))
        draw.line([(cx, cy), (rx, ry)], fill=(6, 78, 59), width=2)

    # Glowing Emerald 3D Shield Logo
    scale = min(1.0, 0.4 + 0.6 * math.sin(min(1.0, t_sec / 1.0) * math.pi / 2))
    # Subtle screen-shake on slam (around t=1.0s)
    shake_x = int(6 * math.sin(f_idx * 2.0) * max(0.0, 1.0 - abs(t_sec - 1.0) * 2.0))
    shake_y = int(6 * math.cos(f_idx * 2.0) * max(0.0, 1.0 - abs(t_sec - 1.0) * 2.0))
    scx, scy = cx + shake_x, cy + shake_y
    
    # Shield Geometry (Polygon)
    sw, sh = int(220 * scale), int(260 * scale)
    shield_pts = [
        (scx, scy - sh),
        (scx + sw, scy - sh * 0.6),
        (scx + sw * 0.85, scy + sh * 0.3),
        (scx, scy + sh),
        (scx - sw * 0.85, scy + sh * 0.3),
        (scx - sw, scy - sh * 0.6)
    ]
    # Glowing perimeter
    draw.polygon(shield_pts, fill=(5, 40, 30), outline=(5, 242, 146))
    
    # Inner faceted geometric shield
    inner_pts = [
        (scx, scy - int(sh * 0.8)),
        (scx + int(sw * 0.75), scy - int(sh * 0.45)),
        (scx + int(sw * 0.65), scy + int(sh * 0.2)),
        (scx, scy + int(sh * 0.75)),
        (scx - int(sw * 0.65), scy + int(sh * 0.2)),
        (scx - int(sw * 0.75), scy - int(sh * 0.45))
    ]
    draw.polygon(inner_pts, fill=(6, 78, 59), outline=(16, 185, 129))
    draw.line([(scx, scy - int(sh * 0.8)), (scx, scy + int(sh * 0.75))], fill=(5, 242, 146), width=2)
    draw.line([(scx - int(sw * 0.65), scy + int(sh * 0.2)), (scx + int(sw * 0.65), scy + int(sh * 0.2))], fill=(5, 242, 146), width=2)
    
    # Glowing Core Emblem
    draw.ellipse([(scx - 16, scy - 16), (scx + 16, scy + 16)], fill=(255, 255, 255))
    draw.ellipse([(scx - 24, scy - 24), (scx + 24, scy + 24)], outline=(5, 242, 146), width=2)

    # Title Slam: AEGIS 2.0
    title_font = get_font(72, bold=True)
    draw.text((scx + 2, scy + sh + 42), "AEGIS 2.0", fill=(0, 0, 0), font=title_font, anchor="mm")
    draw.text((scx, scy + sh + 40), "AEGIS 2.0", fill=(255, 255, 255), font=title_font, anchor="mm")
    
    sub_font = get_font(18, bold=True)
    draw.text((scx, scy + sh + 88), "AUTONOMOUS • INTELLIGENT • IMPENETRABLE", fill=(5, 242, 146), font=sub_font, anchor="mm")

    render_kinetic_subtitle(draw, SCENES[1]["caption"])
    return img

def render_scene_3_frame(f_idx: int, total_f: int = 1080) -> Image.Image:
    """Scene 3: UI/UX & Global Dashboard Walkthrough - Fly into dashboard, camera pan, cursor clicks tab."""
    t_sec = f_idx / 60.0
    
    # Load dashboard image
    dash_path = ROOT_DIR / "test_captures" / "dashboard.png"
    threat_path = ROOT_DIR / "test_captures" / "surveillance.png"
    
    # After click (t >= 9.0s), transition smoothly to Active Threat Analysis tab
    if t_sec < 9.0:
        base_img = Image.open(dash_path).convert("RGB") if dash_path.exists() else Image.new("RGB", (1920, 1080), (7, 10, 17))
    else:
        base_img = Image.open(threat_path).convert("RGB") if threat_path.exists() else Image.new("RGB", (1920, 1080), (7, 10, 17))
        
    img = base_img.copy()
    draw = ImageDraw.Draw(img)
    
    # Top Status Banner Pill
    draw.rounded_rectangle([(1480, 12), (1895, 52)], radius=6, fill=(11, 15, 25), outline=(16, 185, 129))
    draw.ellipse([(1500, 26), (1512, 38)], fill=(16, 185, 129))
    draw.text((1524, 23), "SYSTEM OPTIMAL [99.99%]", fill=(226, 232, 240), font=get_font(12, bold=True))
    draw.text((1875, 23), "LIVE", fill=(5, 242, 146), font=get_font(11, bold=True), anchor="ra")

    # Animated High-Tech Digital Cursor
    # Cursor starts at (1200, 400), glides to "Active Threat Analysis" tab button at (540, 28) around t=7.5s - 9.0s
    if t_sec < 9.0:
        cur_progress = min(1.0, max(0.0, (t_sec - 5.0) / 3.0))
        cur_x = int(1100 + (320 - 1100) * cur_progress)
        cur_y = int(350 + (30 - 350) * cur_progress)
        
        # Click ripple right at 8.8s - 9.0s
        if 8.5 <= t_sec < 9.0:
            rip_r = int((t_sec - 8.5) * 60)
            if rip_r > 0:
                draw.ellipse([(cur_x - rip_r, cur_y - rip_r), (cur_x + rip_r, cur_y + rip_r)], outline=(5, 242, 146), width=2)
            
        # Draw sleek cursor arrow
        cursor_pts = [(cur_x, cur_y), (cur_x + 14, cur_y + 14), (cur_x + 6, cur_y + 16), (cur_x + 9, cur_y + 24), (cur_x + 4, cur_y + 26), (cur_x + 1, cur_y + 18), (cur_x - 3, cur_y + 22)]
        draw.polygon(cursor_pts, fill=(5, 242, 146), outline=(255, 255, 255))
    else:
        # Threat Analysis Tab Active Highlight Indicator
        draw.rounded_rectangle([(240, 8), (420, 52)], radius=6, outline=(5, 242, 146), width=2)
        draw.text((330, 30), "THREAT ANALYSIS ACTIVE", fill=(5, 242, 146), font=get_font(10, bold=True), anchor="mm")

    render_kinetic_subtitle(draw, SCENES[2]["caption"])
    return img

def render_scene_4_frame(f_idx: int, total_f: int = 600) -> Image.Image:
    """Scene 4: Core Engine & 3D Threat Isolation - Blurs background, isolates infected 3D node, neutralizes to emerald."""
    t_sec = f_idx / 60.0
    
    # Blurred UI Background
    bg_path = ROOT_DIR / "test_captures" / "isolates.png"
    if bg_path.exists():
        img = Image.open(bg_path).convert("RGB").filter(ImageFilter.GaussianBlur(radius=8))
    else:
        img = Image.new("RGB", (1920, 1080), (7, 10, 17))
        
    draw = ImageDraw.Draw(img)
    cx, cy = 960, 480
    
    is_neutralized = t_sec >= 5.0
    rot = f_idx * 0.04
    
    # Color Shift: Warning Crimson -> Secure Neon Emerald
    if not is_neutralized:
        node_color = (239, 68, 68)
        glow_color = (220, 38, 38)
        status_text = "⚠️ ZERO-DAY THREAT DETECTED — ISOLATING SECTOR 7G"
        sub_status = "ANOMALY: REVERSE SHELL INTRUSION IN PROGRESS"
    else:
        node_color = (5, 242, 146)
        glow_color = (16, 185, 129)
        status_text = "🛡️ THREAT NEUTRALIZED [100%] — AUTONOMOUS AI CONTAINMENT COMPLETE"
        sub_status = "INTEGRITY RESTORED • ZERO DATA EXFILTRATION • AIR-GAPPED"

    # Rotating 3D Holographic Node (Icosahedron projection)
    r_node = 160
    num_pts = 8
    poly_pts = []
    for p in range(num_pts):
        ang = p * (2 * math.pi / num_pts) + rot
        px = cx + int(r_node * math.cos(ang))
        py = cy + int(r_node * 0.6 * math.sin(ang))
        poly_pts.append((px, py))
        
    # Draw connections to central core
    for px, py in poly_pts:
        draw.line([(cx, cy), (px, py)], fill=glow_color, width=2)
    draw.polygon(poly_pts, outline=node_color, width=3)

    # Orbital Security Containment Rings
    for ring_i, r_mult in enumerate([1.3, 1.6, 1.9]):
        r_orb = int(r_node * r_mult)
        rot_r = rot * (1.2 if ring_i % 2 == 0 else -1.2)
        eff_rx = max(1, int(r_orb * abs(math.cos(rot_r))))
        eff_ry = max(1, r_orb // 2)
        draw.ellipse([(cx - eff_rx, cy - eff_ry), (cx + eff_rx, cy + eff_ry)], outline=glow_color, width=1)

    # Core Glowing Sphere
    draw.ellipse([(cx - 24, cy - 24), (cx + 24, cy + 24)], fill=node_color)
    draw.ellipse([(cx - 36, cy - 36), (cx + 36, cy + 36)], outline=(255, 255, 255), width=2)

    # Top Holographic Isolation HUD
    hud_w = 840
    draw.rounded_rectangle([(cx - hud_w // 2, 70), (cx + hud_w // 2, 140)], radius=8, fill=(7, 11, 20), outline=node_color, width=2)
    draw.text((cx, 95), status_text, fill=node_color, font=get_font(16, bold=True), anchor="mm")
    draw.text((cx, 120), sub_status, fill=(203, 213, 225), font=get_font(12, bold=False), anchor="mm")

    render_kinetic_subtitle(draw, SCENES[3]["caption"])
    return img

def render_scene_5_frame(f_idx: int, total_f: int = 420) -> Image.Image:
    """Scene 5: Real-World Application & Impact - Split screen (Polished AEGIS UI | Global Metropolis/Server Farm)."""
    t_sec = f_idx / 60.0
    img = Image.new("RGB", (1920, 1080), color=(7, 10, 17))
    
    # Left Side: AEGIS UI Incident Report
    rep_path = ROOT_DIR / "test_captures" / "reports.png"
    if rep_path.exists():
        ui_left = Image.open(rep_path).convert("RGB").crop((0, 0, 960, 1080))
        img.paste(ui_left, (0, 0))
    else:
        draw_left = ImageDraw.Draw(img)
        draw_left.rectangle([(0, 0), (960, 1080)], fill=(11, 15, 25))
        
    draw = ImageDraw.Draw(img)
    
    # Right Side: Futuristic Server Farm / Metropolis Continuity Visual
    # Render procedural high-tech datacenter server rack visualization
    draw.rectangle([(960, 0), (1920, 1080)], fill=(4, 8, 16))
    
    # Draw perspective grid for server room corridor
    vp_x, vp_y = 1440, 480
    for side_x in range(960, 1920, 120):
        draw.line([(side_x, 1080), (vp_x, vp_y)], fill=(15, 23, 42), width=1)
        draw.line([(side_x, 0), (vp_x, vp_y)], fill=(15, 23, 42), width=1)
        
    # Server rack columns with blinking optimal green LEDs
    for rack_x in [1060, 1200, 1680, 1820]:
        draw.rectangle([(rack_x - 30, 200), (rack_x + 30, 880)], fill=(9, 14, 26), outline=(30, 41, 59))
        for slot in range(16):
            sy = 220 + slot * 40
            draw.rectangle([(rack_x - 24, sy), (rack_x + 24, sy + 28)], fill=(15, 23, 42))
            # Blinking green activity LEDs
            led_blink = ((f_idx + rack_x + slot * 7) % 20) > 4
            led_col = (5, 242, 146) if led_blink else (6, 78, 59)
            draw.ellipse([(rack_x + 14, sy + 10), (rack_x + 20, sy + 16)], fill=led_col)
            
    # Right Side Overlay Banner
    draw.rounded_rectangle([(1080, 80), (1800, 145)], radius=6, fill=(7, 11, 20), outline=(5, 242, 146))
    draw.text((1440, 102), "GLOBAL DATACENTER INFRASTRUCTURE", fill=(5, 242, 146), font=get_font(14, bold=True), anchor="mm")
    draw.text((1440, 126), "ZERO DOWNTIME • CONTINUOUS OPERATION • 100% RECOVERY", fill=(203, 213, 225), font=get_font(11, bold=True), anchor="mm")

    # Center Glowing Emerald Laser Divider Beam
    draw.line([(960, 0), (960, 1080)], fill=(5, 242, 146), width=3)
    draw.line([(958, 0), (958, 1080)], fill=(167, 243, 208), width=1)

    # Left Side Label
    draw.rounded_rectangle([(120, 80), (840, 145)], radius=6, fill=(7, 11, 20), outline=(5, 242, 146))
    draw.text((480, 102), "AUTONOMOUS INCIDENT REPORT & AUDIT", fill=(5, 242, 146), font=get_font(14, bold=True), anchor="mm")
    draw.text((480, 126), "CRYPTOGRAPHIC PROVENANCE • ISO/IEC 27001 & CISA COMPLIANT", fill=(203, 213, 225), font=get_font(11, bold=True), anchor="mm")

    render_kinetic_subtitle(draw, SCENES[4]["caption"])
    return img

def render_scene_6_frame(f_idx: int, total_f: int = 480) -> Image.Image:
    """Scene 6: Outro & Call to Action - UI zooms out, collapses into glowing shield logo, final fade."""
    t_sec = f_idx / 60.0
    img = Image.new("RGB", (1920, 1080), color=(3, 7, 18))
    draw = ImageDraw.Draw(img)
    
    # Fade out at end (last 1.5 seconds)
    fade = max(0.0, min(1.0, (8.0 - t_sec) / 1.5))
    if fade < 1.0:
        # We will dim everything with fade factor
        pass
        
    cx, cy = 960, 440
    
    # Emerald Pulse Aura
    pulse = 1.0 + 0.08 * math.sin(f_idx * 0.1)
    aura_r = int(280 * pulse)
    draw.ellipse([(cx - aura_r, cy - aura_r), (cx + aura_r, cy + aura_r)], outline=(6, 78, 59), width=2)
    
    # Glowing 3D Shield Logo
    sw, sh = 160, 200
    shield_pts = [
        (cx, cy - sh),
        (cx + sw, cy - sh * 0.6),
        (cx + sw * 0.85, cy + sh * 0.3),
        (cx, cy + sh),
        (cx - sw * 0.85, cy + sh * 0.3),
        (cx - sw, cy - sh * 0.6)
    ]
    draw.polygon(shield_pts, fill=(5, 40, 30), outline=(5, 242, 146), width=2)
    
    # Inner facets
    draw.line([(cx, cy - sh + 20), (cx, cy + sh - 20)], fill=(5, 242, 146), width=2)
    draw.ellipse([(cx - 16, cy - 16), (cx + 16, cy + 16)], fill=(255, 255, 255))
    
    # Main Outro Typography
    title_font = get_font(68, bold=True)
    draw.text((cx, cy + sh + 45), "AEGIS 2.0", fill=(255, 255, 255), font=title_font, anchor="mm")
    
    sub_font = get_font(18, bold=True)
    draw.text((cx, cy + sh + 95), "THE FUTURE OF AUTONOMOUS DIGITAL DEFENSE", fill=(5, 242, 146), font=sub_font, anchor="mm")
    
    cta_font = get_font(14, bold=True)
    draw.rounded_rectangle([(cx - 240, cy + sh + 125), (cx + 240, cy + sh + 168)], radius=6, fill=(11, 15, 25), outline=(5, 242, 146))
    draw.text((cx, cy + sh + 146), "DEPLOY YOUR DEFENSE MATRIX — AEGIS.DEV", fill=(226, 232, 240), font=cta_font, anchor="mm")

    render_kinetic_subtitle(draw, SCENES[5]["caption"])
    
    # Apply fade to black if near end
    if fade < 1.0:
        dark_overlay = Image.new("RGB", (1920, 1080), (0, 0, 0))
        img = Image.blend(dark_overlay, img, fade)
        
    return img

def render_and_encode_video(audio_track_path: Path):
    output_video = ROOT_DIR / "aegis_2.0_master_promotional_60s.mp4"
    print(f"[AEGIS 60s] Encoding 3,600 frames at 60 FPS directly into high-bitrate MP4 ({output_video.name})...")
    
    w, h = 1920, 1080
    fps = 60
    
    # FFmpeg Pipe Command with 60fps and Master Audio Muxing
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{w}x{h}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", str(audio_track_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-b:v", "12M",
        "-maxrate", "16M",
        "-bufsize", "24M",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-r", str(fps),
        "-t", "60.0",
        str(output_video)
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    scene_renderers = [
        render_scene_1_frame,
        render_scene_2_frame,
        render_scene_3_frame,
        render_scene_4_frame,
        render_scene_5_frame,
        render_scene_6_frame
    ]
    
    total_encoded = 0
    start_t = time.time()
    
    for s_idx, scene in enumerate(SCENES):
        print(f"  Rendering {scene['id']}: {scene['title']} ({scene['frames']} frames @ 60fps)...")
        renderer = scene_renderers[s_idx]
        for f in range(scene["frames"]):
            frame_img = renderer(f, scene["frames"])
            proc.stdin.write(frame_img.tobytes())
            total_encoded += 1
            if total_encoded % 300 == 0:
                elapsed = time.time() - start_t
                fps_rate = total_encoded / max(1e-5, elapsed)
                print(f"    Rendered {total_encoded}/3600 frames ({fps_rate:.1f} fps, {total_encoded/60:.1f}s)...")
                
    proc.stdin.close()
    proc.wait()
    
    print(f"[AEGIS 60s] Encoding complete in {time.time() - start_t:.1f}s!")
    print(f"  Exported Master 60s Video to: {output_video}")
    print(f"  File Size: {output_video.stat().st_size / (1024*1024):.2f} MB")
    
    # Also copy to root aegis_promotional_video.mp4 so default shortcuts open this latest master
    root_video = ROOT_DIR / "aegis_promotional_video.mp4"
    import shutil
    shutil.copy(output_video, root_video)
    print(f"  Synchronized root promotional video: {root_video}")

async def main():
    await generate_voiceovers()
    audio_path = synthesize_audio()
    
    # Mix Voiceovers into Master Audio at exact cue points
    voice_audio = PROD_DIR / "final_mixed_audio_60s.wav"
    
    # Time offsets for the 6 voiceover tracks:
    # Scene 1: 0.5s
    # Scene 2: 10.5s
    # Scene 3: 17.5s
    # Scene 4: 35.5s
    # Scene 5: 45.5s
    # Scene 6: 52.5s
    filter_complex = (
        "[0:a]volume=0.45[music]; "
        "[1:a]adelay=500|500,volume=1.1[v1]; "
        "[2:a]adelay=10500|10500,volume=1.1[v2]; "
        "[3:a]adelay=17500|17500,volume=1.1[v3]; "
        "[4:a]adelay=35500|35500,volume=1.1[v4]; "
        "[5:a]adelay=45500|45500,volume=1.1[v5]; "
        "[6:a]adelay=52500|52500,volume=1.1[v6]; "
        "[music][v1][v2][v3][v4][v5][v6]amix=inputs=7:duration=first:dropout_transition=2[aout]"
    )
    
    mix_cmd = [
        FFMPEG_EXE, "-y",
        "-i", str(audio_path),
        "-i", str(PROD_DIR / "scene_01_voice.mp3"),
        "-i", str(PROD_DIR / "scene_02_voice.mp3"),
        "-i", str(PROD_DIR / "scene_03_voice.mp3"),
        "-i", str(PROD_DIR / "scene_04_voice.mp3"),
        "-i", str(PROD_DIR / "scene_05_voice.mp3"),
        "-i", str(PROD_DIR / "scene_06_voice.mp3"),
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-ac", "2",
        "-ar", "44100",
        str(voice_audio)
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[AEGIS 60s] Voiceover layered into master soundtrack ({voice_audio.name}).")
    
    render_and_encode_video(voice_audio)

if __name__ == "__main__":
    asyncio.run(main())

