from screen import Screen
import sys
from ship import Ship
import random

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        ship_location_x = random.randint(self.__screen_min_x, self.__screen_max_x)
        ship_location_y = random.randint(self.__screen_min_y, self.__screen_max_y)
        self.__ship = Ship((ship_location_x, ship_location_y), (0, 0), 0)



    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def calc_move(self, location_i, speed_i, screen_min_i, screen_max_i):
        # calculates the new values for x,y location of an object.
        delta = screen_max_i - screen_min_i
        return screen_min_i + (location_i + speed_i - screen_min_i ) % delta

    def move_object(self, obj):
        # moves any game object to a new location
        # notice to send specific object AKA self.__something
        location_obj_x, location_obj_y = obj.get_location()
        speed_obj_x, speed_obj_y = obj.get_speed()
        new_obj_x = self.calc_move(location_obj_x, speed_obj_x, self.__screen_min_x, self.__screen_max_x)
        new_obj_y = self.calc_move(location_obj_y, speed_obj_y, self.__screen_min_y, self.__screen_max_y)
        obj.set_location((new_obj_x, new_obj_y))

    def _game_loop(self):
        # TODO: Your code goes here
        ship_location_x, ship_location_y = self.__ship.get_location()
        ship_heading = self.__ship.get_heading()
        self.__screen.draw_ship(ship_location_x, ship_location_y, ship_heading)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
