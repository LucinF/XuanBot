from dataclasses import dataclass
import re
from this import d
from typing import Dict, List, Set, Tuple, Union, Any

@dataclass
class BaseResult:
    error:bool
    info:str

    def success(self)->bool:
        return not self.error


class Result:
    
    @dataclass
    class IntResult(BaseResult):
        result:int

        def __repr__(self) -> str:
            return f"<IntResult(error={self.error}, info={self.info}, result={self.result})>"

    @dataclass
    class ListResult(BaseResult):
        result:list

        def __repr__(self) -> str:
            return f"<ListResult(error={self.error}, info={self.info}, result={self.result})>"