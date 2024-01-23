import pygame

# Basic settings
width = 1024
height = 768
title = "Pacman"
tileSize = 32
gridWidth = width / tileSize
gridheight = height / tileSize

# Player+
playerSpeed = 6 * tileSize

# Food
foodRadius = tileSize // 8

# Directions
right = pygame.math.Vector2(1, 0)
left = pygame.math.Vector2(-1, 0)
down = pygame.math.Vector2(0, 1)
up = pygame.math.Vector2(0, -1)