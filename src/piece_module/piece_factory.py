#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from piece_module.piece import Piece
from piece_module.piece_element import PieceElement


class PieceFactory:

    def __init__(self):
        pass

    @staticmethod
    def get_shape() -> Piece:
        return Piece(5, 0, random.choice(PieceElement.SHAPE_LIST))

    @staticmethod
    def convert_shape_format(shape: Piece) -> list:
        positions = []
        # 余り = ローテーション回数 % パターン数
        # 余りがshapeのインデックスになる
        shape_format = shape.shape[shape.rotation % len(shape.shape)]

        # format = ['.....', '..0..', '.00..', '..0..', '.....']
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
        # positions = [(2, 1), (1, 2), (2, 2), (2, 3)]
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
        # positions = [(0, -3), (-1, -2), (0, -2), (0, -1)]
        return positions


if __name__ == '__main__':
    print(PieceFactory.get_shape())
