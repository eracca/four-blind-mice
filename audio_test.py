import time
import pygame

pygame.init()
pygame.mixer.init()
sounda = pygame.mixer.Sound('ahem_x.wav')
sounda.play()

#once you start playing a sound with pygame, you are free to execute commands
#while the audio file plays through

for i in range(5):
    print(i)
    time.sleep(0.5)

