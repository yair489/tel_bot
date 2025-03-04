import google.generativeai as genai
import json
import os
import time
from itertools import permutations

# ✅ Replace with your actual Gemini AI API Key
GEMINI_API_KEY = "AIzaSyCn4I1LomNR4MJSOF0xP1JRirad5Q0YcdA"

# ✅ Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ✅ List of the top 10 most spoken languages
LANGUAGES = [
    "English", "Spanish", "Chinese", "Hindi", "Arabic",
    "French", "Bengali", "Russian", "Portuguese", "German"
]

# ✅ Ensure output directory exists
OUTPUT_DIR = "generated_word_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_words(known_lang, unknown_lang):
    """ Generate 5 translated words using Gemini AI """
    prompt = f"""
    Generate a list of 15 common words in {known_lang} and their translations in {unknown_lang}.
    Provide each word in this structured format:

    [
        {{
            "word_id": "<word in {unknown_lang}>",
            "meaning": "<translation in {known_lang}>",
            "similar_words": ["<similar word 1 in {known_lang}>", "<similar word 2 in {known_lang}>", "<similar word 3 in {known_lang}>"],
            "sentence_with_word": "<example sentence in {unknown_lang}>"
        }},
        ...
    ]

    Return ONLY a valid JSON array, nothing else.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt, generation_config={"max_output_tokens": 2048})

        if not response.text.strip():
            print(f"⚠️ Empty response from Gemini AI for {known_lang} → {unknown_lang}")
            return []

        print(f"🔹 Raw Response from API ({known_lang} → {unknown_lang}):\n{response.text}\n")

        return json.loads(response.text.strip())  # Convert response to JSON format

    except json.JSONDecodeError as e:
        print(f"❌ JSON Error for {known_lang} → {unknown_lang}: {e}")
        return []

    except Exception as e:
        print(f"❌ Error generating words for {known_lang} → {unknown_lang}: {e}")
        return []

def create_language_files():
    """ Create JSON word files for each language pair """
    print("func")
    unknown_lang = "Arabic"
    known_lang = "Hebrew"
    # for known_lang, unknown_lang in permutations(LANGUAGES, 2):
    print(f"📖 Generating words for {known_lang} → {unknown_lang}...")
    words_data = generate_words(known_lang, unknown_lang)

    if words_data:
        filename = f"{OUTPUT_DIR}/{known_lang.upper()}_{unknown_lang.upper()}_WORDS.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(words_data, f, indent=4, ensure_ascii=False)
        print(f"✅ File saved: {filename}")
    else:
        print(f"⚠️ Skipped {known_lang} → {unknown_lang} due to errors.")

        # time.sleep(3)  # Add delay to avoid API rate limits

if __name__ == "__main__":
    create_language_files()
    print("🎉 All files generated successfully!")