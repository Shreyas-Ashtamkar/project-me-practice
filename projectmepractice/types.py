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
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "domain":self.domain,
            "duration":self.duration,
            "group_id":self.group_id,
            "group_part":self.group_part,
            "allocations":self.allocations,
        }

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