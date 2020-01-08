import math
import random

X = 'x'
Y = 'y'
RADIUS = 4


class Torpedo:
    """
    This class creates objects of type torpedo and preforms methods on them
    """

    def __init__(self, location, speed, angle, life_span):
        """
        constructor of a torpedo object
        :param location: a tuple representing the location of the torpedo, in (x,y) format
        :param speed:a tuple representing the speed of the torpedo in each axis, in (x,y) format
        :param angle: a ???? representing the angle of the torpedo
        :param life_span: the life span of the torpedo, determines how much time the torpedo will survive on screen
        """

        self.__location = location
        self.__angle = angle
        self.__speed = speed
        self.__speed = self.speed_calculation()
        self.__radius = RADIUS
        self.__life_span = life_span

    def speed_calculation(self):
        """
        calculates the updated speed for the torpedo
        :return: returns new speed in (x,y) format
        """
        rdangle = math.radians(self.__angle)
        new_spd_x = self.__speed[0] + (2 * math.cos(rdangle))
        new_spd_y = self.__speed[1] + (2 * math.sin(rdangle))

        return (new_spd_x, new_spd_y)

    def get_drawing_param(self):
        """
        returns all parameters needed for drawing the torpedo om screen
        :return: list of drawing parameters in [x location,y location,angle] format
        """
        lst = [self.__location[0], self.__location[1], self.__angle]
        return lst

    def get_location(self):
        """
        a getter for the torpedos location
        :return: torpedos current location in (x,y) format
        """
        return self.__location

    def move_torp(self, min_x, max_x, min_y, max_y):
        """
        calculates and moves the torpedo to its next location based on its speed
        :param min_x: minimum x coordinate of screen
        :param max_x: maximum x coordinate of screen
        :param min_y: minimum y coordinate of screen
        :param max_y: maximum y coordinate of screen
        """
        prev_x_spd = self.__speed[0]
        prev_x_lct = self.__location[0]
        prev_y_spd = self.__speed[1]
        prev_y_lct = self.__location[1]

        x_spot = min_x + (prev_x_lct + prev_x_spd - min_x) % (max_x - min_x)
        y_spot = min_y + (prev_y_lct + prev_y_spd - min_y) % (max_y - min_y)
        self.set_location(x_spot, y_spot)

    def set_location(self, new_x, new_y):
        """
        setter for torpedos location
        :param new_x: new x location
        :param new_y: new y location
        """
        self.__location = (new_x, new_y)

    def get_radius(self):
        """
        getter for torpedos radius
        :return:
        """
        return self.__radius

    def get_speed(self):
        """
        a getter for the torpedoes speed
        :return: a tuple representing the torpedoes current speed in (x,y) format
        """
        return self.__speed

    def reduce_span(self):
        """
        reduces the topredoes life span
        :return: the new
        """
        self.__life_span -= 1
        return self.__life_span
