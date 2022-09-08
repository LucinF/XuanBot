

import nonebot
from nonebot import  on_command
from nonebot.adapters.onebot.v11 import Bot,MessageSegment, ActionFailed, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from .data_source import get_live_status_list
from .model import LiveInfo
from nonebot.log import logger
import xuanbot.utils.database as Database

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText,EventPlainText

# uid_temp = '11475378'
# group = '224256871'
live_statu = {}

live = on_command("live", aliases={'live'}, priority=3,permission=SUPERUSER)

@live.handle()
async def live_handle(matcher: Matcher, event:GroupMessageEvent,args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg('live',args)
        # if plain_text[0].isdigit():
        #     live_table = Database.Live_subscribe(uid=plain_text[0],subscriber_id=str(event.group_id))
        #     await live_table.insert()
        #     await matcher.finish(f'uid:{plain_text[0]} insert success.')


@live.got('live',prompt='Give me uid who you wanna to push')
async def live_got(matcher: Matcher, event:GroupMessageEvent,uid:str=ArgPlainText('live')):
    list = uid.strip().split()
    if list and list[0].isdigit():
        uid = list[0]
        live_table = Database.Live_subscribe(uid=uid,subscriber_id=str(event.group_id))
        await live_table.insert()
        await matcher.finish(f'uid:{uid} insert success.')
    else:
        await matcher.finish(f'the parm is invalid.')



@scheduler.scheduled_job("interval", seconds=10, id="live_push")
async def live_push():
#     result = await get_live_status_list([uid])
#     result = result[uid]
#     statu = 0 if result['live_status'] == 2 else result['live_status']
#     logger.info(f"uid:{uid} info:{statu}")
#     #print(result)
#     if statu != live_statu[uid] and statu == 1:
#         temp = LiveInfo(uid=uid,result=result)
#         msg = temp.live_at_all()
#         bot = nonebot.get_bot()
#         try:
#                 await bot.call_api("send_msg", **{
#                     "message": msg,
#                     "group_id": group
#                 })
#                 #pass
#         except ActionFailed as e:
#                 print(e)
#     live_statu[uid] = statu

    #logger.info('start')
    uid_result =await Database.Live_subscribe(uid=' ',subscriber_id=' ').select_uids()
    live_statu_dict = await get_live_status_list(uid_result.result)
    if not live_statu_dict:
        logger.info(uid_result)
        return
    for uid,result in live_statu_dict.items():
        if uid not in live_statu:
            live_statu[uid] = 1
        statu = 0 if result['live_status'] == 2 else result['live_status']
        logger.info(f"uid:{uid} info:{statu}")
        if statu != live_statu[uid] and statu == 1:
            temp = LiveInfo(uid=uid,result=result)
            msg = temp.live_at_all()
            bot = nonebot.get_bot()
            group_result = await Database.Live_subscribe(uid=uid,subscriber_id=' ').select_subscribe()
            try:
                    for group in group_result.result:
                        await bot.call_api("send_msg", **{
                        "message": msg,
                        "group_id": group
                        })
            except ActionFailed as e:
                    print(e)
        live_statu[uid] = statu
