#!/usr/bin/env python
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from random import shuffle

'''
@param 
    tone_amp        -   tone amplitude
    tone_dur        -   tone duration
    tone_playtime   -   tone playing time
    tone_pause      -   tone pause/idle time
    total_tones     -   total number of tones to be played
    total_distract  -   total number of distraction freq tones
    freq_t          -   target frequency
    freq_d          -   distractor frequency
    fs              -   sampling rate
'''
tone_amp = 1.0 #? full-scale is 1
tone_dur = 2.5 #? 2.5 seconds
tone_playtime = 0.015 #? 20 milliseconds
tone_pause = 0.01 #? 5 milliseconds
total_tones = int(tone_dur/(tone_playtime + tone_pause)) #? (2.5/0.025) = 100
total_distract = 3
freq_t = np.array([1000.0, 1000.0, 0.0]) #? 1KHz Stereo, Trigger
freq_d = np.array([1100.0, 1100.0, 0.0]) #? 1.1KHz Stereo, Trigger
fs = 44100

#* time instance/ticks
t = np.arange(np.ceil(tone_dur * fs)) / fs
#* reshaping it to generate stereo signal
t = t.reshape(-1, 1)

#* list of 1's and 0's
play_1s = np.ones(int(tone_playtime * fs))
play_0s = np.zeros(int(tone_pause * fs))
#* Single tone duration - on time + off time
time_arr = np.concatenate((play_1s, play_0s))
#* reshaping for stereo and multiplying by time ticks
#* target tones (total_tones - total_distract) times
time_arr_t = np.tile(time_arr, total_tones-total_distract).reshape(-1,1)
time_arr_t *= t[:len(time_arr_t)]
#* distractor tones (total_distract) times
time_arr_d = np.tile(time_arr, total_distract).reshape(-1,1)
time_arr_d *= t[:len(time_arr_d)]

#* target and distractor tones with trigger value
target_tone = tone_amp * np.sin(2 * np.pi * freq_t * time_arr_t)
target_tone[:,2] = 25
distractor_tone = tone_amp * np.sin(2 * np.pi * freq_d * time_arr_d)
distractor_tone[:,2] = 35
#* the final tone, containing both target and distractor before shuffling
final_tone = np.concatenate((target_tone, distractor_tone))
#* spliting into individual tones
tone_split = np.split(final_tone, total_tones)
#* random shuffle
shuffle(tone_split)
#* joining, final tone after random shuffle
final_tone = np.concatenate(tone_split)
print(final_tone.shape)

#? New frequency array to create multi-channel signal
freq = np.array([   0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0])  #? channel 1 - target, channel 2 - distractor, channel 13 - trig
tone_18CH = tone_amp * np.sin(2 * np.pi * freq * t[:len(final_tone)])
print(tone_18CH.shape)

#? Assign the tone signal to respective channels
tone_18CH[:, 6] = final_tone[:, 0]  #* tone on 7th channel
tone_18CH[:, 7] = final_tone[:, 1]  #* tone on 8th channel

#? change the trigger amplitude by explicitly replacing the 13th column
tone_18CH[:, 12] = final_tone[:, 2] #* trigger on 13th channel

#* plotting signals for visualizing
fig = plt.figure()
gs = gridspec.GridSpec(nrows = 3, ncols = 2)
ax1 = fig.add_subplot(gs[0,0])
ax1.plot(target_tone[:5000])
ax1.grid()
ax1.set_title("Target Tone")
ax2 = fig.add_subplot(gs[0,1])
ax2.plot(distractor_tone[:5000])
ax2.grid()
ax2.set_title("Distractor Tone")
ax3 = fig.add_subplot(gs[1,:])
ax3.plot(tone_18CH)
ax3.grid()
ax3.set_title("18 Channel Array : Trig Actual")

#? generate trigger signal
#* modifying trig value, why? Don't ask me. 
tone_18CH[:, 12] = [(trig/2 + (trig%2)*127.5)/(255*64) for trig in tone_18CH[:, 12]]
ax4 = fig.add_subplot(gs[2,:])
ax4.plot(tone_18CH)
ax4.grid()
ax4.set_title("18 Channel Array : Trig Signal")

plt.show()

#? Set the device and channels before playing the tone
sd.default.device = 3
sd.default.channels = 18
sd.play(tone_18CH, fs, blocking=True)