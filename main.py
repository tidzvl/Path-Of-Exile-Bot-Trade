#
# File: main.py
# Author: TiDz
# Contact: nguyentinvs123@gmail.com
# Created on Thu Jan 16 2025
#
# Description: 
#
# The MIT License (MIT)
# Copyright (c) 2025 TiDz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions: unconditional.
#
# Useage: 
#

import time 
import os
import re
import pyperclip
import pyautogui
from random import randint
from dotenv import load_dotenv
import subprocess
import telegram
import requests

load_dotenv()

stash = {
    '~b/o 4 divine' : 0,
    '~b/o 1.5 divine' : 1,
    '~b/o 0.5 divine' : 2
}

logs_path = os.getenv('PATH_OF_CLIENT')
bot_api = os.getenv('BOT_API')
chat_id = os.getenv('CHAT_ID')
click_path = 'click.exe'

whisper_pattern = re.compile(r'@From (\w+): Hi, I would like to buy your (.+) listed for (.+) in (.+)')
whisper_bulk_pattern = re.compile(r"@From (\w+): Hi, I'd like to buy your (.+) (.+) for my (.+) Orb in Settlers")
join_hideout_pattern = re.compile(r'(\w+) has joined the area.')
trade_accept_pattern = re.compile(r'Trade accepted.')
wait_count = 0
is_pm = False
is_wait = False
is_trade = False

class Bot:
    def __init__(self, api_key, chat_id):
        self.api_key = api_key
        self.chat_id = chat_id
        self.bot = telegram.Bot(api_key)    
        pass

    def Send(self, mess123):
        self.bot.send_message(self.chat_id, text=mess123,
                                parse_mode='Markdown')

    def GetMess(self):
        url = "https://api.telegram.org/bot"+self.api_key+"/getUpdates"
        data = requests.post(url).json()
        data = str(data)
        i = -6
        while i != -999:
            if data[i] == "'":
                i = i + 1
                break
            else:
                i = i - 1
        text = data[i:-5]
        text = bytes(text, 'utf-8')
        text = bytes.decode(text)
        return text

    def wait_whisper(self, line, pattern):
        result = []
        match = pattern.search(line)
        if match:
            self.Send(match.group(0))
            # print(match.group(0))
            print(f'New whisper detected:')
            result.append(match.group(1))
            result.append(match.group(2))
            result.append(match.group(3))
            result.append(match.group(4))
            return result
        return result

    def wait_join(self, line, pattern):
        result = []
        match = pattern.search(line)
        if match:
            return True
        return False

    def invite(self, name):
        clipboard = "/invite " + name
        pyperclip.copy(clipboard)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press("enter")

    def take_item(self):
        pyautogui.press("tab")

    def send_trade(self, name):
        clipboard = "/tradewith " + name
        pyperclip.copy(clipboard)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press("enter")

    def kick_and_ty(self, name):
        clipboard = "/kick " + name
        pyperclip.copy(clipboard)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press("enter")
        clipboard = "@"+name+" ty"
        pyperclip.copy(clipboard)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press("enter")
    
    def afk_off(self):
        clipboard = "/afkoff"
        pyperclip.copy(clipboard)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press("enter")

    def ctrl_click(self, x, y, z):
        with open("logs.txt", "w") as f:
            f.write(f"{x}, {y}, {z}")
        subprocess.call([click_path])

if __name__ == "__main__":
    bot = Bot(bot_api, chat_id)
    current_mess = bot.GetMess()
    current_name = ""
    i = 0
    print(current_mess)
    with open(logs_path, 'r', encoding='utf-8') as file:
        file.seek(0, 2)
        while True:
            i += 1
            line = file.readline()
            if i == 300:
                bot.afk_off()
                i = 0
            if not line:
                time.sleep(1)
                if is_pm and not is_wait:
                    mess = bot.GetMess()
                    if current_mess == mess:
                        time.sleep(0.1)
                    elif mess == "Invite":
                        bot.invite(current_name)
                        print("Invited!")
                        is_pm = False
                        current_mess = "Done!"
                        current_name = ""
                    wait_count += 1
                    if wait_count == 30:
                        print("Cancelled")
                        is_pm = False
                        is_wait = False
                        is_trade = False
                        wait_count = 0
                else:
                    wait_count = 0
                continue

            info_whisper = bot.wait_whisper(line, whisper_pattern)
            if info_whisper and not is_pm:
                is_pm = True
                current_name = info_whisper[0]
            info_whisper = bot.wait_whisper(line, whisper_pattern)
            if info_whisper and not is_pm:
                is_pm = True
                current_name = info_whisper[0]
            # if info_whisper and not is_pm:
            #     is_pm = True
            #     print(info_whisper)
            #     name = info_whisper[0]
            #     price = info_whisper[2]
            #     pos = info_whisper[3]
            #     match = re.search(r'stash tab "([^"]+)"; position: left (\d+), top (\d+)', pos)
            #     tab = match.group(1)
            #     x = match.group(2)
            #     y = match.group(3)
            #     print("command /invite " + name + " sale " + pos + " " + price)
            #     bot.invite(name)
            
            # info_bulk_whisper = bot.wait_whisper(line, whisper_bulk_pattern)
            # if info_bulk_whisper and not is_pm:
            #     is_pm = True
            #     print(info_bulk_whisper)
            #     name = info_bulk_whisper[0]
            #     num = info_bulk_whisper[1]
            #     item = info_bulk_whisper[2]
            #     price = info_bulk_whisper[3]
            #     print("command /invite " + name + " sale " + num + " " + item + " " + price)
            #     bot.invite(name)


            # info_join = bot.wait_join(line, join_hideout_pattern)
            # if info_join and not is_wait:
            #     is_wait = True
            #     print("Join done!")
            #     bot.ctrl_click(int(x)-1, int(y)-1, stash[str(tab)])
            #     #take item
            #     time.sleep(1)
            #     bot.send_trade(name)

            # info_trade = bot.wait_join(line, trade_accept_pattern)
            # if info_trade and not is_trade:
            #     is_trade = True
            #     print("Trade done")
            #     bot.kick_and_ty(name)
            #     is_pm = False
            #     is_wait = False
            #     is_trade = False

            # wait_count += 1
            # if wait_count == 30:
            #     print("Cancelled")
            #     is_pm = False
            #     is_wait = False
            #     is_trade = False
            #     wait_count = 0

                