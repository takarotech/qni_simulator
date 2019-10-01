#!/usr/bin/python3

import argparse
import os.path
import logging
import pygame
import pygame.locals
import pyscreenshot

from qni_core import logger, config
import paws
import simulator_electrodes


class QniSimulator(object):
    _logger = logging.getLogger('qni_simulator')

    LED_SEP_PIXELS = 2
    LED_SIZE_PIXELS = 4
    FPS = 30

    RES_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(
        os.path.realpath(__file__))), 'res', 'paws'))

    def __init__(self):
        logger.config_logger()
        pygame.init()

        self.LED_MAP = [self.LED_SEP_PIXELS + i * (self.LED_SIZE_PIXELS + self.LED_SEP_PIXELS) for i in
            range(max(config.TILE_SIZE))]

        self.WINDOW_SIZE = [self.LED_MAP[i - 1] + self.LED_SIZE_PIXELS + self.LED_SEP_PIXELS for i in
            config.TILE_SIZE]
        self.WINDOW_TITLE = 'QNI Simulator %sx%s' % tuple(config.TILE_SIZE)

        self.PAWS_PATH = [os.path.join(self.RES_PATH, i) for i in (
            'leg_left.png', 'leg_right.png', 'hand_left.png', 'hand_right.png')]

        self.SCREEN_RECT = tuple(config.SCREEN_POSITION)
        self.SCREEN_RECT += tuple([i + j for i, j in zip(config.SCREEN_POSITION, config.TILE_SIZE)])

        self.window_surface = pygame.display.set_mode(self.WINDOW_SIZE)
        self.leds_surface = pygame.Surface(self.window_surface.get_size())
        self.screen_surface = pygame.Surface(config.TILE_SIZE)
        pygame.display.set_caption(self.WINDOW_TITLE)

        self.paws = paws.Paws(self.window_surface, self.PAWS_PATH)

        self.electrodes = simulator_electrodes.SimulatorElectrodes(
            config.ELECTRODES_SIZE, config.TILE_SIZE, self.paws,
            self.LED_MAP, self.LED_SEP_PIXELS // 2)

        self.running = True
        self.fps_clock = pygame.time.Clock()
        self._logger.info('Started %s, %s paws', self.WINDOW_TITLE, len(self.paws.paws))

    def _draw_display(self):
        self.window_surface.blit(self.leds_surface, (0, 0))
        self.paws.draw()
        pygame.display.update()

    def draw_surface(self, surface):
        for y in range(config.TILE_SIZE[1]):
            for x in range(config.TILE_SIZE[0]):
                pygame.draw.rect(
                    self.leds_surface, surface.get_at((x, y)),
                    pygame.locals.Rect(
                        self.LED_MAP[x], self.LED_MAP[y],
                        self.LED_SIZE_PIXELS, self.LED_SIZE_PIXELS))
        self._draw_display()

    def draw_screen_surface(self):
        i = pyscreenshot._grab_simple(False, bbox=self.SCREEN_RECT)
        m = pygame.image.frombuffer(i.tobytes(), i.size, 'RGB')
        self.screen_surface.blit(m, (0, 0)) 
        self.draw_surface(self.screen_surface)

    def handle_events(self, events):
        needs_redraw = False
        for i in events:
            if i.type == pygame.MOUSEMOTION:
                self.paws.selected_paw.set_mouse_pos(i.pos)
                needs_redraw = True
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    self.paws.selected_paw.toggle_press()
                elif i.button == 3:
                    self.paws.select_next_paw()
                    pygame.mouse.set_pos(
                        self.paws.selected_paw.get_mouse_pos())
                needs_redraw = True
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    self.running = False
            elif i.type == pygame.QUIT:
                self.running = False
        if needs_redraw:
            self._draw_display()
            self.electrodes.update()

    def __loop__(self):
        while self.running:
            # limit framerate
            self.fps_clock.tick(self.FPS)
            # handle pygame events
            self.handle_events(pygame.event.get())
            # update surface
            self.draw_screen_surface()


def main():
    app = QniSimulator()
    app.__loop__()


if __name__ == '__main__':
    main()
