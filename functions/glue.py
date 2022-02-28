# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/telePicCutBot
File Name:     glue.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/02/27
Software:      Vscode
'''

'''Some Glue Function Common Used'''
import logging
import yaml

def show_progress_upload(current, total):
    # print('Uploaded', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))
    logging.info(f"Uploaded {current} out of {total} bytes: {(current/total): .2%}")

def show_progress_download(current, total):
    # print('Download', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))
    logging.info(f"Downloaded {current} out of {total} bytes: {(current/total): .2%}")


# make config globally
def read_config(path):
    global config
    with open(path, "r", encoding="utf-8") as c:
        config = yaml.load(c, yaml.FullLoader)

def get_config():
    return config


# init logger
def set_logger(config):
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    if config['log']['level'] == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    elif config['log']['level'] == 'INFO':
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    elif config['log']['level'] == 'ERROR':
        logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)