import whisper
import sys
import os
import subprocess
from pydub import AudioSegment
import torch

def get_device():
    """Determine the best available device for processing"""
    return "cuda" if torch.cuda.is_available() else "cpu"

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except Exception as e:
        print(f"FFmpeg check failed: {str(e)}")
        print("Please ensure FFmpeg is installed and accessible in your system PATH")
        return False

def convert_audio_to_wav(input_path, output_path):
    """Convert any audio format to WAV using pydub"""
    try:
        print(f"Converting audio file: {input_path}")
        audio = AudioSegment.from_file(input_path)
        
        # Standardize audio parameters
        audio = audio.set_frame_rate(16000)  # Required by Whisper
        audio = audio.set_channels(1)  # Convert to mono
        audio = audio.set_sample_width(2)  # 16-bit depth
        
        audio.export(output_path, format="wav")
        print("Audio conversion successful")
        return True
    except Exception as e:
        print(f"Error converting audio: {str(e)}")
        return False

def transcribe_audio(audio_path):
    """
    Transcribe audio file using OpenAI's Whisper model with improved handling
    """
    try:
        # Verify FFmpeg installation
        print("Checking FFmpeg installation...")
        if not check_ffmpeg():
            return False

        # Check if file exists and print absolute path
        abs_path = os.path.abspath(audio_path)
        print(f"Processing file: {abs_path}")
        if not os.path.exists(abs_path):
            print(f"Error: File does not exist at {abs_path}")
            return False
            
        print(f"File size: {os.path.getsize(abs_path)} bytes")
        
        # Convert audio to WAV format
        wav_path = os.path.join(os.getcwd(), "temp_audio.wav")
        if not convert_audio_to_wav(abs_path, wav_path):
            return False
        
        # Determine device and load appropriate model
        device = get_device()
        print(f"Using device: {device}")
        
        print("Loading Whisper model...")
        model = whisper.load_model("small", device=device)
        print("Model loaded successfully!")
        
        print("Transcribing audio...")
        # Add transcription options for better results
        result = model.transcribe(
            wav_path,
            language=None,  # Auto-detect language
            task="transcribe",
            fp16=False if device == "cpu" else True,
            initial_prompt="This is a transcription of an audio file."
        )
        print("Transcription complete!")
        
        # Clean up temporary WAV file
        try:
            os.remove(wav_path)
            print("Temporary files cleaned up")
        except:
            print("Warning: Could not remove temporary WAV file")
        
        output_file = os.path.join(os.getcwd(), "transcript.txt")
        print(f"Saving transcription to {output_file}...")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print("Transcription saved successfully!")
        
        # Print transcription preview
        preview = result["text"][:100] + "..." if len(result["text"]) > 100 else result["text"]
        print(f"\nTranscription preview:\n{preview}")
        
        # Print detected language
        if "language" in result:
            print(f"Detected language: {result['language']}")
            
        return True
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe_audio.py <audio_file_path>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    success = transcribe_audio(audio_file)
    if not success:
        sys.exit(1) 