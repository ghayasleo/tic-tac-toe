import pygame

from src.font import Font
from src.color import Color


class Input:
    def __init__(self, x, y, w, h, text='', placeholder=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = Color.white
        self.text = text
        self.placeholder = placeholder
        self.txt_surface = Font.base.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = Color.theme if self.active else Color.white
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # print(self.text)
                    # self.text = ''
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = Font.base.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+30)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        self.placeholder_surface = Font.base.render(self.placeholder, True, self.color)
        screen.blit(self.placeholder_surface, (self.rect.x, self.rect.y-self.rect.height))
        screen.blit(self.txt_surface, (self.rect.x+15, self.rect.y+10))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
