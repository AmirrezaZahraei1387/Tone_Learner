# Import the required module for text
# to speech conversion
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


def set_speed(from_file: str, to_file: str, speed: float):
    audio = AudioSegment.from_file(from_file)
    audio = audio.speedup(playback_speed=speed)
    audio.export(to_file)


def convert_to_speed(text: str, to_file: str, lang='en'):
    language = 'en'
    myObj = gTTS(text=text, lang=language, slow=True)
    myObj.save(to_file)


set_speed("original.wav", "original_.wav", 9/7)

