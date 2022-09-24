'''
Description: 
Autor: LucinF
Date: 2022-08-13 21:34:50
LastEditors: LucinF
LastEditTime: 2022-09-22 20:07:49
'''
from dataclasses import dataclass
import re
from this import d
from typing import Dict, List, Set, Tuple, Union, Any
from nonebot.adapters.onebot.v11 import Message

@dataclass
class BaseResult:
    error:bool
    info:str

    def success(self)->bool:
        return not self.error


class Result:
    
    @dataclass
    class IntResult(BaseResult):
        """成员变量:
        
        error : bool 
        函数执行是否异常
        info : str
        执行成功/异常信息
        result : int
        存储int类型的返回结果
        """
        result:int

        def __repr__(self) -> str:
            return f"<IntResult(error={self.error}, info={self.info}, result={self.result})>"

    @dataclass
    class ListResult(BaseResult):
        """成员变量:
        
        error : bool 
        函数执行是否异常
        info : str
        执行成功/异常信息
        result : list
        存储list类型的返回结果
        """
        result:list

        def __repr__(self) -> str:
            return f"<ListResult(error={self.error}, info={self.info}, result={self.result})>"

    @dataclass
    class DictResult(BaseResult):
        """成员变量:
        
        error : bool 
        函数执行是否异常
        info : str
        执行成功/异常信息
        result : dict
        存储dict类型的返回结果
        """
        result:dict

        def __repr__(self) -> str:
            return f"<DictResult(error={self.error}, info={self.info}, result={self.result})>"

    @dataclass
    class StrResult(BaseResult):
        """成员变量:
        
        error : bool 
        函数执行是否异常
        info : str
        执行成功/异常信息
        result : str
        存储str类型的返回结果
        """
        result:str

        def __repr__(self) -> str:
            return f"<StrResult(error={self.error}, info={self.info}, result={self.result})>"

    @dataclass
    class MessageResult(BaseResult):
        """成员变量:
        
        error : bool 
        函数执行是否异常
        info : str
        执行成功/异常信息
        result : Message
        存储str类型的返回结果
        """
        result:Message

        def __repr__(self) -> str:
            return f"<MessageResult(error={self.error}, info={self.info}, result={self.result})>"

