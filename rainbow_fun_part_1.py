
import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Game Window
screen_width = 800
screen_height = 600
# Set screen width to size of screen
screen_width = pygame.display.Info().current_w
# Set screen height to size of screen
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