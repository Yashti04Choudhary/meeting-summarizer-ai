# Autonomous Meeting Summarizer

An AI-powered tool that automatically transcribes audio recordings and generates concise summaries.

## Features
- Audio transcription using OpenAI's Whisper
- Text summarization using T5 transformer model
- Simple web interface built with Streamlit
- Supports WAV and MP3 audio formats

## Setup Instructions

1. Activate the virtual environment:
   ```
   # On Windows
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL shown in the terminal (usually http://localhost:8501)

3. Upload an audio file (WAV or MP3) and click "Transcribe & Summarize"

## Project Structure
- `app.py`: Main Streamlit web application
- `transcribe_audio.py`: Audio transcription module using Whisper
- `summarize_text.py`: Text summarization module using T5
- `requirements.txt`: Project dependencies

## Notes
- First-time run will download the required AI models
- Processing time depends on audio length and your computer's specifications
- For best results, use clear audio recordings with minimal background noise

## Future Enhancements
- Speaker diarization
- Real-time transcription
- Multiple language support
- Custom summarization parameters 