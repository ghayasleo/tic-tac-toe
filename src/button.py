import pygame

from src.font import Font

class Button:
    def __init__(self, screen, x, y, height, width, colour, border, curve, text, textColour):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.border = border
        self.curve = curve
        self.text = text
        self.textColour = textColour

    def drawRect(self):
        button = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.colour, button, self.border, self.curve)
        if self.text != "":
            self.drawText()

        if button.collidepoint(pygame.mouse.get_pos()):
            return True

        return False

    def drawText(self):
        font = Font.xsmall
        text_surf = font.render(self.text, True, self.textColour)
        text_rect = text_surf.get_rect(center=(self.x+self.width//2, self.y+self.height//2))
        self.screen.blit(text_surf, text_rect)