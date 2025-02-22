import streamlit as st
from PIL import Image

# --- Page Configuration ---
st.set_page_config(page_title="Truy vấn thông tin", layout="wide")

# --- Custom CSS Styling ---
st.markdown(
    """
    <style>
    /* Overall background and font */
    body {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Centered header styling */
    .header {
        text-align: center;
        margin-bottom: 40px;
    }
    /* Card-like container for sections */
    .custom-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    /* Generic button styling */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    /* Make record button full width */
    #record-container .stButton button {
        width: 100%;
    }
    /* Microphone icon pulse animation */
    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.2); }
      100% { transform: scale(1); }
    }
    .mic-animate {
      display: inline-block;
      animation: pulse 1s infinite;
    }
    /* Blinking text animation */
    @keyframes blink {
      0% { opacity: 1; }
      50% { opacity: 0; }
      100% { opacity: 1; }
    }
    .blink {
      color: red;
      animation: blink 1s infinite;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Functions --------------------------------
import sounddevice as sd
import numpy as np
import wave
from io import BytesIO
from pydub import AudioSegment
from transformers import pipeline
import ffmpeg
import numpy as np
import os

# Cấu hình ghi âm
SAMPLE_RATE = 44100  # Tần số lấy mẫu
DURATION = 3  # Thời gian ghi âm (giây)
CHANNELS = 1  # Số kênh (1 = mono, 2 = stereo)

def record_audio(duration=DURATION, sample_rate=SAMPLE_RATE, channels=CHANNELS):
    print("Bắt đầu ghi âm...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype=np.int16)
    sd.wait()  # Đợi quá trình ghi âm hoàn tất
    print("Ghi âm xong!")

    # Lưu dữ liệu vào một buffer WAV
    buffer = BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit = 2 byte
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    buffer.seek(0)  # Đưa con trỏ về đầu buffer
    audio = AudioSegment.from_wav(buffer)
    audio.export("output.wav", format="wav")  # Lưu file WAV
    print("File ghi âm đã được lưu: output.wav")
    transcriber = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-small", device='cuda')
    output = transcriber('./output.wav')['text']
    return output

# --- Header Section ---
st.markdown(
    """
    <div class="header">
        <h1>Truy vấn thông tin</h1>
        <h3>Tìm kiếm thông tin từ cơ sở dữ liệu</h3>
        <p>Nhập thông tin bằng văn bản hoặc tải lên hình ảnh để bắt đầu tìm kiếm.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ###################### Recording Session ##################

# Create a full-width column
transcript = ""
col = st.columns(1)[0]  # Get the single full-width column
with col:
    if st.button("🎙️ Start Recording", use_container_width=True):
        # Use a spinner to indicate that recording is in progress
        with st.spinner("Recording in progress..."):
            transcript = record_audio()
        st.success("Recording completed!")
        st.write("Transcript:", transcript)
st.markdown("</div>", unsafe_allow_html=True)


# --- Main Content Section (Input & Preview) ---
col_input, col_preview = st.columns(2)

# Left Column: Search Input
with col_input:
    st.subheader("Truy vấn")

    # Use a form so that all inputs are submitted together
    with st.form("search_form"):
        text_query = st.text_input("Nhập truy vấn văn bản:", transcript)
        uploaded_image = st.file_uploader("Hoặc tải lên hình ảnh", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Tìm kiếm")

    if submitted:
        st.success("Đang xử lý yêu cầu của bạn...")
    st.markdown("</div>", unsafe_allow_html=True)

# Right Column: Preview and Result Output
with col_preview:
    st.subheader("Xem trước kết quả")

    # Show text query preview (if provided)
    if text_query:
        st.markdown("**Truy vấn văn bản:**")
        st.write(text_query)

    # Show image preview (if provided)
    if uploaded_image is not None:
        st.markdown("**Hình ảnh đã tải lên:**")
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Kết quả truy vấn (Tính năng đang phát triển)")
    st.info("Kết quả truy vấn sẽ được hiển thị tại đây sau khi hệ thống hoàn thiện.")
    st.markdown("</div>", unsafe_allow_html=True)


