#!/usr/bin/python

from PIL import Image, ImageDraw, ImageFont, ImageColor
import logging
logging.basicConfig(level=logging.INFO)

class ImageText(object):

  _DEFAULT_FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
  _DEFAULT_FONT_SIZE = 18
  def __init__(self, text, **kw):
    self._text = text
    self._font = 'font' in kw and kw['font'] or \
                 ImageFont.truetype(ImageText._DEFAULT_FONT_PATH, \
                 ImageText._DEFAULT_FONT_SIZE)
    self._color = 'color' in kw and kw['color'] or (0, 0, 0, 255)
    self._pos = 'position' in kw and kw['position'] or (0, 0)
  
  @property
  def font(self):
    return self._font

  @property
  def color(self):
    return self._color

  @property
  def text(self):
    return self._text

  @property
  def position(self):
    return self._pos

  def set_font(self, font, font_size=None):
    if not font:
      font = ImageText._DEFAULT_FONT_PATH
    if font_size is None:
      font_size = ImageText._DEFAULT_FONT_SIZE
    if isinstance(font, ImageFont.FreeTypeFont):
      self._font = font
    elif isinstance(font, str):
      self._font = ImageFont.truetype(font, font_size)
    else:
      logging.warning('font was not set successfully. keep default font')
  
  @color.setter
  def color(self, color):
    if isinstance(color, str):
      self._color = ImageColor.getrgb(color)
    elif isinstance(color, tuple):
      self._color = color
    elif isinstance(color, list):
      self._color = tuple(color)
    else:
      logging.warning('color was not set successfully. keep default color')

  @position.setter
  def position(self, pos):
    if isinstance(pos, tuple):
      self._pos = pos
    elif isinstance(pos, list):
      self._pos = tuple(pos)
    elif isinstance(pos, str):
      self._pos = tuple(map(lambda x: int(x.strip()), pos.split(',')))
    else:
      logging.warning('position was not set successfully. keep stay 0,0')
  
  @text.setter
  def text(self, text):
    self._text = text

class ImageTextDrawer(object):
  
  def __init__(self, imgfile):
    self._imgfile = imgfile
    self._texts = []

  def add_text(self, text):
    if not isinstance(text, ImageText):
      self._texts.append(ImageText(text))
    else:
      self._texts.append(text)
  
  def draw(self):
    base = Image.open(self._imgfile).convert('RGBA')
    for t in self._texts:
      new_layer = Image.new('RGBA', base.size, (255, 255, 255, 0))
      draw_context = ImageDraw.Draw(new_layer)
      draw_context.text(t.position, t.text, font=t.font, fill=t.color)
      base = Image.alpha_composite(base, new_layer)
    return base

if __name__ == '__main__':
  text = ImageText('I Love Reimi!')
  text.position = 10,10
  text.set_font('', 40)
  text.color = (0,255,255, 200)
  text1 = ImageText('by qiuli', position=(10, 60))
  text1.set_font('', 20)
  text1.color = (0,255, 200, 200)
  import sys
  args = sys.argv
  for infile in args[1:]:
    drawer = ImageTextDrawer(infile)
    drawer.add_text(text)
    drawer.add_text(text1)
    img = drawer.draw()
    img.save('test.png', 'PNG')
