import os
import sys
import pygame
from pygame import *
import requests

from Samples.business import find_businesses
from Samples.distance import lonlat_distance
from Samples.geocoder import get_coordinates
from Samples.mapapi_PG import show_map

size = w, h = 600, 450

class Map_params():
    def __init__(self):
        self.lat = 37.90374
        self.lon = 59.11963
        self.z = 15
        self.type = 'map'

    def ll(self):
        return f'{self.lat},{self.lon}'

    def key_pressed(self, event):
        if event.key == pygame.K_PAGEUP:
            self.z = min(19, self.z + 1)
        elif event.key == pygame.K_PAGEDOWN:
            self.z = max(1, self.z - 1)


def load_map(mp):
    map_request = f'http://static-maps.yandex.ru/1.x/?ll={mp.ll()}&z={mp.z}&l={mp.type}'
    response = requests.get(map_request)

    # print(response.url)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


pygame.init()

pygame.event.set_blocked(None)
pygame.event.set_allowed((KEYDOWN, QUIT))


screen = pygame.display.set_mode(size)

pygame.display.update()
clock = pygame.time.Clock()
mp = Map_params()

start = True
running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        mp.key_pressed(event)
    elif start:
        start = False
    else:
        continue
        

    map_file = load_map(mp)
    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.update()


pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
