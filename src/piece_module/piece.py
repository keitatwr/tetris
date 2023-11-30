#!/usr/bin/env python
# -*- coding: utf-8 -*-


from piece_module.piece_element import PieceElement


class Piece:

    def __init__(self, x, y, shape):
        self.__x = x
        self.__y = y
        self.__shape = shape
        self.__color = PieceElement.COLORS[
            PieceElement.SHAPE_LIST.index(shape)]
        self.__rotation = 0

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def shape(self):
        return self.__shape

    @shape.setter
    def shape(self, shape):
        self.__shape = shape

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, rotation):
        self.__rotation = rotation


if __name__ == '__main__':
    pass
