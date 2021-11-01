from typing import ForwardRef
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

'''
@param tone_amp tone amplitude
@param tone_dur tone duration
@param freq_t target frequency
@param freq_d distractor frequency
@param fs sampling rate
'''
tone_amp = 1.0 #? full-scale is 1
tone_dur = 2.5 #? 2.5 seconds
tone_playtime = 0.02 #? 20 milliseconds
tone_pause = 0.005 #? 5 milliseconds
total_tones = int(tone_dur/(tone_playtime + tone_pause)) #? (2.5/0.025) = 100
freq_t = np.array([1000.0, 1000.0]) #? 1KHz
freq_d = np.array([1100.0, 1100.0]) #? 1.1KHz
fs = 44100

#* time instance
t = np.arange(np.ceil(tone_dur * fs)) / fs
#* to generate stereo signal
t = t.reshape(-1, 1)

#* list of 1's and 0's
play_1s = np.ones(np.ceil(tone_playtime * fs))
play_0s = np.zeros(np.ceil(tone_pause * fs))

# target mono tone and distractor mono tone
target_tone = tone_amp * np.sin(2 * np.pi * freq_t * t)
distractor_tone = tone_amp * np.sin(2 * np.pi * freq_d * t)

#? New frequency array to create multi-channel signal
freq = np.array([   0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0])  #? channel 1 - target, channel 2 - distractor, channel 13 - trig
#! but all tones have have amplitude
tone_18CH = tone_amp * np.sin(2 * np.pi * freq * t)

#? change the trigger amplitude by explicitly replacing the 13th column
tone_18CH[:, 12] = 0.25

fig = plt.figure()
gs = gridspec.GridSpec(nrows = 3, ncols = 2)
ax1 = fig.add_subplot(gs[0,0])
ax1.plot(target_tone[:500])
ax1.grid()
ax1.set_title("Target Tone")
ax2 = fig.add_subplot(gs[0,1])
ax2.plot(distractor_tone[:500])
ax2.grid()
ax2.set_title("Distractor Tone")
ax3 = fig.add_subplot(gs[1,:])
ax3.plot(tone_18CH[:500])
ax3.grid()
ax3.set_title("18 Channel Array : Trig = 0.25")

#? change the trigger amplitude by explicitly replacing the 13th column
tone_18CH[:, 12] = 0.5
ax4 = fig.add_subplot(gs[2,:])
ax4.plot(tone_18CH[:500])
ax4.grid()
ax4.set_title("18 Channel Array : Trig = 0.50")

plt.show()

sd.default.device = 3
sd.default.channels = 18
sd.play(tone_18CH, fs)