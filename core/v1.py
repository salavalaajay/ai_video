from PIL import Image, ImageDraw, ImageFont
import os, requests, urllib.parse, random, time, textwrap, logging

logger = logging.getLogger(__name__)


def create_scene_visuals(scenes, topic, output_dir="temp_assets", retries=3):
    os.makedirs(output_dir, exist_ok=True)
    paths = []

    headers = {'User-Agent': 'Mozilla/5.0'}

    for scene in scenes:
        path = os.path.join(output_dir, f"scene_{scene['scene_num']}.jpg")
        success = False

        for attempt in range(retries):
            try:
                prompt = f"{scene['text']}, {topic}, cinematic lighting"
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1280&height=720&seed={random.randint(1,99999)}"

                time.sleep(1)
                r = requests.get(url, headers=headers, timeout=20)

                if r.status_code == 200 and len(r.content) > 1000:
                    with open(path, "wb") as f:
                        f.write(r.content)

                    img = Image.open(path)
                    img.verify()
                    success = True
                    break

            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed: {e}")

        if not success:
            logger.warning(f"Fallback image for scene {scene['scene_num']}")

            img = Image.new("RGB", (1280, 720), (20, 20, 25))
            draw = ImageDraw.Draw(img)

            text = textwrap.fill(scene['text'], 40)

            try:
                font = ImageFont.load_default()
            except:
                font = None

            draw.text((50, 250), text, fill="white", font=font)
            img.save(path)

        if not os.path.exists(path):
            raise RuntimeError(f"Image creation failed: {path}")

        paths.append(path)

    return paths
