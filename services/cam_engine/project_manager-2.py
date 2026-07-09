from __future__ import annotations

from .project import Project

class ProjectManager:
    _project: Project | None = None

    @classmethod
    def new_project(cls) -> Project:
        cls._project = Project()
        return cls._project

    @classmethod
    def current_project(cls) -> Project | None:
        return cls._project

    @classmethod
    def reset(cls) -> Project:
        cls._project = Project()
        return cls._project
