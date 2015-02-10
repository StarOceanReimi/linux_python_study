from PIL import Image, ImageDraw, ImageFont

base = Image.open('hancock_1.jpg').convert('RGBA')

txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

d = ImageDraw.Draw(txt)

d.text((10, 10), "I Love Boa Hancock", font=fnt, fill=(255, 0, 0, 255))

out = Image.alpha_composite(base, txt)

out.show()
