import cv2
import os
from natsort import natsorted
import numpy as np

# --- SETTINGS ---
image_folder = 'D:\DDPM\Pytorch_codes\DDPM-Pytorch\default\samples'     # ✅ Replace with your folder
video_name = 'output_video.avi'            # ✅ Output video name
frame_rate = 30                            # ✅ FPS
padding = 5                               # ✅ Padding in pixels (around all sides)
border_color = (255, 255, 255)                   # ✅ Padding color (B, G, R) — here black

# --- Load & Sort Images ---
images = [img for img in os.listdir(image_folder) if img.lower().endswith((".png", ".jpg", ".jpeg"))]
images = natsorted(images)  # natural sort: frame1, frame2, ..., frame10 (not frame1, frame10, frame2)

# --- Read first image to get size ---
first_image = cv2.imread(os.path.join(image_folder, images[0]))
h, w = first_image.shape[:2]

# New size with padding
new_w, new_h = w + 2 * padding, h + 2 * padding

# --- Set up video writer ---
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_name, fourcc, frame_rate, (new_w, new_h))

# --- Process each frame ---
for img_name in images:
    img_path = os.path.join(image_folder, img_name)
    img = cv2.imread(img_path)

    # Add padding
    padded_img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=border_color)

    out.write(padded_img)

out.release()
print("✅ Video saved as:", video_name)

# --- Input and Output Video ---
input_path = 'output_video.avi'       # ✅ Your current video
output_path = 'reversed_video.avi'    # ✅ Output reversed video

# --- Read input video ---
cap = cv2.VideoCapture(input_path)

# Get properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# --- Read all frames into a list ---
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()

# --- Reverse the frame list ---
frames.reverse()

# --- Write reversed video ---
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
for frame in frames:
    out.write(frame)
out.release()

print("✅ Reversed video saved as:", output_path)

