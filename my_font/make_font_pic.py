# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
import pygame


def f(font):
    print(font)
    pygame.init()  # 初始化
    my_font = pygame.font.FontType(font, 50)  # 设置字体和大小
    name_surface = my_font.render('后台字体', True, (0, 255, 0))  # 添加文字和字体颜色
    pygame.image.save(name_surface, f"../font_pic/{font}.png")  # 生成无背景文字图片


for root, dirs, files in os.walk('/Users/lishuo/spider/workspace/draw_logo/my_font'):
    for font in files:
        if '.py' not in font:
            f(font)
        # if '王汉宗细新宋简.ttf' == font:
        #     f(font)