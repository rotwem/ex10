from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import random
import math

ASTEROID_DEFAULT_SIZE = 3
TORPEDO_LIFE_MAX = 200
DEFAULT_ASTEROIDS_NUM = 5
SHIP_COLLISION = "Ship collision"
QUIT_GAME = "You quit"
NO_MORE_LIFE = "You died"
NO_MORE_ASTEROIDS = "You win!"
MESSAGE_DICTIONARY = {SHIP_COLLISION: "Oh no! Your ship has struck an asteroid.\nYou lost one life",
                      QUIT_GAME: "Such a quitter", NO_MORE_LIFE: "Such a loser", NO_MORE_ASTEROIDS: "Good game!"}
SCORE_DICTIONARY = {3: 20, 2: 50, 1: 100}


class GameRunner:
    """this class is for an object asteroid game runner"""
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
        self.init_asteroids(asteroids_amount)

    def init_asteroids(self, asteroids_amount):
        """these function initiates asteroids"""
        for i in range(asteroids_amount):
            asteroid_location = (self.random_location_x(), self.random_location_y())
            while asteroid_location == self.__ship.get_location():
                asteroid_location = (self.random_location_x(), self.random_location_y())
            asteroid_speed = (random.randint(1, 4), random.randint(1, 4))
            self.__asteroid_lst.append(Asteroid(asteroid_location, asteroid_speed, ASTEROID_DEFAULT_SIZE))
        # these lines are for registering the asteroids and initial draw
        for asteroid in self.__asteroid_lst:
            asteroid_x, asteroid_y = asteroid.get_location()
            self.__screen.register_asteroid(asteroid, ASTEROID_DEFAULT_SIZE)
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

    @staticmethod
    def calc_move(location_i, speed_i, screen_min_i, screen_max_i):
        """calculates the new values for x,y location of an object."""
        delta = screen_max_i - screen_min_i
        return screen_min_i + (location_i + speed_i - screen_min_i) % delta

    @staticmethod
    def calc_new_asteroid_speed_i(torpedo_speed_i, old_asteroid_speed_i, old_asteroid_speed_j):
        """calculates the new values for x/y speed of an asteroid after collision."""
        numerator = torpedo_speed_i + old_asteroid_speed_i
        denominator = (old_asteroid_speed_i ** 2) + (old_asteroid_speed_j ** 2)
        return numerator / math.sqrt(denominator)

    def move_object(self, obj):
        """moves any game object to a new location. notice to send specific object AKA self.__something"""
        location_obj_x, location_obj_y = obj.get_location()
        speed_obj_x, speed_obj_y = obj.get_speed()
        new_obj_x = self.calc_move(location_obj_x, speed_obj_x, self.__screen_min_x, self.__screen_max_x)
        new_obj_y = self.calc_move(location_obj_y, speed_obj_y, self.__screen_min_y, self.__screen_max_y)
        obj.set_location((new_obj_x, new_obj_y))

    def end_loop(self):
        """checks if one the conditions for ending the game exists"""
        if self.__screen.should_end():
            return QUIT_GAME
        elif self.__ship.get_life_count() == 0:
            return NO_MORE_LIFE
        elif len(self.__asteroid_lst) == 0:
            return NO_MORE_ASTEROIDS
        return False

    def _game_loop(self):
        """runs the game while passively checking the user's actions in the game"""
        end_loop = self.end_loop()
        if end_loop:
            self.__screen.show_message(end_loop, MESSAGE_DICTIONARY[end_loop])
            self.__screen.end_game()
            sys.exit()
        # check life span of existing torpedoes, remove if past max life
        self.monitor_torpedoes_life()
        # these lines are to move and draw ship
        self.move_and_draw_ship()
        # these lines are to move and draw all asteroids
        self.move_and_draw_asteroids()
        # these lines are for ship change direction
        self.update_ship_heading()
        # these lines are for speeding up ship
        if self.__screen.is_up_pressed():
            self.__ship.speed_up()
        # these lines are to create torpedoes
        if self.__screen.is_space_pressed() and len(self.__torpedo_lst) < 10:
            self.create_torpedo()
        # these lines are for moving torpedoes
        self.move_and_draw_torpedoes()
        # these lines are for checking if ship hit asteroids
        self.ship_hit_asteroid_handling()
        # these lines are for checking if torpedo hit asteroids
        self.torpedo_hit_asteroid_handling()

    def torpedo_hit_asteroid_handling(self):
        """checks for each torpedo if it has hit any of the asteroids. if so, it runs some actions according
        to the game's instructions"""
        for torpedo in self.__torpedo_lst:
            for asteroid in self.__asteroid_lst:
                if asteroid.has_intersection(torpedo):
                    self.__score += SCORE_DICTIONARY[asteroid.get_size()]
                    self.__screen.set_score(self.__score)
                    asteroid_size = asteroid.get_size()
                    if asteroid_size > 1:  # if the asteroid's size is 1, it doesn't split and just disappears
                        # from the game
                        self.create_two_smaller_asteroids(asteroid, asteroid_size, torpedo)
                    self.__asteroid_lst.remove(asteroid)
                    self.__screen.unregister_asteroid(asteroid)
                    self.__torpedo_lst.remove(torpedo)
                    self.__screen.unregister_torpedo(torpedo)

    def create_two_smaller_asteroids(self, asteroid, asteroid_size, torpedo):
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

    def ship_hit_asteroid_handling(self):
        """checks if the ship has hit an asteroid, and if so it does stuff according to the game instructions"""
        for asteroid in self.__asteroid_lst:
            if asteroid.has_intersection(self.__ship):
                self.__ship.remove_one_life()
                self.__screen.show_message(SHIP_COLLISION, MESSAGE_DICTIONARY[SHIP_COLLISION])
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroid_lst.remove(asteroid)
                self.__screen.remove_life()

    def move_and_draw_torpedoes(self):
        """moves each torpedo in the game's torpedoes list, then draws them in their new current location"""
        for torpedo in self.__torpedo_lst:
            self.move_object(torpedo)
            torpedo_location_x, torpedo_location_y = torpedo.get_location()
            torpedo_heading = torpedo.get_heading()
            self.__screen.draw_torpedo(torpedo, torpedo_location_x, torpedo_location_y, torpedo_heading)

    def create_torpedo(self):
        """creates a torpedo and adds it to the game"""
        torpedo_location_x, torpedo_location_y = self.__ship.get_location()
        ship_speed_x, ship_speed_y = self.__ship.get_speed()
        # calculate the x,y speed according to the given formula
        torpedo_speed_x = ship_speed_x + 2 * math.cos(math.radians(self.__ship.get_heading()))
        torpedo_speed_y = ship_speed_y + 2 * math.sin(math.radians(self.__ship.get_heading()))
        new_torpedo = Torpedo((torpedo_location_x, torpedo_location_y), (torpedo_speed_x, torpedo_speed_y),
                              self.__ship.get_heading())
        self.__screen.register_torpedo(new_torpedo)
        self.__screen.draw_torpedo(new_torpedo, torpedo_location_x, torpedo_location_y,
                                   new_torpedo.get_heading())
        self.__torpedo_lst.append(new_torpedo)

    def update_ship_heading(self):
        """changes the direction of the ship according to the user's input (right/left click on keyboard)"""
        ship_heading = self.__ship.get_heading()
        if self.__screen.is_left_pressed():
            self.__ship.set_heading(ship_heading + 7)
        if self.__screen.is_right_pressed():
            self.__ship.set_heading(ship_heading - 7)

    def move_and_draw_asteroids(self):
        """moves each asteroid in the game's asteroids list, then draws them in their new current location"""
        for asteroid in self.__asteroid_lst:
            self.move_object(asteroid)
            asteroid_x, asteroid_y = asteroid.get_location()
            self.__screen.draw_asteroid(asteroid, asteroid_x, asteroid_y)

    def move_and_draw_ship(self):
        """draws the ship in the current location,
        then moves the ship according to its speed"""
        ship_location_x, ship_location_y = self.__ship.get_location()
        ship_heading = self.__ship.get_heading()
        self.__screen.draw_ship(ship_location_x, ship_location_y, ship_heading)  # we draw first because otherwise we
        # miss the printing of the ship in its first location.
        self.move_object(self.__ship)

    def monitor_torpedoes_life(self):
        """goes over each torpedo and checks whether it has reached max life spam. if so,
        the torpedo is deleted, else, 1 is added to its life counter"""
        for torpedo in self.__torpedo_lst:
            if torpedo.get_life_span() == TORPEDO_LIFE_MAX:
                self.__torpedo_lst.remove(torpedo)
                self.__screen.unregister_torpedo(torpedo)
            else:
                torpedo.add_life_circle()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
