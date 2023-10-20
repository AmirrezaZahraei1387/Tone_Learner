import pydub
from numpy import array
from numpy import float32
from numpy import int16


def read_audio(f, normalized=False):
    """wav to numpy array"""
    a = pydub.AudioSegment.from_wav(f)
    y = array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, float32(y) / 2**15
    else:
        return a.frame_rate, y


def write_audio(f, sr, x, normalized=False):
    """numpy array to wav"""
    if x.ndim == 2 and x.shape[1] == 2:
        channels = 2
    else:
        channels = 1

    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = int16(x * 2 ** 15)
    else:
        y = int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="wav", bitrate="320k")
