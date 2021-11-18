from psychopy import prefs
from psychopy.logging import setDefaultClock
prefs.general['audioLib'] = ['sounddevice']
from psychopy import sound
import sounddevice as sd

'''
#? Printing all devices from sounddevice and psychopy
print(sd.query_devices())
dev_list = sound.getDevices()
for idx, dev in enumerate(dev_list) :
    print(idx, dev)
'''
#* Selecting the default device
sd.default.device = 3
print(sd.default.device)
#* Selecting the default input and output channels
sd.default.channels = 1,[1,2]
#* getting the output channels
out_channels = sd.default.channels[1]
print(sd.default.channels)
print(out_channels)

#* Setting the device in psychopy
sound.setDevice(sd.default.device)
SD = sound.Sound()
#* setting the output channels in psychopy
SD.__dict__['channels'] = out_channels
#print(SD)
