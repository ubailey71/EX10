from screen import Screen
import math
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint
import random

MAX_TORP = 10
TORPEDO_SPAN = 200
DEFAULT_ASTEROIDS_NUM = 5
CRUSH_TITLE = 'WARNING'
CRUSH_MESSAGE = 'YOU WERE HIT BY THE EMPIRE!'
QUIT_TITLE = 'GOODBYE'
QUIT_MESSAGE = 'YOU ABANDONED THE GALAXY'
WIN_TITLE = 'GREAT WORK'
WIN_MESSAGE = 'YOU DEFEATED THE EMPIRE'
LOSE_TITLE = 'OH NO!'
LOSE_MESSAGE = 'THE EMPIRE DEFEATED YOU'
SGN = [1, -1]

POINT_CHART = {1: 100, 2: 50, 3: 20}
SMALL = 1
MEDIUM = 2
LARGE = 3
START_LIVES = 3
SCREEN_SIZE = 500

class GameRunner:

    def __init__(self, asteroids_amount):

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__torpedoes_on = 0
        self.__screen = Screen()
        self.__xwing = Ship((randint(-SCREEN_SIZE, SCREEN_SIZE), randint(-SCREEN_SIZE, SCREEN_SIZE)), (0, 0), 0, 1)
        self.__score = 0
        self.__asteroids = self.add_asteroids(asteroids_amount)
        self.__torpedoes = set()
        self.__lives = START_LIVES

    def set_speed(self):
        """
        sets random speed for asteroid between -4,4 (but not 0)
        :return: int representing a random speed
        """
        sgn = random.choice(SGN)
        speed_sgn = randint(1, 4)
        speed = sgn * speed_sgn
        return speed

    def add_asteroids(self, asteroids_amount):
        """
        adds asteroids to game with random locations and speeds
        :param asteroids_amount: int, amount of asteroids allowed in game
        """
        ast = set()
        ast_num = 0
        while ast_num < asteroids_amount:

            x = randint(-SCREEN_SIZE, SCREEN_SIZE)
            x_speed = self.set_speed()
            y = randint(-SCREEN_SIZE, SCREEN_SIZE)
            y_speed = self.set_speed()
            current_ast = Asteroid((x, y), (x_speed, y_speed))

            if not current_ast.has_intersection(self.__xwing):
                self.__screen.register_asteroid(current_ast, 3)
                ast_num += 1
                ast.add(current_ast)

        return ast

    def run(self):

        """
        starts the game and initiates the game loop
        :return:
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):

        # You should not to change this method!
        self._game_loop()  # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def move_spaceship(self):
        """
        part of _game_loop(self), checks for user input for moving th spaceship and rotates
        / changes speed accordingly
        """
        if self.__screen.is_left_pressed():
            self.__xwing.rotate('l')

        if self.__screen.is_right_pressed():
            self.__xwing.rotate('r')

        if self.__screen.is_up_pressed():
            self.__xwing.update_spd()

    def shoot(self):
        """
        sub function of _game_loop(self), checks for user input for shooting a torpedo, and shoots/does nothing
        accordingly
        """
        if self.__screen.is_space_pressed():
            if self.__torpedoes_on < MAX_TORP:
                self.add_torp()
                self.__torpedoes_on += 1

    def _game_loop(self):
        """
        main loop for the game, iterates through all functions required for gameplay, updates the screen and updates all
        parameters of the game
        """
        self.move_objects()
        self.draw_spaceship()
        self.move_spaceship()
        self.draw_ast()
        self.handle_intersections_ship()
        self.draw_torpedos()
        self.shoot()
        self.check_intersections_torp()
        self.check_end()
        self.update_torpedos()

    def draw_ast(self):
        """
        uses draw_asteroid(ast,x,y) function to draw the asteroid in its current location
        """
        ast = self.__asteroids
        for ast in ast:
            location = ast.get_location()
            self.__screen.draw_asteroid(ast, location[0], location[1])

    def add_torp(self):
        """
        if player shoots a torpedo, the function calculates torpedoes speed and location, and adds torpedo to game
        """
        location = self.__xwing.get_location()
        speed = self.__xwing.get_speed()
        angle = self.__xwing.get_angle()
        new_torp = Torpedo(location, speed, angle, TORPEDO_SPAN)
        self.__torpedoes.add(new_torp)
        self.__screen.register_torpedo(new_torp)

    def update_torpedos(self):
        """
        this function takes care of removing torpedoes that either hit an asteroid, or have outlived their lifespan
        and removes the torpedoes from game and screen
        """
        to_discard = set()
        for torp in self.__torpedoes:
            cur_span = torp.reduce_span()
            if cur_span == 0:
                to_discard.add(torp)

        for to_remove in to_discard:
            self.__torpedoes.discard(to_remove)
            self.__screen.unregister_torpedo(to_remove)
            self.__torpedoes_on -= 1

    def move_objects(self):
        """
        this function goes through all objects in the game (spaceship, topredos, asteroids) and moves them to their
        updated location
        """
        x_max = self.__screen_max_x
        x_min = self.__screen_min_x
        y_max = self.__screen_max_y
        y_min = self.__screen_min_x

        self.__xwing.move_ship(x_max, x_min, y_max, y_min)

        ast_set = self.__asteroids
        for ast in ast_set:
            ast.move_asteroid(x_max, x_min, y_max, y_min)

        torp_set = self.__torpedoes
        for torp in torp_set:
            torp.move_torp(x_max, x_min, y_max, y_min)

    def draw_torpedos(self):
        """
        calls draw_torpedo(torpedo,x,y) function form screen to draw all torpedoes in their updated location)
        """
        torpedos = self.__torpedoes
        for torp in torpedos:
            lct = torp.get_drawing_param()
            self.__screen.draw_torpedo(torp, lct[0], lct[1], lct[2])

    def draw_spaceship(self):
        """
        calls the draw_ship (x,y,heading) to draw the ship in its updated location
        """
        draw_params = self.__xwing.get_drawing_param()
        self.__screen.draw_ship(draw_params[0], draw_params[1], draw_params[2])

    def handle_intersections_ship(self):
        """
        handles actions in case the ship has an intersection with an asteroid
        checks if the ship has an interaction with any of the asteroids,does all required actions and removes all
        asteroids that have intersections
        """
        asteroids = self.__asteroids
        ast_to_remove = []

        for ast in asteroids:
            if ast.has_intersection(self.__xwing):
                self.__screen.show_message(CRUSH_TITLE, CRUSH_MESSAGE)
                self.__lives -= 1
                self.check_end()
                self.__screen.remove_life()
                ast_to_remove.append(ast)

        for i in ast_to_remove:
            self.__screen.unregister_asteroid(i)
            self.__asteroids.discard(i)

        self.check_end()

    def check_intersections_torp(self):
        """
        handles actions in case of an intersection of a torpedo with  an asteroid
        checks if the torpedo has an interaction with any of the asteroids,does all required actions and removes all
        torpedos that have intersections
        """
        asteroids = self.__asteroids
        torpedos = self.__torpedoes

        torp_to_remove = []
        ast_to_split = {}
        for ast in asteroids:
            for tor in torpedos:
                if ast.has_intersection(tor):
                    ast_to_split[ast] = tor
                    torp_to_remove.append(tor)
                    self.update_score(ast)
                    break

        for torp in torp_to_remove:
            self.__screen.unregister_torpedo(torp)
            self.__torpedoes.discard(torp)
            self.__torpedoes_on -= 1

        self.split_asteroids(ast_to_split)

    def update_score(self, ast):
        """
        updates the score after a successful hit
        :param ast: the asteroid that was hit
        """
        self.__score = self.__score + POINT_CHART[ast.get_size()]
        self.__screen.set_score(self.__score)

    def split_asteroids(self, to_split):
        """
        after a successful hit, the function splits the asteroid into smaller asteroids
        :param to_split: the asteroid being split
        """
        for ast in to_split:
            if ast.get_size() == SMALL:
                self.__asteroids.discard(ast)
                self.__screen.unregister_asteroid(ast)
                self.check_end()
            else:
                size = ast.get_size() - 1
                lct = ast.get_location()
                spd = self.split_speed(ast, to_split[ast])
                sub_stroid1 = Asteroid(lct, spd, size)
                sub_stroid2 = Asteroid(lct, (-spd[0], -spd[1]), size)
                self.__asteroids.discard(ast)
                self.__screen.unregister_asteroid(ast)
                self.__screen.register_asteroid(sub_stroid1, size)
                self.__screen.register_asteroid(sub_stroid2, size)

                self.__asteroids.add(sub_stroid1)
                self.__asteroids.add(sub_stroid2)

    @staticmethod
    def split_speed(ast, torpedo):
        """
        a static method calculating the speed of an asteroid after being split from a bigger one
        :param ast: the former asteroid
        :param torpedo: the torpedo that hit the asteroid
        :return: the speed of the new asteroid
        """
        ast_spd = ast.get_speed()
        tor_spd = torpedo.get_speed()

        divisor = math.sqrt(math.pow(ast_spd[0], 2) + math.pow(ast_spd[1], 2))
        speed = (tor_spd[0] + ast_spd[0]) / divisor, \
                (tor_spd[1] + ast_spd[1]) / divisor

        return speed

    def check_end(self):
        """
        checks if the game is over (game won, game lost or user exit), prints a relevant message and terminates the game
        """
        if len(self.__asteroids) == 0:
            self.__screen.show_message(WIN_TITLE, WIN_MESSAGE)
            self.__screen.end_game()
            sys.exit()

        if self.__lives < 0:
            self.__screen.show_message(LOSE_TITLE, LOSE_MESSAGE)
            self.__screen.end_game()
            sys.exit()

        if self.__screen.should_end():
            self.__screen.show_message(QUIT_TITLE, QUIT_MESSAGE)
            self.__screen.end_game()
            sys.exit()


def main(amount):
    """
    creates the game and starts the game itself
    :param amount: amount of initial asteroids
    """
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
