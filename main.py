#! python3

import os, sys
import pygame
import random
import fist
import chimp
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', wav)
        raise SystemExit(message)
    return sound

def main():
    pygame.init()
    screen = pygame.display.set_mode((468, 200))
    pygame.display.set_caption('Monkey Fisting')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((51, 51, 51))

    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Pummel the Chimp, and Win $$$", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    bitchchimp = chimp.Chimp()
    bitchfist = fist.Fist()
    whiff = ['whiff1.wav', 'whiff2.wav', 'whiff3.wav']
    whiff_sound = []
    for i in whiff:
        whiff_sound.append(bitchfist.load_sound(i))

    #whiff_sound = bitchfist.load_sound('effect.wav')
    punch_sound = bitchfist.load_sound('hit.wav')

    allsprites = pygame.sprite.RenderPlain((bitchchimp, bitchfist))
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if bitchfist.punch(bitchchimp):
                    punch_sound.play()
                    bitchchimp.punched()
                else:
                    choice = random.choice(whiff_sound)
                    choice.play()
            elif event.type == MOUSEBUTTONUP:
                bitchfist.unpunch()

        allsprites.update()

        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()




if __name__ == '__main__':
    main()
