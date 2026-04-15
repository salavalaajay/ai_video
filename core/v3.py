from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
import os

def assemble_video(images, audios, output_path="output.mp4"):
    """
    Combines images and audio into a final video.
    Each image is shown for the duration of its corresponding audio.
    """

    clips = []
    audio_clips = []
    final_video = None

    try:
        for img, aud in zip(images, audios):
            try:
                audio_clip = AudioFileClip(aud)
                clip = ImageClip(img)
                clip = clip.set_duration(audio_clip.duration)
                clip = clip.resize(newsize=(1280, 720))
                clip = clip.set_audio(audio_clip)

                audio_clips.append(audio_clip)
                clips.append(clip)

            except Exception as e:
                print(f"Error processing {img}: {e}")

        if not clips:
            raise ValueError("No clips were created. Check input images/audio.")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )
        return output_path
    finally:
        if final_video is not None:
            final_video.close()
        for clip in clips:
            clip.close()
        for audio_clip in audio_clips:
            audio_clip.close()
