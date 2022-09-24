'''
Description: 
Autor: LucinF
Date: 2022-08-11 22:45:26
LastEditors: LucinF
LastEditTime: 2022-09-24 22:51:11
'''
#import xuanbot.utils.database
# import imp
# from os import times_result
# from re import T
from time import sleep
from nonebot import  on_command,get_bot,get_driver
from nonebot.adapters.onebot.v11 import ActionFailed, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.log import logger
import xuanbot.utils.database as Database
from .data_source import Dynamic,Dynamic_history
from .model import get_timestamp_now,dynamic_list

from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg, ArgPlainText
from xuanbot.utils.database import Dynamic_subscribe,Dynamic_recode
from asyncio import sleep as asyncsleep
# import os
# from pathlib import Path
# from PIL import Image


# def ImgPath() -> str:
#     path = os.path.dirname(os.path.abspath(__file__))
#     path = path.replace('\\','/')
#     return path

dynamic_command = on_command("dynamic", aliases={'动态'}, priority=3,permission=SUPERUSER)

@dynamic_command.handle()
async def dynamic_command_handle(matcher: Matcher,args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg('dynamic',args)

@dynamic_command.got('dynamic',prompt='Give me uid who you wanna to push')
async def dynamic_got(matcher: Matcher, event:GroupMessageEvent,uid:str=ArgPlainText('dynamic')):
    list = uid.strip().split()
    matcher.stop_propagation()
    if list and list[0].isdigit():
        mid = int(list[0])
        result = Dynamic_history(uid=mid,offset_dynamic_id=0).get_history_list()
        if result.error is False and result.result != []:
            live_table = Dynamic_subscribe(uid=str(mid),subscriber_id=str(event.group_id))
            intResult = await live_table.insert()
            if intResult.error is False:
                #插入表Dynamic_record 当前时间时间戳，动态id:0
                dynamic_table = Dynamic_recode(uid=str(mid),dynamic_id='0',timestamp=str(get_timestamp_now()))
                intResult2 = await dynamic_table.insert()
                if intResult2.error is False:
                    await matcher.finish(f'uid:{mid} insert success.')
                else:
                    await matcher.finish(f'The uid:{mid} insert failed because of {intResult2.info}.')
            else:
                await matcher.finish(f'The uid:{mid} insert failed because of {intResult.info}.')
        else:
            await matcher.finish(f'the uper(uid:{mid}) is non-existen.')
    else:
        await matcher.finish(f'the parm is invalid.')


dynamic_delete = on_command('dynamic_delete', priority=3,permission=SUPERUSER)

@dynamic_delete.handle()
async def dynamic_delete_handle(matcher:Matcher,args=CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        matcher.set_arg('dynamic_delete',args)

@dynamic_delete.got('dynamic_delete',prompt="Who don't you want to read his/her dynamic?")
async def dynamic_delete_got(matcher:Matcher,event:GroupMessageEvent,uid:str=ArgPlainText('dynamic_delete')):
    list = uid.strip().split()
    matcher.stop_propagation()
    if list and list[0].isdigit():
        uid = list[0]
        live_table = Dynamic_subscribe(uid=uid,subscriber_id=str(event.group_id))
        intResult = await live_table.delete()
        if intResult.error is False:
            result = await live_table.select_subscribe()
            if result.error == False and result.result == []:
                # live_statu.pop(uid,0)
                pass
            await matcher.finish(f'uid:{uid} delete success.')
        else:
            await matcher.finish(f'The uid:{uid} delete failed because of {intResult.info},result={intResult.result}.')
    else:
        await matcher.finish(f'the parm is invalid.')



@scheduler.scheduled_job("interval", seconds=120, id="dynamic_push")
async def dynamic_push():
    table = Dynamic_subscribe(uid='',subscriber_id='')
    result= await table.select_uids()
    del table
    if(result.error == True):
        logger.error(result.info)
        return

    for uid in result.result:
        table = Dynamic_recode(uid=uid,dynamic_id='',timestamp='')
        last_dynamic_result = await table.get_last_dynamic()
        if(last_dynamic_result.error == True):
            logger.error(f'获取主播uid:{uid}最新动态时间戳失败,错误信息:\n{last_dynamic_result.info}')
            continue
        logger.info(repr(last_dynamic_result.result))

        #先获取最新的动态，插入表中，再发送消息，避免出问题堆积发送过多延后动态
        dynamic_last_list = await dynamic_list(uid=uid,
                                            dynamic_id=last_dynamic_result.result['dynamic_id'],
                                            timestamp=int(last_dynamic_result.result['timestamp']))
        if(dynamic_last_list.error):
            logger.error(dynamic_last_list.info)
            continue
        for row in dynamic_last_list.result:
            insert_result = await Dynamic_recode(uid=uid,dynamic_id=str(row['dynamic_id']),timestamp=str(row['timestamp'])).insert()
            if(insert_result.error):
                logger.error(insert_result.info)

        table = Dynamic_subscribe(uid=uid,subscriber_id='')
        group_result = await table.select_subscribe()
        if(group_result.error == True):
            logger.error(f'获取主播uid:{uid}群号列表失败,错误信息:\n{group_result.info}')
            continue
        del table

        bot = get_bot()
        for row in dynamic_last_list.result:
            msg = await Dynamic(dynamic_id=row['dynamic_id'],dynamic_type=row['type'],dynamic_user=uid).send_msg()
            for group in group_result.result:
                try:
                    await bot.call_api("send_msg", **{
                        "message": msg.result,
                        "group_id": group
                        })
                except ActionFailed as e:
                    logger.error(e)
        await asyncsleep(10)