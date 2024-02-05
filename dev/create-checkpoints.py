import pygame
import sys

# Initialize Pygame
pygame.init()

# Get path from command line
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    print("Usage: create-checkpoints.py path_to_image")
    sys.exit()

# Load the track image
track_image = pygame.image.load(path)
screen_width, screen_height = track_image.get_size()

# Create a screen with the size of the track image
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Checkpoint Selector')

# Define your checkpoint selection and drawing code here...


# Function to handle checkpoint selection
def select_checkpoints():
    checkpoints = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the left mouse button is clicked, save the position
                if event.button == 1:
                    checkpoints.append(event.pos)
                    print(f"Checkpoint added at: {event.pos}")
        
        # Draw the track image
        screen.blit(track_image, (0, 0))
        
        # Draw existing checkpoints
        for checkpoint in checkpoints:
            pygame.draw.circle(screen, (255, 0, 0), checkpoint, 5)
        
        pygame.display.flip()

    return checkpoints

# Call the function and print the selected checkpoints
selected_checkpoints = select_checkpoints()
print(f"Selected checkpoints: {selected_checkpoints}")

pygame.quit()

