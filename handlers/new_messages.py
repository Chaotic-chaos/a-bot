import logging
from math import ceil
import os


from functions.cut_pic import cut_and_reply,cv2_read_bytes
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
        photo_name = "default.jpg"

        # try:
        #     # send type is a photo, must be downloaded
        #     event.media.photo
        #     event.media.document
        # except:
        #     logging.warn("Is not a picture-like media, return anyway")
        #     return

        if not hasattr(event.media, "photo") and not hasattr(event.media, "document"):
            # not a cuttable picture
            logging.warn("Is not a picture-like media, return anyway")
            return

        if hasattr(event.media, "document"):
            if not event.media.document.mime_type.startswith("image/"):
                # not a cuttable picture
                logging.warn("Is not a picture-like media, return anyway")
                return
        
        try:
            photo_name = event.media.document.attributes[1].file_name
        except:
            logging.warn("Cannot get the photo name, using the default name")

        logging.info(f"Photo name is {photo_name}")
        photo_bytes = bytes()
        photo_bytes = await event.download_media(file=bytes, progress_callback=show_progress_download)
        logging.info(f"New media downloaded")
        # print(photo_bytes)

        # check if the image's height bigger than 1000
        config = get_config()
        photo = cv2_read_bytes(photo_bytes)
        length_width_ratio = photo.shape[0]/photo.shape[1]
        if length_width_ratio > config['params']['dynamic_gate']:
            logging.info(f"Cutting and Replying")
            await cut_and_reply(event=event, data=photo_bytes, photo_name=photo_name)
        else:
            # remove the pic and do nothing for now
            logging.warn(f"no need to cut, clean...")
            photo = b'\x00'

