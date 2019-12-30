import math


class Ship:

    def __init__(self, x_location, y_location, x_spd, y_spd, angle):
        self.__angle = angle
        self.__x_params = [x_location, x_spd]
        self.__y_params = [y_location, y_spd]
        self.__radius = 1

    def get_drawing_param(self):
        lst = [self.__x_params[0], self.__y_params[0], self.__angle]
        return lst

    def move_ship(self, min_x, max_x, min_y, max_y):
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

    def rotate(self, direction):
        if direction == 'l':
            new_angle = (self.__angle + 7) % 360
            self.__angle = new_angle

        if direction == 'r':
            new_angle = (self.__angle - 7) % 360
            self.__angle = new_angle

    def get_angle(self):
        return self.__angle

    def update_spd(self):
        angle = math.radians(self.__angle)
        self.__x_params[1] += math.cos(angle)
        self.__y_params[1] += math.sin(angle)

    def get_radius(self):
        return self.__radius

    def get_location(self):
        x_loct = self.__x_params[0]
        y_loct = self.__y_params[0]

        return x_loct, y_loct

    def get_speed(self):
        return self.__x_params[1], self.__y_params[1]
