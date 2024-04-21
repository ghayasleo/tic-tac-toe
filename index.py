import pygame

# pygame setup
pygame.init()

screen_width, screen_height = 1280, 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

COLORS = {
  "bg": "#121212",
  "hover": "#1d1d1d"
}

running = True

def drawGrid():
    blockSize = 150
    grid = 450
    for x in range(0, grid, blockSize):
        for y in range(0, grid, blockSize):
            rect = pygame.Rect(screen_width / 2 + x - grid / 2, screen_height / 2 + y - grid / 2, blockSize, blockSize, topleft=20)
            box = pygame.draw.rect(screen, COLORS.get("bg"), rect)
            hover = box.collidepoint(pygame.mouse.get_pos())
            if hover:
              box = pygame.draw.rect(screen, COLORS.get("hover"), rect)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(COLORS.get("bg"))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    drawGrid()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
