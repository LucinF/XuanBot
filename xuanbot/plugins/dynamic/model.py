'''
Description: 
Autor: LucinF
Date: 2022-08-11 23:08:50
LastEditors: LucinF
LastEditTime: 2022-10-03 13:36:26
'''

# from pydantic import BaseModel
# import imp
from .data_source import Dynamic_history
from xuanbot.utils.result import Result
import time


def get_timestamp_now() -> int:
    """获取当前秒级的时间戳"""
    return int(time.time())

async def dynamic_list(uid:str,dynamic_id:int,timestamp:int) -> Result.ListResult:
    """获取最新的动态记录列表
        
        Returns Result.ListResult
        result:List[Dict] 
                    [{'dynamic_id':int, 动态id
                    'timestamp':int 动态时间戳
                    'type':int 动态类型
                    'uname':str up主用户名}]
    """
    result = Dynamic_history(uid=int(uid),offset_dynamic_id=0).get_history_list()
    if(result.error):
        return Result.ListResult(error=True,info=result.info,result=[])
    dynaimc_list_temp = []
    while True:
        list = result.result['list']
        if(list[-1]['timestamp']>timestamp and list[-1]['dynamic_id'] != dynamic_id):
            dynaimc_list_temp.extend(list)
            result = Dynamic_history(uid=int(uid),offset_dynamic_id=result.result['next_offset']).get_history_list()
            if(result.error):
                return Result.ListResult(error=True,info=result.info,result=[])
        else:
            for dict_temp in list:
                if dict_temp['timestamp']>timestamp and dict_temp['dynamic_id']!=dynamic_id:
                    dynaimc_list_temp.append(dict_temp)
                else:
                    break
            break
    dynaimc_list_temp.reverse()
    return Result.ListResult(error=False,info='成功获取最新动态列表',result=dynaimc_list_temp)