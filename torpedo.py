import math
X = 'x'
Y = 'y'
RADIUS = 4


class Torpedo:
    def __init__(self, location, speed, angle, life_span):
        x_spd = self.speed_calculation(speed[0], angle, X)
        y_spd = self.speed_calculation(speed[1], angle, Y)
        self.__x_params = [location[0], x_spd]
        self.__y_params = [location[1], y_spd]
        self.__angle = angle
        self.__radius = RADIUS
        self.__life_span = life_span

    @staticmethod
    def speed_calculation(speed, angle, axis):
        rdangle = math.radians(angle)
        if axis == X:
            new_spd = speed + (2 * math.cos(rdangle))
            return new_spd
        if axis == Y:
            new_spd = speed + (2 * math.sin(rdangle))
            return new_spd

    def get_drawing_param(self):
        lst = [self.__x_params[0], self.__y_params[0], self.__angle]
        return lst

    def get_location(self):
        x_loct = self.__x_params[0]
        y_loct = self.__y_params[0]

        return x_loct, y_loct

    def move_torp(self, min_x, max_x, min_y, max_y):
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
        return self.__radius

    def get_speed(self):
        x_spd = self.__x_params[1]
        y_spd = self.__y_params[1]

        return x_spd, y_spd

    def reduce_span(self):
        self.__life_span -= 1
        return self.__life_span


