import random


class Asteroid:
    def __init__(self):
        # random initial x,y coordinate of the ship within the screen limits
        self.__location = (random.randint(-500, 500), random.randint(-500, 500))
        # speed for x, y axis
        self.__speed = (random.randint(1, 4), random.randint(1, 4))
        self.__size = 3
