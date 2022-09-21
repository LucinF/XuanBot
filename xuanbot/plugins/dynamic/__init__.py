'''
Description: 
Autor: LucinF
Date: 2022-08-11 22:45:26
LastEditors: LucinF
LastEditTime: 2022-09-21 22:34:38
'''
#import xuanbot.utils.database
import imp
from tkinter import Image
from .data_source import Dynamic_history
from nonebot import  on_command,get_bot
from nonebot.adapters.onebot.v11 import ActionFailed, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
import xuanbot.utils.database as Database
from .data_source import Dynamic,Dynamic_history

from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageSegment,Message
from nonebot.params import CommandArg, ArgPlainText
# import os
# from pathlib import Path
# from PIL import Image


# def ImgPath() -> str:
#     path = os.path.dirname(os.path.abspath(__file__))
#     path = path.replace('\\','/')
#     return path

# dynamic_command = on_command("dynamic", aliases={'动态'}, priority=3,permission=SUPERUSER)

# @dynamic_command.handle()
# async def dynamic_command_handle(matcher: Matcher,args: Message = CommandArg()):
#     plain_text = args.extract_plain_text().strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
#     logger.info(plain_text)
#     result = await Dynamic(dynamic_id =int(plain_text)).get_screenshot()
#     # cover = 'file:///'+ImgPath()+'/1.jpg'
#     # logger.info(Path('F://bot//XuanBot//xuanbot//plugins//dynamitc//1.png').resolve())
#     # img =Image.open('F://bot//XuanBot//xuanbot//plugins//dynamitc//1.png').resize((1920*2,1080*2))
#     # img.save('F://bot//XuanBot//xuanbot//plugins//dynamitc//1.png')
#     await matcher.finish(' '+MessageSegment.image(f'base64://{result}')) # type: ignore