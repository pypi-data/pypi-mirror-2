# Copyright 2010 Westley Martinez
#
# This file is part of Anikom15's Computer Game (ACG).
# ACG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ACG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ACG.  If not, see <http://www.gnu.org/licenses/>.
"""acg __init__.py

Functions:
set_options -- set constants
init -- initialize pygame
shutodwn -- quit pygame

"""

import os

import pygame
from pygame.locals import *

import acg.tools
import acg.copyright
import acg.sprite

DIRNAME = os.path.dirname(__file__)
DATA = {'version': '1.0.0a7',
        'images': os.path.join(DIRNAME, 'data', 'images'),
        'sounds': os.path.join(DIRNAME, 'data', 'sounds'),
        'fonts': os.path.join(DIRNAME, 'data', 'fonts')}
SETTINGS = {}

def set_options(options):
    """Set constant variables.

    Keyword arguments:
    options -- dictionary of settings

    """
    for key in options:
        SETTINGS[key] = options[key]
    SETTINGS['resolution'] = (800, 480)
    SETTINGS['srcalpha'] = SRCALPHA
    SETTINGS['doublebuf'] = DOUBLEBUF if options['doublebuf'] else 0
    SETTINGS['hwsurface'] = HWSURFACE if options['hwsurface'] or \
                            options['doublebuf'] else 0
    SETTINGS['fullscreen'] = FULLSCREEN if options['fullscreen'] or \
                             options['hwsurface'] or \
                             options['doublebuf'] else 0


def init():
    """Initialize all the stuff needed for the game, display, mixer, &c."""
    pygame.mixer.pre_init(SETTINGS['afrequency'], SETTINGS['asize'],
                          SETTINGS['achannels'], SETTINGS['abuffersize'])
    pygame.init()
    pygame.display.set_caption("Anikom15's Computer Game")
    pygame.mouse.set_visible(False)
    pygame.display.set_mode(SETTINGS['resolution'],
                            SETTINGS['srcalpha'] | SETTINGS['fullscreen'] |
                            SETTINGS['hwsurface'] | SETTINGS['doublebuf'])
    icon = tools.load_image(os.path.join(DATA['images'], 'icon.png'))
    pygame.display.set_icon(icon)
    DATA['clock'] = pygame.time.Clock()
    if SETTINGS['fullscreen']:
        pygame.time.wait(3000)


def preface():
    """Display copyright information."""
    text = copyright.Copyright(pygame.font.Font(os.path.join(DATA['fonts'],
                               'Junicode-Bold.ttf'), 21))
    screen = pygame.display.get_surface()
    counter = -3000 if SETTINGS['fullscreen'] else 0
    while True:
        time = DATA['clock'].tick(SETTINGS['frame_rate'])
        counter += time
        if counter > 10000:
            return
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                return
        text.update(screen)
        pygame.display.flip()


def title():
    """Display the title and allow the user to choose a mode.

    Returns a string that represents the chosen mode.

    """
    image = tools.load_image(os.path.join(DATA['images'], 'all.png'))
    titlefont = pygame.font.Font(os.path.join(DATA['fonts'],
                                 'Junicode-Regular.ttf'), 60)
    title = titlefont.render('Anikom15\u2019s Computer Game', True,
                             (255, 255, 255))
    titlerect = title.get_rect(centerx=400, y=0)
    itemfont = pygame.font.Font(os.path.join(DATA['fonts'],
                                'Junicode-Regular.ttf'), 36)
    linesize = itemfont.get_linesize()
    items = [itemfont.render('1. Start', True, (255, 255, 255)),
             itemfont.render('2. Save Score', True, (255, 255, 255)),
             itemfont.render('3. Quit', True, (255, 255, 255))]
    itemrects = [items[0].get_rect(x=200, centery=360),
                 items[1].get_rect(x=200, centery=360 + linesize),
                 items[2].get_rect(x=200, centery=360 + linesize * 2)]
    screen = pygame.display.get_surface()
    while True:
        time = DATA['clock'].tick(SETTINGS['frame_rate'])
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and \
               event.key == K_ESCAPE:
                return 'quit'
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    return 'start'
                elif event.key == K_2:
                    return 'save'
                elif event.key == K_3:
                    return 'quit'
        screen.blit(image, image.get_rect(center=(400, 240)))
        screen.blit(title, titlerect)
        for item in items:
            screen.blit(item, itemrects[items.index(item)])
        pygame.display.flip()


def run(mode):
    """Run the mode selected at the title screen."""
    eval(mode)()


def start():
    """Start playing the actual game!"""
    taxman = sprite.TaxMan(DATA)
    playersprites = pygame.sprite.RenderUpdates(taxman)
    bulletsprites = pygame.sprite.RenderUpdates(())
    screen = pygame.display.get_surface()
    while True:
        time = DATA['clock'].tick(SETTINGS['frame_rate'])
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and \
               event.key == K_ESCAPE:
                return
        if taxman.alive():
            bullets = taxman.update(time)
        if bullets is not None:
            bulletsprites.add(bullets)
        bulletsprites.update(time)
        bulletsprites.draw(screen)
        playersprites.draw(screen)
        pygame.display.flip()


def save():
    pass


def shutdown():
    """Shutdown all the pygame stuff."""
    pygame.quit()
