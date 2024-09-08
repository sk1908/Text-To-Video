# Import required libraries
from diffusers import StableDiffusionPipeline
from gtts import gTTS
from moviepy.editor import *
import torch

# Ensure you're using GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe = pipe.to(device)


def generate_image_from_text(prompt, output_image_path="output.png"):
    print(f"Generating image for prompt: {prompt}")
    image = pipe(prompt).images[0]
    image.save(output_image_path)
    print(f"Image saved at {output_image_path}")
    return output_image_path


def generate_audio_from_text(text, output_audio_path="speech.mp3"):
    print(f"Generating speech for text: {text}")
    tts = gTTS(text)
    tts.save(output_audio_path)
    print(f"Audio saved at {output_audio_path}")
    return output_audio_path


def create_video_with_audio(image_path, audio_path, output_video_path="output_video.mp4", duration=5):

    print(f"Creating video from image {image_path} and audio {audio_path}")

    # Load the image and set the duration of the clip
    image_clip = ImageClip(image_path).set_duration(duration)

    # Load the audio file
    audio_clip = AudioFileClip(audio_path)

    # Set the audio to the image clip
    video_clip = image_clip.set_audio(audio_clip)

    # Write the final video file
    video_clip.write_videofile(output_video_path, fps=24)
    print(f"Video saved at {output_video_path}")
    return output_video_path


def generate_video_from_text(input_text):
    # Generate image from text
    image_path = generate_image_from_text(input_text)

    # Generate audio from text
    audio_path = generate_audio_from_text(input_text)

    # Create a video from the image and audio
    video_path = create_video_with_audio(image_path, audio_path)

    print(f"Video generated: {video_path}")


# Main program
if __name__ == "__main__":
    # Input text for generating the video
    input_text = "birds flying in sunset time"

    # Generate the video
    generate_video_from_text(input_text)
