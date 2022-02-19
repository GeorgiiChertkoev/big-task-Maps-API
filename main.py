import os
import math
import sys
import pygame
from pygame.locals import *
import requests

from Samples.business import find_businesses
from Samples.distance import lonlat_distance
from Samples.geocoder import get_coordinates
from Samples.mapapi_PG import show_map

size = w, h = 600, 450
LAT_STEP = 0.008
LON_STEP = 0.002


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
        elif event.key == pygame.K_LEFT:  # LEFT_ARROW
            self.lat -= LAT_STEP * math.pow(2, 15 - self.z)
        elif event.key == pygame.K_RIGHT:  # RIGHT_ARROW
            self.lat += LAT_STEP * math.pow(2, 15 - self.z)
        elif event.key == pygame.K_UP and self.lat < 85:  # UP_ARROW
            self.lon += LON_STEP * math.pow(2, 15 - self.z)
        elif event.key == pygame.K_DOWN and self.lat > -85:  # DOWN_ARROW
            self.lon -= LON_STEP * math.pow(2, 15 - self.z)


def load_map(mp):
    map_request = f'http://static-maps.yandex.ru/1.x/?ll={mp.ll()}&z={mp.z}&l={mp.type}'
    response = requests.get(map_request)

    # print(response.url)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


pygame.init()

pygame.event.set_blocked((MOUSEMOTION))


screen = pygame.display.set_mode(size)

pygame.event.clear()
clock = pygame.time.Clock()

mp = Map_params()
map_file = load_map(mp)
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.update()

start = True
running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        mp.key_pressed(event)
        

    map_file = load_map(mp)
    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.update()


pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
