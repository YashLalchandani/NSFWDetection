# NSFW Detection Using Flask, NudeNet, and OpenCV

## Introduction

This project implements a real-time NSFW (Not Safe For Work) content detection and blurring system using Flask, NudeNet, and OpenCV. The goal is to monitor and filter inappropriate content in live video streams, ensuring a safer viewing experience.

## Objectives

- Develop a real-time video processing system that detects NSFW content.
- Blur detected NSFW content to protect viewers from inappropriate visuals.
- Provide a web interface for users to view the filtered video stream.

## Methodology

### Tools and Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python used to develop the web interface.
- **NudeNet**: A pre-trained deep learning model specialized in detecting NSFW content.
- **OpenCV**: An open-source computer vision and machine learning software library used for real-time video capture and processing.
- **Python**: The primary programming language used for implementing the backend logic.

## Implementation

The implementation is divided into several key steps:

1. **Setup and Configuration**: Initializing Flask and configuring the NudeNet model for NSFW detection.
2. **Video Capture**: Using OpenCV to capture video frames from the default camera.
3. **NSFW Detection**: Processing each frame to detect NSFW content using NudeNet.
4. **Blurring NSFW Content**: Applying Gaussian blur to parts of the frame identified as NSFW.
5. **Web Streaming**: Streaming the processed video to a web interface using Flask.
