# XuanBot

## 项目依赖
本项目基于Go-cqhttp 和NoneBot框架，使用前我建议对其了解下。

## 如何使用

1. run your bot using `nb run` .
2.你有许多的python包需要实现准备好，嗯我还不清楚怎么把这堆跑一次性整理起来，哦对了还有下一个Go-cqhttp。
3.该项目基于nonebot，所以你需要先下好nb驱动aiohttp: nb driver install aiohttp,以及依赖的定时任务插件:nb plugin install nonebot-plugin-apscheduler
  怎么用上面写的命令?首先pip install nb-cli 安装所需要的nonebot框架 . 然后把上面俩个命令复制运行就行了.

## 目前你需要知道的
1.目前go-cqhttp端在win上可能有些bug，比如动态插件里面发送动态的截图可能失败，但Ubuntu上我测试能成功发送，建议部署到Linux。
2.部署到Ubuntu server那种无桌面GUI版本的Linux系统，建议使用NoneBot的go-cqhttp插件:nb plugin install nonebot-plugin-gocqhttp .
3.Ubuntu server版本在使用pyppeteer时可能会出现环境问题，问题详情和解决方案请看: https://blog.csdn.net/qq_26870933/article/details/101288399 .

## Documentation

See [Docs](https://v2.nonebot.dev/)

## B站API参考链接
https://github.com/SocialSisterYi/bilibili-API-collect
