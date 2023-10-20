from numpy import poly1d, polyfit, np_empty, ndenumerate
import tlet.oi as io
import tlet.tone as tone


def normalize_size(original_f_o, base_f_o):
    """if the size of the two audios are not equal
    this functon  will cut off the part to make them equal."""

    if len(original_f_o) > len(base_f_o):
        original_f_o = original_f_o[len(original_f_o) - len(base_f_o):]
    else:
        base_f_o = base_f_o[len(base_f_o) - len(original_f_o):]


def tletprocess(original_file: str, base_file: str):
    """getting the file names of audios and then start use
     the polynomial regression on them to predict the tone
     of the person

     original file is the sound of the person we want to
     learn their tone, and the base_file is the base saying of
     the text. it can be for example the way that Google Translate
     say the word."""

    lx, original_f_o = io.read_audio(original_file)
    ly, base_f_o = io.read_audio(base_file)

    normalize_size(original_f_o, base_f_o)
    return tone.ToneOPoly(polyfit(base_f_o, original_f_o, 3))


def tpredict_audio(from_file: str, to_file: str, tone_obj: tone.ToneOPoly, frame_rate: int = None):

    fr, audio = io.read_audio(from_file)
    p_module = poly1d(tone_obj.polyfit)
    new_audio = np_empty(len(audio))

    if frame_rate is not None:
        fr = frame_rate

    for index, element in ndenumerate(audio):
        new_audio[index[0]] = p_module(element)

    io.write_audio(to_file, fr, new_audio)


