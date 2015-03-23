#!/usr/bin/python
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random

_CODE_STR = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
_CODE_STR_LEN = len(_CODE_STR)
_DEFAULT_FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def _random_code(length):
    code = ''
    for x in xrange(length):
        r_index = random.randint(0, _CODE_STR_LEN-1)
        code += _CODE_STR[r_index]
    return code

def _draw_background(size):
    #White transparent layer
    bg_layer = Image.new('RGBA', size, (255,255,255,0))
    intervene_layer = Image.new('RGBA', size, (150,150,150,40))
    draw_intervene = ImageDraw.Draw(intervene_layer)
    w,h = size
    for y in xrange(0,h,5):
        draw_intervene.line([(0, y), (w, y)], fill='#fff', width=2)
    bg_img = Image.alpha_composite(bg_layer, intervene_layer)
    #bg_img.show()
    return bg_img

def _draw_text_on(image, text):

    colors = ["#f00", "#0f0", "#00f", "#0ff", "#f0f", "#000", "#ff0"]
    c_len = len(colors)
    font = ImageFont.truetype(_DEFAULT_FONT_PATH, 30)
    base = image.convert('RGBA')
    text_layer = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(text_layer)
    i = 0
    w, h = image.size
    t_n = len(text)
    t_w = w / t_n

    for c in text:
        color = random.choice(colors)
        colors.pop(colors.index(color))
        draw.text((i*(t_w)+5, 5), c, font=font, fill=color)
        i+=1
    enhancer = ImageEnhance.Sharpness(text_layer)
    text_layer = enhancer.enhance(0.1)
    img = Image.alpha_composite(text_layer, base)
    img.save('validcode.jpg', 'JPEG')
if __name__ == '__main__':
    img = _draw_background((200, 50))
    _draw_text_on(img, _random_code(5))
