"""
Import all models to make them available
"""
from app.models.user import User, UserRole, UserStatus
from app.models.project import Project, ProjectStage
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.bug import Bug, BugSeverity, BugStatus
from app.models.lore import Character, Location, Faction

__all__ = [
    "User",
    "UserRole",
    "UserStatus",
    "Project",
    "ProjectStage",
    "Task",
    "TaskStatus",
    "TaskPriority",
    "Bug",
    "BugSeverity",
    "BugStatus",
    "Character",
    "Location",
    "Faction",
]
