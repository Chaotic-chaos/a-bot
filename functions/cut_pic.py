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
from functions.glue import get_config, show_progress_upload

from functions.login import get_bot

async def cut_and_reply(event, path):
    # get config
    config = get_config()

    pic = cv2.imread(path)
    sub_path = "".join(path.split(".")[:-1])
    if os.path.exists(sub_path):
        # 存在历史同名路径，删除
        shutil.rmtree(sub_path)
    else:
        # 不存在路径，创建
        os.mkdir(sub_path)
    # print(pic.shape)
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
    logging.info(f"Cutting {os.path.split(path)[-1]} for {total_cuts} pieces")
    for cut in range(total_cuts):
        start = cut*step
        cropped = pic[start:start+step, :]

        # saving
        cv2.imwrite(os.path.join(sub_path, f"cut_{cut}.{path.split('.')[-1]}"), cropped)
    
    bot = get_bot()

    # send the pics back
    files = [os.path.join(sub_path, e) for e in os.listdir(sub_path)]
    # sort the pics with file name
    files.sort(key=lambda name: int(os.path.split(name)[-1].split('.')[0][4:]))
    send_limit = config['params']['send_limit']
    logging.info(f"Sending {sub_path} back")
    for send_step in range(ceil(len(files)/send_limit)):
        await bot.send_file(event.chat, file=files[send_step*send_limit:(send_step*send_limit)+send_limit], reply_to=event, progress_callback=show_progress_upload)
    logging.info(f"All done for pic {path}")

    # Delete all the files
    logging.warn("Deleting all the files")
    shutil.rmtree(sub_path)
    os.remove(path)