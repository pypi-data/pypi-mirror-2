# workout_timer.py
#
# depends on espeak, only tested under Linux
# By Jesse O'Brien to integrate with the Men's Health Spartacus workout by Adam Campbell and Rachel Cosgrove.	
# Details on the workout are available here: http://www.menshealth.com/spartacus/workouts/
# Difficulty adjusts the work and recovery time for each workout.

import sys, os, time
from threading import Thread

difficulty = 1 # multiplier for all workouts, from .1-1 (.1 = 10% difficulty, 1 = 100% difficulty, 2 = 200% difficulty)
###########################
# all variables are in seconds
leadin = 10 # preparation before starting workout, minimum 10
stationRecovery = 15 / difficulty # in seconds
work = 60 * difficulty # in seconds
stretch = 30
stations = ['goblet squat','mountain climber','single arm dumbell swing','t pushup', 'split jump','Dumbbell row','Dumbbell side lunge and touch','Pushup-position row','Dumbbell lunge and rotation','Dumbbell push press']

class spkThread(Thread):
	def __init__ (self):
		Thread.__init__(self)
		self._active = True
		self._speakText = None

	def run(self):
		while self._active:
			if self._speakText:
				os.system('espeak "%s"' % self._speakText)
				self._speakText = None
			else:
				time.sleep(0.1)

	def speak(self, text):
		self._speakText = text

	def terminate(self):
		self._active = False

def printNSpeak(text):
	spkThread.speak(text)
	print text

def countdown(self):
	num = self
	while num >= 1:
		printNSpeak("%s" % num)
		time.sleep(1)
		num = num - 1

spkThread = spkThread()
spkThread.start()
try:
	printNSpeak("%d seconds until the workout begins!" % leadin)
	time.sleep(leadin - 6)
	printNSpeak("Stretch for %s seconds." % stretch)
	time.sleep(stretch)
	for station in stations:
		printNSpeak("Get ready for %s station..." % station)
		time.sleep(3)
		printNSpeak("10 seconds!")
		time.sleep(9)
		countdown(3)
		printNSpeak("Begin %s" % station)
		printNSpeak("Work out for %d seconds." % work)
		time.sleep(work - 3)
		countdown(3)
		printNSpeak("Stop")
		time.sleep(3)
		printNSpeak("Take a breather for %d seconds." % stationRecovery)
		time.sleep(stationRecovery - 10) # imprecise but is accurate enough for this
	printNSpeak("Stretch for %s." % stretch)
	printNSpeak("Session complete.	Good workout!")

except KeyboardInterrupt:
	spkThread.terminate()
finally:
	spkThread.terminate()

