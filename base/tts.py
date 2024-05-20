from gtts import gTTS
import pyttsx3
from translate import Translator

def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation

def synthesize_speech(text, language_code, gender):
    if language_code == 'ur':
        text = translate_text(text, 'ur')

    if gender == 'male':
        engine = pyttsx3.init()
        engine.setProperty('voice', 'english')
        engine.say(text)
        engine.save_to_file(text, 'output.mp3')
        engine.runAndWait()
        with open('output.mp3', 'rb') as audio:
            audio_content = audio.read()
        return audio_content
    elif gender == 'female':
        tts = gTTS(text=text, lang=language_code, slow=False)
        audio_file = 'output.mp3'
        tts.save(audio_file)
        with open(audio_file, 'rb') as audio:
            audio_content = audio.read()
        return audio_content
