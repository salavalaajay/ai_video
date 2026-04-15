import os, asyncio, edge_tts, re, logging

logger = logging.getLogger(__name__)


async def _generate_audio(text, voice, path):
    text = re.sub(r'\s+', ' ', text).strip()

    try:
        tts = edge_tts.Communicate(text, voice)
        await tts.save(path)

        if not os.path.exists(path) or os.path.getsize(path) < 100:
            raise RuntimeError("Invalid audio")

    except Exception as e:
        logger.error(f"Audio generation failed: {e}")

        with open(path, "wb") as f:
            f.write(b"\x00\x00")


def generate_voiceover(scenes, language, output_dir="temp_assets"):
    os.makedirs(output_dir, exist_ok=True)

    voice_map = {
        "English": "en-US-AriaNeural",
        "Hindi": "hi-IN-SwaraNeural",
        "Spanish": "es-ES-ElviraNeural"
    }

    voice = voice_map.get(language, "en-US-AriaNeural")
    paths = []

    async def run():
        tasks = []
        for s in scenes:
            path = os.path.join(output_dir, f"audio_{s['scene_num']}.mp3")
            paths.append(path)
            tasks.append(_generate_audio(s['text'], voice, path))
        await asyncio.gather(*tasks)

    try:
        asyncio.run(run())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())

    for p in paths:
        if not os.path.exists(p):
            raise RuntimeError(f"Missing audio: {p}")

    return paths
