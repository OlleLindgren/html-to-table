from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

save_dir = r'C:\Users\lindg\Documents\html-to-table\letter_images'

lower_eng = 'abcdefghijklmnopqrstuvwxyz'
upper_eng = lower_eng.upper()
numeric = '0123456789'

font_dir = r'C:\Windows\Fonts'
font_name = 'arial'

font_file = os.path.join(font_dir, f'{font_name}.ttf')

assert os.path.isfile(font_file)

img_size = (8, 16)
fnt = ImageFont.truetype(font_file, 15)

alphanumeric = lower_eng + upper_eng + numeric

for l in alphanumeric[:3]:

    img = Image.new(mode='1', size=img_size, color=1)

    dr = ImageDraw.Draw(img)
    dr.text((0,0), l, fill=0, font=fnt)

    img.save(os.path.join(save_dir, f'{l}.png'))
    asarr = np.asarray(img)
    
    asarr_float = asarr.astype(np.float)

    print(l)

    print(asarr_float)