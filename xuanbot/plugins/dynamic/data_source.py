'''
Description: 
Autor: LucinF
Date: 2022-09-04 15:54:34
LastEditors: LucinF
LastEditTime: 2022-10-03 13:35:08
'''
# from asyncio.log import logger
# from cmath import inf
# import imp
# from tkinter import N
from asyncio import exceptions
import httpx
from pyppeteer import launch
from pydantic import BaseModel
from xuanbot.utils.result import Result
from nonebot.adapters.onebot.v11 import Message,MessageSegment


space_headers = {"Origin": "https://space.bilibili.com", "Accept": "application/json, text/plain, */*",
                 "Connection": "close",
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                 "Referer": "https://space.bilibili.com/", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Dest": "empty",
                 "DNT": "1", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9",
                 "Sec-Fetch-Mode": "cors"}


class Dynamic_history(BaseModel):
    """查询用户动态记录
        uid:int 用户uid
        offset_dynamic_id:int 从哪条动态开始,最新的则值为0
    """
    uid:int
    offset_dynamic_id:int
    __history_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'

    def get_history_list(self) -> Result.DictResult:
        """获取动态历史记录，一次最多十二条
        
        Returns Result.DictResult
        result:dict 
                   {'has_more':int 是否有下一页动态记录,1代表有
                    'next_offset':int 下一页动态记录第一条动态的id
                    'list':list
                                [{'dynamic_id':int, 动态id
                                'timestamp':int 动态时间戳
                                'type':int 动态类型
                                'uname':str up主用户名}]
                    }
        """
        result = httpx.get(url=self.__history_url, params= {'host_uid':self.uid, 
                                                            'visitor_uid':self.uid, 
                                                            'offset_dynamic_id':self.offset_dynamic_id,
                                                            'need_top':0})
        r = result.json()
        if r['code'] != 0:
            return Result.DictResult(error=True, info=f"""httpx.get({result.url}) response 
                                                                                  code:{r['code']},
                                                                                  message:{r['message']},
                                                                                  msg:{r['msg']}.""", result={})
        rdict = {'has_more':r['data']['has_more'],
                 'next_offset':r['data']['next_offset']}
        # rdict['list'] = []
        # for card in r['data']['cards']:
        #     rdict['list'].append({'dynamic_id':card['desc']['dynamic_id'],'timestamp':card['desc']['timestamp'],'type':card['desc']['type']})
        try:
            rdict['list'] = [{
                'dynamic_id':card['desc']['dynamic_id'],
                'timestamp':card['desc']['timestamp'],
                'type':card['desc']['type'],
                'uname':card['desc']['user_profile']['info']['uname']
                }
                for card in r['data']['cards']
            ]
            return Result.DictResult(error=False, info='',result=rdict)
        except Exception as e:
            from traceback import format_exc
            return Result.DictResult(error=True,info=f'动态{self.uid}历史动态获取异常,错误原因:\n{format_exc()}',result={})


class Dynamic(BaseModel):
    """动态类型
        dynamic_id:int 动态id
        dynamic_type:int 动态类型
        dynamic_user:str 动态所属用户id
    """
    dynamic_id:int
    dynamic_type:int
    dynamic_user:str

    __dynamic_url = "https://t.bilibili.com/%s?tab=3" #跳转到对应动态转发界面，不显示评论
    # __dynamic_type_dict = {
    #     1:'转发动态',
    #     2:'相册投稿',
    #     4:'文字动态',
    #     8:'视频投稿',
    #     16:'VC小视频投稿',
    #     64:'专栏投稿',
    #     256:'音频投稿',
    #     512:'番剧更新',
    #     2048:'分享歌单',
    # }

    async def get_screenshot(self, retry=3) ->Result.StrResult:
        """
            截图B站空间动态主要内容。
            Args:
                retry:int 重连次数,默认为3
            Returns:
                Result.StrResult

                result:str 执行成功则存储动态截图base64编码,异常存储空字符串
        """
        browser = await launch( args=["--no-sandbox"],dumpio=True,waitUntil="networkidle0", timeout=10000, handleSIGINT=False,
                            handleSIGTERM=False, handleSIGHUP=False)
        assert browser is not None
        page = await browser.newPage()
        assert page is not None
        for i in range(retry + 1):
            try:
                await page.goto(self.__dynamic_url % self.dynamic_id)
                await page.waitForSelector("div[class=bili-dyn-item__main]")
                await page.setViewport(viewport={"width": 2560*5, "height": 1440*5})
                card = await page.querySelector("div[class=bili-dyn-item__main]")
                assert card is not None
                clip = await card.boundingBox()
                assert clip is not None
                """
                encoding='base64' 返回str
                encoding='binary' 返回bytes
                """
                image = await page.screenshot(clip=clip, encoding="base64")#,path='%s.png'%(self.dynamic_id))
                #await page.screenshot(clip=clip, encoding="binary",path='%s.png'%(self.dynamic_id))
                assert image is not None
                await browser.close()
                return Result.StrResult(error=False,info=f'动态{str(self.dynamic_id)}截图成功.',result=image)  # type: ignore
                # return image
            except Exception as e:
                if i >= retry:
                    from traceback import format_exc
                    await browser.close()
                    return Result.StrResult(error=True,info=f'动态{self.dynamic_id}截图异常,错误原因:\n{format_exc()}',result='')
        await browser.close()
        return Result.StrResult(error=True,info=f'未对动态{self.dynamic_id}进行截图操作,retry次数设定:{retry}',result='')

    async def send_msg(self) ->Result.MessageResult:
        """
            返回 xxxx发布xxx动态+动态截图的Onebot.v11.Message类型消息.

            Returns:
                Result.MessageResult

                result:Onebot.v11.Message 执行成功则返回Message类型消息,异常存储None
        """
        MessageDict = {
        1:f'{self.dynamic_user}转发了一条动态:',
        2:f'{self.dynamic_user}发布了一条相册投稿',
        4:f'{self.dynamic_user}发布了一条文字动态',
        8:f'{self.dynamic_user}发布了视频投稿',
        16:f'{self.dynamic_user}发布了VC小视频投稿',
        64:f'{self.dynamic_user}发布了专栏投稿',
        256:f'{self.dynamic_user}发布了音频投稿',
        512:f'{self.dynamic_user}发布了番剧更新',
        2048:f'{self.dynamic_user}分享歌单'
        }
        image_base64 = await self.get_screenshot()
        if(image_base64.error == True):
            return Result.MessageResult(error=True,info=image_base64.info,result=Message(None))
        msg = MessageDict.get(self.dynamic_type,f'{self.dynamic_user}发布了动态.')
        return Result.MessageResult(error=False,info=msg,result=Message(msg+MessageSegment.image(f'base64://{image_base64.result}')))            
        
        
