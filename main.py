import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

class Checkpoint:
    def __init__(self, position, radius, checkpoint_number, visible=True):
        self.position = position
        self.radius = radius
        self.checkpoint_number = checkpoint_number
        self.visible = visible

    def draw(self, surface, font):
        if self.visible:
            pygame.draw.circle(surface, (0, 255, 0), self.position, self.radius, 2)
        text = font.render(str(self.checkpoint_number), True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.position[0], self.position[1] - self.radius - 10))
        surface.blit(text, text_rect)





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

ruby_image = pygame.image.load('ruby.jpg')


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
    def __init__(self, kart_image, char_image, char_name, position):
        self.kart_image = kart_image
        self.char_image = char_image
        self.rect = self.kart_image.get_rect()
        self.rect.topleft = position
        self.speed = 5
        self.angle = 0  # New attribute for the kart's angle
        self.moving = False  # New attribute to track movement
        self.next_checkpoint_index = 0
        self.laps_completed = 0
        self.current_rank = 0
        self.checkpoints = [] 
        self.checkpoint_crossed = False
        self.character_name = char_name.capitalize()
        self.rubies_collected = 0  # New attribute to track collected rubies


    def check_ruby_collision(self, rubies):
        for ruby in rubies:
            if self.rect.colliderect(ruby.rect) and not ruby.picked_up:
                ruby.picked_up = True
                self.rubies_collected += 1  # Increment the ruby count
                self.speed += 2  # Increase speed temporarily
                # Set a timer to reset the speed after a certain duration
                pygame.time.set_timer(pygame.USEREVENT, 5000)  # 5 seconds

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

    def update(self, checkpoints):
        # If the player is moving, update position
        if self.moving:
            # Move forward based on angle
            self.rect.x += self.speed * math.cos(math.radians(self.angle))
            self.rect.y += self.speed * math.sin(math.radians(self.angle))
            
            # Make sure the player's position is within screen bounds
            if self.rect.left > screen_width:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = screen_width
            if self.rect.top > screen_height:
                self.rect.bottom = 0
            if self.rect.bottom < 0:
                self.rect.top = screen_height

        # Check if the player has crossed a checkpoint
        self.check_checkpoint_crossing(checkpoints)



    def check_checkpoint_crossing(self, checkpoints):
        # Ensure we have checkpoints to check against
        if not checkpoints:
            return
        
        # Get the next checkpoint to check against
        next_checkpoint = checkpoints[self.next_checkpoint_index]
        
        # Calculate the distance from the player to the next checkpoint
        dx = self.rect.centerx - next_checkpoint.position[0]
        dy = self.rect.centery - next_checkpoint.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        # Check if the player has crossed the checkpoint
        if distance <= next_checkpoint.radius:
            print(f"Checkpoint {self.next_checkpoint_index} crossed by {self.character_name}")
            # Increment the checkpoint index, wrap around if at the end
            self.next_checkpoint_index = (self.next_checkpoint_index + 1) % len(checkpoints)
            # If we've wrapped around, it means we've completed a lap
            if self.next_checkpoint_index == 0:
                self.laps_completed += 1
                print(f"Lap completed by {self.character_name}")


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


class Ruby:
    def __init__(self, image, position):
        self.image = pygame.transform.scale(image, (30, 30))  # Scale the image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.picked_up = False

    def draw(self, surface):
        if not self.picked_up:
            surface.blit(self.image, self.rect)




def draw_text(surface, text, position, font, color=(255, 255, 255)):  # Default color is white
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)



def update_rankings(players):
        players.sort(key=lambda p: (-p.laps_completed, -p.next_checkpoint_index))
        for i, player in enumerate(players):
            player.current_rank = i + 1


def load_checkpoints(track_name, race_number):
    checkpoints = []
    try:
        filename = f'{track_name}-{race_number}_checkpoints.txt'
        print(f"Loading checkpoints from {filename}")
        with open(f'{track_name}-{race_number}-checkpoints.txt', 'r') as file:
            for line in file:
                _, x, y = line.strip().split(', ')
                checkpoints.append(Checkpoint((int(x), int(y)), 20, len(checkpoints) + 1))
    except FileNotFoundError:
        print(f"No checkpoint file found for {track_name}.")
        
    return checkpoints

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


def get_character_name_from_image_path(image_path):
    # Extract the base name of the file (e.g., 'mario.jpg')
    base_name = os.path.basename(image_path)
    # Split the base name by the dot and return the first part (e.g., 'mario')
    return os.path.splitext(base_name)[0].capitalize()


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
    checkpoints = load_checkpoints(selected_cup, race_number)



    player = Player(kart_image, char_image, selected_character, (screen_width // 2, screen_height // 2))
    player.checkpoints = checkpoints  # Assign the loaded checkpoints to the player


    start_x = player.rect.x + 100
    start_y = player.rect.y + 100

    # Do the same for AI players
    for ai_char in ai_characters:
        ai_image = character_images[ai_char]
        ai_player = Player(kart_image, ai_image, ai_char, (start_x, start_y))
        ai_player.checkpoints = checkpoints  # Assign the loaded checkpoints to the AI player
        ai_players.append(ai_player)


    margin = 50  # Margin to avoid placing rubies too close to the edges

    def random_ruby_position():
        x = random.randint(margin, screen_width - margin)
        y = random.randint(margin, screen_height - margin)
        return (x, y)

    # Generate an array of 6 rubies with random positions
    rubies = [Ruby(ruby_image, random_ruby_position()) for _ in range(6)]


    font = pygame.font.SysFont(None, 36)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_keys()
     

            # Update AI characters
        for ai_player in ai_players:
            ai_player.ai_move()

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


        player.update(checkpoints)
        for ai_player in ai_players:
            ai_player.update(checkpoints)


        screen.blit(background_image, (0, 0))

         # Draw the track
        screen.blit(current_track, (0, 0))

         # Placeholder for during race logic
            # update_race()

        
        player.check_ruby_collision(rubies)

        # Draw rubies
        for ruby in rubies:
            ruby.draw(screen)


        player.draw(screen)

            # Draw AI characters
        for ai_player in ai_players:
            ai_player.draw(screen)


        for checkpoint in checkpoints:
            checkpoint.draw(screen, font)

        update_rankings([player] + ai_players)

    
        # Inside the main game loop, where you draw the leaderboard:
        for i, p in enumerate([player] + ai_players):
            lap_text = f"{p.character_name}: Lap {p.laps_completed}"
            rank_text = f"Rank: {p.current_rank}"
            ruby_text = f"Rubies: {p.rubies_collected}"  # Display the number of rubies collected

            GREY = (128, 128, 128)

            draw_text(screen, lap_text, (10, 30 * i), font, GREY)
            draw_text(screen, rank_text, (200, 30 * i), font, GREY)
            draw_text(screen, ruby_text, (400, 30 * i), font, GREY)  # Display rubies collected




           


        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
