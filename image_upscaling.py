import cv2
from tkinter import filedialog
from os import getcwd
import numpy as np

def CPUprocessing(video):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # for sharpening
    result_video = cv2.VideoWriter('rezultat.mp4', cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (1920,1080))

    while video.isOpened():
        success, frame = video.read()

        if success:
            frame_upscaled = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_CUBIC)
            # frame_denoised = cv2.fastNlMeansDenoisingColored(frame_upscaled, None, 5, 5, 7, 15)
            frame_denoised = cv2.bilateralFilter(frame_upscaled, 9, 100, 100)
            frame_sharpened = cv2.filter2D(frame_denoised, -1, kernel)
            #result_video.write(frame_sharpened)
            cv2.imshow('Video', frame_sharpened)
        else:
            break

        cv2.waitKey(25)

    result_video.release()

def GPUprocessing(video):
    gpu_frame = cv2.cuda.GpuMat()
    valid_frame, frame = video.read()

    while valid_frame:
        gpu_frame.upload(frame)
        frame_upscaled = cv2.cuda.resize(frame, (1280, 720), interpolation=cv2.INTER_CUBIC)
        frame_denoised = cv2.cuda.fastNlMeansDenoisingColored(frame)
        result = frame_denoised.download()
        cv2.imshow('Video', result)

        valid_frame, frame = video.read()

        cv2.waitKey(33)

video_path = filedialog.askopenfilename(title="Select a video", filetypes=[("MP4 files", "*.mp4")], initialdir=getcwd())
video_original = cv2.VideoCapture(video_path)

CPUprocessing(video_original)