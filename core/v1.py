from PIL import Image, ImageDraw, ImageFont
import os, requests, urllib.parse, random, time, textwrap, logging
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

# -------------------- SIMPLE CACHE (SPEED BOOST) --------------------
_image_cache = {}


def _generate_single_image(scene, topic, output_dir, retries=3):
    path = os.path.join(output_dir, f"scene_{scene['scene_num']}.jpg")

    if path in _image_cache and os.path.exists(path):
        return path

    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(retries):
        try:
            prompt = f"{scene['text']}, {topic}, cinematic lighting, ultra realistic"
            url = (
                "https://image.pollinations.ai/prompt/"
                + urllib.parse.quote(prompt)
                + f"?width=1280&height=720&seed={random.randint(1,99999)}"
            )

            time.sleep(0.8 + attempt * 1.5)

            r = requests.get(url, headers=headers, timeout=50)

            if r.status_code == 200 and len(r.content) > 1000:
                img = Image.open(BytesIO(r.content)).convert("RGB")

                img = img.resize((1280, 720), Image.Resampling.LANCZOS)
                img.save(path, "JPEG", quality=95)

                _image_cache[path] = True
                return path

        except Exception as e:
            logger.warning(f"Scene {scene['scene_num']} attempt {attempt+1} failed: {e}")

    # ---------------- FALLBACK ----------------
    logger.warning(f"Fallback image for scene {scene['scene_num']}")

    img = Image.new("RGB", (1280, 720), (15, 15, 20))
    draw = ImageDraw.Draw(img)

    text = textwrap.fill(scene["text"], 45)

    try:
        font = ImageFont.load_default()
    except:
        font = None

    draw.text((60, 300), text, fill="white", font=font)

    img.save(path, "JPEG", quality=90)
    return path


# -------------------- MAIN FUNCTION (PARALLEL BOOSTED) --------------------
def create_scene_visuals(scenes, topic, output_dir="temp_assets", retries=3):
    os.makedirs(output_dir, exist_ok=True)

    paths = [None] * len(scenes)

    # Run up to 4 images at same time (FAST)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(_generate_single_image, scene, topic, output_dir, retries): i
            for i, scene in enumerate(scenes)
        }

        for future in as_completed(futures):
            idx = futures[future]
            try:
                paths[idx] = future.result()
            except Exception as e:
                logger.error(f"Scene {idx} failed completely: {e}")

    # Final safety check
    for i, p in enumerate(paths):
        if not p or not os.path.exists(p):
            raise RuntimeError(f"Image generation failed for scene {i}")

    return paths
