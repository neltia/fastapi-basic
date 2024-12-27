from pydantic import BaseModel
from typing import List


# Base Model
class User(BaseModel):
    id: int
    name: str
    is_active: bool = True


# Inheritance
class AdminUser(User):
    admin_level: int


# Nested Models
class Team(BaseModel):
    team_name: str
    members: List[User]


# Serialization Example
user = User(id=1, name="Alice")
print(user.model_dump_json())  # Serialize to JSON
admin = AdminUser(id=2, name="Bob", admin_level=5)
print(admin.model_dump_json())  # Convert to dict
