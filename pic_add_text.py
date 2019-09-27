# coding:utf-8
# author:ls
import time, datetime, json, re, os, sys, random, shutil
from PIL import Image, ImageDraw, ImageFont
import pygame
import requests
import logging


logging.basicConfig(level=logging.INFO, filename='/data/workspace/pic_add_text/add_text.log', datefmt='%Y/%m/%d %H:%M:%S', format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)


def add_text(post_id: str, text: str, size: int, color: tuple, location: int, pic_path: str, font: str, background: int,background_color: tuple, lucency: float, *args, **kwargs):
    pygame.init()  # 初始化
    pic = requests.get(pic_path, timeout=3)
    logging.info(pic.status_code)
    with open(f'/data/workspace/pic_add_text/{post_id}.jpg', 'wb') as f:  # 下载目标图片并保存
        f.write(pic.content)
    my_font = pygame.font.FontType(font, size)  # 设置字体和大小
    name_surface = my_font.render(text, True, color)  # 添加文字和字体颜色
    pygame.image.save(name_surface, f"/data/workspace/pic_add_text/{post_id}_text.png")  # 生成无背景文字图片
    base_img = Image.open(f'/data/workspace/pic_add_text/{post_id}.jpg')  # 打开目标图片
    base_img = base_img.convert("RGBA")  # 格式化图片
    os.remove(f'/data/workspace/pic_add_text/{post_id}.jpg')  # 删除目标图片
    base_width, base_height = base_img.size  # 获取目标图片的宽和高
    region = Image.open(f"/data/workspace/pic_add_text/{post_id}_text.png")  # 打开无背景图片
    os.remove(f"/data/workspace/pic_add_text/{post_id}_text.png")  # 删除无背景图片
    region = region.convert("RGBA")  # 格式化图片
    region_width, region_height = region.size  # 获取无背景图片的高宽
    if background:
        im = Image.new('RGBA', (base_width, region.size[1]), background_color)
        transparent = int(250 * lucency)
        mask = Image.new('L', im.size, color=transparent)
        im.putalpha(mask)

    if base_height / base_width > 1.33:
        new_base_height = base_width * 1.33
        if location == 1:
            box = (int(base_width / 2 - region_width / 2), int((base_height-new_base_height)//2+new_base_height//10*1), int(base_width / 2 - region_width / 2) + region_width, int((base_height-new_base_height)//2+new_base_height//10*1)+region_height)
            im_box = (0, int((base_height-new_base_height)//2+new_base_height//10*1), base_width, int((base_height-new_base_height)//2+new_base_height//10*1)+region_height)
        elif location == 3:
            box = (int(base_width / 2 - region_width / 2), int((base_height-new_base_height)//2+new_base_height//10*9-region_height), int(base_width / 2 - region_width / 2) + region_width, int((base_height-new_base_height)//2+new_base_height//10*9))
            im_box = (0, int((base_height-new_base_height)//2+new_base_height//10*9-region_height), base_width, int((base_height-new_base_height)//2+new_base_height//10*9))
        else:
            box = (int(base_width / 2 - region_width / 2), int((base_height-new_base_height)//2+new_base_height//2-region_height/2), int(base_width / 2 - region_width / 2) + region_width, int((base_height-new_base_height)/2+new_base_height//2-region_height/2)+region_height)
            im_box = (0, int((base_height-new_base_height)//2+new_base_height//2-region_height/2), base_width, int((base_height-new_base_height)/2+new_base_height//2-region_height/2)+region_height)

        if background:
            base_img.paste(im, im_box, mask=im)

        base_img.paste(region, box, mask=region)
        base_img = base_img.convert("RGB")
        if all(base_img.size):
            base_img.save(f'/data/workspace/pic_add_text/text_pic/{post_id}.jpg')
            print(f'/data/workspace/pic_add_text/text_pic/{post_id}.jpg')
        else:raise

    elif base_height / base_width < 1:
        new_base_width = base_height
        if location == 1:
            box = (int(base_width / 2 - region_width / 2), int(base_height/10*1), int(base_width / 2 - region_width / 2)+region_width, int(base_height/10*1+region_height))
            im_box = (0, int(base_height/10*1), base_width, int(base_height/10*1+region_height))
        elif location == 3:
            box = (int(base_width / 2 - region_width / 2), int(base_height/10*9)-region_height, int(base_width / 2 - region_width / 2) + region_width, int(base_height/10*9))
            im_box = (0, int(base_height/10*9)-region_height, base_width, int(base_height/10*9))
        else:
            box = (int(base_width / 2 - region_width / 2), int(base_height/2-region_height/2), int(base_width / 2 - region_width / 2)+region_width, int(base_height/2-region_height/2+region_height))
            im_box = (0, int(base_height/2-region_height/2), base_width, int(base_height/2-region_height/2+region_height))

        if background:
            base_img.paste(im, im_box, mask=im)

        base_img.paste(region, box, mask=region)
        base_img = base_img.convert("RGB")
        if all(base_img.size):
            base_img.save(f'/data/workspace/pic_add_text/text_pic/{post_id}.jpg')
            print(f'/data/workspace/pic_add_text/text_pic/{post_id}.jpg')
        else:raise
    else:
        if location == 1:
            box = (int(base_width / 2 - region_width / 2), int(base_height//10*1), int(base_width / 2 - region_width / 2) + region_width, int(base_height//10*1+region_height))
            im_box = (0, int(base_height//10*1), base_width, int(base_height//10*1+region_height))
        elif location == 3:
            box = (int(base_width / 2 - region_width / 2), int(base_height//10*9)-region_height, int(base_width / 2 - region_width / 2) + region_width, int(base_height//10*9))
            im_box = (0, int(base_height//10*9)-region_height, base_width, int(base_height//10*9))
        else:
            box = (int(base_width / 2 - region_width / 2), int(base_height/2-region_height/2), int(base_width / 2 - region_width / 2) + region_width, int(base_height/2-region_height/2+region_height))
            im_box = (0, int(base_height/2-region_height/2), base_width, int(base_height/2-region_height/2+region_height))

        if background:
            base_img.paste(im, im_box, mask=im)

        base_img.paste(region, box, mask=region)
        base_img = base_img.convert("RGB")
        if all(base_img.size):
            base_img.save(f'/data/workspace/pic_add_text/text_pic/{post_id}.jpg')
            print(f'/data/workspace/pic_add_text/text_pic/{post_id}.jpg')
        else:raise

params = json.loads(sys.argv[1])
logging.info(params)
post_id = params['impression_id']
text = params['text']
size = params['size']
#color = [int(i.strip()) for i in params['color'].split(',')]
color = [int(i.strip()) for i in re.sub('rgb|\(|\)', '', params['color']).split(',')]
location = params['location']
font = '/data/workspace/pic_add_text/my_font/'+params['font']
pic_path = params['pic_path']
background = params['background']
lucency = params['lucency']
#background_color = [int(i.strip()) for i in params['background_color'].split(',')]
background_color = [int(i.strip()) for i in re.sub('rgb|\(|\)', '', params['background_color']).split(',')]
try:
    add_text(background_color=tuple(background_color), post_id=str(post_id), text=str(text), size=int(size), color=tuple(color), location=int(location), pic_path=str(pic_path), font=str(font), background=int(background), lucency=float(lucency))
except Exception as e:
    try:
        time.sleep(0.5)
        add_text(background_color=tuple(background_color), post_id=str(post_id), text=str(text), size=int(size), color=tuple(color), location=int(location), pic_path=str(pic_path), font=str(font), background=int(background), lucency=float(lucency))
    except:
        logging.error(e)
        print(pic_path)

