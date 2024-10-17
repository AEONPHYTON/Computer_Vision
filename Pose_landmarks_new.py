import cv2
import mediapipe as mp
import time
import pandas as pd
import numpy as np
from tqdm import tqdm

# Initialize MediaPipe Pose
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Funciot to process video
def process_video(video_path, iterations=10):
    data = []

    for iteration in tqdm(range(iterations), desc="Processing iterations"):
        cap = cv2.VideoCapture(video_path)
        iteration_data = []

        while True:
            success, img = cap.read()
            if not success:
                break
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            if results.pose_landmarks:
                frame_data = {'time': time.time()}
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    frame_data[f'lm_{id}_x'] = cx
                    frame_data[f'lm_{id}_y'] = cy
                iteration_data.append(frame_data)

        cap.release()

        if iteration == 0:
            data = iteration_data
        else:
            for i in range(len(data)):
                for key in data[i]:
                    if key != 'time':
                        data[i][key] = (data[i][key] * iteration + iteration_data[i][key]) / (iteration + 1)

    return data

# Select video

video_path = "Nome del video"


# process X time the video for a better precision of a landmark

iterations = 10
ext = '.mp4'
file = video_path + ext
landmarks_data = process_video(file, iterations)

# Salva i dati in un file CSV
df = pd.DataFrame(landmarks_data)
df.to_csv(f'{video_path}.csv', index=False)

print(f"Processing complete. Data saved to {video_path}.csv")
