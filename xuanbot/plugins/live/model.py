'''
Description: 
Autor: LucinF
Date: 2022-08-11 23:08:58
LastEditors: LucinF
LastEditTime: 2022-09-16 20:31:00
'''
from pydantic import BaseModel
from nonebot.adapters.onebot.v11 import MessageSegment,Message
import os


def ImgPath() -> str:
    path = os.path.dirname(os.path.abspath(__file__))+'/img/'
    path = path.replace('\\','/')
    return path

class LiveInfo(BaseModel):
    uid : str
    result : dict

    def live_at_all(self) -> Message:
        ''' 返回@全体成员的主播直播消息

        return {*} Message
        
        author: LucinF
        '''    
        room_id = self.result['short_id'] if self.result['short_id'] else self.result['room_id']
        url = 'https://live.bilibili.com/' + str(room_id)
        name = self.result['uname']
        title = self.result['title']
        cover = str(self.result['cover_from_user'] if self.result['cover_from_user'] else self.result['keyframe'])
        if "https://" in cover:
            cover = cover.replace('https://','http://')
        #cover = 'file:///'+ImgPath()+'3.jpg' #go-cqhttp疑似存在bug，一定清晰度下图片无法加载
        live_message = (f"{name} 正在直播：\n{title}\n" + MessageSegment.image(cover) + f"\n{url} "+MessageSegment.at("all"))
        return live_message
    