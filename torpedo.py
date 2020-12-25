import random

class Torpedo:
    def __init__(self, location, speed, heading):
        # tuple: random initial x,y coordinate of the ship within the screen limits
        self.__location = location
        # tuple: speed for x, y axis
        self.__speed = speed
        # int: torpedo is headed
        self.__heading =heading
