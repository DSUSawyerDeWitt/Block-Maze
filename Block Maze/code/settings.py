import pygame
from os.path import join
from os import walk
import math

TILE_SIZE = 64
GRID_ROWS = 8
GRID_COLUMNS = 8

WINDOW_WIDTH, WINDOW_HEIGHT = 900, 700

FLIPPER = {
    'FLIPPER_IMPORT': {
        2:'Down_Flipper_2',
        3:'Up_Flipper_3',
        5:'Left_Flipper_5',
        6:'Right_Flipper_6'
    },
    'FLIPPER_SIDE': {
        2: 'Down',
        3: 'Up',
        5: 'Left',
        6: 'Right'
    },
    'FLIPPER_PLACEMENT': {
        'Left': (-64, 0),
        'Right': (64, 0),
        'Up': (0, -64),
        'Down': (0, 64)
    }
}
TUBE = {
    'SIDE':{
        'Bottom Right': (0, -1),
        'Bottom Left': (-1, 0)
    }
}