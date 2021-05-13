# Shooter and Snake combined
import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0
Y_down = 66

class Block(pygame.sprite.Sprite):
    """ This class represents the block. """

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([5, 11])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 5

class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()

# Call this function so the Pygame library can initialize itself
pygame.init()

# Set the height and width of the screen
screen_width = 500
screen_height = 700
screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Centipede')

all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# Create an initial snake
snake_segments = pygame.sprite.Group()
for i in range(10):

    snake = Segment(WHITE)

    # Add the block to the list of objects
    snake_segments.add(snake)
    all_sprites_list.add(snake)

    if snake == 0:
        snake = Segment(WHITE)

        snake_segments.add(snake)
        all_sprites_list.add(snake)

for i in range(25):
    # This represents a block
    block = Block(BLUE)

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(550)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

    if block == 0:
        block = Block(BLUE)
        block.rect.x = random.randrange(screen_width)
        block.rect.y = random.randrange(550)

        block_list.add(block)
        all_sprites_list.add(block)

# Create a red player block
player = Player()
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

clock = pygame.time.Clock()

score = 0
player.rect.y = 650

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button
            bullet = Bullet()
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y
            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)

    # --- Game logic

    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)

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
        all_sprites_list.add(segment)

        # -- Draw everything
        # Clear screen
        screen.fill(BLACK)

        all_sprites_list.draw(screen)

        # Flip screen
        pygame.display.flip()

        # Pause
        clock.tick(120)

pygame.quit()