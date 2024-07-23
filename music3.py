"""
The music3 module is a collection of classes and functions for working with music in Python.
It utilizes the music21 library for music representation and manipulation.

The main goal is to provide a simple and intuitive interface for creating and manipulating music objects.
Clarify and simplify the music21 library for common tasks.

"""
from music21 import environment, scale, note, chord, stream, harmony, key, roman
from typing import Union, List

# Set up the music21 environment
us = environment.UserSettings()
us['musescoreDirectPNGPath'] = 'D:\\apps\\musescore\\bin\\MuseScore4.exe'
classical_major_chord = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'viio']
classical_minor_chord = ['i', 'iio', 'III', 'iv', 'v', 'bVI', 'bVII']

class diatonic_chord(chord.Chord):
    """
    A class for creating diatonic chords in a given key.
    """
    def __init__(self, chord_init:List[Union[str, int]], _key:str='C'):
        """
        Create a diatonic chord in a given key.

        Parameters:
        chord_init: str or list of str or int
            The chord name or chord tones.
        scale: music21.scale.MajorScale or music21.scale.MinorScale

        Returns:
        music21.chord.Chord
        """
        # chord init
        super().__init__(chord_init)

        # some custom attributes
        self._key = key.Key(_key)
        self._scale = self._key.getScale()
        self.classicalChordName = roman.romanNumeralFromChord(self, self._scale).figure

        if isinstance(self._scale, scale.MajorScale):
            self.isDiatonic = True if self.classicalChordName in classical_major_chord else False
        elif isinstance(self._scale, scale.MinorScale):
            self.isDiatonic = True if self.classicalChordName in classical_minor_chord else False
        else:
            self.isDiatonic = False
    
class split_chord(chord.Chord):
    """
    A class for splitting a chord into two parts.
    """
    def __init__(self, chord_init):
        """
        Split a chord into two parts.

        Parameters:
        chord_init: str or list of str or int
            The chord name or chord tones.
        scale: music21.scale.MajorScale or music21.scale.MinorScale

        Returns:
        music21.chord.Chord
        """
        super().__init__(chord_init)
        
    @classmethod
    def from_chord(cls, chord:chord.Chord):
        return cls(chord.pitches)

    def __str__(self):
        return self.split_chord