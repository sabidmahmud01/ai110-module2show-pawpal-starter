from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", "other"
    age: int
    special_needs: list[str] = field(default_factory=list)
    tasks: list["Task"] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a summary of the pet's basic details and special needs."""
        needs = ', '.join(self.special_needs) if self.special_needs else 'none'
        return f"{self.name} is a {self.age}-year-old {self.species} with special needs: {needs}"

    def add_task(self, task: "Task") -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list["Task"]:
        """Return the list of tasks assigned to this pet."""
        return self.tasks


@dataclass
class Task:
    description: str
    time: int  # duration in minutes
    frequency: str  # e.g., "daily", "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Return this task as a serializable dictionary."""
        return {
            "description": self.description,
            "time": self.time,
            "frequency": self.frequency,
            "completed": self.completed
        }


class Owner:
    def __init__(self, name: str, time_available: int, preferences: Optional[dict] = None):
        """Initialize an owner with available time, preferences, and pets."""
        self.name = name
        self.time_available = time_available  # minutes per day
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list["Task"]:
        """Return a combined list of tasks for all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_available_time(self) -> int:
        """Return the owner's available care time in minutes."""
        return self.time_available

    def update_preferences(self, key: str, value) -> None:
        """Update a single owner preference by key."""
        self.preferences[key] = value


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize a scheduler for the given owner and their pet tasks."""
        self.owner = owner
        self.tasks = self.owner.get_all_tasks()
        self.scheduled_plan: list["Task"] = []  # stores result of generate_plan()

    def add_task(self, task: "Task", pet: Pet) -> None:
        """Add a task to a pet and refresh the scheduler task list."""
        pet.add_task(task)
        self.tasks = self.owner.get_all_tasks()  # refresh tasks list

    def remove_task(self, description: str, pet: Pet) -> None:
        """Remove matching tasks from a pet and refresh the scheduler task list."""
        pet.tasks = [t for t in pet.tasks if t.description != description]
        self.tasks = self.owner.get_all_tasks()

    def _filter_by_time(self, tasks: list["Task"]) -> list["Task"]:
        """Keep tasks that fit within the owner's available time."""
        total_time = 0
        filtered = []
        for task in tasks:
            if total_time + task.time <= self.owner.get_available_time():
                filtered.append(task)
                total_time += task.time
        return filtered

    def _sort_by_priority(self, tasks: list["Task"]) -> list["Task"]:
        """Sort tasks by frequency priority and then by longer duration first."""
        # Sort by frequency: daily first, then weekly, etc.
        freq_order = {"daily": 0, "weekly": 1, "monthly": 2}
        return sorted(tasks, key=lambda t: (freq_order.get(t.frequency, 3), -t.time))

    def generate_plan(self) -> list["Task"]:
        """Generate and store a time-constrained prioritized task plan."""
        sorted_tasks = self._sort_by_priority(self.tasks)
        self.scheduled_plan = self._filter_by_time(sorted_tasks)
        return self.scheduled_plan

    def explain_plan(self) -> str:
        """Return a human-readable summary of the scheduled task plan."""
        if not self.scheduled_plan:
            return "No tasks scheduled."
        plan_str = "Scheduled tasks:\n"
        for task in self.scheduled_plan:
            plan_str += f"- {task.description} ({task.time} min, {task.frequency})\n"
        return plan_str
