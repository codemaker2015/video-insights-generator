import os
import streamlit as st
from pytube import YouTube

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=output_path)
        return yt.title, stream.default_filename
    except Exception as e:
        return None, str(e)

# Create medias directory if it doesn't exist
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
medias_dir = os.path.join(parent_dir, 'medias')
os.makedirs(medias_dir, exist_ok=True)

st.title("YouTube Video Downloader")

url = st.text_input("Enter the YouTube URL:")

if st.button("Download"):
    if url:
        with st.spinner("Downloading..."):
            title, result = download_video(url, medias_dir)
            if title:
                st.success(f"'{title}' has been downloaded successfully!")
                st.write(f"File saved to: {os.path.join(medias_dir, result)}")
            else:
                st.error(f"Error: {result}")
    else:
        st.warning("Please enter a valid YouTube URL.")
