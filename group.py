
from typing import Dict
from attr import dataclass

class Schedule(Dict[str,list[str]]):
    pass

@dataclass
class Group:
    name : str
    schedule : Schedule