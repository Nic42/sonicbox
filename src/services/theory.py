from functools import lru_cache

from pytheory import TonedScale

from constants.synth import SCALES


@lru_cache()
def get_note_name(tonic, scale, degree):
    tonic = tonic.upper()

    if not (tonic and scale):
        return str(degree + 1)

    tone = TonedScale(tonic=tonic)

    try:
        scale_ = tone[scale]
    except KeyError:
        return str(degree + 1)

    return scale_[degree].name


def is_octave(note, scale):
    return bool(note % SCALES[scale] == 0)


def get_chord_name(tonic, key_type, degree):
    tonic = tonic.upper()

    key = TonedScale(tonic=tonic)[key_type]

    return key[degree].name
