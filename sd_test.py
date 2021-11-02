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
tone_dur = 1.0 #? 2.5 seconds
tone_playtime = 0.015 #? 20 milliseconds
tone_pause = 0.01 #? 5 milliseconds
total_tones = int(tone_dur/(tone_playtime + tone_pause)) #? (2.5/0.025) = 100
total_distract = 3 #? number of distract tones
freq_t = np.array([1000.0, 1000.0, 0.0]) #? 1KHz Stereo, Trigger
freq_d = np.array([1100.0, 1100.0, 0.0]) #? 1.1KHz Stereo, Trigger
fs = 44100 #? Sample Rate

'''
    #* time instance/ticks
    Get the number of samples using the samplerate and total duration
    This generates a (n,) type array [0,1,.....]
'''
t = np.arange(np.ceil(tone_dur * fs)) / fs
'''
    #* reshaping it to generate stereo signal
    reshaping the array to (n,1) [[0,1,]] (vertical)
'''
t = t.reshape(-1, 1)

'''
    #* list of 1's and 0's
    using variable tone playtime and pause to get an array of 1's and 0's
    to help us make the final tone
'''
play_1s = np.ones(int(tone_playtime * fs))
play_0s = np.zeros(int(tone_pause * fs))
'''
    #* Single tone duration - on time + off time
    This array has duration of a single tone, play + stop time
'''
time_arr = np.concatenate((play_1s, play_0s))
'''
    #* reshaping for stereo and multiplying by time ticks
    #* target tones (total_tones - total_distract) times
    #* distractor tones (total_distract) times
    #! Read slowly
    trig_t - on and off time array for target (1's and 0's)
    time_arr_t - (n,1) type array of generated
    by repeating time_arr for total target tone duration time
    then reshaping it to get 1's and 0's (n,1) type array
    lastly multiplying it by time ticks 
    to get target tone time array
'''
trig_t = np.tile(time_arr, total_tones-total_distract)
time_arr_t = np.tile(time_arr, total_tones-total_distract).reshape(-1,1)
time_arr_t *= t[:len(time_arr_t)]
'''
    #* distractor tones (total_distract) times
    same as above
'''
trig_d = np.tile(time_arr, total_distract)
time_arr_d = np.tile(time_arr, total_distract).reshape(-1,1)
time_arr_d *= t[:len(time_arr_d)]

'''
    #* target and distractor tones with trigger value
    first we generate target tone using time_arr_t
    then we set the trigger, with help of trig_t (
        this sets trigger only when the tone is being played
    )
    we do the same for distract tone
'''
target_tone = tone_amp * np.sin(2 * np.pi * freq_t * time_arr_t)
target_tone[:,2] = 25*trig_t
distractor_tone = tone_amp * np.sin(2 * np.pi * freq_d * time_arr_d)
distractor_tone[:,2] = 35*trig_d

'''
    #* the final tone, containing both target and distractor before shuffling
    here we combine both target and distractor tone
    then we split it into separate tone arrays
    a little bit of shuffle (mix?)
    and then combining individual tones to get the final_tone
'''
final_tone = np.concatenate((target_tone, distractor_tone))
tone_split = np.split(final_tone, total_tones)
shuffle(tone_split)
final_tone = np.concatenate(tone_split)
print(final_tone.shape)

'''
    #? New frequency array to create multi-channel signal
    creating a multi-channel tone
'''
freq = np.array([   0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0,   0.0,   0.0,
                    0.0,    0.0])  #? channel 1 - target, channel 2 - distractor, channel 12 - trig
tone_18CH = tone_amp * np.sin(2 * np.pi * freq * t[:len(final_tone)])
print(tone_18CH.shape)

'''
    #? Assign the tone signal to respective channels
    final_tone is a stereo signal, with 0 and 1 being the tone data
    and 2 the trigger data
    channels for playback - 7 and 8 (python's array 6 and 7)
    channel for trigger - 12
'''
tone_18CH[:, 6] = final_tone[:, 0]  #* tone on 7th channel
tone_18CH[:, 7] = final_tone[:, 1]  #* tone on 8th channel
tone_18CH[:, 11] = final_tone[:, 2] #* trigger on 12th channel

'''
    #* plotting signals for visualizing
    can comment out this part, this is just to visualize the tones and trigger 
'''
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

'''
    #* modifying trig value, why? Don't ask me.
    I don't know head or tail about this step,
    copied it from Jasmine's MATLAB scripts 
'''
tone_18CH[:, 11] = [(trig/2 + (trig%2)*127.5)/(255*64) for trig in tone_18CH[:, 11]]
ax4 = fig.add_subplot(gs[2,:])
ax4.plot(tone_18CH)
ax4.grid()
ax4.set_title("18 Channel Array : Trig Signal")
plt.show()

'''
    #? Set the device and channels before playing the tone
    Finally, what we wanted to do. Play the tone on ASIO device,
    find the device number, channels
'''
sd.default.device = 3
sd.default.channels = 18
sd.play(tone_18CH, fs, blocking=True)