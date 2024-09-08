import requests
from gtts import gTTS
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

# Function to get stock video clips
def get_stock_video_clips(query):
    video_urls = []
    response = requests.get(f"https://api.pexels.com/videos/search?query={query}",
                            headers={"Authorization": "Your_API"})
    if response.status_code == 200:
        video_data = response.json()
        for video in video_data['videos']:
            video_urls.append(video['video_files'][0]['link'])  # Get the first video file
    return video_urls

# Function to generate audio from text
def generate_audio_from_text(text, output_audio_path="speech.mp3"):
    print(f"Generating speech for text: {text}")
    tts = gTTS(text)
    tts.save(output_audio_path)
    print(f"Audio saved at {output_audio_path}")

    # Check audio duration
    audio_clip = AudioFileClip(output_audio_path)
    print(f"Audio duration: {audio_clip.duration} seconds")  # Print audio duration
    
    return output_audio_path

# Function to create a video from stock clips and audio
def create_video_from_clips_and_audio(video_urls, audio_path, output_video_path="output_video.mp4"):
    video_clips = []

    for url in video_urls:
        print(f"Loading video from: {url}")
        clip = VideoFileClip(url).subclip(0, 10)  # Use only the first 10 seconds of each clip
        video_clips.append(clip)

    if not video_clips:
        print("No video clips available to concatenate.")
        return

    # Concatenate video clips
    final_video = concatenate_videoclips(video_clips)

    # Load audio file
    audio_clip = AudioFileClip(audio_path)
    
    # Ensure final video does not exceed audio duration
    final_video = final_video.subclip(0, min(audio_clip.duration, final_video.duration))
    
    # Set audio to the video
    final_video = final_video.set_audio(audio_clip)

    # Write the final video file
    final_video.write_videofile(output_video_path, fps=24)
    print(f"Video saved at {output_video_path}")

# Main program
if __name__ == "__main__":
    # Input text for generating the video
    input_text = "nissan gtr "
    
    # Generate audio from text
    audio_path = generate_audio_from_text(input_text)
    
    # Get stock video clips
    video_urls = get_stock_video_clips(input_text)
    
    # Create video from clips and audio
    create_video_from_clips_and_audio(video_urls, audio_path)
