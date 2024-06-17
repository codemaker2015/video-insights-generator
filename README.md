# Video Insights Generator

This application uses Google's Gemini Flash and Streamlit to generate insights from video files. It allows users to upload a video file, which is then processed using Gemini Flash to extract insights. The insights are then displayed in the application.

![demo](demos/demo.gif)

## Usage

1. Upload a video file (mp4, avi, mov, or mkv) using the file uploader.
2. The video file will be processed using Gemini Flash.
3. The insights extracted from the video will be displayed in the application.

## Requirements

- Google Gemini API key (set as an environment variable GEMINI_API_KEY)
- Streamlit library
- Google GenAI library

## Installation

1. Install Streamlit using pip install streamlit
2. Install Google GenAI using pip install google.generativeai
3. Set your Gemini API key as an environment variable `GEMINI_API_KEY`

## Running the Application

1. Run the application using `streamlit run app.py`
2. Open a web browser and navigate to http://localhost:8501

Notes

- The application uses a temporary folder medias to store uploaded video files. These files are removed after processing.
- The application uses the Gemini Flash model models/gemini-1.5-flash to extract insights from videos.