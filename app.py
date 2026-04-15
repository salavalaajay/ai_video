<<<<<<< HEAD
<<<<<<< HEAD
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
=======
import streamlit as st
import os, shutil

from core.script_generator import generate_script
from core.sg import split_into_scenes
from core.v1 import create_scene_visuals
from core.v2 import generate_voiceover
from core.v3 import assemble_video

st.set_page_config(page_title="Script to Screen", layout="wide")

st.title("🎬 Script to Screen")

topic = st.text_input("Topic", "Solar Energy")
video_type = st.selectbox("Type", ["Educational", "Marketing", "Story"])
duration = st.selectbox("Duration", ["1 Minute", "3 Minutes", "5 Minutes"])
language = st.selectbox("Language", ["English", "Hindi", "Spanish"])

if st.button("Generate Video"):

    # Clean temp
    if os.path.exists("temp_assets"):
        shutil.rmtree("temp_assets")

    os.makedirs("temp_assets", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    with st.spinner("Generating video..."):

        script = generate_script(topic, video_type, duration, language)
        scenes = split_into_scenes(script)
        visuals = create_scene_visuals(scenes, topic)
        audio = generate_voiceover(scenes, language)

        output = f"outputs/{topic.replace(' ', '_')}.mp4"
        assemble_video(visuals, audio, output)

    st.success("Video Generated!")
    st.video(output)
>>>>>>> 43bbe316785669a311c6ac506acfc4f4a132fab9
=======
import streamlit as st
import os, shutil

from core.script_generator import generate_script
from core.sg import split_into_scenes
from core.v1 import create_scene_visuals
from core.v2 import generate_voiceover
from core.v3 import assemble_video

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Script to Screen", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
body {
    background-color: #0e0e0e;
    color: white;
}
.main {
    background-color: #0e0e0e;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: #1a1a1a;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #2a2a2a;
}
.title {
    font-size: 42px;
    font-weight: bold;
}
.subtitle {
    color: #aaa;
    margin-bottom: 20px;
}
.stButton>button {
    background-color: #ff7a00;
    color: white;
    border-radius: 10px;
    padding: 10px;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="title">🎬 Script to Screen</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform any topic into a full video — script, visuals & voice</div>', unsafe_allow_html=True)

# -------------------- LAYOUT --------------------
left, right = st.columns([1, 2])

# -------------------- LEFT PANEL --------------------
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    topic = st.text_input("Topic", placeholder="e.g. How black holes are formed")

    st.markdown("### Video Type")
    video_type = st.radio(
        "",
        ["Educational", "Marketing", "Story"],
        horizontal=True
    )

    st.markdown("### Duration")
    duration = st.slider("", 1, 5, 2)
    duration_map = {1: "1 Minute", 2: "3 Minutes", 5: "5 Minutes"}
    duration_label = duration_map.get(duration, "1 Minute")

    st.markdown("### Language")
    language = st.selectbox("", ["English", "Hindi", "Spanish"])

    generate_btn = st.button("✨ Generate Video")

    st.markdown("</div>", unsafe_allow_html=True)

    # How it works
    st.markdown('<div class="card" style="margin-top:20px;">', unsafe_allow_html=True)
    st.markdown("### ⚙️ How it works")
    st.markdown("""
    1. Script Generation  
    2. Scene Segmentation  
    3. Visual Creation  
    4. Voice Synthesis  
    5. Video Assembly  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- RIGHT PANEL --------------------
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if "video_path" in st.session_state:
        st.video(st.session_state.video_path)
    else:
        st.markdown("""
        <div style='text-align:center; padding:100px; color:#777;'>
        ▶️ Your video will appear here<br><br>
        Fill the form and click Generate
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- GENERATION LOGIC --------------------
if generate_btn:

    if not topic:
        st.error("Please enter a topic")
        st.stop()

    if os.path.exists("temp_assets"):
        shutil.rmtree("temp_assets")

    os.makedirs("temp_assets", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    with st.spinner("Generating video..."):

        try:
            script = generate_script(topic, video_type, duration_label, language)
            scenes = split_into_scenes(script)
            visuals = create_scene_visuals(scenes, topic)
            audio = generate_voiceover(scenes, language)

            if len(visuals) != len(audio):
                st.error("Mismatch in visuals and audio")
                st.stop()

            output = f"outputs/{topic.replace(' ', '_')}.mp4"

            assemble_video(visuals, audio, output)

            st.session_state.video_path = output
            st.success("✅ Video Generated!")

        except Exception as e:
            st.error(f"Error: {e}")
>>>>>>> 7a4006e9d54cd7e3d858f74953a100824b2349ba
