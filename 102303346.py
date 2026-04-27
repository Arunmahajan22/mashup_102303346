import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

# -----------------------------
# INPUT VALIDATION
# -----------------------------
if len(sys.argv) != 5:
    print("Usage: py -3.11 <RollNumber>.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
    sys.exit()

singer = sys.argv[1]

try:
    number_of_videos = int(sys.argv[2])
    duration = int(sys.argv[3])
except:
    print("NumberOfVideos and AudioDuration must be integers.")
    sys.exit()

output_file = sys.argv[4]

if number_of_videos <= 10:
    print("NumberOfVideos must be greater than 10")
    sys.exit()

if duration <= 20:
    print("AudioDuration must be greater than 20 seconds")
    sys.exit()

# -----------------------------
# CREATE WORKING DIRECTORY
# -----------------------------
base_dir = os.path.join(os.getcwd(), "mashup_work")
trimmed_dir = os.path.join(base_dir, "trimmed")

if os.path.exists(base_dir):
    shutil.rmtree(base_dir)

os.makedirs(trimmed_dir)

print("Working directory created.")
print("Downloading only required duration (fast mode)...")

# -----------------------------
# DOWNLOAD ONLY FIRST N SECONDS
# -----------------------------
ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': os.path.join(trimmed_dir, '%(id)s.%(ext)s'),
    'quiet': True,
    'noplaylist': True,
    'ignoreerrors': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    # IMPORTANT: Download only first part
    'postprocessor_args': [
        '-t', str(duration)
    ]
}

try:
    with YoutubeDL(ydl_opts) as ydl:
        search_query = f"ytsearch{number_of_videos}:{singer} audio song"
        ydl.download([search_query])
except Exception as e:
    print("Download error:", e)
    sys.exit()

print("Download complete.")

# -----------------------------
# MERGE AUDIO
# -----------------------------
print("Merging audio files...")

final_audio = AudioSegment.empty()

for file in os.listdir(trimmed_dir):
    if file.endswith(".mp3"):
        audio_path = os.path.join(trimmed_dir, file)
        sound = AudioSegment.from_mp3(audio_path)
        final_audio += sound

final_audio.export(output_file, format="mp3")

print("\nMashup created successfully:", output_file)
