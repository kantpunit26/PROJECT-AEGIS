import os
import sys
import time
import subprocess
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import imageio_ffmpeg

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "video_production"
OUTPUT_DIR.mkdir(exist_ok=True)
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

VOICE = "en-US-ChristopherNeural"

SCENES = [
    {
        "id": "scene_01_intro",
        "tab": None,
        "is_card": True,
        "title": "PROJECT AEGIS",
        "subtitle": "Advanced Genomic Epidemiology & Intelligence System",
        "badge": "AMR SURVEILLANCE PLATFORM",
        "voice_text": "Welcome to Project AEGIS, the Advanced Genomic Epidemiology and Intelligence System. Designed from the ground up for high-priority antimicrobial resistance surveillance.",
        "caption": "Project AEGIS — Advanced Genomic Epidemiology & Intelligence System"
    },
    {
        "id": "scene_02_dashboard",
        "tab": "dashboard",
        "is_card": False,
        "title": "GLOBAL SURVEILLANCE HUB",
        "subtitle": "Real-Time Pathogen Tracking • Outbreak Detection • Multi-Drug Resistance",
        "badge": "SURVEILLANCE HUB",
        "voice_text": "At its core, AEGIS connects global pathogen data with interactive 3D geospatial intelligence, tracking high-risk Klebsiella pneumoniae clones and carbapenemase dissemination.",
        "caption": "Real-time pathogen distribution, clinical isolate feeds, and active outbreak monitoring"
    },
    {
        "id": "scene_03_surveillance",
        "tab": "surveillance",
        "is_card": False,
        "title": "GEOSPATIAL INTELLIGENCE & NL QUERY",
        "subtitle": "PostGIS Spatial Indexing • Safe Parameterized Proximity Analysis",
        "badge": "3D GEOSPATIAL INTELLIGENCE",
        "voice_text": "Equipped with a safe natural-language query interface, epidemiologists can immediately detect active micro-outbreaks within kilometers of any hospital center, with zero arbitrary SQL execution.",
        "caption": "Interactive 3D Three.js surveillance globe with parameterized natural-language outbreak queries"
    },
    {
        "id": "scene_04_amr",
        "tab": "amr",
        "is_card": False,
        "title": "GENOMIC REGISTRY & AMR DETERMINANTS",
        "subtitle": "NCBI AMRFinderPlus Integration • Acquired Genes & Point Mutations",
        "badge": "AMRFINDERPLUS ENGINE",
        "voice_text": "Explore verified genome assemblies with quality control flags, AMRFinderPlus determinant prevalence, and co-occurrence matrices for carbapenemases, colistin resistance, and ESBLs.",
        "caption": "Population gene prevalence bar charts, co-occurrence heatmaps, and resistance mechanisms"
    },
    {
        "id": "scene_05_comparative",
        "tab": "comparative",
        "is_card": False,
        "title": "COMPARATIVE GENOMICS & CORE SNPS",
        "subtitle": "Core-Genome SNP Distance Matrix • IQ-TREE Maximum Likelihood",
        "badge": "COMPARATIVE GENOMICS",
        "voice_text": "AEGIS performs reference-guided core-genome SNP calling, pairwise distance heatmaps with outbreak threshold clustering, and maximum-likelihood phylogenetics.",
        "caption": "Pairwise core SNP distance heatmap, outbreak clustering threshold, and IQ-TREE phylogeny"
    },
    {
        "id": "scene_06_modelling",
        "tab": "modelling",
        "is_card": False,
        "title": "AST CONCORDANCE & SEIR MODELLING",
        "subtitle": "CLSI & EUCAST Breakpoints • Runge-Kutta Numerical Dynamics",
        "badge": "TRANSMISSION DYNAMICS",
        "voice_text": "Clinical MIC records are benchmarked against CLSI and EUCAST standards, paired with a deterministic Runge-Kutta numerical simulator predicting hospital transmission and asymptomatic colonization.",
        "caption": "Genotype-phenotype concordance validation and Runge-Kutta numerical differential equation solver"
    },
    {
        "id": "scene_07_outro",
        "tab": None,
        "is_card": True,
        "title": "PROJECT AEGIS",
        "subtitle": "The Future of Genomic Epidemiology & AMR Intelligence",
        "badge": "REPRODUCIBLE RESEARCH",
        "voice_text": "Empowering molecular epidemiology with Docker reproducibility, PostGIS spatial indexing, and WHO GLASS reporting. Project AEGIS: The Future of Genomic Intelligence.",
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

async def generate_voiceovers():
    print("[AEGIS Video] Generating neural voiceovers via edge-tts...")
    for idx, scene in enumerate(SCENES):
        audio_path = OUTPUT_DIR / f"{scene['id']}.mp3"
        print(f"  Generating voice for {scene['id']}...")
        communicate = edge_tts.Communicate(scene['voice_text'], VOICE, rate="+3%", pitch="+0Hz")
        await communicate.save(str(audio_path))

def capture_ui_screenshots():
    print("[AEGIS Video] Launching background servers and capturing UI screenshots...")
    # 1. Start Backend & Frontend Dev Server
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--port", "8000"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    frontend_proc = subprocess.Popen(
        ["cmd.exe", "/c", "npm", "--prefix", "frontend", "run", "dev"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    
    time.sleep(8) # Wait for Vite and FastAPI to bind
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

    try:
        for scene in SCENES:
            if scene["is_card"]:
                continue
            tab = scene["tab"]
            url = f"http://localhost:5173/?tab={tab}"
            raw_shot = OUTPUT_DIR / f"{scene['id']}_raw.png"
            print(f"  Capturing UI: {url} -> {raw_shot.name}...")
            cmd = [
                chrome_path,
                "--headless=new",
                f"--screenshot={str(raw_shot.resolve())}",
                "--user-data-dir=C:\\Users\\Punit\\AppData\\Local\\Temp\\chrome_vid_profile",
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

def build_composed_frames():
    print("[AEGIS Video] Composing animated title banners, overlays, and captions onto frames...")
    title_font = get_font(42, bold=True)
    sub_font = get_font(20, bold=False)
    badge_font = get_font(15, bold=True)
    caption_font = get_font(22, bold=True)

    for scene in SCENES:
        frame_path = OUTPUT_DIR / f"{scene['id']}_frame.png"
        raw_path = OUTPUT_DIR / f"{scene['id']}_raw.png"

        if scene["is_card"]:
            # High-tech Title / Outro Card
            img = Image.new("RGB", (1920, 1080), color=(7, 10, 17))
            draw = ImageDraw.Draw(img)

            # Draw background grid lines
            for x in range(0, 1920, 60):
                draw.line([(x, 0), (x, 1080)], fill=(15, 23, 42), width=1)
            for y in range(0, 1080, 60):
                draw.line([(0, y), (1920, y)], fill=(15, 23, 42), width=1)

            # Center Card Container
            cx, cy = 960, 500
            w, h = 1100, 460
            draw.rectangle(
                [(cx - w//2, cy - h//2), (cx + w//2, cy + h//2)],
                fill=(11, 15, 25),
                outline=(139, 0, 0),
                width=2
            )

            # Crimson Top Bar
            draw.rectangle(
                [(cx - w//2, cy - h//2), (cx + w//2, cy - h//2 + 6)],
                fill=(220, 38, 38)
            )

            # Badge
            badge_text = scene["badge"]
            draw.rounded_rectangle([(cx - 150, cy - 150), (cx + 150, cy - 115)], radius=6, fill=(76, 5, 5), outline=(185, 28, 28))
            draw.text((cx, cy - 133), badge_text, fill=(248, 113, 113), font=badge_font, anchor="mm")

            # Main Title
            draw.text((cx, cy - 50), scene["title"], fill=(255, 255, 255), font=get_font(68, bold=True), anchor="mm")
            
            # Subtitle
            draw.text((cx, cy + 25), scene["subtitle"], fill=(148, 163, 184), font=get_font(26, bold=False), anchor="mm")

            # Feature Pillars / Architecture Tags
            tags = ["FastAPI", "React + Vite", "PostGIS Spatial", "Nextflow Pipelines", "IQ-TREE", "MOB-suite", "WHO GLASS"]
            tag_x_start = cx - 440
            for i, tag in enumerate(tags):
                tx = tag_x_start + i * 125
                draw.rounded_rectangle([(tx - 55, cy + 110), (tx + 55, cy + 145)], radius=4, fill=(30, 41, 59), outline=(51, 65, 85))
                draw.text((tx, cy + 128), tag, fill=(226, 232, 240), font=get_font(13, bold=True), anchor="mm")

        else:
            # Composed Screen Walkthrough Frame
            if raw_path.exists():
                img = Image.open(raw_path).convert("RGB")
            else:
                img = Image.new("RGB", (1920, 1080), color=(11, 15, 25))

            draw = ImageDraw.Draw(img)

            # Top Cinematic Banner
            banner_height = 80
            draw.rectangle([(0, 0), (1920, banner_height)], fill=(11, 15, 25))
            draw.line([(0, banner_height), (1920, banner_height)], fill=(139, 0, 0), width=3)

            # Badge Pill
            draw.rounded_rectangle([(40, 22), (230, 58)], radius=6, fill=(76, 5, 5), outline=(185, 28, 28))
            draw.text((135, 40), scene["badge"], fill=(248, 113, 113), font=badge_font, anchor="mm")

            # Scene Title & Subtitle in Banner
            draw.text((250, 26), scene["title"], fill=(255, 255, 255), font=get_font(22, bold=True))
            draw.text((250, 52), scene["subtitle"], fill=(148, 163, 184), font=get_font(14, bold=False))

            # System Indicator
            draw.ellipse([(1820, 36), (1832, 48)], fill=(16, 185, 129))
            draw.text((1842, 34), "AEGIS LIVE", fill=(226, 232, 240), font=get_font(13, bold=True))

            # Bottom Subtitle / Narration Caption Bar
            caption_bar_y = 1000
            draw.rectangle([(0, caption_bar_y), (1920, 1080)], fill=(7, 10, 17))
            draw.line([(0, caption_bar_y), (1920, caption_bar_y)], fill=(30, 41, 59), width=1)
            draw.text((960, caption_bar_y + 40), scene["caption"], fill=(255, 255, 255), font=caption_font, anchor="mm")

        img.save(frame_path)
        print(f"  Frame created: {frame_path.name}")

def get_audio_duration(audio_file: Path) -> float:
    cmd = [
        FFMPEG_EXE,
        "-i", str(audio_file),
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    for line in result.stderr.splitlines():
        if "Duration:" in line:
            time_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = time_str.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 6.0

def compile_final_video():
    print("[AEGIS Video] Compiling video segments and merging with neural audio via FFmpeg...")
    segment_files = []

    for scene in SCENES:
        frame_file = OUTPUT_DIR / f"{scene['id']}_frame.png"
        audio_file = OUTPUT_DIR / f"{scene['id']}.mp3"
        segment_file = OUTPUT_DIR / f"{scene['id']}_segment.mp4"

        duration = get_audio_duration(audio_file) + 0.6 # Add comfortable pause
        print(f"  Encoding {scene['id']}: duration={duration:.2f}s...")

        # Encode static frame with audio to MP4 with subtle slow zoom (Ken Burns)
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", str(frame_file),
            "-i", str(audio_file),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-t", str(duration),
            "-vf", "scale=1920:1080,format=yuv420p",
            str(segment_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segment_files.append(segment_file)

    # Concat file list
    concat_list = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for seg in segment_files:
            f.write(f"file '{seg.name}'\n")

    output_video = ROOT_DIR / "aegis_promotional_video.mp4"
    print(f"[AEGIS Video] Merging segments into final production MP4: {output_video.name}...")

    concat_cmd = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(output_video)
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[AEGIS Video] SUCCESS! Promotional video exported to {output_video}")

async def main():
    await generate_voiceovers()
    capture_ui_screenshots()
    build_composed_frames()
    compile_final_video()

if __name__ == "__main__":
    asyncio.run(main())
