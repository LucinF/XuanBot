# XuanBot
这个项目完全出于个人兴趣，要写什么功能我已经莫得头绪，现阶段就修正BUG和随缘写了，反正没什么人用.

## 项目依赖
本项目基于[go-cqhttp](https://docs.go-cqhttp.org/)和[Nonebot2](https://v2.nonebot.dev/)框架，使用前我建议对其了解下。

## 如何使用

1. run your bot using `nb run` .
2. 你有许多的python包需要实现准备好，嗯我还不清楚怎么把这堆跑一次性整理起来，哦对了还有下一个Go-cqhttp。
3. 该项目基于nonebot，所以你需要先下好nb驱动aiohttp: nb driver install aiohttp,以及依赖的定时任务插件:nb plugin install nonebot-plugin-apscheduler
4. 怎么用上面写的命令?首先pip install nb-cli 安装所需要的nonebot框架.然后把上面俩个命令复制运行就行了
5. 使用方面遇到不清楚和遇到困难的地方，可以在issuse那里贴上flag:help wanted 留言,我一般每天上去看一次，也可以发我Github上的邮箱留言.

## 已有功能

1. B站主播直播提醒 命令格式 .live 主播uid 在当前群订阅该主播直播提醒;.live_delete 主播uid 在当前群取消订阅该主播提醒
2. B站主播动态监视，隔一段时间轮询一次所有群订阅主播的最新动态进行发布，轮询时间一般是俩分钟+主播数量*10s，10s是为了防止频繁调用API导致被B站暂时屏蔽.
  命令格式 .dynamic 主播uid 在当前群订阅该主播动态发布;.live_delete 主播uid 在当前群取消订阅该动态发布
3. 概率复读，10%概率复读当前群消息

## 目前你需要知道的
1. 目前go-cqhttp端在win上可能有些bug，比如动态插件里面发送动态的截图可能失败，但Ubuntu上我测试能成功发送，建议部署到Linux。
2. 部署到Ubuntu server那种无桌面GUI版本的Linux系统，建议使用NoneBot的go-cqhttp插件:nb plugin install nonebot-plugin-gocqhttp .
3. Ubuntu server版本在使用pyppeteer时可能会出现环境问题，问题详情和解决方案请看: https://blog.csdn.net/qq_26870933/article/details/101288399 .

## B站API参考链接
https://github.com/SocialSisterYi/bilibili-API-collect
