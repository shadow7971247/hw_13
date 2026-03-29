from dataclasses import dataclass
from typing import List


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    gender: str
    mobile: str
    subjects: List[str]
    hobbies: List[str]
    picture: str
    address: str
    state: str
    city: str