import pydub
from pydub import AudioSegment
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


mytext = 'Welcome to the home!'
language = 'en'


def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y


def write(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")


def convert_1d(array):
    f = []
    for i in array:
        f.append(i[0])
    return f


l_x, learning_audio = read("learn.mp3")
n_x, normal_audio = read("welcome.mp3")
# normalizing  the data to match lengths
learning_audio = learning_audio[len(learning_audio)-len(normal_audio):]
learning_audio = convert_1d(learning_audio)


mymodel = np.poly1d(np.polyfit(normal_audio, learning_audio, 3))
newaudio = []

for i in normal_audio:
    newaudio.append(mymodel(i)+10)

write("hello.mp3", n_x, np.array(newaudio))

song = AudioSegment.from_mp3("hello.mp3")
song = song + 50
song.export("hello.mp3", format='mp3')

plt.plot(newaudio)
plt.show()

