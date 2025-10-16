import streamlit as st
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Speech Recognition App", layout="wide")

st.title("🎤 Speech Recognition App")
st.write("Simple speech to text converter!")

# Initialize session state
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# Try to import speech recognition
try:
    import speech_recognition as sr
    sr_available = True
except ImportError:
    sr_available = False
    st.error("⚠️ Speech Recognition not available on this system")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Selection
    st.subheader("1. Choose API")
    api_choice = st.radio(
        "Select API:",
        ["Google Speech Recognition", "CMU Sphinx"],
        help="Google needs internet, CMU Sphinx works offline"
    )
    
    # Language Selection
    st.subheader("2. Choose Language")
    language_dict = {
        "English": "en-US",
        "Spanish": "es-ES",
        "French": "fr-FR",
        "German": "de-DE",
    }
    selected_language = st.selectbox(
        "Select language:",
        list(language_dict.keys())
    )
    language_code = language_dict[selected_language]

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("3. Recording")
    
    if sr_available:
        if st.button("🔴 Record Audio", use_container_width=True):
            try:
                recognizer = sr.Recognizer()
                
                with sr.Microphone() as source:
                    st.info(f"🎤 Listening in {selected_language}...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=10)
                
                st.info("Processing...")
                
                if api_choice == "Google Speech Recognition":
                    try:
                        text = recognizer.recognize_google(audio, language=language_code)
                        st.session_state.transcribed_text += " " + text
                        st.success("✅ Transcribed successfully!")
                    except sr.UnknownValueError:
                        st.error("❌ Could not understand. Speak clearly please.")
                    except sr.RequestError as e:
                        st.error(f"❌ Internet error: {str(e)}")
                
                else:  # CMU Sphinx
                    try:
                        text = recognizer.recognize_sphinx(audio)
                        st.session_state.transcribed_text += " " + text
                        st.success("✅ Transcribed successfully!")
                    except sr.UnknownValueError:
                        st.error("❌ Could not understand. Speak clearly please.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Microphone error: {str(e)}")
    else:
        st.warning("Speech Recognition not available. Install: pip install SpeechRecognition")
    
    st.subheader("4. Your Text")
    text_area = st.text_area(
        "Transcribed text:",
        value=st.session_state.transcribed_text,
        height=200
    )
    st.session_state.transcribed_text = text_area

with col2:
    st.subheader("Actions")
    
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.transcribed_text = ""
        st.rerun()
    
    if st.button("📋 Copy", use_container_width=True):
        st.info("Ready to paste!")
    
    st.subheader("Save")
    if st.button("💾 Save File", use_container_width=True):
        if st.session_state.transcribed_text.strip():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transcription_{timestamp}.txt"
            
            try:
                with open(filename, "w") as f:
                    f.write(st.session_state.transcribed_text)
                st.success(f"✅ Saved: {filename}")
            except Exception as e:
                st.error(f"❌ Save error: {str(e)}")
        else:
            st.warning("No text to save")

st.markdown("---")
st.markdown("""
### How to use:
1. Choose API and language
2. Click "Record Audio"
3. Speak clearly (10 seconds max)
4. Text will appear below
5. Save or clear as needed
""")
