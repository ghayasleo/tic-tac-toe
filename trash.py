import pygame

# pygame setup
pygame.init()

screen_width, screen_height, box_size, grid_size, = 1280, 720, 150, 450
boxes = []
running = True
hover = False
clicked_box = -1

COLORS = {
    "white": "#ffffff",
    "black": "#000000",
    "bg": "#121212",
    "hover": "#1d1d1d"
}

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()


class Box:
    def __init__(self, grid_size, size, color, x, y):
        self.grid_size = grid_size
        self.size = size
        self.color = color
        self.x = x
        self.y = y

    def create_box(self):
        global screen_width, screen_height
        left = screen_width / 2 + self.x - self.grid_size / 2
        top = screen_height / 2 + self.y - self.grid_size / 2
        self.rect = pygame.Rect(left, top, self.size, self.size, topleft=20)
        self.box = pygame.draw.rect(screen, "#ffffff", self.rect, 1)
        print(self.x, self.y, left, top)
        self.hover()

    def hover(self):
        global screen, hover
        hover = self.box.collidepoint(pygame.mouse.get_pos())
        if hover:
            self.box = pygame.draw.rect(screen, COLORS.get("hover"), self.rect)

    def click(self):
        # print(f"Clicked #{self.x} #{self.y}")
        pass


for x in range(3):
    for y in range(3):
        box = Box(grid_size, box_size, COLORS.get("white"), x, y)
        boxes.append(box)

print(len(boxes))


def render_grid():
    for x in range(0, grid_size, box_size):
        for y in range(0, grid_size, box_size):
            box = Box(grid_size, box_size, COLORS.get("white"), x, y)
            box.create_box()


while running:
    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('Mouse button pressed ', hover)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(COLORS.get("bg"))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    render_grid()

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # flip() the display to put your work on screen
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
