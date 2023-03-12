from sqlalchemy import Column, Integer, String, select, distinct,delete
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from xuanbot.utils.result import Result
from .mapperConnect import Base,DB

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
            result = Result.IntResult(error=True, info="Live_subscribe.select():Select_No_Result", result=0)
        except MultipleResultsFound:
            result = Result.IntResult(error=True, info="Live_subscribe.select():Multiple_Results_Found", result=-1)
        except Exception as e:
            result = Result.IntResult(error=True, info='Live_subscribe.select():'+repr(e), result=-2)
        return result

    async def insert(self) -> Result.IntResult:
        '''插入

        return {*} Result.IntResult
                        result >= 0 代表表内已存在该条记录或者插入成功,反之代表执行异常

        author: LucinF
        '''
        try:
            result = await self.select()
            if  not result.error:
                return Result.IntResult(error=True,info=f'Live_subscribe.select():The uid:{self.uid} group:{self.subscriber_id} was existed',result=result.result)
            elif result.error and result.result == 0:
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    session.add(self)
                return Result.IntResult(error=False,info='Live_subscribe.insert():Instance insert successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info='Live_subscribe.insert():'+repr(e), result=-2)
        return result

    async def delete(self) -> Result.IntResult:
        try:
            result = await self.select()
            if not result.error :
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    await session.execute(delete(Live_subscribe).where(
                            Live_subscribe.uid == self.uid).where(
                            Live_subscribe.subscriber_id == self.subscriber_id))
                return Result.IntResult(error=False,info='Live_subscribe.delete():Instance delete successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info='Live_subscribe.delete():'+repr(e), result=-2)
        return result
    
    async def select_uids(self) -> Result.ListResult:
        '''获取表内所有主播uid
        
        return {*} Result.ListResult
                    ListResult.result存放含有全部uid的列表
        
        author: LucinF
        '''
        async_session = DB().get_session()
        try:
            async with async_session.begin() as session:
                session_result = await session.execute(select(Live_subscribe.uid))
                result = Result.ListResult(error=False,info='Live_subscribe.select_uids():Select uids successed',result= session_result.scalars().all())
        except NoResultFound:
            result = Result.ListResult(error=False, info="Live_subscribe.select_uids():Select uids not result", result=[])
        except Exception as e:
            result = Result.ListResult(error=True, info="Live_subscribe.select_uids():"+repr(e), result=[])
        return result
        

    
    async def select_subscribe(self) -> Result.ListResult:
        '''根据主播uid获取所有对应的群号
        
        return {*} Result.ListResult
                    ListResult.result存放含有全部群号的列表
        
        author: LucinF
        '''
        async_session = DB().get_session()
        try:
            async with async_session.begin()  as session: 
                session_result = await session.execute(select(distinct(Live_subscribe.subscriber_id)).where(
                            Live_subscribe.uid == self.uid))
                result = Result.ListResult(error=False,info='Live_subscribe.select_subscribe():Select subscribes successed',result= session_result.scalars().all())
        except NoResultFound:
            result = Result.ListResult(error=False, info="Live_subscribe.select_subscribe():Select subscribes not result", result=[])
        except Exception as e:
            result = Result.ListResult(error=True, info='Live_subscribe.select_subscribe():'+repr(e), result=[])
        return result

