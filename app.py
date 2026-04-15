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
        "Video Type",
        ["Educational", "Marketing", "Story"],
        horizontal=True
    )

    st.markdown("### Duration")
    duration = st.slider(
        "Duration (minutes)",
        1, 5, 2
    )

    duration_map = {
        1: "1 Minute",
        2: "2 Minutes",
        3: "3 Minutes",
        4: "4 Minutes",
        5: "5 Minutes"
    }

    duration_label = duration_map[duration]

    st.markdown("### Language")
    language = st.selectbox(
        "Language",
        ["English", "Hindi", "Spanish"]
    )

    generate_btn = st.button("✨ Generate Video")

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

    # Clean temp folders
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

            if not visuals or not audio or len(visuals) != len(audio):
                st.error("Scene mismatch error. Try again.")
                st.stop()

            safe_name = topic.replace(" ", "_").replace("/", "_")
            output = f"outputs/{safe_name}.mp4"

            assemble_video(visuals, audio, output)

            st.session_state.video_path = output
            st.success("✅ Video Generated Successfully!")

        except Exception as e:
            st.error(f"Error: {e}")
