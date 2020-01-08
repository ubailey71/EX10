import math


class Asteroid:
    """
    This class creates objects of type asteroids and preform methods on them
    in the following methods you will find a specific instructions about
    every method input and output.

    make sure you follow them, wrong input may cause the program to collapse.
    """

    def __init__(self, location, speed, size=3):
        """
        This is the constructor of the asteroids.
        :param location: a tuple representing the location of the asteroid, in (x,y) format
        :param speed:a tuple representing the speed of the asteroid in each axis, in (x,y) format
        :param size: a integer representing the size of asteroid
        """
        self.__location = location
        self.__speed = speed
        self.__size = size

    def move_asteroid(self, min_x, max_x, min_y, max_y):
        """
        calculates and moves the asteroid to its next location based on its speed
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
        a setter for the asteroids location
        :param new_x: new x coordinate
        :param new_y: new y coordinate
        :return:
        """
        self.__location = (new_x, new_y)

    def get_radius(self):
        """
        getter for the asteroids radius
        :return: asteroids radius
        """
        return (self.__size * 10) - 5

    def get_location(self):
        """
        getter for the asteroids location
        :return: asteroids location in (x,y) format
        """
        return self.__location

    def get_speed(self):
        """
        getter for the asteroids speed
        :return: asteroids speed in (x,y) format
        """

        return self.__speed

    def has_intersection(self, obj):
        """
        checks if the asteroid has an intersection with another object
        :param obj: the object checked for intersections
        :return: True if has interaction, False if not
        """
        rdius_sum = self.get_radius() + obj.get_radius()
        ast_x = self.get_location()[0]
        ast_y = self.get_location()[1]

        obj_x = obj.get_location()[0]
        obj_y = obj.get_location()[1]

        x_dist = math.pow(obj_x - ast_x, 2)
        y_dist = math.pow(obj_y - ast_y, 2)
        distance = math.sqrt(x_dist + y_dist)

        if distance <= rdius_sum:
            return True

        return False

    def get_size(self):
        """
        getter for the asteroids size
        :return: asteroids size
        """

        return self.__size
