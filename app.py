from flask import Flask, render_template, request
from google.cloud import translate_v2
import os

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'

translate_client = translate_v2.Client()

@app.route('/')
def home():
    return 'Hello, welcome to my Flask app!'

@app.route('/form', methods=['GET', 'POST'])
def form():
    translated_text = None

    if request.method == 'POST':
        user_input = request.form.get('user_input')

        translation = translate_client.translate(user_input, target_language='es')
        print(*translation)
        translated_text = translation['translatedText']

    return render_template('form.html', translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
