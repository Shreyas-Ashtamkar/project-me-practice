from __future__ import annotations
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
    
    def get_id(self) -> str:
        pass
    
    def to_dict(self) -> Dict[str, Any]:
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
    
    def to_dict(self) -> Dict[str, Any]:
        pass
    
@dataclass
class AllocationType():
    id: UUID
    user: UserType
    project: ProjectType
    date: date
    
    def to_dict(self) -> Dict[str, Any]:
        pass