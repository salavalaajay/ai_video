import streamlit as st
import os
import shutil
from utils.script_generator import generate_script, split_into_scenes
from utils.visual_generator import create_scene_visuals
from utils.voice_generator import generate_voiceover
from utils.video_assembler import assemble_video

# --- STREAMLIT APP CONFIGURATION ---
st.set_page_config(page_title="Script to Screen", page_icon="🎬", layout="wide")

st.title("🎬 Script to Screen: Automated Video Generation")
st.markdown("An Agentic AI-Based Video Generation Platform.")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("OpenAI API Key (Optional for Demo)", type="password")
st.sidebar.info("💡 If no API key is provided, the system will use a mock generator to demonstrate the agentic workflow without hitting API limits.")

# Main Input Section
st.subheader("1. Video Preferences")
col1, col2, col3, col4 = st.columns(4)
with col1:
    topic = st.text_input("📝 Topic", "Solar Energy")
with col2:
    video_type = st.selectbox("🎯 Video Type", ["Educational", "Marketing", "Storytelling"])
with col3:
    duration = st.selectbox("⏱️ Duration", ["1 Minute", "3 Minutes", "5 Minutes"])
with col4:
    language = st.selectbox("🌐 Language", ["English", "Spanish", "French", "Hindi", "German"])

if st.button("🚀 Generate Video", type="primary"):
    # Clean up previous temp assets
    if os.path.exists("temp_assets"):
        shutil.rmtree("temp_assets")
        
    with st.status("🤖 Agent Planning Tasks...", expanded=True) as status:
        try:
            # STEP 1: Script Generation
            st.write(f"📝 **Step 1: Generating Script in {language}...**")
            script = generate_script(topic, video_type, duration, language, api_key)
            st.success("Script generated successfully!")
            with st.expander("View Generated Script"):
                st.write(script)
            
            # STEP 2: Scene Segmentation
            st.write("✂️ **Step 2: Splitting into Scenes...**")
            scenes = split_into_scenes(script)
            st.success(f"Divided script into {len(scenes)} scenes.")
            
            # STEP 3: Visual Generation
            st.write("🖼️ **Step 3: Creating Scene Visuals...**")
            visual_paths = create_scene_visuals(scenes, topic)
            st.success("Slide visuals generated successfully!")
            
            # STEP 4: Voice Synthesis
            st.write(f"🎙️ **Step 4: Generating {language} Voiceover...**")
            audio_paths = generate_voiceover(scenes, language)
            st.success("Text-to-Speech (TTS) completed!")
            
            # STEP 5: Video Assembly
            st.write("🎞️ **Step 5: Assembling Final Video...**")
            final_video_path = assemble_video(visual_paths, audio_paths)
            st.success("Video and audio merged successfully using MoviePy!")
            
            status.update(label="Video Generation Complete!", state="complete", expanded=False)
            
            # Output Display
            st.subheader("🎉 Final Output")
            st.video(final_video_path)
            
            with open(final_video_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download MP4 Video",
                    data=file,
                    file_name=f"{topic.replace(' ', '_')}_video.mp4",
                    mime="video/mp4"
                )
        except Exception as e:
            status.update(label="An error occurred during generation", state="error", expanded=True)
            st.error(f"Error during execution: {str(e)}")