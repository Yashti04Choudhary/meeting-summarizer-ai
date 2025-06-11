import streamlit as st
import os
from transcribe_audio import transcribe_audio
from summarize_text import summarize_text
from audio_recorder import AudioRecorder
import time
from datetime import datetime

def initialize_session_state():
    """Initialize session state variables"""
    if 'recorder' not in st.session_state:
        st.session_state.recorder = AudioRecorder()
    if 'recorded_file' not in st.session_state:
        st.session_state.recorded_file = None
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"

def apply_theme_css():
    """Apply theme-specific CSS with consistent dark theme"""
    # Define theme colors with warmer, more balanced palette
    light_theme_colors = {
        "background": "#ffffff",
        "text": "#2d3748",
        "secondary_bg": "#faf9f7",
        "border": "#e9ecef",
        "accent1": "#7c3aed",  # Purple
        "accent2": "#e11d48",  # Rose
        "success": "#059669",  # Emerald
        "warning": "#d97706",  # Amber
        "error": "#dc2626",    # Red
        "gradient1": "#9333ea", # Purple
        "gradient2": "#db2777",  # Pink
        "title_gradient1": "#ff6b6b",  # Warm Coral
        "title_gradient2": "#e11d48",  # Rose
        "title_gradient3": "#7c3aed",   # Purple
        "label_text": "#1a1625"  # Dark text for labels in light theme
    }
    
    dark_theme_colors = {
        "background": "#1a1625",
        "text": "#e2e8f0",
        "secondary_bg": "#2d283e",
        "border": "#3f3951",
        "accent1": "#a855f7",  # Light Purple
        "accent2": "#f43f5e",  # Light Rose
        "success": "#10b981",  # Light Emerald
        "warning": "#f59e0b",  # Light Amber
        "error": "#ef4444",    # Light Red
        "gradient1": "#a855f7", # Light Purple
        "gradient2": "#ec4899",  # Light Pink
        "title_gradient1": "#ff8080",  # Light Coral
        "title_gradient2": "#f43f5e",  # Light Rose
        "title_gradient3": "#a855f7",   # Light Purple
        "label_text": "#e2e8f0"  # Light text for labels in dark theme
    }

    # Get current theme colors
    colors = dark_theme_colors if st.session_state.theme == "dark" else light_theme_colors
    
    custom_css = f"""
        <style>
        /* Global theme styles */
        .stApp {{
            background: {colors['background']} !important;
            color: {colors['text']} !important;
        }}

        /* Ensure all text elements use theme text color */
        .stMarkdown, 
        .stText, 
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stMultiselect label,
        .stSlider label,
        .stFileUploader label,
        [data-testid="stWidgetLabel"],
        [data-testid="stHeader"],
        .streamlit-expanderHeader,
        .stRadio label,
        .stCheckbox label,
        .stExpander {{
            color: {colors['label_text']} !important;
        }}

        /* Dark theme specific overrides */
        [data-testid="stSidebar"] [data-testid="stMarkdown"] p,
        [data-testid="stSidebar"] [data-testid="stMarkdown"] span {{
            color: {colors['label_text']} !important;
        }}

        /* Ensure tab labels are visible */
        .stTabs [data-baseweb="tab"] {{
            color: {colors['label_text']} !important;
        }}

        /* Style headers and titles */
        h1, h2, h3, h4, h5, h6 {{
            color: {colors['label_text']} !important;
        }}

        /* Style expander text */
        .streamlit-expanderContent {{
            color: {colors['label_text']} !important;
        }}

        /* Rest of your existing CSS */
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        .block-container {{
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }}

        [data-testid="stSidebar"] {{
            width: 16rem !important;
            background: {colors['secondary_bg']} !important;
            border-right: 1px solid {colors['border']} !important;
            margin-right: 2rem !important;
        }}

        [data-testid="stSidebar"] > div {{
            width: 16rem !important;
            background: {colors['secondary_bg']} !important;
        }}

        .main {{
            padding-left: 3rem !important;
        }}

        section[data-testid="stSidebarContent"] {{
            padding-right: 2rem !important;
        }}

        .header-section {{
            text-align: center !important;
            padding: 2rem !important;
            background: {colors['secondary_bg']} !important;
            border: 1px solid {colors['border']} !important;
            border-radius: 0.75rem !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            margin: 0 5rem !important;
        }}

        .stTabs {{
            padding: 0 5rem !important;
            margin-top: 1rem !important;
            margin-left: 2rem !important;
        }}

        .stTabs [data-baseweb="tab-panel"] {{
            padding: 1rem 0 !important;
        }}

        .stTabs [data-baseweb="tab-panel"] > div {{
            background: {colors['secondary_bg']} !important;
            border: 1px solid {colors['border']} !important;
            border-radius: 0.75rem !important;
            padding: 2rem !important;
        }}

        .main-title {{
        color: orange !important;  # Change this line
        font-weight: 800 !important;
        font-size: 3.2em !important;
        margin: 0 0 0.5rem 0 !important;
        text-align: center !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        line-height: 1.2 !important;
        }}

        .subtitle {{
            color: {colors['text']} !important;
            font-size: 1.5em !important;
            font-weight: 500 !important;
            margin: 0.5rem 0 1.5rem 0 !important;
            opacity: 0.9 !important;
        }}

        .quote-section {{
            font-style: italic !important;
            opacity: 0.85 !important;
            max-width: 800px !important;
            margin: 0 auto !important;
            color: {colors['text']} !important;
        }}

        .results-section {{
            width: 100% !important;
            padding: 2rem !important;
            background: {colors['secondary_bg']} !important;
            border: 1px solid {colors['border']} !important;
            border-radius: 0.75rem !important;
            margin: 2rem 0 !important;
        }}

        .stButton > button {{
            background: linear-gradient(120deg, {colors['accent1']}, {colors['accent2']}) !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            border-radius: 0.5rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1) !important;
            opacity: 0.95 !important;
        }}

        [data-testid="stFileUploader"] {{
            background: {colors['background']} !important;
            border: 2px dashed {colors['border']} !important;
            color: {colors['label_text']} !important;
            padding: 1rem !important;
            border-radius: 0.5rem !important;
        }}

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background: {colors['background']} !important;
            color: {colors['text']} !important;
            border-color: {colors['border']} !important;
        }}

        .stAlert {{
            background: {colors['background']} !important;
            color: {colors['text']} !important;
            border-left: 4px solid {colors['accent1']} !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            border-radius: 0.25rem !important;
        }}

        /* Status text and recording indicator */
        .recording-status {{
            color: {colors['label_text']} !important;
            font-weight: 500 !important;
        }}

        /* File upload status and info text */
        .upload-info {{
            color: {colors['label_text']} !important;
            font-size: 0.9em !important;
        }}

        /* Ensure all status messages are visible */
        [data-testid="stStatusWidget"] {{
            color: {colors['label_text']} !important;
        }}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="MeetingMind - Your Meeting Memory Keeper",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    apply_theme_css()
    
    # Sidebar settings
    with st.sidebar:
        st.title("⚙️ Settings")
        theme_emoji = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(f"{theme_emoji} Switch to {'Dark' if st.session_state.theme == 'light' else 'Light'} Theme", key="theme_toggle"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

    # Main content - removed the outer main-content-wrapper div
    st.markdown('''
        <div class="header-section">
            <h1 class="main-title">🧠 MeetingMind</h1>
            <h2 class="subtitle">Because Life's Too Short to Remember Every Meeting Detail</h2>
            <div class="quote-section">
                <p>"Another meeting that could've been an email?" 😩<br>
                "Did I zone out during the important part?" 😴<br>
                "Wait, what were my action items again?" 😅</p>
                <p>We feel you! Meetings can be like trying to drink from a firehose while juggling flaming torches... 
                on a unicycle... in a hurricane. 🌪️</p>
                <p><strong>But fear not, fellow meeting survivor!</strong> 🦸‍♂️</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Create tabs for different input methods
    input_tab1, input_tab2 = st.tabs(["📂 Upload Audio", "🎙️ Record Meeting"])
    
    with input_tab1:
        st.write("Drop your meeting recording here and let AI do the heavy lifting!")
        st.info("📝 You can upload audio files up to 25MB. For reference:\n" + 
                "- WAV files: ~5 minutes\n" + 
                "- MP3 files (128kbps): ~25-30 minutes\n" + 
                "- M4A files: ~20-25 minutes\n" + 
                "\nPro tip: If your file is larger, consider converting it to MP3 first! 🎯", icon="ℹ️")
        
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=["wav", "mp3", "m4a", "ogg"],
            help="Supported formats: WAV, MP3, M4A, OGG"
        )
        
        if uploaded_file is not None:
            # Check file size
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 25:
                st.error(f"❌ File size ({file_size_mb:.1f}MB) exceeds the 25MB limit. Please upload a smaller file or convert to a compressed format like MP3.")
            else:
                st.audio(uploaded_file)
                
                if st.button("🚀 Process Audio", key="process_upload", use_container_width=True):
                    try:
                        # Save uploaded file
                        with st.spinner("Saving uploaded file..."):
                            with open("uploaded_audio.wav", "wb") as f:
                                f.write(uploaded_file.getbuffer())
                        
                        # Process the audio
                        process_audio_file("uploaded_audio.wav")
                        
                        # Clean up
                        try:
                            os.remove("uploaded_audio.wav")
                        except:
                            pass
                            
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.write("Please try again or contact support if the problem persists.")

    with input_tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.write("Record your meeting directly and get an AI-powered transcription and summary.")
        st.info("ℹ️ You can record up to 5 minutes of audio to stay within the 25MB limit.", icon="⏱️")
        
        # Add status information
        status = st.session_state.recorder.get_status()
        with st.expander("🔧 Recording Status", expanded=True):
            st.write(f"Recording active: {status['is_recording']}")
            st.write(f"Frames captured: {status['frames_captured']}")
            if status['error']:
                st.error(f"Error: {status['error']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not status['is_recording']:
                if st.button("🎙️ Start Recording", use_container_width=True):
                    if st.session_state.recorder.start_recording():
                        st.success("Recording started!")
                        st.rerun()
                    else:
                        st.error(f"Failed to start recording: {st.session_state.recorder.error}")
            else:
                if st.button("⏹️ Stop Recording", use_container_width=True):
                    filename = st.session_state.recorder.stop_recording()
                    if filename:
                        st.session_state.recorded_file = filename
                        st.success("✅ Recording saved!")
                        st.rerun()
                    else:
                        st.error(f"Failed to save recording: {st.session_state.recorder.error}")
        
        with col2:
            if status['is_recording']:
                st.markdown("""
                    <div style='text-align: center;'>
                        <div style='color: #FF4B4B; animation: blink 1s infinite;'>
                            🔴 Recording in progress...
                        </div>
                    </div>
                    <style>
                        @keyframes blink {
                            50% { opacity: 0.5; }
                        }
                    </style>
                """, unsafe_allow_html=True)
        
        # Display recorded audio and processing options
        if st.session_state.recorded_file and os.path.exists(st.session_state.recorded_file):
            st.markdown("---")
            st.subheader("📼 Recorded Audio")
            
            try:
                st.audio(st.session_state.recorded_file)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    with open(st.session_state.recorded_file, "rb") as f:
                        st.download_button(
                            "💾 Save Recording",
                            f.read(),
                            file_name=st.session_state.recorded_file,
                            mime="audio/wav",
                            key="download_recording",
                            use_container_width=True
                        )
                
                with col2:
                    if st.button("🚀 Generate Summary", key="process_recording", use_container_width=True):
                        process_audio_file(st.session_state.recorded_file)
            
            except Exception as e:
                st.error(f"Error loading audio file: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

def process_audio_file(audio_path):
    """Process an audio file to generate transcript and summary"""
    try:
        # Transcription progress
        with st.spinner("🎯 Transcribing audio... This may take a few minutes."):
            success = transcribe_audio(audio_path)
            if not success:
                st.error("❌ Error during transcription. Please try again.")
                return
            
            st.success("✅ Transcription completed!")
        
        # Summarization progress
        with st.spinner("📝 Generating summary..."):
            success = summarize_text("transcript.txt", "summary.txt")
            if not success:
                st.error("❌ Error during summarization. Please try again.")
                return
            
            st.success("✅ Summary generated!")
        
        # Create a new card for results
        st.markdown("""
            <div style="height: 2rem;"></div>
            <div class="main-content-wrapper">
                <h3 style="color: inherit; margin-bottom: 1rem; padding: 1rem; border-bottom: 1px solid var(--border-color);">
                    🎯 Analysis Results
                </h3>
        """, unsafe_allow_html=True)
        
        # Display results in tabs
        result_tab1, result_tab2 = st.tabs(["📝 Transcription", "📋 Summary"])
        
        with result_tab1:
            st.markdown('<p class="results-header">Full Transcript</p>', unsafe_allow_html=True)
            with open("transcript.txt", "r", encoding="utf-8") as f:
                transcript = f.read()
                st.text_area(
                    label="",
                    value=transcript,
                    height=400,
                    help="The complete transcription of your audio file"
                )
                st.download_button(
                    "📥 Download Transcript",
                    transcript,
                    file_name="transcript.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        with result_tab2:
            st.markdown('<p class="results-header">Summary</p>', unsafe_allow_html=True)
            with open("summary.txt", "r", encoding="utf-8") as f:
                summary = f.read()
                st.text_area(
                    label="",
                    value=summary,
                    height=400,
                    help="AI-generated summary with key points"
                )
                st.download_button(
                    "📥 Download Summary",
                    summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Close the results card
        st.markdown('</div>', unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.write("Please try again or contact support if the problem persists.")

if __name__ == "__main__":
    main() 