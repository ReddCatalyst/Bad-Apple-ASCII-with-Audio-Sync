import cv2
import os
import sys
import time
import numpy as np
from pygame import mixer

# Ambil lokasi folder src, lalu naik satu level ke folder utama proyek
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_PATH = os.path.join(BASE_DIR, "assets", "bad_apple.mp4")
AUDIO_PATH = os.path.join(BASE_DIR, "assets", "bad_apple.mp3")

os.system("") # Aktifkan ANSI
mixer.init()
CHARS = np.array(list(" .:-=+*#%@"))

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"Error: Video gak ketemu di {VIDEO_PATH}")
        return

    if os.path.exists(AUDIO_PATH):
        mixer.music.load(AUDIO_PATH)
        mixer.music.play()

    fps = cap.get(cv2.CAP_PROP_FPS)

    try:
        while cap.isOpened():
            current_time_ms = mixer.music.get_pos()
            target_frame = int((current_time_ms / 1000) * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            
            ret, frame = cap.read()
            if not ret: break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            width = 110
            height = int(gray.shape[0] * width / gray.shape[1] * 0.45)
            resized = cv2.resize(gray, (width, height))

            indices = (resized.astype(float) * (len(CHARS) - 1) / 255).astype(int)
            output = CHARS[indices]
            
            sys.stdout.write("\033[H" + "\n".join(["".join(row) for row in output]))
            sys.stdout.flush()
    except KeyboardInterrupt:
        mixer.music.stop()
    finally:
        cap.release()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()