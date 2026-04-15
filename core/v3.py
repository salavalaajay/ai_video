from pathlib import Path
from typing import Iterable, List, Tuple
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
import logging

logger = logging.getLogger(__name__)


def assemble_video(
    images: Iterable[str],
    audios: Iterable[str],
    output_path: str = "output.mp4",
    size: Tuple[int, int] = (1280, 720),
    fps: int = 24,
) -> str:

    images = list(images)
    audios = list(audios)

    if len(images) != len(audios):
        raise ValueError("Images and audio mismatch")

    clips = []

    for i, (img, aud) in enumerate(zip(images, audios), start=1):
        img_path = Path(img)
        aud_path = Path(aud)

        if not img_path.exists() or not aud_path.exists():
            raise FileNotFoundError(f"Missing file at index {i}")

        try:
            audio = AudioFileClip(str(aud_path))

            if audio.duration <= 0:
                raise ValueError("Invalid audio duration")

            clip = (
                ImageClip(str(img_path))
                .resize(height=size[1])
                .set_duration(audio.duration)
                .set_audio(audio)
            )

            clips.append(clip)

        except Exception as e:
            logger.error(f"Clip error {i}: {e}")
            raise

    final = concatenate_videoclips(clips, method="compose")

    final.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

    final.close()
    for c in clips:
        c.close()

    if not Path(output_path).exists():
        raise RuntimeError("Video creation failed")

    logger.info("Video created successfully")
    return output_path
