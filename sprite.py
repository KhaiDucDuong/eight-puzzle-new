import pygame
from settings import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, tile_size, game_size, img_surface = None):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.tile_size = tile_size
        self.game_size = game_size
        self.game = game
        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("Consolas", 50)
            if(img_surface == None):
                font_surface = self.font.render(self.text, True, BLACK)
                self.image.fill(WHITE)
                self.font_size = self.font.size(self.text)
                draw_x = (self.tile_size / 2) - self.font_size[0] / 2
                draw_y = (self.tile_size / 2) - self.font_size[1] / 2
                self.image.blit(font_surface, (draw_x, draw_y))
            else:
                self.image.blit(img_surface, (0, 0))
        else:
            self.image.fill(BGCOLOUR)

    def update(self):
        self.rect.x = self.x * self.tile_size
        self.rect.y = self.y * self.tile_size

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + self.tile_size < self.game_size * self.tile_size

    def left(self):
        return self.rect.x - self.tile_size >= 0

    def up(self):
        return self.rect.y - self.tile_size >= 0

    def down(self):
        return self.rect.y + self.tile_size < self.game_size * self.tile_size


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, colour, text_colour):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
    
class Sprite:
    def __init__(self, x, y, image_path, width, height):
        #load the image with pygame
        loaded_image = pygame.image.load(image_path).convert_alpha()
        #scale the image to the desired width and height
        self.image = pygame.transform.scale(loaded_image, (width, height))
        #x and y coordinates
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def getSurface(self):
        return self.image
