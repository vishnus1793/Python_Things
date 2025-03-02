from flask import Flask, request, jsonify, send_from_directory
import os
import fitz  # PyMuPDF
from gtts import gTTS

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text if text.strip() else "No text found in the PDF."
    except Exception as e:
        return None, str(e)

def convert_text_to_speech(text, output_file):
    """Converts extracted text to speech and saves it as an MP3 file."""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_file)
        return True, None
    except Exception as e:
        return False, str(e)

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file."}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    text = extract_text_from_pdf(file_path)
    if not text:
        return jsonify({"error": "Could not extract text from the PDF."}), 500
    
    audio_file = os.path.join(AUDIO_FOLDER, f"{os.path.splitext(file.filename)[0]}.mp3")
    success, error = convert_text_to_speech(text, audio_file)
    
    if not success:
        return jsonify({"error": f"Speech conversion failed: {error}"}), 500
    
    return jsonify({"audio": os.path.basename(audio_file)})

@app.route("/audio/<filename>")
def get_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
