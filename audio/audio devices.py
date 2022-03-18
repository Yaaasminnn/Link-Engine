import time

import pygame
import pygame._sdl2 as sdl2

pygame.init()
is_capture = 0  # zero to request playback devices, non-zero to request recording devices
num = sdl2.get_num_audio_devices(is_capture)
names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]

"""for name in names:
    try:
        pygame.mixer.pre_init(devicename=name)
        pygame.mixer.init()
        pygame.mixer.music.load("./voices/sans.wav")
        pygame.mixer.music.play()
        time.sleep(10)
        print(name); print("success")
    except:
        print("Error")
        continue"""
#print("\n".join(names))
#pygame.quit()

