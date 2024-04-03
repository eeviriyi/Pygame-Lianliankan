import os
import random

import numpy as np
import pygame

from algorithm import can_remove


class Config:
    ROW_COUNT = 4
    COLUMN_COUNT = 8
    WIDTH = 200
    HEIGHT = 200
    MARGIN = 5
    SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
    SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
    BG_COLOR = (200, 200, 200)
    RESOURCE_DIR = 'pic'


class ImageButton:
    def __init__(self, screen, imgobj, x, y):
        self.checked = False
        self.checkable = True
        self.screen = screen
        self.imgobj = imgobj
        self.x = x
        self.y = y

    def draw(self):
        if self.checkable:
            if self.checked:
                pygame.draw.rect(self.imgobj, (255, 0, 0), [0, 0, Config.WIDTH, Config.HEIGHT], 4)
            else:
                pygame.draw.rect(self.imgobj, (0, 0, 0), [0, 0, Config.WIDTH, Config.HEIGHT], 4)
            self.screen.blit(self.imgobj, (self.x, self.y))


class MyGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.grid = np.zeros((Config.ROW_COUNT, Config.COLUMN_COUNT), dtype='<U10')

        # 存储两个点击的图片
        self.match_img = {1: {"point"   : None,  # 表示被点图片坐标
                              "pbtn_img": ''  # 被点击按钮对应的图片名
                              }, 2: {"point": None, "pbtn_img": ''}}

        self.clicked_num = 0
        self.all_imgs = None
        self.all_imgs_obj = []
        self.all_imgs_button = []
        self.pos_x = -1
        self.pos_y = -1

        self.load_imgs_obj()
        self.init_imgs_obj()

    def init_imgs_obj(self):
        for row in range(Config.ROW_COUNT):
            for column in range(Config.COLUMN_COUNT):
                x = (Config.MARGIN + Config.WIDTH) * column + Config.MARGIN
                y = (Config.MARGIN + Config.HEIGHT) * row + Config.MARGIN
                obj = ImageButton(self.screen, self.all_imgs_obj[row * Config.COLUMN_COUNT + column], x, y)
                self.grid[row, column] = self.all_imgs[row * Config.COLUMN_COUNT + column]
                self.all_imgs_button.append(obj)
        print(self.grid)

    def load_imgs_obj(self):
        imgs = os.listdir(Config.RESOURCE_DIR)
        self.all_imgs = 2 * imgs.copy()
        random.shuffle(self.all_imgs)
        for img in self.all_imgs:
            img_obj = pygame.image.load(f'{Config.RESOURCE_DIR}/{img}')
            img_obj = pygame.transform.scale(img_obj, (Config.WIDTH, Config.HEIGHT))
            self.all_imgs_obj.append(img_obj)

    def get_img(self, x, y):
        column = int(x // (Config.WIDTH + Config.MARGIN))
        row = int(y // (Config.HEIGHT + Config.MARGIN))
        if row < Config.ROW_COUNT and column < Config.COLUMN_COUNT:
            return (row, column)

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # 鼠标左键检测
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos_x, self.pos_y = pygame.mouse.get_pos()
                if self.clicked_num < 2:
                    point = self.get_img(self.pos_x, self.pos_y)
                    self.clicked_num += 1
                    # 存储按钮对应的图片位置和图片
                    self.match_img[self.clicked_num]["point"] = point
                    self.match_img[self.clicked_num]["pbtn_img"] = self.all_imgs[
                        point[0] * Config.COLUMN_COUNT + point[1]]

                    self.all_imgs_button[
                        self.match_img[1]["point"][0] * Config.COLUMN_COUNT + self.match_img[1]["point"][
                            1]].checked = True

    def judge(self):
        # 判断图片是否配对
        if self.clicked_num == 2:
            # 重置点击按钮次数
            self.clicked_num = 0
            # 判断是否相同
            if self.match_img[1]["pbtn_img"] == self.match_img[2]["pbtn_img"] and can_remove(self.grid,
                                                                                             self.match_img[1]['point'],
                                                                                             self.match_img[2][
                                                                                                 'point']):
                print('匹配成功')
                # 隐藏按钮图片 设置为不可点击
                self.grid[self.match_img[1]["point"][0], self.match_img[1]["point"][
                    1]] = 0
                self.grid[self.match_img[2]["point"][0], self.match_img[2]["point"][
                    1]] = 0
                self.all_imgs_button[self.match_img[1]["point"][0] * Config.COLUMN_COUNT + self.match_img[1]["point"][
                    1]].checkable = False
                self.all_imgs_button[self.match_img[2]["point"][0] * Config.COLUMN_COUNT + self.match_img[2]["point"][
                    1]].checkable = False
                print(self.grid)
            else:
                # 恢复图片原始状态
                print('不匹配')
                print(self.match_img[1]["pbtn_img"] , self.match_img[2]["pbtn_img"],self.match_img[1]["pbtn_img"] == self.match_img[2]["pbtn_img"])
                self.all_imgs_button[
                    self.match_img[1]["point"][0] * Config.COLUMN_COUNT + self.match_img[1]["point"][1]].checked = False
                self.all_imgs_button[
                    self.match_img[2]["point"][0] * Config.COLUMN_COUNT + self.match_img[2]["point"][1]].checked = False
                print(self.grid)

            # 清空已保存的两张图片按钮信息
            self.match_img[1]["point"] = self.match_img[2]["point"] = None
            self.match_img[1]["pbtn_img"] = self.match_img[2]["pbtn_img"] = None


    def on_draw(self):
        self.screen.fill(Config.BG_COLOR)
        for imgbtn in self.all_imgs_button:
            imgbtn.draw()

    def on_update(self):
        self.judge()
        pygame.display.update()
        self.clock.tick(30)

    def run(self):
        while True:
            self.process_event()
            self.on_draw()
            self.on_update()


if __name__ == '__main__':
    game = MyGame()
    game.run()
