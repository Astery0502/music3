import matplotlib.pyplot as plt
import matplotlib.patches as patches
from functools import cached_property
from typing import Union, Iterable, List
from abc import ABC

ScaleStep = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
ScaleStep_2 = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MajorScale = [2,2,1,2,2,2,1]
MinorScale = [2,1,2,2,1,2,2]

class SCALES(ABC):

    @staticmethod
    def step2interval(steps:Iterable[int]):
        return [(steps[i]-steps[i-1])%12 for i in range(1, len(steps))]+ \
            [(steps[0]-steps[-1])%12]

    @staticmethod
    def index2step_1d(indices:Iterable[int]):
        return [ScaleStep[i] for i in indices]

    @staticmethod
    def index2step_2d(indices:Iterable[Iterable[int]]):
        return [[ScaleStep[i] for i in index] for index in indices]
    
    @staticmethod
    def step2index_1d(steps:Iterable[str]):
        return [ScaleStep.index(step) for step in steps]

    @staticmethod
    def step2index_2d(steps:Iterable[Iterable[str]]):
        return [[ScaleStep.index(step) for step in index] for index in steps]

    @staticmethod
    def plot_Steps(steps:Iterable[int]):
        
        # set the indices to the steps for display
        indices = steps

        # Define the keys on the keyboard
        keys = ScaleStep

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot white keys
        white_keys = [step for step in keys if len(step) == 1]
        white_key_positions = [0, 2, 4, 5, 7, 9, 11]

        for i, key in enumerate(white_keys):
            rect = patches.Rectangle((white_key_positions[i], 0), 1, 2, edgecolor='black', facecolor='white')
            ax.add_patch(rect)
            ax.text(white_key_positions[i] + 0.5, 1.0, key, ha='center', va='center', fontsize=12)

        # Plot black keys
        black_keys = [step for step in keys if len(step) == 2]
        black_key_positions = [1, 3, 6, 8, 10]

        for i, key in enumerate(black_keys):
            rect = patches.Rectangle((black_key_positions[i], 1), 1, 1, edgecolor='black', facecolor='black')
            ax.add_patch(rect)
            ax.text(black_key_positions[i]+0.5, 1.5, key, ha='center', va='center', fontsize=12, color='white')

        # Highlight the scale steps
        seq = 0
        for i, step in enumerate(indices):
            ax.text(step+0.5, 0.5, i, ha='center', va='center', fontsize=12, color='r')

        # Set the limits and remove the axes
        ax.set_xlim(-0.5, 12.5)
        ax.set_ylim(-0.1, 2)
        ax.axis('off')

        # Set the aspect ratio to be equal
        ax.set_aspect('equal')

        # Show the plot
        plt.show()

        print("Scale Steps: ", [keys[i] for i in indices])

class scale(SCALES):

    def __init__(self, scaleName:Union[str, Iterable[int]]):

        """
        Single scale from given scale name eg: C, Cm

        Parameters:
        scaleName (str): The scale name

        Returns:
        None

        >>> s = scale('Db')
        >>> s.step == 'Db'
        True
        >>> s.index == 1
        True
        >>> s.get_ScaleSteps() == ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C']
        True
        >>> s1 = scale([0, 2, 3, 5, 7, 8, 10])
        >>> s1.name == 'Cm'
        True
        """

        if isinstance(scaleName[0], int):
            # Read the scale interval from the input int list
            step_interval = self.step2interval(scaleName)
            if step_interval == MajorScale:
                self.scale = MajorScale
            elif step_interval == MinorScale:
                self.scale = MinorScale
            else:
                raise ValueError(f"Invalid scale type: {step_interval}")
            
            # Save the scale name and base step and its index
            self.ScaleIndex = scaleName
            self.step = self.index2step_1d(scaleName)[0]
            self.index = scaleName[0]
            self.name = self.step + ('m' if self.scale == MinorScale else '')
            return

        # Check if the scale name is valid
        if scaleName[0] not in ScaleStep:
            raise ValueError(f"Invalid scale name: {scaleName}")

        # Save the scale name and base step and its index
        self.name = scaleName
        if (len(scaleName) > 1) & (scaleName[1] == 'b'):
            self.step = scaleName[0] + 'b'
            scaleName = scaleName[1:]
        else:
            self.step = scaleName[0]

        # check if the scale is major or minor
        if (len(scaleName) > 1):
            assert scaleName[1] == 'm', "Invalid minor scale name"
            self.scale = MinorScale
            scaleName = scaleName[1:]
        else:
            self.scale = MajorScale
        
        assert len(scaleName) == 1, f"Invalid scale name: {scaleName}"

        self.index = ScaleStep.index(self.step)

    def __repr__(self):
        return f"{self.name}: {self.get_ScaleSteps()}"

    @cached_property
    def ScaleIndex(self):
        # Get the index of the scale step based on the scale name
        return [(self.index + sum(self.scale[:i])) % 12 for i in range(7)]

    def get_ScaleSteps(self):
        # Get the scale steps based on the self.ScaleIndex to index on ScaleStep
        return self.index2step_1d(self.ScaleIndex)
    
    def get_mainChords(self):
        # Get the main chords of the scale (index)
        return [[self.ScaleIndex[i], self.ScaleIndex[(i+2)%7], 
                 self.ScaleIndex[(i+4)%7], self.ScaleIndex[(i+6)%7]] for i in range(7)]
    
    def plot_scale(self):
        # Plot the scale steps
        self.plot_Steps(self.ScaleIndex)
    


class chord(SCALES):

    def __init__(self, chordName:Union[str,Iterable[str]]):

        # check if the chord is a string or a list of strings
        if isinstance(chordName, str):
            self.name = chordName
            self.steps = chord.name2chord(chordName)
        else:
            self.steps = self.step2index_1d(chordName)
            self.name = chord.chord2name(self.steps)
    
    def __repr__(self):
        return f"{self.name}: {self.index2step_1d(self.steps)}"
    
    def get_scale(self):
        if len(self.steps) == 4:
            return self.chord2scale(self.steps)
        if (self.steps[2]-self.steps[1]) % 12 == 4:
            return self.chord2scale(self.steps+[self.steps[0]+10])
        return self.chord2scale(self.steps+[self.steps[0]+10]), \
            self.chord2scale(self.steps+[self.steps[0]+11])
        
    @staticmethod
    def _chords(rootIntervals:Iterable[int]):
        chords = [[si, (si+rootIntervals[0])%12, (si+rootIntervals[1])%12,
                    (si+rootIntervals[2])%12] for si in range(12)]
        return chord.index2step_2d(chords)
    
    @staticmethod
    def get_M3M7chords():
        # Get the major 3 and major 7 chords
        return chord._chords([4, 7, 11])

    @staticmethod
    def get_m3M7chords():
        # Get the minor 3 and major 7 chords, which is not in natural scale
        return chord._chords([3, 7, 11])
    
    @staticmethod
    def get_M37chords():
        # Get he major 3 and minor 7 chords
        return chord._chords([4, 7, 10])

    @staticmethod
    def get_m37chords():
        # Get the minor 3 and minor 7 chords (contains b5 minor chords)
        return chord._chords([3, 7, 10])+chord._chords([3, 6, 10])

    @staticmethod
    def chord2name(chord:Iterable[Union[int,str]]):
        """
        Convert a chord to its name

        Parameters:
        chord (Iterable[Union[int,str]]): The chord to convert

        Returns:
        str: The name of the chord

        >>> chord.chord2name([0, 4, 7, 11]) == 'CM7'
        True
        >>> chord.chord2name([0, 3, 7]) == 'Cm'
        True
        >>> chord.chord2name([0, 3, 6, 10]) == 'Cm7(b5)'
        True
        """

        # Convert the chord to indices if it is a list of strings and the length is 4/3
        if isinstance(chord[0], str):
            chord = chord.step2index_1d(chord)
        assert (len(chord) == 4) or (len(chord) == 3), "Invalid chord"

        # check minor/major 3rd chord
        # the mod operator is on [-11, 11] range to solve like 3,-9 equivalence issue
        if (((chord[1]-chord[0])%12) == 3): 
            chord3 = ScaleStep[chord[0]] + "m" 
        elif (((chord[1]-chord[0])%12) == 4): 
            chord3 = ScaleStep[chord[0]]
        else:
            raise ValueError("Invalid chord")

        # consider the (b5) at the end of the scale
        if len(chord) == 3:
            return chord3 + "(b5)" if (((chord[2]-chord[0])%12) == 6) else chord3

        # check minor/major 7th chord
        if (((chord[3]-chord[0])%12) == 10):
            chord7 = "7"
        elif (((chord[3]-chord[0])%12) == 11):
            chord7 = "M7"
        else:
            raise ValueError(f"Invalid chord with interval {chord[3]-chord[0]}")
        
        # also consider the (b5) at the end of the scale
        return chord3 + chord7 + "(b5)" if (((chord[2]-chord[0])%12) == 6) else chord3 + chord7

    @staticmethod
    def name2chord(name:str) -> List[int]:
        """
        Convert a chord name to its indices

        Parameters:
        name (str): The name of the chord

        Returns:
        List[int]: The indices of the chord

        >>> chord.name2chord('CM7') == [0, 4, 7, 11]
        True
        >>> chord.name2chord('Cm') == [0, 3, 7]
        True
        >>> chord.name2chord('Cm7(b5)') == [0, 3, 6, 10]
        True
        """
        # check if the chord base step name is valid
        if name[0] not in ScaleStep:
            raise ValueError(f"Invalid chord name: {name}")
        if (len(name) > 1) and (name[1] == 'b'):
            basestep = name[0] + 'b'
            name = name[1:]
        else:
            basestep = name[0]
        baseindex = ScaleStep.index(basestep)

        # return the case of the chord is only 3 major
        if len(name) == 1:
            return [baseindex, (baseindex+4)%12, (baseindex+7)%12]

        # check if the chord is 3rd minor or major
        if name[1] == 'm':
            interval3 = 3 # the interval from step1 to step3 is 3
            if len(name) == 2:
                return [baseindex, (baseindex+interval3)%12, (baseindex+7)%12]
            if name[2:] == '(b5)':
                return [baseindex, (baseindex+interval3)%12, (baseindex+6)%12]
            name = name[2:]
        else:
            interval3 = 4
            name = name[1:]
        
        # check if the chord is 7 major or minor
        assert name[0] in ['7', 'M'], f"Invalid chord for 7th chord: {name}"
        if name[0] == '7':
            # interval7 = 10
            if len(name) == 1:
                return [baseindex, (baseindex+interval3)%12, (baseindex+7)%12, 
                        (baseindex+10)%12]
            if name[1:] == '(b5)':
                return [baseindex, (baseindex+interval3)%12, (baseindex+6)%12, 
                        (baseindex+10)%12]
        elif name[0:] == 'M7':
            # interval7 = 11
            return [baseindex, (baseindex+interval3)%12, (baseindex+7)%12, 
                    (baseindex+11)%12]
    
    @staticmethod
    def chord2scale(chord:Iterable[int]):
        """
        Find the major scale of the chord with chord steps on the main steps

        Parameters:
        chord (Iterable[int]): The chord steps

        Returns:
        List[int]: The major scale steps
        """
        # The criteria is based on 2212221 intervals:
        # 1. 4 must be divided to 22
        # 2. 22 must be next to only one 1
        # 3. M7 has an 1 at the end, 7 has a 2 at the end
        # ! Note that the mM7 chords are not available in the natural scale

        # check if the chord is 7 major
        assert len(chord) == 4, "Invalid chord step number"
        assert (chord[1]-chord[0])%12 in [4, 3], "Invalid chord 3rd interval"
        assert (chord[2]-chord[0])%12 in [7, 6], "Invalid chord 5th interval"
        assert (chord[3]-chord[0])%12 in [10, 11], "Invalid chord 7th interval"

        # initiate scale steps (unsorted) and their intervals (unsorted)
        scale_steps = [0,0,0,0,0,0,0]
        scale_intervals = [0,0,0,0,0,0,0]
        # load known 1st 3rd 5th 7th to unsorted scale_steps
        for i in range(4):
            scale_steps[2*i] = chord[i]

        chord_intervals = [0,0,0]
        # check the interval between 1st, 3rd, 5th and 7th
        for i in range(3):
            # load the intervals between chords: like 334,343,434,433
            chord_intervals[i] = chord[i+1]-chord[i] if chord[i+1]>chord[i] \
                else chord[i+1]+12-chord[i]
            # if the chord_intervals[i] is 4, then the scale_intervals[i,i+1] is 2
            if chord_intervals[i] == 4:
                scale_steps[2*i+1] = (chord[i]+2) % 12
                scale_intervals[i] = 2
                scale_intervals[i+1] = 2
        
        # according to the M7 or 7 chord (intervals between 1st and 7th), decide the last interval
        assert sum(chord_intervals) in [11, 12], f"Invalid chord 7th interval: {chord_intervals}"
        scale_intervals[-1] = 1 if sum(chord_intervals) == 11 else 2

        # iterate the scale_intervals based on our criteria
        if scale_intervals[0] == 0 & scale_intervals[-2] == 0:
            scale_intervals = [2,1,2,2,1,2,2]
            sorted_scale_steps = scale_steps[2:] + scale_steps[:2]
        elif scale_intervals[0] == 0 & scale_intervals[-2] == 2:
            scale_intervals = [1,2,2,1,2,2,2]
            sorted_scale_steps = scale_steps[1:] + scale_steps[:1]
        elif scale_intervals[0] == 2 & scale_intervals[-2] == 0:
            scale_intervals = [2,2,1,2,2,1,2]
            sorted_scale_steps = scale_steps[3:] + scale_steps[:3]
        else:
            scale_intervals = [2,2,1,2,2,2,1]
            sorted_scale_steps = scale_steps
        
        # here we only find the major scale, with parallel minor scale just move the base step 2 backward
        return scale_steps

        # there is definitely a 4 in scale_intervals
    
    @staticmethod
    def plot_chord(chord1:Iterable[int]):
        chord.plot_Steps(chord1) 
    
class diatonic_chord(chord):

    def __init__(self, chordname:str):
        """
        Diaotonic chord with the name of the chord
        [C, Dm, Em, F, G, Am, Bm(b5)]

        Parameters:
        chordname (str): The chord name

        Returns:
        None
        """
        assert chordname in ScaleStep, f"Invalid scale name: {chordname}"
        assert chordname[0] != 'B', "B  is not supported"
        assert len(chordname) < 3, f"Invalid chord name length: {len(chordname)}"
        if (len(chordname) == 1):
            super().__init__(chordname + ('m' if chordname in ['D','E','A'] else ''))
        elif chordname[0] in ['D','E','A']:
            assert chordname[1] == 'm', f"Invalid chord name for minor {chordname}"
            super().__init__(chordname)
        else:
            raise ValueError(f"Invalid chord name: {chordname}")
    
class dchord_progression:

    def __init__(self, chordprogression:Iterable[str]):
        """
        Diaotonic chord progression with the name of the chords
        [C, Dm, Em, F, G, Am, Bm(b5)]

        Parameters:
        chordprogression (Iterable[str]): The chord progression

        Returns:
        None
        """
        self.chords = [diatonic_chord(chord) for chord in chordprogression]

    def __repr__(self):
        return f"{[chord.name for chord in self.chords]}: {[chord.get_ScaleSteps() for chord in self.chords]}"

    def get_progression(self):
        return [chord.get_ScaleSteps() for chord in self.chords]

    def plot_progression(self):
        for chord in self.chords:
            chord.plot_scale()


def test_m37chords():
    m37 = chord.get_m37chords()
    for c in m37:
        name = chord.chord2name(c)
        c2 = chord.name2chord(name)
        c2 = [ScaleStep[i] for i in c2]
        assert c2 == c , f"Error: {c} != {c2}"
