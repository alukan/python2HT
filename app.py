from flask import Flask, render_template, request, send_file
from google.cloud import translate_v2, texttospeech
import time
import os

tts_client = texttospeech.TextToSpeechClient()

SUPPORTED_GENDER_LANGUAGES = {
    'pl': None,  # Polish
    'en': texttospeech.SsmlVoiceGender.NEUTRAL,  # English
    'ru': texttospeech.SsmlVoiceGender.FEMALE,  # Russian
    'es': None,  # Spanish
    'fr': None,  # French
}

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'

translate_client = translate_v2.Client()


@app.route('/')
def home():
    return 'Hello, welcome to my Flask app!'


@app.route('/form', methods=['GET', 'POST'])
def process_form():
    translated_text = None
    audio_file = 'static/output.wav'  # Fixed filename

    user_input = request.form.get('user_input')
    target_language = request.form.get('target_language')

    # Check if target_language is None or empty
    if target_language is None or not target_language.strip():
        return render_template('form.html', error="Target language is required", translated_text=translated_text, audio_file=audio_file)

    # Translate the input to the selected language
    translation = translate_client.translate(user_input, target_language=target_language)
    translated_text = translation['translatedText']

    # Determine the voice gender based on language
    supported_gender = SUPPORTED_GENDER_LANGUAGES.get(target_language, texttospeech.SsmlVoiceGender.NEUTRAL)

    # Generate speech from translated text
    synthesis_input = texttospeech.SynthesisInput(text=translated_text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=target_language, ssml_gender=supported_gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )

    with open(audio_file, 'wb') as out:
        out.write(response.audio_content)

    timestamp = int(time.time())
    return render_template('form.html', translated_text=translated_text, audio_file=f'{audio_file}?v={timestamp}')
@app.route('/get_audio')
def get_audio():
    audio_file = 'static/output.wav'
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
