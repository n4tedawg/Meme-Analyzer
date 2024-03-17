import openai
import requests
import os
import json
import logging
from google.cloud import vision
from google.cloud.vision_v1 import types
from flask import Flask, render_template, request, jsonify
from flask import send_from_directory

app = Flask(__name__)

key_path = "yourkeyhere"
credentials = "yourkeyhere"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "yourkeyhere"
openai.api_key = "yourkeyhere"
client = vision.ImageAnnotatorClient()
logging.basicConfig(level=logging.DEBUG)

# Add this code to serve the favicon.ico file
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'favicon_io'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def get_image_description(image_content):
    image = types.Image(content=image_content)

    # Perform text detection
    text_response = client.text_detection(image=image)
    texts = text_response.text_annotations

    # Perform object detection
    object_response = client.object_localization(image=image)
    objects = object_response.localized_object_annotations

    # Perform face detection
    face_response = client.face_detection(image=image)
    faces = face_response.face_annotations

    descriptions = []

    # Add detected text to descriptions
    if texts:
        descriptions.append("Text: " + texts[0].description.strip())

    # Add detected objects to descriptions
    if objects:
        object_names = ", ".join([obj.name for obj in objects])
        descriptions.append("Objects: " + object_names)

    # Add detected faces to descriptions
    if faces:
        descriptions.append("Faces: " + str(len(faces)))

    if descriptions:
        return "; ".join(descriptions)
    else:
        return "No text or objects found"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/explain_meme', methods=['POST'])
def explain_meme():
    try:
        image_file = request.files['image']
        image_content = image_file.read()
        meme_description = get_image_description(image_content)
        prompt = f"Explain this meme with the following details: {meme_description}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100,
            stop=None,
        )
        explanation = response.choices[0].text.strip()
        return render_template("explain_meme.html", explanation=explanation)
    except Exception as e:
        logging.error(f"Error in explain_meme route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/terms_of_service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)