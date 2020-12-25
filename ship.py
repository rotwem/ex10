class Ship:
    def __init__(self, location, speed, heading):
        # tuple: random initial x,y coordinate of the ship within the screen limits
        self.__location = location
        # tuple: speed for x, y axis
        self.__speed = speed
        # int: ship is headed
        self.__heading = heading

    def get_location(self):
        return self.__location

    def set_location(self, new_location):
        self.__location = new_location

    def get_heading(self):
        return self.__heading

    def set_heading(self, new_heading):
        self.__heading = new_heading
