from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import string
import os
from . import settings
def rndColor():
    return (random.randint(32,127),
            random.randint(32,127),
            random.randint(32,127))
def rndColor1():
    return (random.randint(64,255),
            random.randint(64,255),
            random.randint(64,255))
def rndChr():
    return chr(random.randint(65,90))
def getrand(num,many):
    for x in range(many):
        s = ''
        for i in range(num):
            n = random.randint(1,2)
            if n == 1:
                m = random.randint(0,9)
                s += str(m)
            else:
                m = str(random.choice(string.ascii_letters))
                s += str(m)
        return s
def shengcheng():
    ss = ''
    sss = ''
    width = 60*4
    height = 60
    image = Image.new('RGB',(width,height),(0,0,0))
    #创建数字对象
    font = ImageFont.truetype('arial.ttf',36)
    draw = ImageDraw.Draw(image)
    for x in range(width):
        for y in range(height):
            draw.point((x,y),fill=rndColor1())
    for t in range(4):
        s = getrand(1, 4)
        ss+=s
        draw.text((60*t+10,10),s,font=font,fill=rndColor())

    image = image.filter(ImageFilter.BLUR)
    filepath = os.path.join(settings.MEDIA_ROOT,'yanzhengma.jpg')
    image.save(filepath,'jpeg')
    for n in ss:
        if "a" <= n <= "z":
            sss += n
        elif "A" <= n <= "Z":
            sss+=(n.lower())
        else:
            sss+=(n)
    return sss


