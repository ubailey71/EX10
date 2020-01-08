import math

LEFT = 'l'
RIGHT = 'r'
CIRCLE = 360


class Ship:
    """
    This class creates object of the type spaceship and preform methods on
    them.
    In the following methods you will find a specific instructions about
    every method input and output.

    Make sure you follow them, wrong input may cause the program to collapse.
    """

    def __init__(self, location, speed, angle, radius):
        """
        This is the constructor of the spaceships.
        :param x_location: the spaceship location on the x axis a float.
        :param y_location: the spaceship location on the y axis a float.
        :param x_spd: the spaceship speed on the x axis a float.
        :param y_spd: the spaceship speed on the y axis a float.
        :param angle: the spaceship heading angle a float within [0,360].
        :param radius: the spaceship radius a float.
        """
        self.__angle = angle
        self.__speed = speed
        self.__location = location
        self.__radius = radius

    def get_drawing_param(self):
        """
        This method returns the parameters needed to draw the ship.
        :return: a list.
        """
        return [self.__location[0], self.__location[1], self.__angle]

    def move_ship(self, min_x, max_x, min_y, max_y):
        """
        This method move th ship according to it speed.
        :param min_x: the minimum x location possible a float.
        :param max_x: the maximum x location possible a float.
        :param min_y: the minimum y location possible a float.
        :param max_y: the maximum x location possible a float.
        :return: None.
        """
        prev_x_spd = self.__speed[0]
        prev_x_lct = self.__location[0]
        prev_y_spd = self.__speed[1]
        prev_y_lct = self.__location[1]

        x_spot = min_x + (prev_x_lct + prev_x_spd - min_x) % (max_x - min_x)
        y_spot = min_y + (prev_y_lct + prev_y_spd - min_y) % (max_y - min_y)
        self.set_location(x_spot, y_spot)  # setting the location

    def set_location(self, new_x, new_y):
        """
        This method sets the spaceship location.
        :param new_x: the new x location a float.
        :param new_y: the new x location a float.
        :return: None
        """
        self.__location = (new_x, new_y)

    def rotate(self, direction):
        """
        This method rotate the spaceship in a given direction.
        :param direction: a move-key 'l' or 'r'.
        :return: None
        """
        if direction == LEFT:
            new_angle = (self.__angle + 7) % CIRCLE
            self.__angle = new_angle

        if direction == RIGHT:
            new_angle = (self.__angle - 7) % CIRCLE
            self.__angle = new_angle

    def get_angle(self):
        """
        This method returns the spaceship angle.
        :return: a float within [0,360].
        """
        return self.__angle

    def update_spd(self):
        """
        This method updates the spaceship speed.
        :return: None
        """
        angle = math.radians(self.__angle)
        x = self.__speed[0] + math.cos(angle)
        y = self.__speed[1] + math.sin(angle)
        self.__speed = (x, y)

    def get_radius(self):
        """
        This method returns the radius of the spaceship.
        :return: a float representing the spaceship radius.
        """
        return self.__radius

    def get_location(self):
        """
        This method returns the spaceship location.
        :return: a tuple  of floats representing the location on th axises.
        """

        return self.__location

    def get_speed(self):
        """
        This method returns the spaceship speed.
        :return: a tuple of floats representing the speed.
        """
        return self.__speed
