class Torpedo:
    """this class is for the torpedo object in the game 'Asteroids'"""
    def __init__(self, location, speed, heading):
        # tuple: random initial x,y coordinate of the ship within the screen limits
        self.__location = location
        # tuple: speed for x, y axis
        self.__speed = speed
        # int: torpedo is headed
        self.__heading = heading
        # int: counter of game loops passed since torpedo created
        self.__life_span = 0

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
        return 4

    def get_life_span(self):
        return self.__life_span

    def add_life_circle(self):
        """adds to the 'life' counter"""
        self.__life_span += 1
