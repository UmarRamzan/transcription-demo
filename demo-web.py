import whisper
import ffmpeg
import streamlit as st
from audio_recorder_streamlit import audio_recorder

class scribe:

    def __init__(self):
        self.model = None
        self.audio_file = None
        self.transcription = None

    @st.cache_data
    def get_model(_self):
        _self.model = whisper.load_model('base')
        st.session_state.model = _self.model
        st.sidebar.success("Model Loaded")

    def transcribe_audio(self):
        if st.session_state.model is None:
            st.sidebar.error("Please load the model first")
        elif self.audio_file is None:
            st.sidebar.error("Please upload an audio file")
        else:
            st.sidebar.success("Transcribing Audio")
            self.transcription = st.session_state.model.transcribe(self.audio_file.name)
            st.sidebar.success("Transcription Complete")
            st.text(self.transcription['text'])


transcriber = scribe()

st.title("Transcription Demo")

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

if st.sidebar.button("Load Model"):
    transcriber.get_model()
    
if st.sidebar.button("Transcribe Audio"):
    transcriber.transcribe_audio()
        
st.sidebar.header("Original Audio")
st.sidebar.audio(audio_file)
