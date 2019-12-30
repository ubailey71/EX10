import math


class Asteroid:

    def __init__(self, x_location, y_location, x_spd, y_spd, size = 3):
        self.__x_params = [x_location, x_spd]
        self.__y_params = [y_location, y_spd]
        self.__size = size

    def move_asteroid(self, min_x, max_x, min_y, max_y):

        prev_x_spd = self.__x_params[1]
        prev_x_lct = self.__x_params[0]
        prev_y_spd = self.__y_params[1]
        prev_y_lct = self.__y_params[0]

        x_spot = min_x + (prev_x_lct + prev_x_spd - min_x) % (max_x - min_x)
        y_spot = min_y + (prev_y_lct + prev_y_spd - min_y) % (max_y - min_y)
        self.set_location(x_spot, y_spot)

    def set_location(self, new_x, new_y):
        self.__x_params[0] = new_x
        self.__y_params[0] = new_y

    def get_radius(self):
        return (self.__size * 10) - 5

    def get_location(self):
        x_loct = self.__x_params[0]
        y_loct = self.__y_params[0]

        return x_loct, y_loct

    def get_speed(self):
        x_spd = self.__x_params[1]
        y_spd = self.__y_params[1]

        return x_spd,y_spd

    def has_intersection(self, obj):

        rdiusum = self.get_radius() + obj.get_radius()
        ast_x = self.get_location()[0]
        ast_y = self.get_location()[1]

        obj_x = obj.get_location()[0]
        obj_y = obj.get_location()[1]

        x_dist = math.pow(obj_x-ast_x, 2)
        y_dist = math.pow(obj_y-ast_y, 2)
        distance = math.sqrt(x_dist+y_dist)

        if distance <= rdiusum:
            return True

        return False

    def get_size(self):
        return self.__size



