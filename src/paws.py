import pygame
import pygame.locals


class Paw(object):

    def __init__(self, path):
        self.path = path
        img = pygame.image.load(path).convert()
        width = img.get_width() // 2
        self.surface = pygame.Surface((width, img.get_height()))
        self.surface.set_colorkey((0, 0, 0))
        mask_surface = self.surface.copy()
        self.surface.blit(img, (0, 0))
        mask_surface.blit(img, (0, 0), (width, 0) + self.surface.get_size())
        self.mask = pygame.mask.from_surface(mask_surface)
        self.pos = (0, 0)
        self.mid = self.mask.centroid()
        self.pressed = True
        self.toggle_press()

    def toggle_press(self):
        self.pressed = not self.pressed
        self.surface.set_alpha(255 if self.pressed else 40)

    def set_mouse_pos(self, mousepos):
        self.pos = [mousepos[0] - self.mid[0], mousepos[1] - self.mid[1]]

    def get_mouse_pos(self):
        return [self.pos[0] + self.mid[0], self.pos[1] + self.mid[1]]


class Paws(object):

    def __init__(self, window_surface, paths):
        self.window_surface = window_surface
        self.window_mask = pygame.mask.Mask(self.window_surface.get_size())
        self.paws = [Paw(i) for i in paths]
        self.selected_paw = self.paws[0]
        self.selected_paw.toggle_press()

    def select_next_paw(self):
        self.selected_paw = self.paws[(self.paws.index(
                    self.selected_paw) + 1) % len(self.paws)]

    def draw(self):
        for i in self.paws:
            self.window_surface.blit(i.surface, i.pos)

    def update_window_mask(self):
        self.window_mask.clear()
        for i in self.paws:
            if i.pressed:
                self.window_mask.draw(i.mask, i.pos)
