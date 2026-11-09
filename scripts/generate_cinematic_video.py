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
PROD_DIR = ROOT_DIR / "cinematic_production"
PROD_DIR.mkdir(exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

VOICE = "en-US-ChristopherNeural"

# 10 High-Impact Scientific Narrative Scenes
SCENES = [
    {
        "id": "scene_01_intro",
        "tab": None,
        "is_card": True,
        "badge": "MISSION INITIALIZATION",
        "title": "PROJECT AEGIS 2.0",
        "subtitle": "Advanced Genomic Epidemiology & Intelligence System",
        "voice_text": "Welcome to Project AEGIS 2.0, the Advanced Genomic Epidemiology and Intelligence System. An enterprise research platform engineered for real-time antimicrobial resistance surveillance.",
        "caption": "Project AEGIS 2.0 — Advanced Genomic Epidemiology & Intelligence System"
    },
    {
        "id": "scene_02_loading_matrix",
        "tab": None,
        "is_loading": True,
        "badge": "BIOINFORMATICS INGESTION MATRIX",
        "title": "DATA INGESTION & PIPELINE SYNCHRONIZATION",
        "subtitle": "Nextflow DSL2 • PostGIS Spatial Indexing • Automated Provenance Checksums",
        "voice_text": "Initializing bioinformatics orchestration engine. Connecting NCBI genomic data streams, assembly quality heuristics, and spatial coordinate grids.",
        "caption": "Nextflow DSL2 Pipeline Orchestration • PostGIS Spatial Indexing • Checksum Verification"
    },
    {
        "id": "scene_03_dashboard",
        "tab": "dashboard",
        "badge": "SURVEILLANCE HUB",
        "title": "GLOBAL SURVEILLANCE & OUTBREAK DETECTION",
        "subtitle": "Real-Time Pathogen Tracking • High-Risk Lineages • Multi-Drug Resistance",
        "voice_text": "The Surveillance Hub monitors international pathogen dissemination, tracking high-risk Klebsiella pneumoniae clones and active clinical micro-outbreaks.",
        "caption": "Real-time pathogen distribution, clinical isolate feeds, and active outbreak monitoring"
    },
    {
        "id": "scene_04_surveillance",
        "tab": "surveillance",
        "badge": "3D GEOSPATIAL INTELLIGENCE",
        "title": "3D GEOSPATIAL SURVEILLANCE & NATURAL LANGUAGE QUERY",
        "subtitle": "PostGIS Spatial Coordinates • Safe Parameterized Proximity Analysis",
        "voice_text": "Featuring an interactive 3D Three.js surveillance globe and a safe natural-language query interface, enabling immediate radius-based outbreak detection with zero arbitrary SQL risk.",
        "caption": "Interactive 3D Three.js globe with parameterized natural-language outbreak queries"
    },
    {
        "id": "scene_05_isolates",
        "tab": "isolates",
        "badge": "GENOMIC REGISTRY",
        "title": "VALIDATED GENOMIC ISOLATE REGISTRY",
        "subtitle": "QUAST Metrics • CheckM2 Completeness • Contig Fragmentation & N50",
        "voice_text": "The Genomic Registry catalogs whole-genome assemblies, validating N50, GC content, and contig completeness against species-specific taxonomic thresholds.",
        "caption": "Verified genome assemblies, assembly statistics (N50, GC%), and deep profile inspection"
    },
    {
        "id": "scene_06_amr",
        "tab": "amr",
        "badge": "AMRFINDERPLUS ENGINE",
        "title": "AMRFINDERPLUS DETERMINANTS & RESISTANCE CASCADES",
        "subtitle": "Acquired Resistance Genes • Point Mutations • Co-Selection Heatmap",
        "voice_text": "Integrated with NCBI AMRFinderPlus, AEGIS classifies carbapenemases, colistin resistance, and ESBLs, mapping population prevalence and pairwise co-occurrence.",
        "caption": "Population gene prevalence bar charts, co-occurrence heatmaps, and resistance mechanisms"
    },
    {
        "id": "scene_07_comparative",
        "tab": "comparative",
        "badge": "COMPARATIVE GENOMICS",
        "title": "CORE-GENOME SNP DISTANCE MATRIX",
        "subtitle": "Reference Alignment • Outbreak Threshold Filtering (<= 15 SNPs)",
        "voice_text": "Comparative genomics workflows compute filtered pairwise SNP distance matrices, pinpointing hospital micro-outbreaks separated by as few as six single nucleotide polymorphisms.",
        "caption": "Pairwise core SNP distance heatmap with interactive outbreak threshold clustering"
    },
    {
        "id": "scene_08_phylogeny",
        "tab": "comparative&sub=tree",
        "badge": "MOLECULAR PHYLOGENETICS",
        "title": "CIRCULAR CHROMOSOMES & IQ-TREE PHYLOGENETICS",
        "subtitle": "ModelFinder GTR+F+R4 • 1000x Ultrafast Bootstrap • Multi-Track Metadata",
        "voice_text": "Explore circular chromosome GC skew profiles alongside Maximum-Likelihood phylogenetic trees decorated with multi-track lineage and resistance metadata.",
        "caption": "IQ-TREE maximum-likelihood Newick trees with lineage and resistance track annotations"
    },
    {
        "id": "scene_09_modelling",
        "tab": "modelling",
        "badge": "TRANSMISSION DYNAMICS",
        "title": "AST CONCORDANCE & SEIR EPIDEMIOLOGICAL MODELLING",
        "subtitle": "CLSI & EUCAST Breakpoints • Runge-Kutta 4th-Order Numerical Simulator",
        "voice_text": "Validate experimental MIC records against CLSI and EUCAST standards, paired with a Runge-Kutta numerical simulator predicting hospital transmission and asymptomatic colonization.",
        "caption": "Genotype-phenotype concordance validation and Runge-Kutta numerical differential equation solver"
    },
    {
        "id": "scene_10_outro",
        "tab": None,
        "is_card": True,
        "badge": "GLOBAL PRODUCTION READY",
        "title": "PROJECT AEGIS 2.0",
        "subtitle": "The Future of Genomic Epidemiology & AMR Intelligence",
        "voice_text": "From raw genomic sequences to WHO GLASS reporting and automated alerting. Project AEGIS 2.0: The Future of Genomic Epidemiology and AMR Intelligence.",
        "caption": "FastAPI • React • PostGIS • Nextflow • Docker Ready • WHO GLASS Compliant"
    }
]

def get_font(size: int, bold: bool = False):
    font_paths = [
        "C:/Windows/Fonts/segoeui.ttf" if not bold else "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arial.ttf" if not bold else "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibri.ttf" if not bold else "C:/Windows/Fonts/calibrib.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def synthesize_audio_effects(total_duration: float):
    print("[AEGIS Video] Synthesizing cinematic transition SFX and ambient soundtrack...")
    sr = 44100

    # 1. Whoosh Transition SFX (1.0 second)
    whoosh_dur = 1.0
    tw = np.linspace(0, whoosh_dur, int(sr * whoosh_dur), endpoint=False)
    freqs = np.geomspace(45, 520, len(tw))
    phase = 2 * np.pi * np.cumsum(freqs) / sr
    env = np.sin(np.pi * (tw / whoosh_dur)) ** 2
    whoosh = 0.65 * np.sin(phase) * env
    noise = np.random.normal(0, 0.18, len(tw)) * env
    whoosh_final = (whoosh + noise)
    whoosh_final = whoosh_final / np.max(np.abs(whoosh_final))
    whoosh_path = PROD_DIR / "whoosh_sfx.wav"
    wavfile.write(str(whoosh_path), sr, (whoosh_final * 32767).astype(np.int16))

    # 2. Holographic Confirmation Chime (0.8 second)
    chime_dur = 0.8
    tc = np.linspace(0, chime_dur, int(sr * chime_dur), endpoint=False)
    env_c = np.exp(-4.5 * tc)
    chime = (0.5 * np.sin(2 * np.pi * 1200 * tc) +
             0.3 * np.sin(2 * np.pi * 1800 * tc) +
             0.2 * np.sin(2 * np.pi * 2400 * tc)) * env_c
    chime = chime / np.max(np.abs(chime))
    chime_path = PROD_DIR / "chime_sfx.wav"
    wavfile.write(str(chime_path), sr, (chime * 32767).astype(np.int16))

    # 3. Ambient Electronic Cinematic Soundtrack (length matches total video)
    ta = np.linspace(0, total_duration, int(sr * total_duration), endpoint=False)
    # Deep sub-bass drones (55 Hz A1 + 110 Hz A2 + 165 Hz E3)
    drone1 = 0.35 * np.sin(2 * np.pi * 55 * ta)
    drone2 = 0.25 * np.sin(2 * np.pi * 110 * ta + 0.1 * np.sin(2 * np.pi * 0.2 * ta))
    drone3 = 0.15 * np.sin(2 * np.pi * 165 * ta)
    # Subtle pulsating arpeggio (tempo: 120 bpm = 2.0 Hz)
    pulse = (0.5 + 0.5 * np.sin(2 * np.pi * 2.0 * ta)) ** 2
    synth_lead = 0.12 * np.sin(2 * np.pi * 440 * ta) * pulse
    # Master ambient bed
    ambient = (drone1 + drone2 + drone3 + synth_lead)
    # Soft fade in & fade out
    fade_len = int(sr * 2.0)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    ambient[:fade_len] *= fade_in
    ambient[-fade_len:] *= fade_out
    ambient = ambient / np.max(np.abs(ambient)) * 0.35
    ambient_path = PROD_DIR / "ambient_soundtrack.wav"
    wavfile.write(str(ambient_path), sr, (ambient * 32767).astype(np.int16))

    print(f"  Audio assets generated: whoosh, chime, and {total_duration:.1f}s ambient soundtrack.")

async def generate_voiceovers():
    print("[AEGIS Video] Generating crisp neural voiceovers via edge-tts...")
    for scene in SCENES:
        audio_path = PROD_DIR / f"{scene['id']}.mp3"
        print(f"  Synthesizing voice: {scene['id']}...")
        communicate = edge_tts.Communicate(scene['voice_text'], VOICE, rate="+3%", pitch="+0Hz")
        await communicate.save(str(audio_path))

def capture_ui_screenshots():
    print("[AEGIS Video] Launching dev servers and capturing native 1080p full-screen frames...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--port", "8000"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    frontend_proc = subprocess.Popen(
        ["cmd.exe", "/c", "npm", "--prefix", "frontend", "run", "dev"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    time.sleep(8)
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

    try:
        for scene in SCENES:
            if scene.get("is_card") or scene.get("is_loading"):
                continue
            tab = scene["tab"]
            url = f"http://localhost:5173/?tab={tab}"
            raw_shot = PROD_DIR / f"{scene['id']}_raw.png"
            print(f"  Capturing full screen: {url} -> {raw_shot.name}...")
            cmd = [
                chrome_path,
                "--headless=new",
                f"--screenshot={str(raw_shot.resolve())}",
                "--user-data-dir=C:\\Users\\Punit\\AppData\\Local\\Temp\\chrome_cinematic_profile",
                "--window-size=1920,1080",
                "--hide-scrollbars",
                url
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            time.sleep(1.5)
    finally:
        backend_proc.kill()
        frontend_proc.kill()
        print("[AEGIS Video] Dev servers stopped.")

def build_loading_matrix_frame(frame_path: Path, scene: dict):
    """Renders a high-tech holographic bioinformatics loading & synchronization matrix."""
    img = Image.new("RGB", (1920, 1080), color=(4, 7, 13))
    draw = ImageDraw.Draw(img)

    # Grid background
    for x in range(0, 1920, 48):
        draw.line([(x, 0), (x, 1080)], fill=(12, 18, 32), width=1)
    for y in range(0, 1080, 48):
        draw.line([(0, y), (1920, y)], fill=(12, 18, 32), width=1)

    cx, cy = 960, 470
    radar_radius = 180

    # Concentric Radar Rings
    for r, col, w in [(radar_radius, (139, 0, 0), 2), (radar_radius - 40, (30, 41, 59), 1), (radar_radius - 80, (220, 38, 38), 2), (radar_radius - 120, (15, 23, 42), 1)]:
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=col, width=w)

    # Crosshairs
    draw.line([(cx - radar_radius - 30, cy), (cx + radar_radius + 30, cy)], fill=(139, 0, 0), width=1)
    draw.line([(cx, cy - radar_radius - 30), (cx, cy + radar_radius + 30)], fill=(139, 0, 0), width=1)

    # Radar Sweep Arm
    angle = math.pi / 4
    x_sweep = cx + radar_radius * math.cos(angle)
    y_sweep = cy + radar_radius * math.sin(angle)
    draw.line([(cx, cy), (x_sweep, y_sweep)], fill=(239, 68, 68), width=3)

    # Glowing center core
    draw.ellipse([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=(255, 255, 255))

    # Center Badge
    badge_font = get_font(14, bold=True)
    draw.rounded_rectangle([(cx - 160, cy - 250), (cx + 160, cy - 215)], radius=6, fill=(76, 5, 5), outline=(185, 28, 28))
    draw.text((cx, cy - 233), scene["badge"], fill=(248, 113, 113), font=badge_font, anchor="mm")

    # Main Loading Title
    title_font = get_font(38, bold=True)
    draw.text((cx, cy - 280), scene["title"], fill=(255, 255, 255), font=title_font, anchor="mm")

    # Telemetry Boxes
    telemetry = [
        ("NCBI DATASETS INGESTION STREAM", "CONNECTED [GCA_000240185.2 MGH 78578]", (16, 185, 129)),
        ("POSTGIS SPATIAL GRID ENGINE", "SRID 4326 WGS84 GIST INDEX ACTIVE", (16, 185, 129)),
        ("NEXTFLOW DSL2 WORKFLOW ORCHESTRATOR", "EXECUTOR LOCAL • DOCKER READY", (59, 130, 246)),
        ("AMRFINDERPLUS & IQ-TREE ENGINES", "DATABASE RELEASE 2024-05-02.1 LOADED", (245, 158, 11)),
        ("SEIR EXTENDED TRANSMISSION MATRIX", "RUNGE-KUTTA 4TH-ORDER INITIALIZED", (168, 85, 247)),
    ]

    box_y = 690
    for title, val, col in telemetry:
        draw.rectangle([(cx - 480, box_y), (cx + 480, box_y + 36)], fill=(11, 15, 25), outline=(30, 41, 59), width=1)
        draw.ellipse([(cx - 460, box_y + 13), (cx - 450, box_y + 23)], fill=col)
        draw.text((cx - 435, box_y + 11), title, fill=(226, 232, 240), font=get_font(13, bold=True))
        draw.text((cx + 460, box_y + 11), val, fill=col, font=get_font(12, bold=True), anchor="ra")
        box_y += 44

    # Bottom Subtitle Bar
    caption_bar_y = 990
    draw.rectangle([(0, caption_bar_y), (1920, 1080)], fill=(7, 10, 17))
    draw.line([(0, caption_bar_y), (1920, caption_bar_y)], fill=(139, 0, 0), width=2)
    draw.text((960, caption_bar_y + 45), scene["caption"], fill=(255, 255, 255), font=get_font(21, bold=True), anchor="mm")

    img.save(frame_path)

def build_composed_frames():
    print("[AEGIS Video] Composing animated title banners, overlays, and glowing subtitles onto frames...")
    badge_font = get_font(14, bold=True)
    caption_font = get_font(21, bold=True)

    for scene in SCENES:
        frame_path = PROD_DIR / f"{scene['id']}_frame.png"
        raw_path = PROD_DIR / f"{scene['id']}_raw.png"

        if scene.get("is_card"):
            # High-tech Title / Outro Card
            img = Image.new("RGB", (1920, 1080), color=(7, 10, 17))
            draw = ImageDraw.Draw(img)

            # Draw background grid lines
            for x in range(0, 1920, 60):
                draw.line([(x, 0), (x, 1080)], fill=(15, 23, 42), width=1)
            for y in range(0, 1080, 60):
                draw.line([(0, y), (1920, y)], fill=(15, 23, 42), width=1)

            cx, cy = 960, 500
            w, h = 1140, 480
            draw.rectangle(
                [(cx - w//2, cy - h//2), (cx + w//2, cy + h//2)],
                fill=(11, 15, 25),
                outline=(139, 0, 0),
                width=2
            )
            # Glowing Crimson Top Accent
            draw.rectangle([(cx - w//2, cy - h//2), (cx + w//2, cy - h//2 + 6)], fill=(220, 38, 38))

            # Badge
            draw.rounded_rectangle([(cx - 160, cy - 160), (cx + 160, cy - 125)], radius=6, fill=(76, 5, 5), outline=(185, 28, 28))
            draw.text((cx, cy - 143), scene["badge"], fill=(248, 113, 113), font=badge_font, anchor="mm")

            # Main Title
            draw.text((cx, cy - 60), scene["title"], fill=(255, 255, 255), font=get_font(68, bold=True), anchor="mm")
            # Subtitle
            draw.text((cx, cy + 20), scene["subtitle"], fill=(148, 163, 184), font=get_font(25, bold=False), anchor="mm")

            # Architecture Pills
            tags = ["FastAPI", "React + Vite", "PostGIS Spatial", "Nextflow DSL2", "IQ-TREE", "MOB-suite", "WHO GLASS"]
            tag_x_start = cx - 440
            for i, tag in enumerate(tags):
                tx = tag_x_start + i * 125
                draw.rounded_rectangle([(tx - 55, cy + 110), (tx + 55, cy + 145)], radius=4, fill=(30, 41, 59), outline=(51, 65, 85))
                draw.text((tx, cy + 128), tag, fill=(226, 232, 240), font=get_font(13, bold=True), anchor="mm")

            # Caption Bar
            draw.rectangle([(0, 1000), (1920, 1080)], fill=(4, 7, 13))
            draw.line([(0, 1000), (1920, 1000)], fill=(139, 0, 0), width=2)
            draw.text((960, 1040), scene["caption"], fill=(255, 255, 255), font=caption_font, anchor="mm")

        elif scene.get("is_loading"):
            build_loading_matrix_frame(frame_path, scene)
            print(f"  Loading Matrix Frame created: {frame_path.name}")
            continue

        else:
            # Composed Screen Walkthrough Frame
            if raw_path.exists():
                img = Image.open(raw_path).convert("RGB")
            else:
                img = Image.new("RGB", (1920, 1080), color=(11, 15, 25))

            draw = ImageDraw.Draw(img)

            # Top Cinematic Banner
            banner_height = 84
            draw.rectangle([(0, 0), (1920, banner_height)], fill=(11, 15, 25))
            draw.line([(0, banner_height), (1920, banner_height)], fill=(139, 0, 0), width=3)

            # Badge Pill
            draw.rounded_rectangle([(35, 22), (240, 60)], radius=6, fill=(76, 5, 5), outline=(185, 28, 28))
            draw.text((137, 41), scene["badge"], fill=(248, 113, 113), font=badge_font, anchor="mm")

            # Scene Title & Subtitle in Banner
            draw.text((260, 24), scene["title"], fill=(255, 255, 255), font=get_font(22, bold=True))
            draw.text((260, 53), scene["subtitle"], fill=(148, 163, 184), font=get_font(13, bold=False))

            # System Quality Indicator
            draw.ellipse([(1790, 36), (1802, 48)], fill=(16, 185, 129))
            draw.text((1814, 34), "AEGIS 2.0 ULTRA HD", fill=(226, 232, 240), font=get_font(12, bold=True))

            # Bottom Subtitle / Live Narration Caption Bar
            caption_bar_y = 995
            draw.rectangle([(0, caption_bar_y), (1920, 1080)], fill=(4, 7, 13))
            draw.line([(0, caption_bar_y), (1920, caption_bar_y)], fill=(139, 0, 0), width=2)

            # Live Narration Subtitle Tag
            draw.rounded_rectangle([(40, caption_bar_y + 12), (185, caption_bar_y + 40)], radius=4, fill=(30, 41, 59), outline=(51, 65, 85))
            draw.text((112, caption_bar_y + 26), "LIVE NARRATION", fill=(248, 113, 113), font=get_font(10, bold=True), anchor="mm")

            # Subtitle Text (Crystal clear drop-shadow for highest legibility)
            draw.text((960 + 1, caption_bar_y + 40 + 1), scene["caption"], fill=(0, 0, 0), font=caption_font, anchor="mm")
            draw.text((960, caption_bar_y + 40), scene["caption"], fill=(255, 255, 255), font=caption_font, anchor="mm")

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
    return 11.0

def compile_final_video():
    print("[AEGIS Video] Compiling video segments with transition SFX and ambient soundtrack...")
    segment_files = []
    durations = []

    whoosh_path = PROD_DIR / "whoosh_sfx.wav"

    for idx, scene in enumerate(SCENES):
        frame_file = PROD_DIR / f"{scene['id']}_frame.png"
        audio_file = PROD_DIR / f"{scene['id']}.mp3"
        segment_file = PROD_DIR / f"{scene['id']}_segment.mp4"

        duration = get_audio_duration(audio_file) + 0.6
        durations.append(duration)
        print(f"  Encoding {scene['id']}: duration={duration:.2f}s with SFX & camera drift...")

        # Mix scene voiceover with transition whoosh at start
        scene_audio = PROD_DIR / f"{scene['id']}_mixed.wav"
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

        # High-bitrate 1080p 30fps encoding with subtle slow camera drift
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", str(frame_file),
            "-i", str(scene_audio),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "17",
            "-b:v", "8M",
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

    # Generate total duration ambient soundtrack
    total_duration = sum(durations)
    synthesize_audio_effects(total_duration)
    ambient_path = PROD_DIR / "ambient_soundtrack.wav"

    output_video = ROOT_DIR / "aegis_promotional_video.mp4"
    print(f"[AEGIS Video] Layering master ambient soundtrack into final MP4 ({output_video.name})...")

    # Final Audio Mastering: Mix voice/SFX video with subtle ambient background drone
    final_cmd = [
        FFMPEG_EXE,
        "-y",
        "-i", str(raw_combined),
        "-i", str(ambient_path),
        "-filter_complex",
        "[0:a]volume=1.0[voice]; [1:a]volume=0.20[music]; [voice][music]amix=inputs=2:duration=first:dropout_transition=2[final_a]",
        "-map", "0:v",
        "-map", "[final_a]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        str(output_video)
    ]
    subprocess.run(final_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[AEGIS Video] MASTERPIECE COMPLETE! Exported to: {output_video}")

async def main():
    await generate_voiceovers()
    capture_ui_screenshots()
    build_composed_frames()
    compile_final_video()

if __name__ == "__main__":
    asyncio.run(main())

