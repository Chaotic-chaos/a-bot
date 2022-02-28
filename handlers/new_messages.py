import logging
from math import ceil
import os
import shutil
import cv2

from functions.cut_pic import cut_and_reply
from functions.glue import get_config, show_progress_download
from functions.login import login


async def new_message_handler(event):    
    # print("#"*35)
    # print(event)
    # print("-"*45)
    # print(event.media)
    # print("#"*35)

    if event.media is None:
        # there's no media included in this message
        pass
    else:
        '''
        There is two different ways to send pics: Photo or Document
        '''
        logging.info("Reciving a new media")
        try:
            # send type is a photo, must be downloaded
            event.media.photo
        except:
            # check is a picture or not
            if not event.media.document.mime_type.startswith("image"):
                return
        path = await event.download_media(file="media/", progress_callback=show_progress_download)
        logging.info(f"New media downloaded in {path}")
        # print(path)

        # check if the image's height bigger than 1000
        config = get_config()
        length_width_ratio = cv2.imread(path).shape[0]/cv2.imread(path).shape[1]
        if length_width_ratio > config['params']['dynamic_gate']:
            logging.info(f"Cutting and Replying")
            await cut_and_reply(event=event, path=path)
        else:
            # remove the pic and do nothing for now
            logging.warn(f"{os.path.split(path)[-1]} is no need to cut, deleting...")
            os.remove(path=path)