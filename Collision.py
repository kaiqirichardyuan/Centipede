import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3

# Set initial speed


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
        self.rect.y -= 10


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
        self.x_change = 18
        self.y_change = 0
        self.y_down = 48

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        if self.rect.x > 472:
            self.y_change = 18
            self.x_change = 0
        if self.rect.x < 10:
            self.y_change = 18
            self.x_change = 0
        if self.rect.y > self.y_down:
            self.y_change = 0
            self.y_down += 36
            if self.rect.x > 472:
                self.x_change = -18
            if self.rect.x < 10:
                self.x_change = 18


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 30))
        self.image.fill(RED)
        self.rect = self.image. get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(- 80, -30)
        self.speedy = random.randrange(4, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height:
            self.rect.x = random.randrange(0, screen_width - self.rect.width)
            self.rect.y = random.randrange(- 80, -30)
            self.speedy = random.randrange(4, 8)


fontname = pygame.font.match_font("times")


def write_text(surf, text, size, x, y):
    font = pygame.font.Font(fontname, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def gameover_menu():
    write_text(screen, "Welcome to Centipede", 50, screen_width / 2, screen_height - 600)
    write_text(screen, "Click mouse to begin", 18, screen_width / 2, screen_height - 100)
    pygame.display.flip()
    wait_for_click = True
    while wait_for_click:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                wait_for_click = False


# Call this function so the Pygame library can initialize itself
pygame.init()

# Set the height and width of the screen
screen_width = 500
screen_height = 700
screen = pygame.display.set_mode([screen_width, screen_height])

pygame.display.set_caption('Centipede')
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

obstacle = pygame.sprite.Group()
for i in range(5):
    falling_obstacle = Obstacle()
    obstacle.add(falling_obstacle)
    all_sprites_list.add(falling_obstacle)
# List of each bullet
bullet_list = pygame.sprite.Group()

for i in range(25):
    # This represents a block
    block = Block(BLUE)

    # Set a random location for the block
    block.rect.x = random.randrange(400)
    block.rect.y = random.randrange(550)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

    if block == 0:
        block = Block(BLUE)
        block.rect.x = random.randrange(400)
        block.rect.y = random.randrange(550)

        block_list.add(block)
        all_sprites_list.add(block)

snake_segments = pygame.sprite.Group()
for i in range(15):
    x = 260 - (segment_width + segment_margin) * i
    y = 30
    segment = Segment(x, y)
    snake_segments.add(segment)
    all_sprites_list.add(segment)

# Create a red player block
player = Player()
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False
gameover = True
clock = pygame.time.Clock()

score = 0
highscore = 0
player.rect.y = 650

while not done:
    if gameover:
        gameover_menu()
        gameover = False
        all_sprites_list = pygame.sprite.Group()
        obstacle = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        snake_segments = pygame.sprite.Group()
        block_list = pygame.sprite.Group()
        player = Player()
        all_sprites_list.add(player)
        player.rect.y = 650
        for i in range(15):
            x = 260 - (segment_width + segment_margin) * i
            y = 30
            segment = Segment(x, y)
            snake_segments.add(segment)
            all_sprites_list.add(segment)
        for i in range(5):
            falling_obstacle = Obstacle()
            obstacle.add(falling_obstacle)
            all_sprites_list.add(falling_obstacle)
        score = 0

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

    if len(block_list) == 0:

        for i in range(25):
            block = Block(BLUE)

            block.rect.x = random.randrange(400)
            block.rect.y = random.randrange(550)

            block_list.add(block)
            all_sprites_list.add(block)
    # --- Game logic
    # --- Game logic
    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:
        Snake_hit_list = pygame.sprite.spritecollide(bullet, snake_segments, True)

        # For each block hit, remove the bullet and add to the score
        for snake in Snake_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

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
    hit = pygame.sprite.spritecollide(player, snake_segments, True)
    hits = pygame.sprite.spritecollide(player, obstacle, False)
    if hits:
        gameover = True
    elif hit:
        gameover = True


    old_segment = snake_segments.remove()
    all_sprites_list.remove(old_segment)


    segment = Segment(x, y)


    # Insert new segment into the list
    snake_segments.add(segment)
    all_sprites_list.add(segment)

    if score > highscore:
        highscore = score

        # -- Draw everything
        # Clear screen
    screen.fill(BLACK)

    all_sprites_list.draw(screen)
    write_text(screen, "score:" + str(score), 20, screen_width - 450, 10)
    write_text(screen, "highscore:" + str(highscore), 20, screen_width - 50, 10)
    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(50)

pygame.quit()