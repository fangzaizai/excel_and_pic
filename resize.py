#-*- coding:utf-8 -*-
from PIL import Image

image=Image.open('1.jpg')
image_resized=image.resize((200,200),Image.ANTIALIAS)
image_resized.save('2.jpg')