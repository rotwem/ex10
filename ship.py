import random


class Ship:
    def __init__(self):
        # random initial x,y coordinate of the ship within the screen limits
        self.__location = (random.randint(-500, 500), random.randint(-500, 500))
        # speed for x, y axis
        self.__speed = (0, 0)
        # ship is headed
        self.__direction = 0
