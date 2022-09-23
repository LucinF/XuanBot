'''
Description: 
Autor: LucinF
Date: 2022-09-16 14:57:39
LastEditors: LucinF
LastEditTime: 2022-09-23 23:03:37
'''
from nonebot import  on_command,get_bot
from nonebot.adapters.onebot.v11 import ActionFailed, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from .data_source import Live_status
from .model import LiveInfo
from nonebot.log import logger
from xuanbot.utils.database import Live_subscribe

from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, ArgPlainText


live_statu = {}

live = on_command("live", aliases={'live'}, priority=3,permission=SUPERUSER)

@live.handle()
async def live_handle(matcher: Matcher,args: Message = CommandArg()):
    plain_text = args.extract_plain_text().strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg('live',args)


@live.got('live',prompt='Give me uid who you wanna to push')
async def live_got(matcher: Matcher, event:GroupMessageEvent,uid:str=ArgPlainText('live')):
    list = uid.strip().split()
    matcher.stop_propagation()
    if list and list[0].isdigit():
        uid = list[0]
        result = await Live_status(uids=[uid]).get_live_status_list()
        if result.error is False and result.result != []:
            live_table = Live_subscribe(uid=uid,subscriber_id=str(event.group_id))
            intResult = await live_table.insert()
            if intResult.error is False:
                await matcher.finish(f'uid:{uid} insert success.')
            else:
                await matcher.finish(f'The uid:{uid} insert failed because of {intResult.info}.')
        else:
            await matcher.finish(f'the uper(uid:{uid}) is non-existen.')
    else:
        await matcher.finish(f'the parm is invalid.')


live_delete = on_command('live_delete', priority=3,permission=SUPERUSER)

@live_delete.handle()
async def delete_handle(matcher:Matcher,args=CommandArg()):
    plain_text = args.extract_plain_text().strip()
    if plain_text:
        matcher.set_arg('delete',args)

@live_delete.got('delete',prompt="Who don't you want to follow?")
async def delete_got(matcher:Matcher,event:GroupMessageEvent,uid:str=ArgPlainText('delete')):
    list = uid.strip().split()
    matcher.stop_propagation()
    if list and list[0].isdigit():
        uid = list[0]
        live_table = Live_subscribe(uid=uid,subscriber_id=str(event.group_id))
        intResult = await live_table.delete()
        if intResult.error is False:
            result = await live_table.select_subscribe()
            if result.error == False and result.result == []:
                live_statu.pop(uid,0)
            await matcher.finish(f'uid:{uid} delete success.')
        else:
            await matcher.finish(f'The uid:{uid} delete failed because of {intResult.info},result={intResult.result}.')
    else:
        await matcher.finish(f'the parm is invalid.')



@scheduler.scheduled_job("interval", seconds=60, id="live_push")
async def live_push():
    table = Live_subscribe(uid=' ',subscriber_id=' ')
    uid_result =await table.select_uids()
    del table
    if(uid_result.error == True):
        logger.error(uid_result.info)
        return
    try:
        dictresult = await Live_status(uids=uid_result.result).get_live_status_list()
    except Exception as e:
        logger.error(repr(e))
        return 
    if dictresult.error or dictresult.error is False and dictresult.result == []:
        logger.info(repr(dictresult))
        return
    for uid,result in dictresult.result.items():
        if uid not in live_statu:
            live_statu[uid] = 1
        statu = 0 if result['live_status'] == 2 else result['live_status']
        logger.info(f"uid:{uid} info:{statu}")
        if statu != live_statu[uid] and statu == 1:
            temp = LiveInfo(uid=uid,result=result)
            msg = temp.live_at_all()
            bot = get_bot()
            group_result = await Live_subscribe(uid=uid,subscriber_id=' ').select_subscribe()
            try:
                    for group in group_result.result:
                        await bot.call_api("send_msg", **{
                        "message": msg,
                        "group_id": group
                        })
            except ActionFailed as e:
                    print(e)
        live_statu[uid] = statu
