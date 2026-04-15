from PIL import Image, ImageDraw, ImageFont
import os, requests, urllib.parse, random, time, textwrap, logging
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

_image_cache = {}


def _build_prompt(scene, topic):
    return (
        f"{topic}. "
        f"{scene['text']}. "
        "cinematic lighting, ultra realistic, 4k, detailed, depth of field, film still"
    )


def _try_generate(url, headers, timeout):
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200 and len(r.content) > 1000:
            return r.content
    except:
        return None
    return None


def _generate_image(scene, topic, output_dir, retries=3):
    path = os.path.join(output_dir, f"scene_{scene['scene_num']}.jpg")

    if path in _image_cache and os.path.exists(path):
        return path

    headers = {"User-Agent": "Mozilla/5.0"}

    prompt = _build_prompt(scene, topic)

    urls = [
        f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1280&height=720&seed={random.randint(1,99999)}",
        f"https://pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1280&height=720&seed={random.randint(1,99999)}"
    ]

    for attempt in range(retries):
        for url in urls:
            time.sleep(1 + attempt)

            content = _try_generate(url, headers, timeout=70)

            if content:
                img = Image.open(BytesIO(content)).convert("RGB")
                img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                img.save(path, "JPEG", quality=95)

                _image_cache[path] = True
                return path

    # ---------------- FALLBACK (HIGH QUALITY TEXT SCENE) ----------------
    logger.warning(f"Fallback image for scene {scene['scene_num']}")

    img = Image.new("RGB", (1280, 720), (10, 10, 15))
    draw = ImageDraw.Draw(img)

    title = f"Scene {scene['scene_num']}"
    text = textwrap.fill(scene["text"], 45)

    draw.text((60, 80), title, fill="white")
    draw.text((60, 180), text, fill="white")

    img.save(path, "JPEG", quality=90)
    return path


def create_scene_visuals(scenes, topic, output_dir="temp_assets", retries=3):
    os.makedirs(output_dir, exist_ok=True)

    paths = [None] * len(scenes)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(_generate_image, scene, topic, output_dir, retries): i
            for i, scene in enumerate(scenes)
        }

        for future in as_completed(futures):
            idx = futures[future]
            try:
                paths[idx] = future.result()
            except Exception as e:
                logger.error(f"Scene {idx} failed: {e}")

    for i, p in enumerate(paths):
        if not p or not os.path.exists(p):
            raise RuntimeError(f"Scene {i} failed completely")

    return paths
