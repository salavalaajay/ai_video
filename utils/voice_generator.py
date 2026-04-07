import os
import asyncio
import edge_tts

async def _generate_audio(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_voiceover(scenes, language, output_dir="temp_assets"):
    """
    The complete script is converted into speech using Microsoft Edge TTS (Neural Voices).
    Each scene gets an individual audio file for synchronization.
    """
    os.makedirs(output_dir, exist_ok=True)
    audio_paths = []
    
    # Map the selected language to a high-quality realistic neural voice
    # These are free and do not require an API key
    voice_map = {
        "English": "en-US-AriaNeural",
        "Spanish": "es-ES-ElviraNeural",
        "French": "fr-FR-DeniseNeural",
        "Hindi": "hi-IN-SwaraNeural",
        "German": "de-DE-AmalaNeural"
    }
    
    # Fallback to English if something goes wrong
    voice = voice_map.get(language, "en-US-AriaNeural")
    
    # Setup asyncio loop to run the async edge-tts functions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    for scene in scenes:
        text = scene['text']
        path = os.path.join(output_dir, f"audio_{scene['scene_num']}.mp3")
        
        # Run the generation
        loop.run_until_complete(_generate_audio(text, voice, path))
        
        audio_paths.append(path)
        
    loop.close()
    return audio_paths