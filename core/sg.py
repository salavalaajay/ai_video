import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def split_into_scenes(script: str, min_words: int = 40) -> List[Dict]:
    if not script or not script.strip():
        raise ValueError("Empty script provided")

    sentences = re.split(r'(?<=[.!?।])\s+', script.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    scenes = []
    current = []
    word_count = 0
    scene_num = 1

    for sentence in sentences:
        words = len(sentence.split())

        if words == 0:
            continue

        current.append(sentence)
        word_count += words

        if word_count >= min_words:
            scene_text = " ".join(current).strip()

            if scene_text:
                scenes.append({
                    "scene_num": scene_num,
                    "text": scene_text
                })
                scene_num += 1

            current, word_count = [], 0

    if current:
        scene_text = " ".join(current).strip()
        if len(scene_text.split()) >= 5:
            scenes.append({
                "scene_num": scene_num,
                "text": scene_text
            })

    if not scenes:
        raise RuntimeError("Scene generation failed")

    logger.info(f"Generated {len(scenes)} scenes")
    return scenes
