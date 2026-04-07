from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import os

def assemble_video(visual_paths, audio_paths, output_path="final_video.mp4"):
    """
    Visual frames and voiceover are synchronized and merged using MoviePy
    to produce the final MP4 video.
    """
    clips = []
    
    for img_path, audio_path in zip(visual_paths, audio_paths):
        # Load audio clip to determine the exact duration needed for the image slide
        audio_clip = AudioFileClip(audio_path)
        
        # Set image clip duration to match the spoken audio duration
        img_clip = ImageClip(img_path)
        
        # MoviePy v2 compatibility: uses with_duration and with_audio
        if hasattr(img_clip, 'with_duration'):
            img_clip = img_clip.with_duration(audio_clip.duration)
            img_clip = img_clip.with_audio(audio_clip)
        else:
            img_clip = img_clip.set_duration(audio_clip.duration)
            img_clip = img_clip.set_audio(audio_clip)
            
        clips.append(img_clip)
        
    # Concatenate all scenes into one continuous video
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Write the result to a file
    # We use low fps (24) and simple codecs to ensure quick generation
    final_clip.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        logger=None # Suppress MoviePy progress bar in Streamlit
    )
    
    # Clean up file handles from memory
    for clip in clips:
        if hasattr(clip, 'close'):
            clip.close()
    if hasattr(final_clip, 'close'):
        final_clip.close()
    
    return output_path