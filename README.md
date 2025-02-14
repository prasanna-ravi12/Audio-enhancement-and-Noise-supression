# Audio-enhancement-and-Noise-supression
This project enhances audio quality by suppressing noise in audio and video files through a Flask web application. Users can upload files, process them for noise reduction, and download the enhanced versions. It leverages PyTorch, torchaudio, and moviepy for efficient audio and video processing.

Project Title: Audio Enhancement and Noise Suppression

## Features
- Noise suppression for audio files in various formats (e.g., WAV, MP3, FLAC, AAC, M4A).
- Noise suppression for video files by extracting, processing, and reintegrating audio.
- Simple web interface for uploading and downloading files.

## Technologies Used
- Flask
- PyTorch and torchaudio for audio processing
- moviepy for video processing
- HTML, CSS, and JavaScript for the web interface

## Installation

### Prerequisites
- Python 3.12
- Flask
- PyTorch
- torchaudio
- moviepy

### Setup
1.Installation:
   ```
    pip install flask pytorch torchaudio moviepy audiodenoiser
  ```
2. Directory structure:
 - <img width="435" alt="Screenshot 2024-07-11 at 2 00 47 AM" src="https://github.com/prasanna-ravi12/Audio-enhancement-and-Noise-supression/assets/175058249/f426396d-b786-4fb5-82e0-a8844d26ebeb">

3. Create an empty folder 'uploads' to store the uploded image from website.
4. Run the Flask application:

```
    Python app.py
  ```
5. Open your web browser and go to http://127.0.0.1:5000/static/index.html to access the application.


##Web Interface
 - Go to the upload section and click the "Upload" button to select an audio or video file from your device.
 - Once the file is uploaded, the application will process the file to suppress noise.
 = After processing, a download link will appear. Click the link to download the enhanced file.

  - ![1](https://github.com/prasanna-ravi12/Audio-enhancement-and-Noise-supression/assets/175058249/e9711115-f619-4d3a-b82c-76ea986baea1)
