from __future__ import annotations

from .users import register_user
from .projects import feed_all_projects, feed_all_projects, fetch_all_projects
from .practice import allocate_next_project_for_user
from .const import PROD_MODE, EMAIL_SENDER_ADDRESS, EMAIL_SENDER_NAME

from dataclasses import dataclass
from uuid import UUID
from datetime import date
from typing import List, Dict, Any

@dataclass
class ProjectType():
    id: UUID
    title: str
    description: str
    domain: str
    duration: int
    group_id: str
    group_part: str
    allocations: List[AllocationType]
    
    def to_dict() -> Dict[str, Any]:
        pass

@dataclass
class UserType():
    id: UUID
    name: str
    email: str
    created_on: date
    is_active: bool
    current_project: ProjectType
    allocations: List[AllocationType]
    
@dataclass
class AllocationType():
    id: UUID
    user: UserType
    project: ProjectType
    date: date

def db_initialized():    
    return bool(fetch_all_projects().get_or_none())
        