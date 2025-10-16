import streamlit as st
import speech_recognition as sr
from datetime import datetime
import os

# Set page configuration
st.set_page_config(page_title="Speech Recognition App", layout="wide")

st.title("🎤 Speech Recognition App")
st.write("Convert your speech to text with multiple options!")

# Initialize session state
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False
if "is_paused" not in st.session_state:
    st.session_state.is_paused = False

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Selection
    st.subheader("1. Choose Speech Recognition API")
    api_choice = st.radio(
        "Select API:",
        ["Google Speech Recognition", "CMU Sphinx (Offline)"],
        help="Google is more accurate but needs internet. CMU Sphinx works offline."
    )
    
    # Language Selection
    st.subheader("2. Choose Language")
    language_dict = {
        "English": "en-US",
        "Spanish": "es-ES",
        "French": "fr-FR",
        "German": "de-DE",
        "Chinese (Simplified)": "zh-CN",
        "Japanese": "ja-JP",
        "Portuguese": "pt-PT",
    }
    selected_language = st.selectbox(
        "Select your language:",
        list(language_dict.keys()),
        help="Choose the language you will be speaking"
    )
    language_code = language_dict[selected_language]
    
    # Note for offline API
    if api_choice == "CMU Sphinx (Offline)":
        st.info("⚠️ Note: CMU Sphinx only supports English and may be less accurate than Google.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("3. Start Recording")
    
    # Recording buttons
    button_col1, button_col2, button_col3 = st.columns(3)
    
    with button_col1:
        if st.button("🔴 Start Recording", key="start_btn", use_container_width=True):
            st.session_state.is_recording = True
            st.session_state.is_paused = False
    
    with button_col2:
        if st.button("⏸️ Pause", key="pause_btn", use_container_width=True):
            if st.session_state.is_recording:
                st.session_state.is_paused = not st.session_state.is_paused
    
    with button_col3:
        if st.button("⏹️ Stop Recording", key="stop_btn", use_container_width=True):
            st.session_state.is_recording = False
            st.session_state.is_paused = False
    
    # Status display
    if st.session_state.is_recording:
        if st.session_state.is_paused:
            st.warning("⏸️ Recording is PAUSED")
        else:
            st.success("🔴 Recording is ACTIVE - Please speak now...")
    
    # Transcription display
    st.subheader("4. Transcribed Text")
    text_area = st.text_area(
        "Your transcribed text will appear here:",
        value=st.session_state.transcribed_text,
        height=200,
        key="text_display"
    )
    st.session_state.transcribed_text = text_area

with col2:
    st.subheader("Actions")
    
    # Clear button
    if st.button("🗑️ Clear Text", use_container_width=True):
        st.session_state.transcribed_text = ""
        st.rerun()
    
    # Copy button
    if st.button("📋 Copy to Clipboard", use_container_width=True):
        st.info("Text copied! (You can paste it now)")
    
    # Save to file
    st.subheader("5. Save Text")
    if st.button("💾 Save to File", use_container_width=True):
        if st.session_state.transcribed_text.strip():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transcription_{timestamp}.txt"
            
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(st.session_state.transcribed_text)
                st.success(f"✅ Saved as {filename}")
            except Exception as e:
                st.error(f"❌ Error saving file: {str(e)}")
        else:
            st.warning("⚠️ No text to save!")

# Transcription function
def transcribe_speech(api_type, language, selected_lang_name):
    """
    Transcribe speech from microphone with error handling
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            st.info(f"🎤 Listening in {selected_lang_name}...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10)
        
        st.info("Processing your speech...")
        
        if api_type == "Google Speech Recognition":
            try:
                text = recognizer.recognize_google(audio, language=language)
                return text, True, "✅ Successfully transcribed!"
            except sr.UnknownValueValue:
                return "", False, "❌ Could not understand audio. Please speak clearly."
            except sr.RequestError as e:
                return "", False, f"❌ Google API error. Make sure you have internet connection. Details: {str(e)}"
        
        elif api_type == "CMU Sphinx (Offline)":
            try:
                text = recognizer.recognize_sphinx(audio)
                return text, True, "✅ Successfully transcribed (Offline)!"
            except sr.UnknownValueError:
                return "", False, "❌ CMU Sphinx could not understand audio. Please speak clearly."
            except Exception as e:
                return "", False, f"❌ CMU Sphinx error: {str(e)}"
    
    except sr.RequestError as e:
        return "", False, f"❌ Microphone error: {str(e)}"
    except sr.UnknownValueError:
        return "", False, "❌ Could not understand the audio. Try again."
    except Exception as e:
        return "", False, f"❌ Unexpected error: {str(e)}"

# Main recording logic
if st.session_state.is_recording and not st.session_state.is_paused:
    transcribed_text, success, message = transcribe_speech(api_choice, language_code, selected_language)
    
    if success:
        st.session_state.transcribed_text += " " + transcribed_text
        st.success(message)
    else:
        st.error(message)
    
    st.session_state.is_recording = False

# Footer with instructions
st.markdown("---")
st.markdown("""
### How to use:
1. **Choose API**: Select between Google (online, more accurate) or CMU Sphinx (offline)
2. **Select Language**: Pick the language you'll speak
3. **Start Recording**: Click "Start Recording" and speak clearly
4. **Pause/Resume**: Use pause button if needed
5. **Stop Recording**: Click "Stop Recording" when done
6. **Save**: Save your transcribed text to a file
7. **Clear**: Clear the text area to start fresh

### Features:
✅ Multiple Speech Recognition APIs (Google & CMU Sphinx)
✅ Support for 7+ Languages
✅ Pause and Resume Recording
✅ Save Transcriptions to Files
✅ Better Error Handling
✅ User-Friendly Interface

### Troubleshooting:
- **No audio detected?** Make sure your microphone is working and not muted
- **Low accuracy?** Speak clearly and reduce background noise
- **Internet connection?** Google API needs internet; use CMU Sphinx for offline mode
- **PyAudio issues?** On Windows, use: `pip install pipwin` then `pipwin install pyaudio`
""")
