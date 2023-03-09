# from ctypes import resize
# from datetime import datetime
# from lib2to3.pgen2.token import STRING
import os
# from pickle import TRUE
# from re import T
# import re
import nonebot
from nonebot.log import logger
# from sqlalchemy import Column, Integer, String, BLOB, DATETIME, select, distinct, func, Boolean, Text,delete,desc
# from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


__PROJECT_ROOT__ = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))).replace('\\','/')
logger.info(f"{__PROJECT_ROOT__}/xuanbot.db")

try:
    engine = create_async_engine(f"sqlite+aiosqlite:///{__PROJECT_ROOT__}/xuanbot.db", encoding="utf8",
                                 pool_recycle=3600, pool_pre_ping=True, echo=False, future=True)
except Exception as exp:
    import sys

    logger.opt(colors=True).critical(f"<r>创建数据库连接失败</r>, error: {repr(exp)}")
    sys.exit("创建数据库连接失败")


async def database_init():
    try:
        # 初始化数据库结构
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.opt(colors=True).debug(f"<lc>初始化数据库...</lc><lg>完成</lg>")
    except Exception as e:
        import sys
        logger.opt(colors=True).critical(f"<r>数据库初始化失败</r>, error: {repr(e)}")
        sys.exit("数据库初始化失败")


# 初始化化数据库
nonebot.get_driver().on_startup(database_init)
Base = declarative_base(engine) # type: ignore

class DB():

    def __init__(self) -> None:
        self.__sessionmaker = sessionmaker(bind=engine,expire_on_commit=False,class_=AsyncSession)
    """
        :param expire_on_commit:  Defaults to ``True``. When ``True``, all
           instances will be fully expired after each :meth:`~.commit`,
           so that all attribute/object access subsequent to a completed
           transaction will load from the most recent database state.
    """

    def get_session(self) -> sessionmaker:
        return self.__sessionmaker
