from pydantic import BaseSettings
from pydantic import BaseModel
from nonebot.adapters.onebot.v11 import MessageSegment,Message
import os

class Config(BaseSettings):
    # Your Config Here

    class Config:
        extra = "ignore"

def ImgPath() -> str:
    path = os.path.dirname(os.path.abspath(__file__))+'/img/'
    path = path.replace('\\','/')
    return path

class LiveInfo(BaseModel):
    uid : str
    result : dict

    def live_at_all(self) -> Message:
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
    