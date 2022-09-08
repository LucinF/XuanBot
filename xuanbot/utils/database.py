from ctypes import resize
from datetime import datetime
import os
from pickle import TRUE
from re import T
import re
import nonebot
from nonebot.log import logger
from sqlalchemy import Column, Integer, String, BLOB, DATETIME, select, distinct, func, Boolean, Text
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from xuanbot.utils.result import Result

__PROJECT_ROOT__ = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace('\\','/')
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

class Live_subscribe(Base):
    __tablename__ = 'Live_subscribe'
    id = Column(Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    uid = Column(String(16), nullable=False, comment="B站UID")
    subscriber_id = Column(String(16), nullable=False, comment="群号")

    def __init__(self, uid:str,subscriber_id:str):
        self.uid = uid
        self.subscriber_id =subscriber_id

    async def select(self) -> Result.IntResult:
        async_session = DB().get_session()
        try:
            async with async_session.begin() as session:
                session_result = await session.execute(select(Live_subscribe).where(
                            Live_subscribe.uid == self.uid).where(
                            Live_subscribe.subscriber_id == self.subscriber_id))
                subscription = session_result.scalar_one()
                result = Result.IntResult(error=False, info="Exist", result=subscription)
        except NoResultFound:
            result = Result.IntResult(error=True, info="Select_No_Result", result=0)
        except MultipleResultsFound:
            result = Result.IntResult(error=True, info="Multiple_Results_Found", result=-1)
        except Exception as e:
            result = Result.IntResult(error=True, info=repr(e), result=-2)
        return result

    async def insert(self) -> Result.IntResult:
        try:
            result = await self.select()
            if  not result.error:
                return Result.IntResult(error=True,info='Exist',result=result.result)
            elif result.error and result.result == 0:
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    session.add(self)
                return Result.IntResult(error=False,info='Instance insert successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info=repr(e), result=-2)
        return result

    async def delete(self) -> Result.IntResult:
        try:
            result = await self.select()
            if  (not result.error) or (result.error and result.result == 0):
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    session.delete(self)
                return Result.IntResult(error=False,info='Instance delete successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info=repr(e), result=-2)
        return result
    
    async def select_uids(self) -> Result.ListResult:
        async_session = DB().get_session()
        try:
            async with async_session.begin() as session:
                session_result = await session.execute(select(distinct(Live_subscribe.uid)))
                result = Result.ListResult(error=False,info='Select uids successed',result= session_result.scalars().all())
        except NoResultFound:
            result = Result.ListResult(error=False, info="Select uids not result", result=[])
        except Exception as e:
            result = Result.ListResult(error=True, info=repr(e), result=[])
        return result
        

    
    async def select_subscribe(self) -> Result.ListResult:
        async_session = DB().get_session()
        try:
            async with async_session.begin()  as session: 
                session_result = await session.execute(select(distinct(Live_subscribe.subscriber_id)).where(
                            Live_subscribe.uid == self.uid))
                result = Result.ListResult(error=False,info='Select subscribes successed',result= session_result.scalars().all())
        except NoResultFound:
            result = Result.ListResult(error=False, info="Select subscribes not result", result=[])
        except Exception as e:
            result = Result.ListResult(error=True, info=repr(e), result=[])
        return result