import whisper
import ffmpeg
import replicate
import streamlit as st
from scipy.io import wavfile
from audio_recorder_streamlit import audio_recorder

from transformers import WhisperProcessor, WhisperForConditionalGeneration

@st.cache_resource()
def load_model(name):
    model = whisper.load_model(name)
    return model

@st.cache_resource()
def load_model_hugging_face():
    # load model and processor
    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="urdu", task="translate")

placeholder = st.empty()
placeholder.caption("Loading Model (May take upto an hour depending on your internet connection)")

#model = load_model("tiny")
model = load_model_hugging_face()

placeholder.empty()

def transcribe_audio_recording():

    if audio_bytes is None:
        st.error("Please record audio")

    else:
        with st.spinner('Transcribing Audio'):

            #transcription = model.transcribe('recording.wav', task="translate", language="urdu", word_timestamps=False)
            #transcription = replicate.run(
            #     "openai/whisper:e39e354773466b955265e969568deb7da217804d8e771ea8c9cd0cef6591f8bc",
            #     input={"audio": open("recording.wav", "rb"), "translate": True, "language": "ur"}
            # )

            input_array = wavfile.read('recording.wav')
            print(input_array)
            #input_features = processor(input_array, sampling_rate=input_speech["sampling_rate"], return_tensors="pt").input_features
            # generate token ids
            #predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
            # decode token ids to text
            #transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
            
            st.subheader("Transcription")

            #st.markdown(transcription['text'])
            #st.markdown(transcription['translation'])
    
def transcribe_audio_file():
        
        if audio_file is None:
            st.error("Please upload an audio file")
    
        else:
            with st.spinner('Transcribing Audio'):

                # transcription = model.transcribe('file.wav', task="translate", language="urdu")
                transcription = replicate.run(
                    "openai/whisper:e39e354773466b955265e969568deb7da217804d8e771ea8c9cd0cef6591f8bc",
                    input={"audio": open("file.wav", "rb"), "translate": True, "language": "ur"}
                )
                
                st.subheader("Transcription")
                
                #st.markdown(transcription['text'])
                st.markdown(transcription['translation'])
            

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