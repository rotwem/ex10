import random


class Asteroid:
    def __init__(self, location, speed, size):
        # tuple: random initial x,y coordinate of the ship within the screen limits
        self.__location = location
        # tuple: speed for x, y axis
        self.__speed = speed
        # int: ship size
        self.__size = size
