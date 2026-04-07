from PIL import Image, ImageDraw
import os
import requests
import urllib.parse
import random
import time

def create_scene_visuals(scenes, topic, output_dir="temp_assets"):
    """
    For each scene, an image is generated based on the script text and topic.
    This acts as the visual creation module of the Agentic AI.
    """
    os.makedirs(output_dir, exist_ok=True)
    visual_paths = []
    
    # We clean the topic string to make sure it's a good search keyword
    search_keyword = urllib.parse.quote(topic.strip())
    
    for scene in scenes:
        path = os.path.join(output_dir, f"scene_{scene['scene_num']}.jpg")
        
        success = False
        
        # Attempt 1: True AI Generation (Pollinations)
        # AI understands context better (e.g. "Gym" = "Fitness Center", not a basketball court)
        try:
            # We add context words to ensure it doesn't give a literal stock photo interpretation
            ai_prompt = f"{topic}, cinematic, high quality, professional photography"
            encoded_ai = urllib.parse.quote(ai_prompt)
            seed = random.randint(1, 100000)
            ai_url = f"https://image.pollinations.ai/prompt/{encoded_ai}?width=1280&height=720&nologo=true&seed={seed}"
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            time.sleep(1.5) # Gentle pause to prevent 429
            
            response = requests.get(ai_url, headers=headers, timeout=20)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
                success = True
        except Exception as e:
            print(f"AI Generation failed for scene {scene['scene_num']}: {e}")
            
        # Attempt 2: Fallback to Stock Photos (LoremFlickr)
        if not success:
            try:
                print("Falling back to Flickr Stock Photos...")
                flickr_url = f"https://loremflickr.com/1280/720/{search_keyword}?lock={random.randint(1, 1000)}"
                response = requests.get(flickr_url, headers=headers, timeout=15, allow_redirects=True)
                if response.status_code == 200:
                    with open(path, 'wb') as f:
                        f.write(response.content)
                    success = True
            except Exception as e:
                print(f"Flickr fallback failed: {e}")
                
        # Attempt 3: Ultimate Fallback (Dark background)
        if not success:
            img = Image.new('RGB', (1280, 720), color=(30, 34, 43))
            d = ImageDraw.Draw(img)
            d.text((100, 360), f"Topic: {topic} (Image fetch failed)", fill=(255, 255, 255))
            img.save(path)
            
        visual_paths.append(path)
        
    return visual_paths