import math


class Ship:
    """this class is for the spaceship object in the game 'Asteroids'"""
    def __init__(self, location, speed, heading, life_count):
        # tuple: random initial x,y coordinate of the ship within the screen limits
        self.__location = location
        # tuple: speed for x, y axis
        self.__speed = speed
        # int: ship is headed
        self.__heading = heading
        # int: life count
        self.__life_count = life_count

    def get_location(self):
        return self.__location

    def set_location(self, new_location):
        self.__location = new_location

    def get_heading(self):
        return self.__heading

    def set_heading(self, new_heading):
        self.__heading = new_heading

    def get_speed(self):
        return self.__speed

    def set_speed(self, new_speed):
        self.__speed = new_speed

    def get_radius(self):
        return 1

    def get_life_count(self):
        return self.__life_count

    def remove_one_life(self):
        self.__life_count -= 1

    def speed_up(self):
        """eccelerates the ship using the formula given in the instructions"""
        speed_x, speed_y = self.__speed
        new_speed_x = speed_x + math.cos(math.radians(self.__heading))
        new_speed_y = speed_y + math.sin(math.radians(self.__heading))
        self.__speed = (new_speed_x, new_speed_y)

