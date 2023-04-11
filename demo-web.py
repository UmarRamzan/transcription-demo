import whisper
import ffmpeg
import streamlit as st
from scipy.io import wavfile
from audio_recorder_streamlit import audio_recorder

@st.cache_resource()
def load_model(name):
    model = whisper.load_model(name)
    return model

model = load_model("small")

def transcribe_audio_recording():

    if model is None:
        st.error("Model not loaded")

    elif audio_bytes is None:
        st.error("Please record audio")

    else:
        with st.spinner('Transcribing Audio'):
            transcription = model.transcribe('recording.wav', task="translate", language="urdu")
            st.subheader("Transcription")
            st.markdown(transcription['text'])
    
def transcribe_audio_file():
    
        if model is None:
            st.error("Model not loaded")
    
        elif audio_file is None:
            st.error("Please upload an audio file")
    
        else:
            with st.spinner('Transcribing Audio'):
                transcription = model.transcribe('file.wav', task="translate", language="urdu")
                st.subheader("Transcription")
                st.markdown(transcription['text'])
            

st.title("Transcription Demo")

st.divider()

audio_bytes = audio_recorder(energy_threshold=-10, pause_threshold=10, icon_size="2x")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    with open('recording.wav', mode='bw') as f:
        f.write(audio_bytes)

if st.button("Transcribe Audio Recording"):
    transcribe_audio_recording()

st.divider()

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

if audio_file:
    st.audio(audio_file)

    with open('file.wav', mode='bw') as f:
        f.write(audio_file.read())

if st.button("Transcribe Audio File"):
    transcribe_audio_file()

st.divider()