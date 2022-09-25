'''
Description: 
Autor: LucinF
Date: 2022-08-21 00:07:38
LastEditors: LucinF
LastEditTime: 2022-09-26 00:02:37
'''
import json
import httpx
from xuanbot.utils.result import Result
from pydantic import BaseModel
from typing import List


class Live_status(BaseModel):
    uids:List[str]
    __live_headers = {"Origin": "https://live.bilibili.com", "Accept": "application/json, text/plain, */*",
                "Connection": "close",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "Referer": "https://live.bilibili.com/", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Dest": "empty",
                "DNT": "1", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9",
                "Sec-Fetch-Mode": "cors"}

    __live_url = "https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"

    async def get_live_status_list(self) -> Result.DictResult:
        '''请求B站api返回所有列表中用户的直播信息

        Returns: Result.DictResult

        author: LucinF
        '''
        data = json.dumps({'uids': self.uids})
        async with httpx.AsyncClient() as client:
            response = await client.post(headers=self.__live_headers, url=self.__live_url, data=data)   # type: ignore
            # print(response.json()["data"])
            tempjson = response.json()
            isError = False if tempjson['code'] == 0 else True
            info = f"live api get code:{tempjson['code']},message:{tempjson['message']},msg:{tempjson['msg']}."
            dictdata = tempjson['data']
            return Result.DictResult(error=isError,info=info,result=dictdata)