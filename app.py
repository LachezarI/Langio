from flask import Flask, request, jsonify
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample language data
LANGUAGES = [
    {"name": "Spanish", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ʒ/", "region": "Europe, Americas"},
    {"name": "Japanese", "group": "Japonic", "morphology": "Agglutinative", "syntax": "SOV", "least_used_phoneme": "/f/", "region": "East Asia"},
    {"name": "Swahili", "group": "Bantu", "morphology": "Agglutinative", "syntax": "SVO", "least_used_phoneme": "/h/", "region": "East Africa"},
    {"name": "Turkish", "group": "Turkic", "morphology": "Agglutinative", "syntax": "SOV", "least_used_phoneme": "/ʒ/", "region": "Anatolia, Central Asia"},
]

# Pick a random language when the server starts
correct_language = random.choice(LANGUAGES)

def get_similarity_color(correct_value, guess_value):
    if correct_value == guess_value:
        return "green"
    elif correct_value in guess_value or guess_value in correct_value:
        return "yellow"
    else:
        return "red"

@app.route("/guess", methods=["POST"])
def guess_language():
    user_guess = request.json.get("language", "").strip()
    guessed_language = next((lang for lang in LANGUAGES if lang["name"].lower() == user_guess.lower()), None)

    if not guessed_language:
        return jsonify({"error": "Language not found"}), 400

    response = {
        "group": get_similarity_color(correct_language["group"], guessed_language["group"]),
        "morphology": get_similarity_color(correct_language["morphology"], guessed_language["morphology"]),
        "syntax": get_similarity_color(correct_language["syntax"], guessed_language["syntax"]),
        "least_used_phoneme": get_similarity_color(correct_language["least_used_phoneme"], guessed_language["least_used_phoneme"]),
        "region": get_similarity_color(correct_language["region"], guessed_language["region"]),
    }

    return jsonify(response)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)