#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from config.app_config import PlayWindow
from config.app_config import Window
from piece_module.piece import Piece
from piece_module.piece_factory import PieceFactory


class Surface:
    """画面クラス
    """
    def __init__(self):
        self.__surface = pygame.display.set_mode(
            (Window.WIDTH, Window.HEIGHT))

    @staticmethod
    def create_grid(locked_pos=None) -> list:
        """グリッド作成

        Args:
            locked_pos (dict): ピースが存在する座標を格納した値（辞書型）

        Returns:
            grid (list): グリッド情報を格納したリスト

        """

        if locked_pos is None:
            locked_pos = {}
        # ベースとなるグリッドの作成
        # 20 x 10 のリスト作成 [[(0, 0, 0),...], ...[...,(0, 0, 0)]]
        grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

        # グリッドをループする
        # グリッドの要素数（20）でループ
        for i in range(len(grid)):
            # グリッドの入れ子の要素数（10）でループ
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    # 変数locked_posに値が存在する場合
                    # 作成しているgridに存在するピースの情報を反映する
                    c = locked_pos[(j, i)]
                    grid[i][j] = c
        return grid

    @staticmethod
    def is_valid_space(shape: Piece, grid: list) -> bool:
        """有効なスペースがあるか確認する

        Args:
            shape (Piece): ピースオブジェクト
            grid  (list) : グリッド情報が格納されたリスト

        Returns:
            bool: スペースがある場合にはTrue、ない場合にはFalse

        """
        # gridの要素の中に(0, 0, 0)が含まれる（＝ブロックがない）場合に、
        # 空いてるスペースの座標をリストに追加
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]
                        for i in range(20)]

        # [(x, y), (x1, y1), ..., (xn, yn)]を以下のように変換
        # [x, y, x1, y1, ..., xn, yn]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        # 引数のshapeを座標系のリストにフォーマット
        formatted = PieceFactory.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                # 有効なスペースにピースの座標が存在しない場合
                if pos[1] > -1:
                    # ピースのy座標が-1より大きい場合
                    return False
        return True

    @staticmethod
    def clear_rows(grid: list, locked_pos: dict) -> int:
        """揃った行を削除する

        Args:
            grid       (list): グリッド情報が格納されたリスト
            locked_pos (dict): ピースが存在する座標を格納した値（辞書型）

        """
        # 削除する行数を初期化
        inc = 0
        # 逆順にリストをループする
        # gridの要素数 -> -1 まで（step: -1）
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            if (0, 0, 0) not in row:
                # 行の要素に(0, 0, 0)が存在しない場合（=行が揃っている場合）\
                # 削除する行数を加算
                inc += 1
                # 削除対象の行番号を代入
                ind = i
                for j in range(len(row)):
                    try:
                        # 特定の座標の値(キーを指定）削除
                        del locked_pos[(j, i)]
                    except Exception as e:
                        continue
        if inc > 0:
            # 削除した行があった場合
            for key in sorted(list(locked_pos), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    new_key = (x, y + inc)
                    locked_pos[new_key] = locked_pos.pop(key)
        return inc

    @staticmethod
    def is_over_top(locked_pos):
        for pos in locked_pos:
            if pos[1] < 1:
                return True
        return False

    def draw_window(self, grid: list) -> None:
        """画面を描画する

        Args:
            grid (list): グリッド情報が格納されたリスト

        """
        # 画面を白で塗りつぶす
        self.__surface.fill((0, 0, 0))

        # 表示するフォント情報設定
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))

        # 文字ラベルを画面上に描画
        self.__surface.blit(label, (PlayWindow.TOP_LEFT_X +
                                    PlayWindow.WIDTH / 2 -
                                    (label.get_width() / 2), 30))

        # グリッドの外側の要素数（20）でループ
        for i in range(len(grid)):
            # グリッドの内側の要素数（10）でループ
            for j in range(len(grid[i])):
                # グリッド情報を元に描画
                pygame.draw.rect(self.__surface, grid[i][j],
                                 (PlayWindow.TOP_LEFT_X +
                                  j * PlayWindow.BLOCK_SIZE,
                                  PlayWindow.TOP_LEFT_Y +
                                  i * PlayWindow.BLOCK_SIZE,
                                  PlayWindow.BLOCK_SIZE,
                                  PlayWindow.BLOCK_SIZE), 0)

        # play_windowの外枠を赤線で描画
        pygame.draw.rect(self.__surface, (255, 0, 0),
                         (PlayWindow.TOP_LEFT_X,
                          PlayWindow.TOP_LEFT_Y,
                          PlayWindow.WIDTH, PlayWindow.HEIGHT), 4)

        self.__draw_grid(grid)

        # pygame.display.update()

    def draw_next_shape(self, shape: Piece) -> None:
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))

        sx = PlayWindow.TOP_LEFT_X + PlayWindow.WIDTH + 50
        sy = PlayWindow.TOP_LEFT_Y + PlayWindow.HEIGHT / 2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.__surface, shape.color,
                                     (sx + j*30, sy + i*30, 30, 30), 0)
        self.__surface.blit(label,(sx + 10, sy - 30))

    def draw_score(self, point: int) -> None:
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(f'Score: {point*100}', 1, (255, 255, 255))

        sx = PlayWindow.TOP_LEFT_X + PlayWindow.WIDTH + 50
        sy = PlayWindow.TOP_LEFT_Y + PlayWindow.HEIGHT / 1.5
        # format = shape.shape[shape.rotation % len(shape.shape)]

        # for i, line in enumerate(format):
        #     row = list(line)
        #     for j, column in enumerate(row):
        #         if column == '0':
        #             pygame.draw.rect(self.__surface, shape.color,
        #                              (sx + j*30, sy + i*30, 30, 30), 0)
        self.__surface.blit(label, (sx + 10, sy - 10))

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
