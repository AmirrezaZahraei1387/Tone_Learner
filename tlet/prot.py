from numpy import poly1d, polyfit, ndenumerate
from numpy import empty as np_empty
from numpy import array
import tlet.oi as io
import tlet.tone as tone


def normalize_size(base_f_o, original_f_o):
    """if the size of the two audios are not equal
    this functon  will cut off the part to make them equal."""

    if len(original_f_o) > len(base_f_o):
        original_f_o = original_f_o[len(original_f_o) - len(base_f_o):]
    else:
        base_f_o = base_f_o[len(base_f_o) - len(original_f_o):]

    return base_f_o, original_f_o


def PutIn1D(__array__: array):

    length = len(__array__)
    vector = np_empty(length)

    for index in range(length):
        vector[index] = sum(__array__[index])

    return vector


def tletprocess(base_file: str, original_file: str):
    """getting the file names of audios and then start use
     the polynomial regression on them to predict the tone
     of the person

     original file is the sound of the person we want to
     learn their tone, and the base_file is the base saying of
     the text. it can be for example the way that Google Translate
     say the word."""

    lx, original_f_o = io.read_audio(original_file)
    ly, base_f_o = io.read_audio(base_file)
    base_f_o, original_f_o = normalize_size(base_f_o, original_f_o)

    if len(original_f_o.shape) != 1:
        original_f_o = PutIn1D(original_f_o)
    if len(base_f_o.shape) != 1:
        base_f_o = PutIn1D(base_f_o)

    return tone.ToneOPoly(polyfit(original_f_o, base_f_o, 3))


def tpredict_audio(from_file: str, to_file: str, tone_obj: tone.ToneOPoly, frame_rate: int = None):

    fr, audio = io.read_audio(from_file)
    p_module = poly1d(tone_obj.polyfit)

    if frame_rate is not None:
        fr = frame_rate

    if len(audio.shape) == 1:
        new_audio = np_empty(len(audio))
        for indexi, element in ndenumerate(audio):
            new_audio[indexi[0]] = p_module(element)
    else:
        new_audio = np_empty((len(audio), len(audio[0])))
        for indexi, elements in ndenumerate(audio):
            for indexj, el in ndenumerate(elements):
                new_audio[indexi[0]][indexj[0]] = p_module(el)

    io.write_audio(to_file, fr, new_audio)

