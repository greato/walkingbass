#import mingus.core.notes as notes
#import mingus.core.diatonic as diatonic
import mingus.core.intervals as intervals
import mingus.core.chords as chords
#import mingus.core.scales as scales
from mingus.containers.Bar import Bar
from mingus.containers.Track import Track
import mingus.extra.LilyPond as LilyPond
from mingus.containers.Instrument import Instrument
from mingus.containers.Composition import Composition
from mingus.containers.Note import Note

from random import shuffle
from itertools import repeat

class walking_bass():
	''' walking_bass
		Generates basslines from chords procedurally because bass outlines the chordal tone fancy free
			1. lookup chordal tones
			2. sort notes by proximity to the rootnote of the next chord
			3. add bells and whistles when appropriate
			4. add notes patterns for long ones (Longest Substring Algorithm)
		Usage: 
		>>> B = walking_bass(['Bb','Eb7',['Bb','F7'],'Bb7','Eb7','Eb07',['Bb','F7'],'Bb','F7','F7','Bb','Bb'])
		>>> B.prox_interval()
		>>> print B.bassline
	'''
	def __init__(self, chords, title = 'Generated by PyWalking_bass'):
		self.title = title
		self.chords = chords
		self.chordsd = []
		self.bassline = self._realbook(self.chords)
		self.bassline = self.prox_interval()

		self.i = Instrument()
		self.i.name = "Jazz Bass"
		self.i.clef = "bass"
		self.i.set_range((Note('E-1'), Note('D-5')))

		self.track = self._create_track()
		self.track.add_chords(self.chords)
		#print self.track
		self.to_png()

	def _realbook(self, score, depth = 0): 
		'''recusive function, looks up tones like fake books'''
		bassline = []
		for chord in score:
			if type(chord) is list:
				bassline.append(self._realbook(chord,depth+1))
			else:
				notes = chords.from_shorthand(chord)
				rest = notes[1:]
				shuffle(rest)
				notes = [notes[0]] + rest
				take = 4 - depth*2 # [C]xxxx|[G]xx[B]xx|[D]xxxx
				final = notes[:take]
				bassline.append(final)
				self.chordsd.append([chord,final])
		return bassline
	def prox_interval(self): 
		''' sort notes by proximity to the next chord'''
		bassline = []
		for (i, notes) in enumerate(self.chordsd):
			chordname = notes[0]
			rootnote = notes[1][0]
			notes = notes[1][1:]
			try:
				next_chord = self.chordsd[i+1][1][0]
			except IndexError:
				pass
			notes = sorted(notes, key=lambda n: abs(intervals.measure(n,next_chord)-5)) # out of 10 notes
			final = [rootnote] + notes
			bassline.append( final )
			self.chordsd[i] = [chordname, final]
		self.bassline = bassline
		return bassline
	


	def _create_track(self):
		tp = Track(self.i)
		b = Bar( (4,4) )	
		for chord in self.chordsd:
			for i in chord[1]:
				tp + (i+'-3')
		return tp
	def to_png(self):
		c = Composition()
		c.set_author('Liqi Han')
		c.set_title(self.title)
		c.add_track(self.track)
		ly_string = LilyPond.from_Composition(c)
		#print ly_string
		LilyPond.to_png(ly_string, self.title)


				# TODO: memory of pattern
				# triplets and bells and whistles
				# add scales

		
#DONE! displaying chord names
#TODO: up down the staff C-1 or C-2  ??



if __name__ == '__main__':
	B = walking_bass(['Bb','Eb7',['Bb','F7'],'Bb7','Eb7','Eb07',['Bb','F7'],'Bb','F7','F7','Bb','Bb'],'Blue Monk') # Blue Monk - Thelonious Monk
	# B = walking_bass(['C','Bb'],'Tester')
	