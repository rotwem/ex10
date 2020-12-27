import random
import math

class Asteroid:
    def __init__(self, location, speed, size):
        # tuple: random initial x,y coordinate of the ship within the screen limits
        self.__location = location
        # tuple: speed for x, y axis
        self.__speed = speed
        # int: ship size
        self.__size = size

    def get_location(self):
        return self.__location

    def set_location(self, new_location):
        self.__location = new_location

    def get_speed(self):
        return self.__speed

    def set_speed(self, new_speed):
        self.__speed = new_speed

    def get_radius(self):
        return self.__size * 10 - 5

    def get_size(self):
        return self.__size

    def has_intersection(self, obj):
        # notice to send specific object AKA self.__something
        asteroid_x, asteroid_y = self.get_location()
        obj_x, obj_y = obj.get_location()
        distance = math.sqrt(((obj_x - asteroid_x) ** 2) + ((obj_y - asteroid_y) ** 2))
        if distance <= self.get_radius() + obj.get_radius():
            return True
        else:
            return False


