from mutagen.mp3 import MP3

def get_mp3_length(audio: MP3) -> str:
    length_seconds = int(audio.info.length)
    length_minutes = length_seconds // 60
    seconds = length_seconds % 60
    return f'{length_minutes} min {seconds} sec'
