
import random
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.permission import SUPERUSER

from nonebot import on_message
from nonebot.matcher import Matcher

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

copy_msg = on_message(priority=5,permission=SUPERUSER)

@copy_msg.handle()
async def copy_func(matcher:Matcher,event:GroupMessageEvent):
    result = random.uniform(0,200)
    if  result<=10 :
        await matcher.finish(event.get_message())