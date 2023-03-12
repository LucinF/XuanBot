from sqlalchemy import Column, Integer, String,select, distinct,delete,desc
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from xuanbot.utils.result import Result
from .mapperConnect import Base,DB

class Dynamic_subscribe(Base):
    __tablename__ = 'Dynamic_subscribe'
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
                session_result = await session.execute(select(Dynamic_subscribe).where(
                            Dynamic_subscribe.uid == self.uid).where(
                            Dynamic_subscribe.subscriber_id == self.subscriber_id))
                subscription = session_result.scalar_one()
                result = Result.IntResult(error=False, info="Exist", result=subscription)
        except NoResultFound:
            result = Result.IntResult(error=True, info="Dynamic_subscribe.select():Select_No_Result", result=0)
        except MultipleResultsFound:
            result = Result.IntResult(error=True, info="Dynamic_subscribe.select():Multiple_Results_Found", result=-1)
        except Exception as e:
            result = Result.IntResult(error=True, info='Dynamic_subscribe.select():'+repr(e), result=-2)
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
                return Result.IntResult(error=True,info=f'Dynamic_subscribe.select():The uid:{self.uid} group:{self.subscriber_id} was existed',result=result.result)
            elif result.error and result.result == 0:
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    session.add(self)
                return Result.IntResult(error=False,info='Dynamic_subscribe.insert():Instance insert successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info='Dynamic_subscribe.insert():'+repr(e), result=-2)
        return result

    async def delete(self) -> Result.IntResult:
        try:
            result = await self.select()
            if not result.error :
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    await session.execute(delete(Dynamic_subscribe).where(
                            Dynamic_subscribe.uid == self.uid).where(
                            Dynamic_subscribe.subscriber_id == self.subscriber_id))
                return Result.IntResult(error=False,info='Dynamic_subscribe.delete():Instance delete successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info='Dynamic_subscribe.delete():'+repr(e), result=-2)
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
                session_result = await session.execute(select(distinct(Dynamic_subscribe.uid)))
                result = Result.ListResult(error=False,info='Dynamic_subscribe.select_uids():Select uids successed',result= session_result.scalars().all())
        except NoResultFound:
            result = Result.ListResult(error=False, info="Dynamic_subscribe.select_uids():Select uids not result", result=[])
        except Exception as e:
            result = Result.ListResult(error=True, info="Dynamic_subscribe.select_uids():"+repr(e), result=[])
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
                session_result = await session.execute(select(distinct(Dynamic_subscribe.subscriber_id)).where(
                            Dynamic_subscribe.uid == self.uid))
                result = Result.ListResult(error=False,info='Dynamic_subscribe.select_subscribe():Select subscribes successed',result= session_result.scalars().all())
        except NoResultFound:
            result = Result.ListResult(error=False, info="Dynamic_subscribe.select_subscribe():Select subscribes not result", result=[])
        except Exception as e:
            result = Result.ListResult(error=True, info='Dynamic_subscribe.select_subscribe():'+repr(e), result=[])
        return result

class Dynamic_recode(Base):
    __tablename__ = 'Dynamic_recode'
    id = Column(Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    uid = Column(String(16), nullable=False, comment="B站UID")
    dynamic_id = Column(String(30), nullable=False,comment='B站动态id')
    timestamp = Column(String(20), nullable =False,comment='时间戳')

    def __init__(self,uid:str,dynamic_id:str,timestamp:str):
        self.uid = uid
        self.dynamic_id = dynamic_id
        self.timestamp =timestamp
    
    async def select(self) -> Result.IntResult:
        async_session = DB().get_session()
        try:
            async with async_session.begin() as session:
                session_result = await session.execute(select(Dynamic_recode).where(
                            Dynamic_recode.uid == self.uid).where(
                            Dynamic_recode.dynamic_id == self.dynamic_id).where(
                            Dynamic_recode.timestamp == self.timestamp))
                subscription = session_result.scalar_one()
                result = Result.IntResult(error=False, info="Exist", result=subscription)
        except NoResultFound:
            result = Result.IntResult(error=True, info="Dynamic_recode.select():Select_No_Result", result=0)
        except MultipleResultsFound:
            result = Result.IntResult(error=True, info="Dynamic_recode.select():Multiple_Results_Found", result=-1)
        except Exception as e:
            result = Result.IntResult(error=True, info='Dynamic_recode.select():'+repr(e), result=-2)
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
                return Result.IntResult(error=True,info=f'Dynamic_recode.select():The uid:{self.uid} dynamic_id:{self.dynamic_id} timestamp:{self.timestamp} was existed',result=result.result)
            elif result.error and result.result == 0:
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    session.add(self)
                return Result.IntResult(error=False,info='Dynamic_recode.insert():Instance insert successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info='Dynamic_recode.insert():'+repr(e), result=-2)
        return result

    async def delete(self) -> Result.IntResult:
        try:
            result = await self.select()
            if not result.error :
                async_session = DB().get_session()
                async with async_session.begin() as session:
                    await session.execute(delete(Dynamic_recode).where(
                            Dynamic_recode.uid == self.uid).where(
                            Dynamic_recode.dynamic_id == self.dynamic_id).where(
                            Dynamic_recode.timestamp == self.timestamp))
                return Result.IntResult(error=False,info='Dynamic_recode.delete():Instance delete successed',result=0)
            else:
                return result
        except Exception as e:
            result = Result.IntResult(error=True, info='Dynamic_recode.delete():'+repr(e), result=-2)
        return result

    async def get_last_dynamic(self) -> Result.DictResult:
        '''根据主播uid获取表内最新动态的时间戳
        
        return {*} Result.DictResult
                    [{'type':int 结果类型
                    'dynamic_id':str 动态id
                    'timestamp':str 动态时间戳}]
        
        author: LucinF
        '''
        try:
            async_session = DB().get_session()
            async with async_session.begin() as session:
                session_result = await session.execute(select(Dynamic_recode.dynamic_id,Dynamic_recode.timestamp).where(
                        Dynamic_recode.uid == self.uid).order_by(desc(Dynamic_recode.timestamp)))
                row =  session_result.first()
                dictresult = {
                    'type':1,
                    'dynamic_id':str(row[0]),
                    'timestamp':str(row[1])
                }
                result = Result.DictResult(error=False,info='Dynamic_recode.get_last_timestamp():success.',result= dictresult)
        except NoResultFound:
            dictresult = {
                    'type':0,
                    'dynamic_id':'',
                    'timestamp':''
                }
            result = Result.DictResult(error=True, info="Dynamic_recode.get_last_timestamp():Select_No_Result", result=dictresult)
        except MultipleResultsFound:
            dictresult = {
                    'type':-1,
                    'dynamic_id':'',
                    'timestamp':''
                }
            result = Result.DictResult(error=True, info="Dynamic_recode.get_last_timestamp():Multiple_Results_Found", result=dictresult)
        except Exception as e:
            dictresult = {
                    'type':-2,
                    'dynamic_id':'',
                    'timestamp':''
                }
            result = Result.DictResult(error=True, info='Dynamic_recode.get_last_timestamp():'+repr(e), result=dictresult)
        return result
