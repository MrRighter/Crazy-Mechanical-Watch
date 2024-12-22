import pygame
import base64
from io import BytesIO


class PicButton:
    def __init__(self, x, y, width, height, image_encoded):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = self.decode_image(image_encoded)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def decode_image(self, encoded_image):
        decoded_image = base64.b64decode(encoded_image)
        image_stream = BytesIO(decoded_image)
        return pygame.image.load(image_stream)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
