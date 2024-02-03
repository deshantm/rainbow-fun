import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Game Window
screen_width = 800
screen_height = 600
#set screen width to size of screen
screen_width = pygame.display.Info().current_w
#set screen height to size of screen
screen_height = pygame.display.Info().current_h

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rainbow Fun')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load Assets

# Load Character Images
character_images = {
    'mario': pygame.image.load('mario.jpg'),
    'peach': pygame.image.load('princess-peach.jpg'),
    'luigi': pygame.image.load('luigi.jpg'),
    'daisy': pygame.image.load('daisy.jpeg'),
    'yoshi': pygame.image.load('yoshi.jpeg')
}

# Define desired size for cup images
cup_image_size = (80, 80)  # Adjust the size as needed

cup_images = {
    'mushroom': pygame.transform.scale(pygame.image.load('mushroom-cup.jpg'), cup_image_size),
    'turtle': pygame.transform.scale(pygame.image.load('turtle-cup.jpg'), cup_image_size),
    'flower': pygame.transform.scale(pygame.image.load('flower-cup.jpg'), cup_image_size),
    'gold': pygame.transform.scale(pygame.image.load('gold-cup.jpg'), cup_image_size),
    'lightning': pygame.transform.scale(pygame.image.load('lightning-cup.jpg'), cup_image_size),
    'gold_star': pygame.transform.scale(pygame.image.load('gold-star-cup.jpg'), cup_image_size),
    'star': pygame.transform.scale(pygame.image.load('star-cup.jpg'), cup_image_size),
    'advanced_star': pygame.transform.scale(pygame.image.load('advanced-star-cup.jpg'), cup_image_size),
    'villian': pygame.transform.scale(pygame.image.load('villian-cup.jpg'), cup_image_size),
    'dark_master': pygame.transform.scale(pygame.image.load('dark-master-cup.jpg'), cup_image_size),
    'ultimate': pygame.transform.scale(pygame.image.load('ultimate-cup.jpg'), cup_image_size)
}



kart_image = pygame.image.load('kart.jpg')
kart_image = pygame.transform.scale(kart_image, (50, 30))



try:
    kart_image = pygame.image.load('kart.jpg')
    kart_image = pygame.transform.scale(kart_image, (50, 30))
    print("Kart image loaded successfully")
except pygame.error as e:
    print(f"Error loading kart image: {e}")
    sys.exit()

    # Load Background Image
try:
    background_image = pygame.image.load('rainbow-background.webp').convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    sys.exit()

# Game Classes
class Player:
    def __init__(self, kart_image, char_image, position):
        self.kart_image = kart_image
        self.char_image = char_image
        self.rect = self.kart_image.get_rect()
        self.rect.topleft = position
        self.speed = 5
        self.angle = 0  # New attribute for the kart's angle
        self.moving = False  # New attribute to track movement

    def draw_directional_arrow(self, surface):
        arrow_length = 40
        arrow_color = (255, 0, 0)  # Red color for the arrow

        # Calculate the end point of the arrow based on the angle
        end_x = self.rect.centerx + arrow_length * math.cos(math.radians(self.angle))
        end_y = self.rect.centery + arrow_length * math.sin(math.radians(self.angle))

        # Draw the arrow
        pygame.draw.line(surface, arrow_color, self.rect.center, (end_x, end_y), 5)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 1  # Rotate left
        if keys[pygame.K_RIGHT]:
            self.angle -= 1  # Rotate right
        if keys[pygame.K_SPACE]:
            self.moving = True
        else:
            self.moving = False

    def update(self):
        if self.moving:
            # Move forward in the direction the kart is facing
            self.rect.x += self.speed * math.cos(math.radians(self.angle))
            self.rect.y += self.speed * math.sin(math.radians(self.angle))

    def draw(self, surface):
        # Rotate the kart image based on the current angle
        rotated_kart = pygame.transform.rotate(self.kart_image, self.angle)
        kart_rect = rotated_kart.get_rect(center=self.rect.center)

        surface.blit(rotated_kart, kart_rect)   

        # Calculate the position for the character so it appears above the kart
        char_rect = self.char_image.get_rect(center=self.rect.center)
        char_rect.y -= kart_image.get_height()

        surface.blit(self.char_image, char_rect)
        self.draw_directional_arrow(surface)

    def ai_move(self):
        # Simple AI logic
        # For example, move forward and randomly change direction

        self.speed = 1
        if self.char_image == character_images['daisy']:
            self.speed = 5

        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))

        # Randomly change direction
        if random.randint(0, 100) < 10:  # 10% chance to change direction
            self.angle += random.choice([-10, 10])






# Adjust the character selection positioning
character_selection = {}
spacing = 100
screen_center_x = screen_width // 2
initial_x = screen_center_x - (len(character_images) // 2 * spacing)

for i, (name, img) in enumerate(character_images.items()):
    scaled_img = pygame.transform.scale(img, (50, 50))
    character_selection[name] = scaled_img.get_rect(topleft=(initial_x + spacing*i, screen_height//2))

for name, img in character_images.items():
    character_images[name] = pygame.transform.scale(img, (50, 30)) # Scale for in-game
# Character Selection Function
def select_character():
    running = True
    selected_character = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in character_selection.items():
                    if rect.collidepoint(event.pos):
                        selected_character = name
                        running = False

        screen.fill(WHITE)
        for name, rect in character_selection.items():
            screen.blit(character_images[name], rect)
        pygame.display.update()
    
    return selected_character

# Cup Selection Function
def select_cup():
    running = True
    selected_cup = None
    cup_selection = {}
    spacing = 120
    initial_x = 100  # Adjust as needed

    for i, (name, img) in enumerate(cup_images.items()):
        scaled_img = pygame.transform.scale(img, (80, 80))  # Adjust size as needed
        cup_selection[name] = scaled_img.get_rect(topleft=(initial_x + spacing*i, screen_height//2))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in cup_selection.items():
                    if rect.collidepoint(event.pos):
                        selected_cup = name
                        running = False

        screen.fill(WHITE)
        for name, rect in cup_selection.items():
            screen.blit(cup_images[name], rect)
        pygame.display.update()

    return selected_cup


def load_track(cup_name, race_number):
    """
    Load the track image based on the cup name and race number.
    """
    track_filename = f'{cup_name}-{race_number}.webp'
    try:
        track_image = pygame.image.load(track_filename).convert()
        track_image = pygame.transform.scale(track_image, (screen_width, screen_height))
        return track_image
    except pygame.error as e:
        print(f"Error loading track image {track_filename}: {e}")
        sys.exit()

race_number = 1

# Update Main Function
def main():
    selected_character = select_character()


    # Assuming 'selected_character' is the character chosen by the player
    ai_characters = [char for char in character_images.keys() if char != selected_character]

    ai_players = []
    
    
        




    char_image = character_images[selected_character]
    char_image = pygame.transform.scale(char_image, (50, 30))

    selected_cup = select_cup()

 
    # Load the track for the current race
    current_track = load_track(selected_cup, race_number)

    # Placeholder for starting race logic
    # start_race()
    
    player = Player(kart_image, char_image, (screen_width // 2, screen_height // 2))

    start_x = player.rect.x + 100
    start_y = player.rect.y + 100

    for ai_char in ai_characters:
        ai_image = character_images[ai_char]
        # You might want to set different starting positions for each AI character

        ai_player = Player(kart_image, ai_image, (start_x, start_y))
        ai_players.append(ai_player)
        start_x += 100
        start_y += 100 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_keys()
        player.update()

            # Update AI characters
        for ai_player in ai_players:
            ai_player.ai_move()
            ai_player.update()
            if ai_player.rect.left > screen_width:
                ai_player.rect.right = 0
            if ai_player.rect.right < 0:
                ai_player.rect.left = screen_width
            if ai_player.rect.top > screen_height:
                ai_player.rect.bottom = 0
            if ai_player.rect.bottom < 0:
                ai_player.rect.top = screen_height



            # Wrap around logic
        if player.rect.left > screen_width:
            player.rect.right = 0
        if player.rect.right < 0:
            player.rect.left = screen_width
        if player.rect.top > screen_height:
            player.rect.bottom = 0
        if player.rect.bottom < 0:
            player.rect.top = screen_height




        screen.blit(background_image, (0, 0))

         # Draw the track
        screen.blit(current_track, (0, 0))

         # Placeholder for during race logic
            # update_race()

        

        player.draw(screen)

            # Draw AI characters
        for ai_player in ai_players:
            ai_player.draw(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
