import pygame
import sys

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

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, surface):
        # Test drawing a rectangle
        pygame.draw.rect(surface, (0, 255, 0), self.rect)  # Draws a green rectangle

        # Draw the kart
        surface.blit(self.kart_image, self.rect)
       

        # Calculate the position for the character so it appears above the kart
        char_rect = self.char_image.get_rect(center=self.rect.center)
        char_rect.y -= kart_image.get_height()

        surface.blit(self.char_image, char_rect)






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

# Update Main Function
def main():
    selected_character = select_character()
    char_image = character_images[selected_character]
    char_image = pygame.transform.scale(char_image, (50, 30))

    selected_cup = select_cup()
    
    player = Player(kart_image, char_image, (screen_width // 2, screen_height // 2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_keys()

        screen.blit(background_image, (0, 0))

        player.draw(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
