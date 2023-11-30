#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from config.app_config import PlayWindow
from config.app_config import Window
from piece_module.piece import Piece
from piece_module.piece_factory import PieceFactory


class Surface:

    def __init__(self):
        self.__surface = pygame.display.set_mode(
            (Window.WIDTH, Window.HEIGHT))

    @staticmethod
    def create_grid(locked_pos=None) -> list:
        if locked_pos is None:
            locked_pos = {}
        grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j, i)]
                    grid[i][j] = c

        return grid

    @staticmethod
    def is_valid_space(shape: Piece, grid: list) -> bool:
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]
                        for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]
        formatted = PieceFactory.convert_shape_format(shape)
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def draw_window(self, grid: list) -> None:
        self.__surface.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))

        self.__surface.blit(label, (PlayWindow.TOP_LEFT_X +
                                    PlayWindow.WIDTH / 2 -
                                    (label.get_width() / 2), 30))
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(self.__surface, grid[i][j],
                                 (PlayWindow.TOP_LEFT_X +
                                  j * PlayWindow.BLOCK_SIZE,
                                  PlayWindow.TOP_LEFT_Y +
                                  i * PlayWindow.BLOCK_SIZE,
                                  PlayWindow.BLOCK_SIZE,
                                  PlayWindow.BLOCK_SIZE), 0)

        pygame.draw.rect(self.__surface, (255, 0, 0),
                         (PlayWindow.TOP_LEFT_X,
                          PlayWindow.TOP_LEFT_Y,
                          PlayWindow.WIDTH, PlayWindow.HEIGHT), 4)

        self.__draw_grid(grid)

        pygame.display.update()

    def __draw_grid(self, grid: list) -> None:
        for i in range(len(grid)):
            # グリッドの横線
            pygame.draw.line(self.__surface, (128, 128, 128),
                             (PlayWindow.TOP_LEFT_X,
                              PlayWindow.TOP_LEFT_Y +
                              i * PlayWindow.BLOCK_SIZE),
                             (PlayWindow.TOP_LEFT_X + PlayWindow.WIDTH,
                              PlayWindow.TOP_LEFT_Y +
                              i * PlayWindow.BLOCK_SIZE))
            for j in range(len(grid[i])):
                # グリッドの縦線
                pygame.draw.line(self.__surface, (128, 128, 128),
                                 (PlayWindow.TOP_LEFT_X +
                                  j * PlayWindow.BLOCK_SIZE,
                                  PlayWindow.TOP_LEFT_Y),
                                 (PlayWindow.TOP_LEFT_X +
                                  j * PlayWindow.BLOCK_SIZE,
                                  PlayWindow.TOP_LEFT_Y +
                                  PlayWindow.HEIGHT))


if __name__ == '__main__':
    pass
