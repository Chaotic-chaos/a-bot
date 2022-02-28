# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/telePicCutBot
File Name:     main.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/02/27
Software:      Vscode
'''

'''Main Entrence of the whole Bot'''
import logging
import yaml

# Set parameters
from argparse import ArgumentParser
from telethon import events
from functions.glue import get_config, read_config, set_logger

from functions.login import get_bot, login
from handlers.new_messages import new_message_handler



parser = ArgumentParser()

parser.add_argument("--config", "-c", default="./config.yaml", help="Configeration file")

args = parser.parse_args()

if __name__ == '__main__':    
    # Read the configs
    print("Reading Configurations...")
    read_config(args.config)
    config = get_config()

    # Set logger
    set_logger(config=config)

    # login the bot account
    login(config=config)
    bot = get_bot()
    logging.info("Logged in as a bot")

    # add handler: listening all new messages from given chats by config file
    logging.info("Adding New Message handler")
    bot.add_event_handler(new_message_handler, event=events.NewMessage(chats=config["chats"]))


    # start the bot
    logging.info("Bot Started!")
    bot.start(bot_token=config["bot"]["bot_token"])

    # run forever
    bot.run_until_disconnected()
