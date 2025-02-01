from flask import Flask, request, jsonify
import random
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Expanded Language dataset with at least 200 languages
LANGUAGES = [
    {"name": "Spanish", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ʒ/", "region": "Europe, Americas"},
    {"name": "Japanese", "group": "Japonic", "morphology": "Agglutinative", "syntax": "SOV", "least_used_phoneme": "/f/", "region": "East Asia"},
    {"name": "Swahili", "group": "Bantu", "morphology": "Agglutinative", "syntax": "SVO", "least_used_phoneme": "/h/", "region": "East Africa"},
    {"name": "Turkish", "group": "Turkic", "morphology": "Agglutinative", "syntax": "SOV", "least_used_phoneme": "/ʒ/", "region": "Anatolia, Central Asia"},
    {"name": "English", "group": "Indo-European", "morphology": "Isolating", "syntax": "SVO", "least_used_phoneme": "/x/", "region": "Global"},
    {"name": "Russian", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/θ/", "region": "Eastern Europe"},
    {"name": "Mandarin", "group": "Sino-Tibetan", "morphology": "Isolating", "syntax": "SVO", "least_used_phoneme": "/v/", "region": "China"},
    {"name": "Arabic", "group": "Afro-Asiatic", "morphology": "Templatic", "syntax": "VSO", "least_used_phoneme": "/p/", "region": "Middle East, North Africa"},
    {"name": "Hindi", "group": "Indo-European", "morphology": "Fusional", "syntax": "SOV", "least_used_phoneme": "/z/", "region": "India"},
    {"name": "French", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/w/", "region": "Europe, Africa"},
    {"name": "German", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ʒ/", "region": "Europe"},
    {"name": "Korean", "group": "Koreanic", "morphology": "Agglutinative", "syntax": "SOV", "least_used_phoneme": "/z/", "region": "Korea"},
    {"name": "Italian", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ʃ/", "region": "Europe"},
    {"name": "Portuguese", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/h/", "region": "Europe, Americas"},
    {"name": "Bengali", "group": "Indo-European", "morphology": "Fusional", "syntax": "SOV", "least_used_phoneme": "/f/", "region": "India, Bangladesh"},
    {"name": "Vietnamese", "group": "Austroasiatic", "morphology": "Isolating", "syntax": "SVO", "least_used_phoneme": "/r/", "region": "Vietnam"},
    {"name": "Greek", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ʃ/", "region": "Europe"},
    {"name": "Hebrew", "group": "Afro-Asiatic", "morphology": "Templatic", "syntax": "VSO", "least_used_phoneme": "/p/", "region": "Middle East"},
    {"name": "Thai", "group": "Kra-Dai", "morphology": "Isolating", "syntax": "SVO", "least_used_phoneme": "/v/", "region": "Thailand"},
    {"name": "Polish", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ʒ/", "region": "Europe"},
    {"name": "Dutch", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ɲ/", "region": "Europe"},
    {"name": "Czech", "group": "Indo-European", "morphology": "Fusional", "syntax": "SVO", "least_used_phoneme": "/ʃ/", "region": "Europe"}
]

# Store the last chosen language and reset every 24 hours
LAST_LANGUAGE_TIME = 0
correct_language = None

def choose_daily_language():
    global LAST_LANGUAGE_TIME, correct_language
    current_time = int(time.time())
    if correct_language is None or current_time - LAST_LANGUAGE_TIME > 86400:  # 24 hours in seconds
        correct_language = random.choice(LANGUAGES)
        LAST_LANGUAGE_TIME = current_time

choose_daily_language()

def get_similarity_color(correct_value, guess_value):
    if correct_value == guess_value:
        return "green"
    elif correct_value in guess_value or guess_value in correct_value:
        return "yellow"
    else:
        return "red"

@app.route("/guess", methods=["POST"])
def guess_language():
    choose_daily_language()
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
        "correct_attributes": {}
    }
    
    for key in ["group", "morphology", "syntax", "least_used_phoneme", "region"]:
        if correct_language[key] == guessed_language[key]:
            response["correct_attributes"][key] = f"{key}: {correct_language[key]}"
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)