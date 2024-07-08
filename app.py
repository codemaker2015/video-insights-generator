import os
import time
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from pytube import YouTube

MEDIA_FOLDER = 'medias'

def __init__():
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

def download_video(url, output_path):
    """Download youtube video to the media folder and return the file path."""
    try:
        with st.spinner("Downloading video..."):
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            file_path = ""
            file_path = stream.download(output_path=output_path)
        return file_path, yt.title, stream.default_filename
    except Exception as e:
        return None, str(e)

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the media folder and return the file path."""
    file_path = os.path.join(MEDIA_FOLDER, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    return file_path

def get_insights(video_path):
    """Extract insights from the video using Gemini Flash."""
    st.write(f"Processing video: {video_path}")
    video_file = ""

    with st.spinner("Uploading file..."):
        video_file = genai.upload_file(path=video_path)
    # st.write(f"Completed upload: {video_file.uri}")

    while video_file.state.name == "PROCESSING":
        with st.spinner("Waiting for video to be processed."):
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)
    
    prompt = "Describe the video. Provides the insights from the video."

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    
    response = ""

    with st.spinner("Making LLM inference request..."):
        response = model.generate_content([prompt, video_file],
                                    request_options={"timeout": 600})
    st.success(f'Video processing complete')
    st.subheader("Insights")
    st.info(response.text)
    genai.delete_file(video_file.name)


def app():
    st.title("Video Insights Generator")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
    st.markdown("<div style='text-align: center'>OR</div>", unsafe_allow_html=True)
    url = st.text_input("Enter the YouTube URL:")
    file_path = ""

    if st.button('SUBMIT'):
        if uploaded_file is not None:
            file_path = save_uploaded_file(uploaded_file)
            st.video(file_path)
            get_insights(file_path)
        elif url != "":
            file_path, tile, name = download_video(url, MEDIA_FOLDER)
            st.video(file_path)
            get_insights(file_path)
        else: 
            st.error("Please provide a valid file or YouTube URL.")

        if os.path.exists(file_path):  ## Optional: Removing uploaded files from the temporary location
            os.remove(file_path)

__init__()
app()