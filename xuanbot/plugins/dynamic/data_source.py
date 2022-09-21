'''
Description: 
Autor: LucinF
Date: 2022-09-04 15:54:34
LastEditors: LucinF
LastEditTime: 2022-09-21 22:34:25
'''
from tkinter.messagebox import NO
import httpx
from pyppeteer import launch
from pydantic import BaseModel
from xuanbot.utils.result import Result


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
                                'timestamp':int 动态时间戳}]
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
        rdict['list'] = []
        for card in r['data']['cards']:
            rdict['list'].append({'dynamic_id':card['desc']['dynamic_id'],'timestamp':card['desc']['timestamp']})
        return Result.DictResult(error=False, info='',result=rdict)


class Dynamic(BaseModel):
    dynamic_id:int
    __dynamic_url = "https://t.bilibili.com/%s?tab=3" #跳转到对应动态转发界面，不显示评论

    async def get_screenshot(self, retry=3):
        """
            截图B站空间动态主要内容。
            Args:
                retry:int 重连次数,默认为3
            Returns:
                img:bytes|str
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
                await page.setViewport(viewport={"width": 2000, "height": 1080})
                card = await page.querySelector("div[class=bili-dyn-item__main]")
                assert card is not None
                clip = await card.boundingBox()
                assert clip is not None
                image = await page.screenshot(clip=clip, encoding="base64")#,path='%s.png'%(self.dynamic_id))
                assert image is not None
                #await page.screenshot(clip=clip, encoding="binary",path='%s.png'%(self.dynamic_id))
                await browser.close()
                return image
            except Exception as e:
                if i >= retry:
                    await browser.close()
                    raise

