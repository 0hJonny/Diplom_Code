from dataclasses import dataclass, field
from sqlite3 import Timestamp, Date


@dataclass
class User_model:
    user_id: int
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    birthdate: Date
    avatar: str
    confirmed: bool = False
    created_at: Timestamp = field(default_factory=Timestamp)

@dataclass
class User:
    username: str
    password: str

