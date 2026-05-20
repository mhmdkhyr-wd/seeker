#!/usr/bin/env python3
import os
import utils

from colorama import init

init()
from colorama import Fore

R = Fore.RED
G = Fore.GREEN
C = Fore.CYAN
Y = Fore.YELLOW
W = Fore.RESET

redirect = os.getenv('REDIRECT')

if redirect is None:
    redirect = input(G + '[+]' + C + ' Enter GDrive File URL : ' + W)
else:
    utils.print(f'{G}[+] {C}GDrive File URL :{W} '+redirect)
        
with open('template/gdrive/index_temp.html', 'r',encoding='utf-8') as temp_index:
    temp_index_data = temp_index.read()
    temp_index_data = temp_index_data.replace('REDIRECT_URL', redirect)
    if os.getenv("DEBUG_HTTP"):
        temp_index_data = temp_index_data.replace('window.location = "https:" + restOfUrl;', '')

with open('template/gdrive/index.html', 'w',encoding='utf-8') as updated_index:
    updated_index.write(temp_index_data)