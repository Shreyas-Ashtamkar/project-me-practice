from .const import DATABASE_URL, USERS_TABLE, PROJECTS_TABLE, ALLOCATIONS_TABLE
from peewee import SqliteDatabase, Model, CharField, IntegerField, BooleanField, UUIDField, DateField, ForeignKeyField, ModelSelect, DoesNotExist

from datetime import datetime

from uuid import uuid4

db = SqliteDatabase(DATABASE_URL)

class Project(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    title = CharField(unique=True)
    description = CharField()
    domain = CharField()
    duration = IntegerField()
    group_id = CharField(null=True)
    group_part = CharField(null=True)
    
    @property
    def has_parts(self) -> bool:
        return bool(self.group_id)
    
    def next_group_part(self) -> Project | None:
        if not self.has_parts: 
            raise DoesNotExist("This group does not have parts")
        return Project.get(Project.group_id==self.group_id, Project.group_part==(str(int(self.group_part)+1)))

    @property
    def tags(self) -> str:
        tags = (
            f"{self.domain} Domain"
            + (f" | Group {self.group_id} | Step {self.group_part}" if self.has_parts else "")
            + f" | {self.duration}" + (" Week" if self.duration==1 else " Weeks")
        )
        return tags
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "domain": self.domain,
            "duration": self.duration,
            "has_parts": self.has_parts,
            "group_id": self.group_id,
            "group_part": self.group_part,
            "tags": self.tags
        }
    
    def __str__(self):
        return f"<Project(id={self.id}, title={self.title}, domain={self.domain}, duration={self.duration}, has_parts={self.has_parts}, group_id={self.group_id}, group_part={self.group_part})>"
    
    class Meta:
        database = db
        table_name = PROJECTS_TABLE

class User(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField()
    email = CharField(unique=True)
    created_on = DateField(default=datetime.today)
    week_number = IntegerField(default=0)
    is_active = BooleanField(default=True)
    current_project:Project = ForeignKeyField(Project, null=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "created_on": self.created_on.isoformat(),
            "week_number": self.week_number,
            "current_project": str(self.current_project) if self.current_project else ""
        }
    
    def __str__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, created_on={self.created_on}, week_number={self.week_number}, is_active={self.is_active}, current_project={self.current_project})>"

    class Meta:
        database = db
        table_name = USERS_TABLE

class Allocation(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    user:User = ForeignKeyField(User, backref="allocations")
    project:Project = ForeignKeyField(Project, backref="allocations")
    date = DateField(default=datetime.today)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "user": self.user,
            "project": self.project,
            "date": self.date.isoformat()
        }
    
    def __str__(self):
        return f"<Allocation(id={self.id}, user={self.user}, project={self.project}, date={self.date})>"
    
    class Meta:
        database = db
        table_name = ALLOCATIONS_TABLE
        

def initialize_db():
    with db:
        # By default it will only create with IF NOT EXISTS clause, don't worry
        db.create_tables([User, Project, Allocation])