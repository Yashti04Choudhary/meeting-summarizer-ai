import sys
import re
from datetime import datetime
from transformers import pipeline
import torch
from typing import List

def clean_text(text: str) -> str:
    """Clean and format the text for better summarization"""
    # Remove redundant spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove redundant punctuation
    text = re.sub(r'\.+', '.', text)
    # Fix spacing around punctuation
    text = re.sub(r'\s*([.,!?])\s*', r'\1 ', text)
    return text

def split_into_chunks(text: str, max_length: int = 1024) -> List[str]:
    """Split text into chunks that the model can process"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length > max_length:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def extract_key_points(text: str) -> List[str]:
    """Extract key points using keyword matching"""
    important_keywords = [
        'action', 'decide', 'agree', 'plan', 'need', 'must', 'should', 'will',
        'deadline', 'important', 'critical', 'urgent', 'priority', 'key',
        'decision', 'approved', 'rejected', 'concluded', 'assigned', 'responsible'
    ]
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    key_points = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        # Check if sentence contains any important keywords
        if any(keyword in sentence.lower() for keyword in important_keywords):
            key_points.append(sentence)
    
    return key_points

def format_summary(summary_text: str, key_points: List[str]) -> str:
    """Format the summary with sections and structure"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    formatted_summary = f"""🤖 Local AI-Generated Meeting Summary
📅 Generated on: {timestamp}
📝 Model: BART Large CNN
{'=' * 50}

OVERVIEW:
{summary_text}

KEY POINTS IDENTIFIED:
"""
    
    for point in key_points:
        formatted_summary += f"• {point}\n"
    
    # Add potential action items section
    action_items = [point for point in key_points if any(word in point.lower() for word in ['action', 'task', 'need', 'must', 'should', 'will', 'deadline'])]
    if action_items:
        formatted_summary += "\nPOTENTIAL ACTION ITEMS:\n"
        for item in action_items:
            formatted_summary += f"📌 {item}\n"
    
    return formatted_summary

def generate_summary(text: str) -> str:
    """Generate a comprehensive meeting summary using BART"""
    try:
        # Initialize the summarization pipeline
        print("Loading summarization model (this may take a few minutes the first time)...")
        summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Clean the text
        text = clean_text(text)
        
        # Split text into chunks if it's too long
        chunks = split_into_chunks(text)
        
        # Generate summary for each chunk
        print("Generating summary...")
        summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        
        # Combine summaries
        combined_summary = " ".join(summaries)
        
        # Extract key points
        key_points = extract_key_points(text)
        
        # Format the final summary
        final_summary = format_summary(combined_summary, key_points)
        
        return final_summary
        
    except Exception as e:
        print(f"Error in summary generation: {str(e)}")
        return create_basic_summary(text)

def create_basic_summary(text: str) -> str:
    """Create a basic summary when the main summarization fails"""
    key_points = extract_key_points(text)
    
    summary = f"""⚠️ Basic Summary (Fallback Method)
📅 Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'=' * 50}

Key Points Identified:\n"""
    
    for point in key_points[:10]:  # Limit to top 10 points
        summary += f"• {point}\n"
    
    return summary

def summarize_text(input_file: str, output_file: str) -> bool:
    """
    Summarize meeting text using local AI
    """
    try:
        print(f"Reading input file: {input_file}")
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"Input text length: {len(text)} characters")
        
        # Generate summary
        print("Generating AI summary...")
        final_summary = generate_summary(text)
        
        print(f"Saving summary to {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_summary)
        print("✅ Summary saved successfully!")
            
        return True
    except Exception as e:
        print(f"❌ Error during summarization: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python summarize_text.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    success = summarize_text(input_file, output_file)
    if not success:
        sys.exit(1) 