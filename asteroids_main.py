from screen import Screen
import math
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint

MAX_TORP = 10
TORPEDO_SPAN = 200
DEFAULT_ASTEROIDS_NUM = 1
CRUSH_TITLE = 'WARNING'
CRUSH_MESSAGE = 'YOU WERE HIT BY THE EMPIRE!'
QUIT_TITLE = 'GOODBYE'
QUIT_MESSAGE = 'YOU ABANDONED THE GALAXY'
WIN_TITLE = 'GREAT WORK'
WIN_MESSAGE = 'YOU DEFEATED THE EMPIRE'
LOSE_TITLE = 'OH NO!'
LOSE_MESSAGE = 'THE EMPIRE DEFEATED YOU'


POINT_CHART = {1: 100, 2: 50, 3: 20}
SMALL = 1
MEDIUM = 2
LARGE = 3
START_LIVES = 3


class GameRunner:

    def __init__(self, asteroids_amount):

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__torpedoes_on = 0
        self.__screen = Screen()
        self.__x_wing = Ship(randint(-500, 500), randint(-500, 500), 0, 0, 0)
        self.__score = 0
        self.__asteroids = set()
        self.__torpedoes = set()
        self.__lives = START_LIVES
        self.add_asteroids(asteroids_amount)

    def add_asteroids(self, asteroids_amount):
        ast = set()
        ast_num = 0
        while ast_num < asteroids_amount:
            x = randint(-500, 500)
            while True:
                x_speed = randint(-4, 4)
                if x_speed != 0:
                    break
            y = randint(-500, 500)
            while True:
                y_speed = randint(-4, 4)
                if x != 0:
                    break
            current_ast = Asteroid(x, y, x_speed, y_speed)
            if not current_ast.has_intersection(self.__x_wing):
                self.__screen.register_asteroid(current_ast, 3)
                ast_num += 1
                ast.add(current_ast)
        self.__asteroids = ast

    def run(self):
        self.draw()
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()  # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        self.move_objects()
        self.draw()
        if self.__screen.should_end():
            self.__screen.show_message(QUIT_TITLE, QUIT_MESSAGE)
            self.__screen.end_game()
            sys.exit()

        if self.__screen.is_left_pressed():
            self.__x_wing.rotate('l')

        if self.__screen.is_right_pressed():
            self.__x_wing.rotate('r')

        if self.__screen.is_up_pressed():
            self.__x_wing.update_spd()

        if self.__screen.is_space_pressed():
            if self.__torpedoes_on < MAX_TORP:
                self.add_trop()
                self.__torpedoes_on += 1
            else:
                pass

        self.check_intersections()
        self.update_torpedos()

    def add_trop(self):
        location = self.__x_wing.get_location()
        speed = self.__x_wing.get_speed()
        angle = self.__x_wing.get_angle()
        new_torp = Torpedo(location, speed, angle, TORPEDO_SPAN)
        self.__torpedoes.add(new_torp)
        self.__screen.register_torpedo(new_torp)

    def update_torpedos(self):
        to_discard = []
        for torp in self.__torpedoes:
            cur_span = torp.reduce_span()
            if cur_span == 0:
                to_discard.append(torp)

        for to_remove in to_discard:
            self.__screen.unregister_torpedo(to_remove)
            self.__torpedoes.discard(to_remove)
            self.__torpedoes_on -= 1

    def move_objects(self):
        x_max = self.__screen_max_x
        x_min = self.__screen_min_x
        y_max = self.__screen_max_y
        y_min = self.__screen_min_x

        self.__x_wing.move_ship(x_max, x_min, y_max, y_min)

        ast_set = self.__asteroids
        for ast in ast_set:
            ast.move_asteroid(x_max, x_min, y_max, y_min)

        torp_set = self.__torpedoes
        for torp in torp_set:
            torp.move_torp(x_max, x_min, y_max, y_min)

    def draw(self):
        draw_params = self.__x_wing.get_drawing_param()
        self.__screen.draw_ship(draw_params[0], draw_params[1], draw_params[2])

        ast = self.__asteroids
        for ast in ast:
            location = ast.get_location()
            self.__screen.draw_asteroid(ast, location[0], location[1])

        torpedos = self.__torpedoes
        for torp in torpedos:
            lct = torp.get_drawing_param()
            self.__screen.draw_torpedo(torp, lct[0], lct[1], lct[2])

    def check_intersections(self):
        asteroids = self.__asteroids
        torpedos = self.__torpedoes
        ast_to_remove = []

        for ast in asteroids:
            if ast.has_intersection(self.__x_wing):
                self.__screen.show_message(CRUSH_TITLE, CRUSH_MESSAGE)
                self.__lives -= 1
                if self.__lives < 0:
                    self.__screen.show_message(LOSE_TITLE, LOSE_MESSAGE)
                    self.__screen.end_game()
                    sys.exit()
                self.__screen.remove_life()
                ast_to_remove.append(ast)

        if len(self.__asteroids) == 0:
            self.__screen.show_message(WIN_TITLE, WIN_MESSAGE)
            self.__screen.end_game()
            sys.exit()

        for i in ast_to_remove:
            self.__screen.unregister_asteroid(i)
            self.__asteroids.discard(i)

        torp_to_remove = []
        ast_to_split = {}
        for ast in asteroids:
            for tor in torpedos:
                if ast.has_intersection(tor):
                    ast_to_split[ast] = tor
                    self.update_score(ast)
                    break

        for torp in torp_to_remove:
            self.__screen.unregister_torpedo(torp)
            self.__torpedoes.discard(torp)
            self.__torpedoes_on -= 1

        self.split_asteroids(ast_to_split)

    def update_score(self, ast):
        self.__score = self.__score + POINT_CHART[ast.get_size()]
        self.__screen.set_score(self.__score)

    def split_asteroids(self,to_split):
        for ast in to_split:
            if ast.get_size() == SMALL:
                self.__asteroids.discard(ast)
                self.__screen.unregister_asteroid(ast)
                if len(self.__asteroids) == 0:
                    self.__screen.show_message(WIN_TITLE, WIN_MESSAGE)
                    self.__screen.end_game()
                    sys.exit()

            else:
                size = ast.get_size() - 1
                lct = ast.get_location()
                spd = self.split_speed(ast, to_split[ast])
                sub_stroid1 = Asteroid(lct[0], lct[1], spd[0], spd[1], size)
                sub_stroid2 = Asteroid(lct[0], lct[1], -spd[0], -spd[1], size)
                self.__asteroids.discard(ast)
                self.__screen.unregister_asteroid(ast)
                self.__screen.register_asteroid(sub_stroid1, size)
                self.__screen.register_asteroid(sub_stroid2, size)

                self.__asteroids.add(sub_stroid1)
                self.__asteroids.add(sub_stroid2)

    @staticmethod
    def split_speed(ast, torpedo):
        ast_spd = ast.get_speed()
        tor_spd = torpedo.get_speed()

        divisor = math.sqrt(math.pow(ast_spd[0], 2) + math.pow(ast_spd[1], 2))
        speed = (tor_spd[0] + ast_spd[0]) / divisor, \
                (tor_spd[1] + ast_spd[1]) / divisor

        return speed


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
