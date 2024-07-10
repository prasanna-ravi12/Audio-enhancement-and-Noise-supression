from flask import Flask, request, send_from_directory, jsonify
import os
from audio_denoiser.AudioDenoiser import AudioDenoiser
import torch
import torchaudio
import moviepy.editor as mp

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize device for CUDA if available
device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
denoiser = AudioDenoiser(device=device)


def process_audio(input_path):
    out_audio_file = f"{os.path.splitext(input_path)[0]}_denoised.wav"
    auto_scale = True  # Recommended for low-volume input audio
    try:
        waveform, sample_rate = torchaudio.load(input_path, backend='soundfile')
        denoiser.process_audio_file(input_path, out_audio_file, auto_scale=auto_scale)
        return out_audio_file
    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise



def process_video(input_path):
    try:
        video = mp.VideoFileClip(input_path)
        if video.audio is None:
            print(f"No audio track found in video file: {input_path}")
            return None  # Return None to indicate processing failure

        audio_path = f"{os.path.splitext(input_path)[0]}.wav"
        print(f"Extracting audio to: {audio_path}")

        # Extract audio from video
        video.audio.write_audiofile(audio_path)

        # Process extracted audio
        denoised_audio_path = process_audio(audio_path)

        if denoised_audio_path is None:
            print(f"Error processing audio for video: {input_path}")
            return None

        # Attach denoised audio back to the video
        denoised_audio = mp.AudioFileClip(denoised_audio_path)
        new_video = video.set_audio(denoised_audio)
        out_video_file = f"{os.path.splitext(input_path)[0]}_denoised.mp4"
        new_video.write_videofile(out_video_file, codec='libx264', audio_codec='aac')

        return out_video_file
    except Exception as e:
        print(f"Error processing video file: {e}")
        return None  # Return None to indicate processing failure


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Debug: Verify file path and existence
    if not os.path.exists(input_path):
        print(f"File not found after save: {input_path}")
        return jsonify(error='File save failed'), 500
    print(f"File successfully saved: {input_path}")

    file_extension = os.path.splitext(input_path)[1].lower()
    try:
        if file_extension in ['.wav', '.mp3', '.flac', '.aac', '.m4a']:
            output_path = process_audio(input_path)
        elif file_extension in ['.mp4', '.avi', '.mov', '.mkv']:
            output_path = process_video(input_path)
            if output_path is None:
                return jsonify(error='Video processing failed: No audio track found or other error'), 500
        else:
            return jsonify(error='Unsupported file type'), 400
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify(error='Processing failed'), 500

    return jsonify(file=os.path.basename(output_path)), 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
