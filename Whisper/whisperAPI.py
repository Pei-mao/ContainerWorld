# Speech-to-Text Backend API with Flask

from flask import Flask, request, jsonify
import whisper
import os

# Flask Instance
app = Flask(__name__)

# Load Whisper Model
model = whisper.load_model("base")

# Speech-to-Text API
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Ensure file is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        file.save(temp_file_path)

        # Transcribe audio using Whisper
        result = model.transcribe(temp_file_path)

        # Clean up temporary file
        os.remove(temp_file_path)

        return jsonify({"text": result["text"]})

    except Exception as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
