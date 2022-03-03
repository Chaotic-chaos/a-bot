# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/telePicCutBot
File Name:     cut_pic.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/02/27
Software:      Vscode
'''

from gc import callbacks
import logging
from math import ceil
import os
import shutil
from sys import path_hooks
import cv2
import numpy as np
import io
from functions.glue import get_config, show_progress_upload

from functions.login import get_bot

async def cut_and_reply(event, data, photo_name):
    # get config
    config = get_config()

    pic = cv2_read_bytes(data)

    # check total cuts
    if config['params']['dynamic']:
        # dynamic cuts
        logging.info("Using dynamic method for the total cuts")
        total_cuts = ceil((pic.shape[0]*config['params']['dynamic_formula']['x'])/(pic.shape[1]*config['params']['dynamic_formula']['y']))
        step = ceil(pic.shape[0]/total_cuts)
    else:
        logging.info("Using static method for the total cuts")
        step = config['params']['cut_step']
        total_cuts = ceil(pic.shape[0]/step)
    logging.info(f"Cutting for {total_cuts} pieces")
    files = []
    for cut in range(total_cuts):
        start = cut*step
        cropped = pic[start:start+step, :]
        imgbytes = cv2.imencode(photo_name, cropped)[1]
        file = io.BytesIO(imgbytes)
        file.name = photo_name
        files.append(file)
    
    bot = get_bot()

    # send the pics back
    send_limit = config['params']['send_limit']
    logging.info(f"Sending pics back")
    for send_step in range(ceil(len(files)/send_limit)):
        await bot.send_file(event.chat, file=files[send_step*send_limit:(send_step*send_limit)+send_limit], reply_to=event, progress_callback=show_progress_upload)
    logging.info(f"All done for pic {photo_name}")

def cv2_read_bytes(photo_bytes):
    return cv2.imdecode(np.fromstring(photo_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)