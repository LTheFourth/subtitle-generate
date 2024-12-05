import whisper
import argparse
import os
import torch
import warnings
from datetime import timedelta

warnings.filterwarnings("ignore", category=FutureWarning)

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format"""
    td = timedelta(seconds=seconds)
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    seconds = td.seconds%60
    milliseconds = td.microseconds//1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def create_srt_content(segments):
    """Create SRT formatted content from segments"""
    srt_content = []
    for i, segment in enumerate(segments, start=1):
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        text = segment['text'].strip()
        srt_content.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
    return "\n".join(srt_content)

def transcribe_audio(
    audio_path, 
    model_size='base', 
    language=None, 
    output_formats=None,
    output_dir=None
):
    """
    Transcribe audio using Whisper
    
    Parameters:
    - audio_path: Path to audio file
    - model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
    - language: Language code (e.g., 'en', 'ja', 'auto' for auto-detection)
    - output_formats: List of output formats ('srt', 'txt', 'vtt', 'json')
    - output_dir: Directory to save output files (default: same as audio file)
    """
    
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\nUsing device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Validate input file
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Set default output formats
    if output_formats is None:
        output_formats = ['srt']
    
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(audio_path) or '.'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    
    print(f"Loading model: {model_size}")
    model = whisper.load_model(model_size).to(device)
    
    # Prepare transcription options
    options = {
        "task": "transcribe",
        "fp16": device == "cuda"  # Use FP16 if on GPU
    }
    if language and language != "auto":
        options["language"] = language
    
    print("Transcribing audio...")
    result = model.transcribe(audio_path, **options)
    
    # Save outputs in requested formats
    for fmt in output_formats:
        output_path = os.path.join(output_dir, f"{base_name}.{fmt}")
        
        if fmt == 'srt':
            content = create_srt_content(result['segments'])
        elif fmt == 'txt':
            content = result['text']
        elif fmt == 'vtt':
            # Simple WebVTT format
            content = "WEBVTT\n\n" + create_srt_content(result['segments']).replace(',', '.')
        elif fmt == 'json':
            import json
            content = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            print(f"Unsupported format: {fmt}")
            continue
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved {fmt.upper()} file: {output_path}")
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using Whisper")
    parser.add_argument("audio_path", help="Path to the audio file")
    parser.add_argument(
        "--model", 
        choices=['tiny', 'base', 'small', 'medium', 'large'], 
        default='base',
        help="Model size to use"
    )
    parser.add_argument(
        "--language", 
        default="auto",
        help="Language code (e.g., en, ja, zh) or 'auto' for auto-detection"
    )
    parser.add_argument(
        "--output-formats", 
        nargs='+',
        choices=['srt', 'txt', 'vtt', 'json'],
        default=['srt'],
        help="Output formats to generate"
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save output files (default: same as audio file)"
    )
    
    args = parser.parse_args()
    
    try:
        result = transcribe_audio(
            args.audio_path,
            model_size=args.model,
            language=args.language,
            output_formats=args.output_formats,
            output_dir=args.output_dir
        )
        
        # Print transcription to console
        print("\nTranscription:")
        print("-" * 50)
        print(result["text"])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
