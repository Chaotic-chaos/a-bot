# -*- coding: utf-8 -*-
'''
Project:       /root/projects/Pythons/telePicCutBot
File Name:     login.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/02/27
Software:      Vscode
'''

'''Sign in and return a Bot(sync)'''
from telethon import TelegramClient


def login(config):
    global bot
    bot = TelegramClient("bot", api_id=config['bot']['api_id'], api_hash=config['bot']['api_hash'], proxy=config['proxy'])
    # bot.start(bot_token=config['bot']['bot_token'])

    print(bot)

    # bot.idle()

    # return bot

def get_bot():
    return bot


if __name__ == '__main__':
    pass