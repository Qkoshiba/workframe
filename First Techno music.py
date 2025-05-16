import pygame
import time

pygame.init()
pygame.mixer.init()

kick = pygame.mixer.Sound("4.wav")
sound2 = pygame.mixer.Sound('6.wav')
sound3 = pygame.mixer.Sound('7.wav')
snare = pygame.mixer.Sound("5.wav")

for _ in range(8):
    kick.play()
    time.sleep(2.5)
    snare.play()
    time.sleep(3.5)
    sound3.play()
    time.sleep(4)
    sound2.play(2)