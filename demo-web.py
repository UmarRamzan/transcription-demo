import whisper
import streamlit as st
import sounddevice as sd
from scipy.io import wavfile
from audio_recorder_streamlit import audio_recorder
from transformers import WhisperProcessor, WhisperForConditionalGeneration

@st.cache_resource()
def load_model(name):
    model = whisper.load_model(name)
    return model

model = load_model("small")

def transcribe_audio_recording():

    if model is None:
        st.sidebar.error("Model not loaded")

    elif audio_bytes is None:
        st.sidebar.error("Please record audio")

    else:
        transcription = model.transcribe('recording.wav', task="translate", language="urdu")
        st.header("Transcription")
        st.text(transcription['text'])
    
def transcribe_audio_file():
    
        if model is None:
            st.sidebar.error("Model not loaded")
    
        elif audio_file is None:
            st.sidebar.error("Please upload an audio file")
    
        else:
            transcription = model.transcribe('file.wav', task="translate", language="urdu")
            st.subheader("Transcription")
            st.text(transcription['text'])

st.title("Transcription Demo")

audio_bytes = audio_recorder(energy_threshold=-10, pause_threshold=10, icon_size="2x")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    with open('recording.wav', mode='bw') as f:
        f.write(audio_bytes)

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
if audio_file:
    st.audio(audio_file)

    with open('file.wav', mode='bw') as f:
        f.write(audio_file.read())
    
if st.sidebar.button("Transcribe Audio Recording"):
    transcribe_audio_recording()

if st.sidebar.button("Transcribe Audio File"):
    transcribe_audio_file()
