import os
import sys
import time
import math
import subprocess
import asyncio
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import imageio_ffmpeg

ROOT_DIR = Path(__file__).resolve().parent.parent
PROD_DIR = ROOT_DIR / "ultimate_production"
PROD_DIR.mkdir(exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

VOICE = "en-US-ChristopherNeural"

# 13 High-Impact Scientific Narrative Scenes covering 100% of AEGIS 2.0
SCENES = [
    {
        "id": "scene_01_intro",
        "type": "card",
        "badge": "MISSION INITIALIZATION",
        "title": "PROJECT AEGIS 2.0",
        "subtitle": "Advanced Genomic Epidemiology & Intelligence System",
        "voice_text": "Welcome to Project AEGIS 2.0, the Advanced Genomic Epidemiology and Intelligence System. An enterprise research platform engineered for real-time antimicrobial resistance surveillance and comparative genomics.",
        "caption": "Project AEGIS 2.0 — Advanced Genomic Epidemiology & Intelligence System"
    },
    {
        "id": "scene_02_loading",
        "type": "loading",
        "badge": "BIOINFORMATICS INGESTION MATRIX",
        "title": "DATA INGESTION & PIPELINE SYNCHRONIZATION",
        "subtitle": "Nextflow DSL2 • PostGIS Spatial • AMRFinderPlus • IQ-TREE • MOB-suite",
        "voice_text": "Synchronizing bioinformatics pipelines. Orchestrating NCBI genomic data acquisition, Nextflow DSL2 execution environments, and PostGIS high-performance spatial indexing.",
        "caption": "Nextflow DSL2 Pipelines • PostGIS Spatial Indexing • Automated Checksum Provenance"
    },
    {
        "id": "scene_03_dashboard",
        "type": "ui",
        "image": "test_captures/dashboard.png",
        "hud": "SURVEILLANCE HUB • ACTIVE OUTBREAKS",
        "title": "GLOBAL SURVEILLANCE & OUTBREAK DETECTION",
        "voice_text": "The Surveillance Hub monitors international pathogen dissemination, tracking high-risk Klebsiella pneumoniae clones and active clinical micro-outbreaks across healthcare networks.",
        "caption": "Global pathogen surveillance, ESCAPE pathogen tracking, and real-time clinical micro-outbreak alerts"
    },
    {
        "id": "scene_04_surveillance",
        "type": "ui",
        "image": "test_captures/surveillance.png",
        "hud": "3D GEOSPATIAL INTELLIGENCE",
        "title": "3D SURVEILLANCE GLOBE & NATURAL LANGUAGE QUERY",
        "voice_text": "Featuring an interactive 3D surveillance globe and a safe natural-language query engine, enabling immediate radius-based outbreak detection with zero arbitrary SQL execution risk.",
        "caption": "Interactive 3D Three.js globe with parameterized natural-language outbreak queries"
    },
    {
        "id": "scene_05_isolates",
        "type": "ui",
        "image": "test_captures/isolates.png",
        "hud": "GENOMIC REGISTRY • ASSEMBLY QC",
        "title": "VALIDATED GENOMIC ISOLATE REGISTRY & QUALITY CONTROL",
        "voice_text": "The Genomic Registry catalogs whole-genome assemblies, validating N50, GC content, and contig completeness against species-specific taxonomic thresholds.",
        "caption": "Whole-genome assembly metrics (N50, GC content, contigs) with automated taxonomic validation"
    },
    {
        "id": "scene_06_amr",
        "type": "ui",
        "image": "test_captures/amr.png",
        "hud": "NCBI AMRFINDERPLUS • DETERMINANTS",
        "title": "AMRFINDERPLUS DETERMINANTS & RESISTANCE CASCADES",
        "voice_text": "Integrated with NCBI AMRFinderPlus, AEGIS classifies carbapenemases, colistin resistance, and ESBLs, mapping population prevalence and pairwise co-selection patterns.",
        "caption": "NCBI AMRFinderPlus determinant screening, resistance cascades, and pairwise co-selection matrix"
    },
    {
        "id": "scene_07_comparative",
        "type": "ui",
        "image": "test_captures/comparative.png",
        "hud": "COMPARATIVE GENOMICS • SNP DISTANCE",
        "title": "CORE-GENOME SNP DISTANCE MATRIX & OUTBREAK CLUSTERING",
        "voice_text": "Comparative genomics workflows compute filtered pairwise SNP distance matrices, pinpointing hospital micro-outbreaks separated by as few as six single nucleotide polymorphisms.",
        "caption": "Core-genome pairwise SNP distance heatmap with interactive outbreak threshold clustering"
    },
    {
        "id": "scene_08_phylogeny",
        "type": "ui",
        "image": "test_captures/comparative_tree.png",
        "hud": "MOLECULAR PHYLOGENETICS • IQ-TREE",
        "title": "IQ-TREE MAXIMUM LIKELIHOOD & MULTI-TRACK METADATA",
        "voice_text": "Explore circular chromosome GC skew profiles alongside Maximum-Likelihood phylogenetic trees decorated with multi-track lineage and resistance metadata.",
        "caption": "IQ-TREE maximum-likelihood phylogenetic trees annotated with sequence types and resistance determinants"
    },
    {
        "id": "scene_09_plasmids",
        "type": "ui",
        "image": "test_captures/plasmids.png",
        "hud": "MOB-SUITE • PLASMID RECONSTRUCTION",
        "title": "MOB-SUITE PLASMID RECONSTRUCTION & REPLICON TYPING",
        "voice_text": "MOB-suite integration reconstructs extrachromosomal plasmids, identifying IncF and Col replicon types, relaxases, and conjugative transfer genes carrying critical resistance markers.",
        "caption": "MOB-suite plasmid reconstruction, replicon classification, and resistance gene colocalization"
    },
    {
        "id": "scene_10_ast",
        "type": "ui",
        "image": "test_captures/ast.png",
        "hud": "AST VALIDATION • EUCAST / CLSI",
        "title": "GENOTYPE-PHENOTYPE VALIDATION & BREAKPOINT BENCHMARKING",
        "voice_text": "A dedicated AST validation module benchmarks predicted resistance against experimental MIC records, computing sensitivity, specificity, and CLSI and EUCAST concordance.",
        "caption": "Antimicrobial susceptibility testing (AST) concordance, MIC distributions, and confusion matrices"
    },
    {
        "id": "scene_11_modelling",
        "type": "ui",
        "image": "test_captures/modelling.png",
        "hud": "TRANSMISSION DYNAMICS • SEIR",
        "title": "EXTENDED SEIR EPIDEMIOLOGICAL MODELLING",
        "voice_text": "An extended SEIR epidemiological simulator uses Runge-Kutta fourth-order numerical integration to project nosocomial transmission, colonization, and antibiotic exposure dynamics.",
        "caption": "Extended SEIR transmission simulator with Runge-Kutta numerical differential equation solver"
    },
    {
        "id": "scene_12_reports",
        "type": "ui",
        "image": "test_captures/reports.png",
        "hud": "REPRODUCIBLE REPORTING • WHO GLASS",
        "title": "AUTOMATED ALERTING & WHO GLASS REPORTING",
        "voice_text": "Generate reproducible surveillance reports with WHO GLASS data structures, automated Slack and Discord webhook alerts, and multi-format export in PDF, GeoJSON, and Newick.",
        "caption": "WHO GLASS reporting structures, automated webhook alerting, and multi-format data export"
    },
    {
        "id": "scene_13_outro",
        "type": "card",
        "badge": "ENTERPRISE READY",
        "title": "PROJECT AEGIS 2.0",
        "subtitle": "The Future of Genomic Epidemiology & AMR Intelligence",
        "voice_text": "From raw genomic sequences to global surveillance intelligence. Project AEGIS 2.0: The Future of Genomic Epidemiology and AMR Intelligence.",
        "caption": "FastAPI • React • PostGIS • Nextflow DSL2 • Docker Ready • WHO GLASS Compliant"
    }
]

def get_font(size: int, bold: bool = False):
    font_paths = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def synthesize_audio_effects(total_duration: float):
    print("[AEGIS Video] Synthesizing transition SFX and master ambient soundtrack...")
    sr = 44100

    # 1. High-Impact Transition Whoosh SFX (0.9 second)
    whoosh_dur = 0.9
    tw = np.linspace(0, whoosh_dur, int(sr * whoosh_dur), endpoint=False)
    freqs = np.geomspace(40, 580, len(tw))
    phase = 2 * np.pi * np.cumsum(freqs) / sr
    env = np.sin(np.pi * (tw / whoosh_dur)) ** 2
    whoosh = 0.60 * np.sin(phase) * env
    noise = np.random.normal(0, 0.16, len(tw)) * env
    whoosh_final = (whoosh + noise)
    whoosh_final = whoosh_final / np.max(np.abs(whoosh_final))
    whoosh_path = PROD_DIR / "whoosh_sfx.wav"
    wavfile.write(str(whoosh_path), sr, (whoosh_final * 32767).astype(np.int16))

    # 2. Holographic Chime SFX (0.8 second)
    chime_dur = 0.8
    tc = np.linspace(0, chime_dur, int(sr * chime_dur), endpoint=False)
    env_c = np.exp(-4.5 * tc)
    chime = (0.5 * np.sin(2 * np.pi * 1200 * tc) +
             0.3 * np.sin(2 * np.pi * 1800 * tc) +
             0.2 * np.sin(2 * np.pi * 2400 * tc)) * env_c
    chime = chime / np.max(np.abs(chime))
    chime_path = PROD_DIR / "chime_sfx.wav"
    wavfile.write(str(chime_path), sr, (chime * 32767).astype(np.int16))

    # 3. Master Ambient Electronic Soundtrack (exact length of video)
    ta = np.linspace(0, total_duration, int(sr * total_duration), endpoint=False)
    drone1 = 0.35 * np.sin(2 * np.pi * 55 * ta)
    drone2 = 0.22 * np.sin(2 * np.pi * 110 * ta + 0.1 * np.sin(2 * np.pi * 0.2 * ta))
    drone3 = 0.14 * np.sin(2 * np.pi * 165 * ta)
    pulse = (0.5 + 0.5 * np.sin(2 * np.pi * 2.0 * ta)) ** 2
    synth_lead = 0.10 * np.sin(2 * np.pi * 440 * ta) * pulse
    ambient = (drone1 + drone2 + drone3 + synth_lead)
    fade_len = int(sr * 2.0)
    ambient[:fade_len] *= np.linspace(0, 1, fade_len)
    ambient[-fade_len:] *= np.linspace(1, 0, fade_len)
    ambient = ambient / np.max(np.abs(ambient)) * 0.22
    ambient_path = PROD_DIR / "ambient_soundtrack.wav"
    wavfile.write(str(ambient_path), sr, (ambient * 32767).astype(np.int16))
    print(f"  SFX & Ambient Soundtrack generated ({total_duration:.1f}s).")

async def generate_voiceovers():
    print("[AEGIS Video] Generating neural voiceovers via edge-tts...")
    for scene in SCENES:
        audio_path = PROD_DIR / f"{scene['id']}.mp3"
        print(f"  Synthesizing voice: {scene['id']}...")
        communicate = edge_tts.Communicate(scene['voice_text'], VOICE, rate="+3%", pitch="+0Hz")
        await communicate.save(str(audio_path))

def build_loading_matrix_frame(frame_path: Path, scene: dict):
    img = Image.new("RGB", (1920, 1080), color=(4, 7, 13))
    draw = ImageDraw.Draw(img)

    # Grid background
    for x in range(0, 1920, 48):
        draw.line([(x, 0), (x, 1080)], fill=(12, 18, 32), width=1)
    for y in range(0, 1080, 48):
        draw.line([(0, y), (1920, y)], fill=(12, 18, 32), width=1)

    cx, cy = 960, 430
    radar_radius = 160

    # Concentric Radar Rings
    for r, col, w in [(radar_radius, (139, 0, 0), 2), (radar_radius - 35, (30, 41, 59), 1), (radar_radius - 70, (220, 38, 38), 2), (radar_radius - 105, (15, 23, 42), 1)]:
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=col, width=w)

    # Crosshairs & Radar Sweep Arm
    draw.line([(cx - radar_radius - 25, cy), (cx + radar_radius + 25, cy)], fill=(139, 0, 0), width=1)
    draw.line([(cx, cy - radar_radius - 25), (cx, cy + radar_radius + 25)], fill=(139, 0, 0), width=1)
    angle = math.pi / 4
    x_sweep = cx + radar_radius * math.cos(angle)
    y_sweep = cy + radar_radius * math.sin(angle)
    draw.line([(cx, cy), (x_sweep, y_sweep)], fill=(239, 68, 68), width=3)
    draw.ellipse([(cx - 7, cy - 7), (cx + 7, cy + 7)], fill=(255, 255, 255))

    # Center Badge
    badge_font = get_font(13, bold=True)
    draw.rounded_rectangle([(cx - 160, cy - 240), (cx + 160, cy - 208)], radius=5, fill=(76, 5, 5), outline=(185, 28, 28))
    draw.text((cx, cy - 224), scene["badge"], fill=(248, 113, 113), font=badge_font, anchor="mm")

    # Main Loading Title & Subtitle
    title_font = get_font(36, bold=True)
    draw.text((cx, cy - 268), scene["title"], fill=(255, 255, 255), font=title_font, anchor="mm")

    # Telemetry Boxes
    telemetry = [
        ("NCBI DATASETS STREAM", "CONNECTED [K. pneumoniae MGH 78578 & HS11286]", (16, 185, 129)),
        ("POSTGIS SPATIAL GRID", "SRID 4326 WGS84 GIST INDEX ACTIVE", (16, 185, 129)),
        ("NEXTFLOW DSL2 ENGINES", "6 PIPELINE MODULES SYNCHRONIZED & DOCKER READY", (59, 130, 246)),
        ("AMRFINDERPLUS 3.12", "DATABASE 2024-05-02.1 (9,142 HMMs LOADED)", (245, 158, 11)),
        ("IQ-TREE & MOB-SUITE", "MODELFINDER GTR+F+R4 • MOB-RECON PLASMID TYPING", (168, 85, 247)),
        ("EXTENDED SEIR MODEL", "RUNGE-KUTTA 4TH-ORDER NUMERICAL SOLVER READY", (236, 72, 153)),
    ]

    box_y = 635
    for title, val, col in telemetry:
        draw.rounded_rectangle([(cx - 480, box_y), (cx + 480, box_y + 34)], radius=4, fill=(11, 15, 25), outline=(30, 41, 59), width=1)
        draw.ellipse([(cx - 460, box_y + 12), (cx - 450, box_y + 22)], fill=col)
        draw.text((cx - 435, box_y + 10), title, fill=(226, 232, 240), font=get_font(12, bold=True))
        draw.text((cx + 460, box_y + 10), val, fill=col, font=get_font(12, bold=True), anchor="ra")
        box_y += 40

    # Animated Progress Bar (100% Synced)
    prog_y = 900
    draw.rounded_rectangle([(cx - 480, prog_y), (cx + 480, prog_y + 16)], radius=8, fill=(15, 23, 42), outline=(30, 41, 59))
    draw.rounded_rectangle([(cx - 480, prog_y), (cx + 480, prog_y + 16)], radius=8, fill=(220, 38, 38))
    draw.text((cx, prog_y + 32), "INITIALIZATION COMPLETE — ALL SUBSYSTEMS SYNCHRONIZED", fill=(16, 185, 129), font=get_font(11, bold=True), anchor="mm")

    # Floating Bottom Subtitle Bar
    render_subtitle_bar(draw, scene["caption"])

    img.save(frame_path)

def render_subtitle_bar(draw: ImageDraw.Draw, caption_text: str):
    """Draws a floating sleek glass subtitle pill at the bottom with drop shadow."""
    cx = 960
    cy = 1032
    w = 1580
    h = 66
    x1, y1 = cx - w // 2, cy - h // 2
    x2, y2 = cx + w // 2, cy + h // 2

    # Translucent Dark Glass Pill
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=(7, 10, 17), outline=(40, 50, 70), width=1)
    # Glowing Crimson Top Highlight Line
    draw.line([(x1 + 10, y1 + 1), (x2 - 10, y1 + 1)], fill=(220, 38, 38), width=2)

    # Left Badge
    badge_x = x1 + 80
    draw.rounded_rectangle([(badge_x - 55, cy - 14), (badge_x + 55, cy + 14)], radius=4, fill=(76, 5, 5), outline=(185, 28, 28))
    draw.text((badge_x, cy), "AEGIS INTEL", fill=(248, 113, 113), font=get_font(11, bold=True), anchor="mm")

    # Subtitle Text (Crisp drop-shadow)
    caption_font = get_font(19, bold=True)
    draw.text((cx + 50 + 1, cy + 1), caption_text, fill=(0, 0, 0), font=caption_font, anchor="mm")
    draw.text((cx + 50, cy), caption_text, fill=(255, 255, 255), font=caption_font, anchor="mm")

def build_composed_frames():
    print("[AEGIS Video] Composing animated title banners, overlays, and glowing subtitles onto frames...")
    badge_font = get_font(13, bold=True)

    for scene in SCENES:
        frame_path = PROD_DIR / f"{scene['id']}_frame.png"

        if scene["type"] == "card":
            img = Image.new("RGB", (1920, 1080), color=(7, 10, 17))
            draw = ImageDraw.Draw(img)

            # Grid lines
            for x in range(0, 1920, 60):
                draw.line([(x, 0), (x, 1080)], fill=(15, 23, 42), width=1)
            for y in range(0, 1080, 60):
                draw.line([(0, y), (1920, y)], fill=(15, 23, 42), width=1)

            cx, cy = 960, 480
            w, h = 1180, 460
            draw.rectangle([(cx - w//2, cy - h//2), (cx + w//2, cy + h//2)], fill=(11, 15, 25), outline=(139, 0, 0), width=2)
            draw.rectangle([(cx - w//2, cy - h//2), (cx + w//2, cy - h//2 + 6)], fill=(220, 38, 38))

            # Badge
            draw.rounded_rectangle([(cx - 160, cy - 150), (cx + 160, cy - 118)], radius=6, fill=(76, 5, 5), outline=(185, 28, 28))
            draw.text((cx, cy - 134), scene["badge"], fill=(248, 113, 113), font=badge_font, anchor="mm")

            # Main Title & Subtitle
            draw.text((cx, cy - 50), scene["title"], fill=(255, 255, 255), font=get_font(66, bold=True), anchor="mm")
            draw.text((cx, cy + 25), scene["subtitle"], fill=(148, 163, 184), font=get_font(23, bold=False), anchor="mm")

            # Tech Stack Pills
            tags = ["FastAPI", "React + Vite", "PostGIS Spatial", "Nextflow DSL2", "NCBI AMRFinderPlus", "IQ-TREE", "MOB-suite", "WHO GLASS"]
            tag_x_start = cx - 510
            for i, tag in enumerate(tags):
                tx = tag_x_start + i * 145
                draw.rounded_rectangle([(tx - 65, cy + 110), (tx + 65, cy + 142)], radius=4, fill=(30, 41, 59), outline=(51, 65, 85))
                draw.text((tx, cy + 126), tag, fill=(226, 232, 240), font=get_font(12, bold=True), anchor="mm")

            render_subtitle_bar(draw, scene["caption"])

        elif scene["type"] == "loading":
            build_loading_matrix_frame(frame_path, scene)
            print(f"  Loading Matrix Frame created: {frame_path.name}")
            continue

        else:
            # Full Screen UI Walkthrough
            raw_image_path = ROOT_DIR / scene["image"]
            if raw_image_path.exists():
                img = Image.open(raw_image_path).convert("RGB")
            else:
                img = Image.new("RGB", (1920, 1080), color=(11, 15, 25))

            draw = ImageDraw.Draw(img)

            # Floating HUD Badge in Top Right (Leaves Navigation Header 100% visible)
            hud_text = scene.get("hud", "AEGIS 2.0 SURVEILLANCE")
            hud_w = 420
            hud_h = 36
            hx1 = 1920 - hud_w - 24
            hy1 = 14
            hx2 = 1920 - 24
            hy2 = hy1 + hud_h

            draw.rounded_rectangle([(hx1, hy1), (hx2, hy2)], radius=6, fill=(11, 15, 25), outline=(185, 28, 28), width=1)
            # Live Green Blinking Indicator
            draw.ellipse([(hx1 + 14, hy1 + 13), (hx1 + 24, hy1 + 23)], fill=(16, 185, 129))
            draw.text((hx1 + 34, hy1 + 10), hud_text, fill=(248, 113, 113), font=get_font(12, bold=True))
            draw.text((hx2 - 12, hy1 + 10), "1080p ULTRA HD", fill=(148, 163, 184), font=get_font(11, bold=True), anchor="ra")

            # Floating Subtitle Bar at Bottom
            render_subtitle_bar(draw, scene["caption"])

        img.save(frame_path)
        print(f"  Frame created: {frame_path.name}")

def get_audio_duration(audio_file: Path) -> float:
    cmd = [FFMPEG_EXE, "-i", str(audio_file), "-f", "null", "-"]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    for line in result.stderr.splitlines():
        if "Duration:" in line:
            time_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = time_str.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 9.5

def generate_srt_subtitles(durations: list) -> Path:
    srt_path = PROD_DIR / "aegis_promotional_video.srt"
    cur_time = 0.0
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, (scene, dur) in enumerate(zip(SCENES, durations)):
            start_s = cur_time
            end_s = cur_time + dur

            def fmt_time(t):
                hours = int(t // 3600)
                mins = int((t % 3600) // 60)
                secs = int(t % 60)
                millis = int(round((t - int(t)) * 1000))
                return f"{hours:02d}:{mins:02d}:{secs:02d},{millis:03d}"

            f.write(f"{i + 1}\n")
            f.write(f"{fmt_time(start_s)} --> {fmt_time(end_s)}\n")
            f.write(f"{scene['voice_text']}\n\n")
            cur_time += dur
    return srt_path

def compile_final_video():
    print("[AEGIS Video] Beginning Master Production & Compilation...")
    durations = []
    for scene in SCENES:
        audio_file = PROD_DIR / f"{scene['id']}.mp3"
        durations.append(get_audio_duration(audio_file) + 0.5)

    total_duration = sum(durations)
    synthesize_audio_effects(total_duration)

    whoosh_path = PROD_DIR / "whoosh_sfx.wav"
    segment_files = []

    for idx, (scene, duration) in enumerate(zip(SCENES, durations)):
        frame_file = PROD_DIR / f"{scene['id']}_frame.png"
        audio_file = PROD_DIR / f"{scene['id']}.mp3"
        segment_file = PROD_DIR / f"{scene['id']}_segment.mp4"
        scene_audio = PROD_DIR / f"{scene['id']}_mixed.wav"

        print(f"  Encoding segment {idx+1}/{len(SCENES)}: {scene['id']} ({duration:.2f}s)...")

        # Mix voiceover narration with transition whoosh at start
        mix_cmd = [
            FFMPEG_EXE,
            "-y",
            "-i", str(audio_file),
            "-i", str(whoosh_path),
            "-filter_complex",
            "[0:a]volume=1.0[v]; [1:a]volume=0.45[w]; [v][w]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "[aout]",
            "-ac", "2",
            str(scene_audio)
        ]
        subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # High-bitrate 1080p 30fps x264 CRF 16 (Razor sharp visuals & minor text)
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", str(frame_file),
            "-i", str(scene_audio),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "16",
            "-b:v", "10M",
            "-c:a", "aac",
            "-b:a", "256k",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-t", str(duration),
            "-vf", "scale=1920:1080,format=yuv420p",
            str(segment_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segment_files.append(segment_file)

    # Concat all segments
    concat_list = PROD_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for seg in segment_files:
            f.write(f"file '{seg.name}'\n")

    raw_combined = PROD_DIR / "raw_combined.mp4"
    concat_cmd = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(raw_combined)
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Master Soundtrack & Subtitle Layering
    ambient_path = PROD_DIR / "ambient_soundtrack.wav"
    output_video = ROOT_DIR / "aegis_promotional_video.mp4"
    srt_path = generate_srt_subtitles(durations)

    print(f"[AEGIS Video] Mastering ambient music, transition soundscape, and exporting final video...")
    final_cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", str(raw_combined),
        "-i", str(ambient_path),
        "-i", str(srt_path),
        "-filter_complex",
        "[0:a]volume=1.0[voice]; [1:a]volume=0.22[music]; [voice][music]amix=inputs=2:duration=first:dropout_transition=2[final_a]",
        "-map", "0:v",
        "-map", "[final_a]",
        "-map", "2:s?",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-c:s", "mov_text",
        "-metadata:s:s:0", "language=eng",
        str(output_video)
    ]
    subprocess.run(final_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[AEGIS Video] SUCCESS! Ultimate promotional video created at: {output_video}")
    print(f"  File Size: {output_video.stat().st_size / (1024*1024):.2f} MB")

async def main():
    await generate_voiceovers()
    build_composed_frames()
    compile_final_video()

if __name__ == "__main__":
    asyncio.run(main())

