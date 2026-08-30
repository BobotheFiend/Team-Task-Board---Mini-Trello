from enum import Enum


class Role(str, Enum):
    MEMBER = "Member"
    LEAD = "Lead"
    