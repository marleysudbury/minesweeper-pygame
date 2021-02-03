import pygame
import time


class TextBox:
    def __init__(self, x, y, w, h, limit=3):
        """Initialise tiles."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = ""
        self.limit = limit

    def get_val(self):
        return self.value

    def key_response(self, event):
        if event.key == pygame.K_BACKSPACE:
            if len(self.value) > 0:
                self.value = self.value[:-1]
        else:
            if not self.too_big():
                self.value += event.unicode
                self.value = self.value.upper()

    def too_big(self):
        if len(self.value) < self.limit:
            return False
        else:
            return True

    def draw(self, parent):
        font = pygame.font.SysFont('calibritff', 48)
        img = font.render(self.value, True, (255, 255, 255))
        rect = img.get_rect()
        back_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        rect.topleft = (self.x+10, self.y+10)
        cursor = pygame.Rect(
            (rect.bottomright[0], rect.bottomright[1]-5), (20, 5))

        pygame.draw.rect(parent.game_display, (0, 0, 0), back_rect)
        if time.time() % 1 > 0.5 and not self.too_big():
            pygame.draw.rect(parent.game_display, (255, 255, 255), cursor)
        parent.game_display.blit(img, rect)
