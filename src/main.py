#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
import random

from config.app_config import Window
from config.app_config import PlayWindow
from piece_module.piece import Piece
from piece_module.piece_factory import PieceFactory
from window.surface import Surface


"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""


class AppMain:

    def __init__(self):
        self.__is_finish = False
        self.__locked_pos = {}
        self.__surface = Surface()
        self.__clock = pygame.time.Clock()
        self.__fall_time = 0
        self.__fall_speed = 0.27
        self.__point = 0
        pygame.font.init()

    def main(self):
        # 画面の描画
        # surface = pygame.display.set_mode((Widow.WIDTH, Widow.HEIGHT))
        # グリッドの作成
        # grid = self.__surface.create_grid(self.__locked_pos)

        # ピースの取得
        current_piece = PieceFactory.get_shape()
        next_piece = PieceFactory.get_shape()

        while self.__is_finish is False:
            # グリッドの作成
            grid = self.__surface.create_grid(self.__locked_pos)
            # 前回tick実行時の差分(ms)を取得し、加算
            self.__fall_time += self.__clock.get_rawtime()
            # クロックオブジェクト更新（戻り値は前回実行時からの差分(ms)）
            self.__clock.tick()
            # ピース変更フラグ初期化
            change_piece = False

            # （落下時間）と（一つのマスを進める落下時間）の比較
            if self.__fall_time / 1000 >= self.__fall_speed:
                # （落下時間）>= (一つのマスを進める落下時間)　の場合
                # 落下時間を初期化（0）
                self.__fall_time = 0
                # ピースを1マス進める
                current_piece.y += 1

                # マスが落下できるスペースの確認
                if not (self.__surface.is_valid_space(current_piece, grid) and
                        current_piece.y > 0):
                    # 進めるマスがないかつピースがグリッド内に存在する場合
                    current_piece.y -= 1
                    # ピース変更フラグを立てる
                    change_piece = True

            # イベントループ
            for event in pygame.event.get():
                # イベントタイプの比較
                if event.type == pygame.QUIT:
                    # 終了イベントを取得した場合
                    self.__is_finish = True

                if event.type == pygame.KEYDOWN:
                    # キープレスイベント取得
                    if event.key == pygame.K_LEFT:
                        # 左カーソルキーの場合
                        current_piece.x -= 1
                        if not (self.__surface.is_valid_space(current_piece,
                                                              grid)):
                            # 進めるマスのスペースが存在しない場合
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        # 右カーソルキーの場合
                        current_piece.x += 1
                        if not (self.__surface.is_valid_space(current_piece,
                                                              grid)):
                            # 進めるマスのスペースが存在しない場合
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        # 下カーソルキーの場合
                        current_piece.y += 1
                        if not (self.__surface.is_valid_space(current_piece,
                                                              grid)):
                            # 進めるマスのスペースが存在しない場合
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        # 上カーソルキーの場合
                        # ローテーションを進める
                        current_piece.rotation += 1
                        if not (self.__surface.is_valid_space(current_piece,
                                                              grid)):
                            # ローテーションできるスペースがない場合
                            # 元のローテーションに戻す
                            current_piece.rotation -= 1

            # ピースの要素をリストに変換
            shape_pos = PieceFactory.convert_shape_format(current_piece)

            # 変数shape_posをループ
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    # ピースのy成分がグリッド内にある場合
                    # ピースの色を指定する
                    grid[y][x] = current_piece.color

            # ピース変更フラグの確認
            if change_piece:
                # 変更フラグが立っている場合
                # 変数shape_posをループ
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    # 変数locked_posにピースの位置情報を格納
                    # {(1, 2): (255, 0, 0), {.....}, ...}
                    self.__locked_pos[p] = current_piece.color
                current_piece = next_piece
                next_piece = PieceFactory.get_shape()
                point = self.__surface.clear_rows(grid, self.__locked_pos)
                self.__point += point

            self.__surface.draw_window(grid)
            self.__surface.draw_next_shape(next_piece)
            self.__surface.draw_score(self.__point)
            pygame.display.update()


if __name__ == '__main__':
    app = AppMain()
    app.main()
