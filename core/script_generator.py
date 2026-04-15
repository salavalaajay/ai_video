import logging
from typing import List

logger = logging.getLogger(__name__)


def generate_script(topic: str, video_type: str, duration: str, language: str) -> str:
    base: List[str] = [
        f"Welcome to this {video_type.lower()} video about {topic}.",
        f"Today we explore how {topic} impacts our lives.",
        f"Understanding {topic} is important in today's world.",
        f"It has many real world applications across industries.",
        f"There are challenges that need to be addressed carefully.",
        f"In the future, we expect rapid innovation in this area.",
        f"Thank you for watching and learning with us."
    ]

    duration_map = {"1 Minute": 150, "3 Minutes": 450, "5 Minutes": 750}
    target_words = duration_map.get(duration, 150)

    script = []
    total_words = 0
    i = 0

    while total_words < target_words:
        sentence = base[i % len(base)]
        word_count = len(sentence.split())

        if total_words + word_count > target_words:
            break

        script.append(sentence)
        total_words += word_count
        i += 1

    if len(script) < 3:
        logger.warning("Generated script too short, padding content")
        script.extend(base[:3])

    final_script = " ".join(script).strip()

    if not final_script:
        raise ValueError("Script generation failed")

    return final_script
