from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", "other"
    age: int
    special_needs: list[str] = field(default_factory=list)

    def get_info(self) -> str:
        pass


@dataclass
class Task:
    title: str
    duration: int  # minutes
    priority: str  # "low", "medium", "high"
    category: str  # "walk", "feed", "meds", "grooming", "enrichment"

    def is_high_priority(self) -> bool:
        pass

    def to_dict(self) -> dict:
        pass


class Owner:
    def __init__(self, name: str, time_available: int, preferences: Optional[dict] = None):
        self.name = name
        self.time_available = time_available  # minutes per day
        self.preferences = preferences or {}

    def get_available_time(self) -> int:
        pass

    def update_preferences(self, key: str, value) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def generate_plan(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
