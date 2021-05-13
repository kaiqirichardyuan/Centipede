import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0
Y_down = 66


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Call this function so the Pygame library can initialize itself
pygame.init()

screen = pygame.display.set_mode([500, 700])

pygame.display.set_caption('Centipede')

allspriteslist = pygame.sprite.Group()

# Create an initial snake
snake_segments = []
for i in range(15):
    x = 250 - (segment_width + segment_margin) * i
    y = 30
    segment = Segment(x, y)
    snake_segments.append(segment)
    allspriteslist.add(segment)

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        old_segment = snake_segments.pop()
        allspriteslist.remove(old_segment)

        # Figure out where new segment will be
        x = snake_segments[0].rect.x + x_change
        y = snake_segments[0].rect.y + y_change
        segment = Segment(x, y)

        if x > 450 or x < 50:
            y_change = 18
            x_change = 0
        if y == Y_down:
            y_change = 0
            if x > 450:
                x_change = -18
            elif x < 50:
                x_change = 18
            Y_down = Y_down + 36

        # Insert new segment into the list
        snake_segments.insert(0, segment)
        allspriteslist.add(segment)

        # -- Draw everything
        # Clear screen
        screen.fill(BLACK)

        allspriteslist.draw(screen)

        # Flip screen
        pygame.display.flip()

        # Pause
        clock.tick(5)

pygame.quit()