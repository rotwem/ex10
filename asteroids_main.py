from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import random
import math

DEFAULT_ASTEROIDS_NUM = 5
SHIP_COLLISION = "ship collision"
QUIT_GAME = "you quit"
NO_MORE_LIFE = "you died"
NO_MORE_ASTEROIDS = "you win"
MESSAGE_DICTIONARY = {SHIP_COLLISION: "oh no! your ship struck an asteroid. you lost one life",
                      QUIT_GAME: "such a quitter", NO_MORE_LIFE: "such a looser", NO_MORE_ASTEROIDS: "good game"}
SCORE_DICTIONARY = {3: 20, 2: 50, 1: 100}


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship((self.random_location_x(), self.random_location_y()), (0, 0), 0, 3)
        self.__score = 0
        self.__torpedo_lst = []
        self.__asteroid_lst = []
        # these lines are for initiating asteroids
        for i in range(asteroids_amount):
            asteroid_location = (self.random_location_x(), self.random_location_y())
            while asteroid_location == self.__ship.get_location():
                asteroid_location = (self.random_location_x(), self.random_location_y())
            asteroid_speed = (random.randint(1, 4), random.randint(1, 4))
            self.__asteroid_lst.append(Asteroid(asteroid_location, asteroid_speed, 3))
        # these lines are for registering the asteroids and initial draw
        for asteroid in self.__asteroid_lst:
            asteroid_x, asteroid_y = asteroid.get_location()
            self.__screen.register_asteroid(asteroid, 3)
            self.__screen.draw_asteroid(asteroid, asteroid_x, asteroid_y)

    def random_location_x(self):
        return random.randint(self.__screen_min_x, self.__screen_max_x)

    def random_location_y(self):
        return random.randint(self.__screen_min_y, self.__screen_max_y)

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
        return screen_min_i + (location_i + speed_i - screen_min_i) % delta

    def calc_new_asteroid_speed_i(self, torpedo_speed_i, old_asteroid_speed_i, old_asteroid_speed_j):
        numerator = torpedo_speed_i + old_asteroid_speed_i
        denominator = (old_asteroid_speed_i ** 2) + (old_asteroid_speed_j ** 2)
        return numerator / math.sqrt(denominator)

    def move_object(self, obj):
        # moves any game object to a new location
        # notice to send specific object AKA self.__something
        location_obj_x, location_obj_y = obj.get_location()
        speed_obj_x, speed_obj_y = obj.get_speed()
        new_obj_x = self.calc_move(location_obj_x, speed_obj_x, self.__screen_min_x, self.__screen_max_x)
        new_obj_y = self.calc_move(location_obj_y, speed_obj_y, self.__screen_min_y, self.__screen_max_y)
        obj.set_location((new_obj_x, new_obj_y))

    def end_loop(self):
        if self.__screen.should_end():
            return QUIT_GAME
        elif self.__ship.get_life_count() == 0:
            return NO_MORE_LIFE
        elif len(self.__asteroid_lst) == 0:
            return NO_MORE_ASTEROIDS
        return False

    def _game_loop(self):
        end_loop = self.end_loop()
        if end_loop:
            self.__screen.show_message(end_loop, MESSAGE_DICTIONARY[end_loop])
            self.__screen.end_game()
            sys.exit()
        # these lines are to check life span of existing torpedos
        for torpedo in self.__torpedo_lst:
            if torpedo.get_life_span() == 200:
                self.__torpedo_lst.remove(torpedo)
                self.__screen.unregister_torpedo(torpedo)
            else:
                torpedo.add_life_circle()
        # these lines are to move and draw ship
        ship_location_x, ship_location_y = self.__ship.get_location()
        ship_heading = self.__ship.get_heading()
        self.__screen.draw_ship(ship_location_x, ship_location_y, ship_heading)
        self.move_object(self.__ship)
        # these lines are to move and draw all asteroids
        for asteroid in self.__asteroid_lst:
            self.move_object(asteroid)
            asteroid_x, asteroid_y = asteroid.get_location()
            self.__screen.draw_asteroid(asteroid, asteroid_x, asteroid_y)
        # these lines are for ship change direction
        ship_heading = self.__ship.get_heading()
        if self.__screen.is_left_pressed():
            self.__ship.set_heading(ship_heading + 7)
        if self.__screen.is_right_pressed():
            self.__ship.set_heading(ship_heading - 7)
        # these lines are for speeding up ship
        if self.__screen.is_up_pressed():
            self.__ship.speed_up()
        # these lines are to create torpedos
        if self.__screen.is_space_pressed() and len(self.__torpedo_lst) < 10:
            torpedo_location_x, torpedo_location_y = self.__ship.get_location()
            ship_speed_x, ship_speed_y = self.__ship.get_speed()
            torpedo_speed_x = ship_speed_x + 2 * math.cos(math.radians(self.__ship.get_heading()))
            torpedo_speed_y = ship_speed_y + 2 * math.sin(math.radians(self.__ship.get_heading()))
            new_torpedo = Torpedo((torpedo_location_x, torpedo_location_y), (torpedo_speed_x, torpedo_speed_y),
                                  self.__ship.get_heading())
            self.__screen.register_torpedo(new_torpedo)
            self.__screen.draw_torpedo(new_torpedo, torpedo_location_x, torpedo_location_y,
                                       new_torpedo.get_heading())
            self.__torpedo_lst.append(new_torpedo)
        # these lines are for moving torpedos
        for torpedo in self.__torpedo_lst:
            self.move_object(torpedo)
            torpedo_location_x, torpedo_location_y = torpedo.get_location()
            torpedo_heading = torpedo.get_heading()
            self.__screen.draw_torpedo(torpedo, torpedo_location_x, torpedo_location_y, torpedo_heading)
        # these lines are for checking if ship hit asteroids
        for asteroid in self.__asteroid_lst:
            if asteroid.has_intersection(self.__ship):
                self.__ship.remove_one_life()
                self.__screen.show_message(SHIP_COLLISION, MESSAGE_DICTIONARY[SHIP_COLLISION])
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroid_lst.remove(asteroid)
                self.__screen.remove_life()
        # these lines are for checking if torpedo hit asteroids
        for torpedo in self.__torpedo_lst:
            for asteroid in self.__asteroid_lst:
                if asteroid.has_intersection(torpedo):
                    self.__score += SCORE_DICTIONARY[asteroid.get_size()]
                    self.__screen.set_score(self.__score)
                    asteroid_size = asteroid.get_size()
                    if asteroid_size > 1:
                        asteroid_location = asteroid.get_location()
                        old_asteroid_speed_x, old_asteroid_speed_y = asteroid.get_speed()
                        torpedo_speed_x, torpedo_speed_y = torpedo.get_speed()
                        x_speed = self.calc_new_asteroid_speed_i(torpedo_speed_x, old_asteroid_speed_x,
                                                                 old_asteroid_speed_y)
                        y_speed = self.calc_new_asteroid_speed_i(torpedo_speed_y, old_asteroid_speed_y,
                                                                 old_asteroid_speed_x)
                        new_asteroid_1 = Asteroid(asteroid_location, (x_speed, y_speed), asteroid_size - 1)
                        new_asteroid_2 = Asteroid(asteroid_location, (-x_speed, -y_speed), asteroid_size - 1)
                        self.__asteroid_lst.extend([new_asteroid_1, new_asteroid_2])
                        self.__screen.register_asteroid(new_asteroid_1, asteroid_size - 1)
                        self.__screen.register_asteroid(new_asteroid_2, asteroid_size - 1)
                    self.__asteroid_lst.remove(asteroid)
                    self.__screen.unregister_asteroid(asteroid)
                    self.__torpedo_lst.remove(torpedo)
                    self.__screen.unregister_torpedo(torpedo)



def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
