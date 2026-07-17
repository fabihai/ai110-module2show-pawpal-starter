from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional


@dataclass
class Task:
    description: str
    pet: 'Pet'
    task_type: str  # e.g., "food", "medicine", "play"
    scheduled_time: time
    frequency: str  # e.g., "daily", "weekly", "once"
    is_completed: bool = False
    owner: Optional['Owner'] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_completed = False

    def __str__(self) -> str:
        """Return a formatted string representation of the task."""
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.description} ({self.task_type}) at {self.scheduled_time.strftime('%H:%M')} [{self.frequency}]"


@dataclass
class Pet:
    name: str
    owner: 'Owner'
    meds: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        task.pet = self
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return uncompleted tasks for this pet."""
        return [t for t in self.tasks if not t.is_completed]

    def get_meds(self) -> List[str]:
        """Return list of medications for this pet."""
        return self.meds

    def add_med(self, medication: str) -> None:
        """Add a medication to this pet's medication list."""
        self.meds.append(medication)


class Owner:
    def __init__(self, name: str):
        """Initialize an owner with a name."""
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all uncompleted tasks from all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks

    def add_task(self, scheduler: 'Scheduler', task: Task) -> None:
        """Add a task to a pet through the scheduler."""
        task.owner = self
        scheduler.add_task(task)

    def perform_action(self, pet: Pet, action: str) -> None:
        """Perform an action on a pet (generic handler for various pet actions)."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} is not owned by {self.name}")
        # Action handler - can be extended with specific logic
        print(f"[{self.name}] Performing '{action}' on {pet.name}")


class Scheduler:
    """The brain of the system - retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner: Owner = owner

    def add_task(self, task: Task) -> None:
        """Add a task to a pet's task list."""
        if task.pet not in self.owner.pets:
            raise ValueError(f"Pet {task.pet.name} is not in {self.owner.name}'s collection")
        task.pet.add_task(task)

    def get_daily_plan(self, pet: Optional[Pet] = None) -> List[Task]:
        """
        Get tasks organized by time for the day.
        If pet is specified, return only that pet's tasks.
        Otherwise, return all tasks from all pets, sorted by time.
        """
        if pet:
            tasks = pet.get_tasks()
        else:
            tasks = self.owner.get_all_tasks()

        # Sort by scheduled time
        return sorted(tasks, key=lambda t: t.scheduled_time)

    def get_pending_tasks(self, pet: Optional[Pet] = None) -> List[Task]:
        """
        Get pending (uncompleted) tasks.
        If pet is specified, return only that pet's pending tasks.
        """
        if pet:
            return pet.get_pending_tasks()
        else:
            return self.owner.get_all_pending_tasks()

    def get_tasks_by_type(self, task_type: str, pet: Optional[Pet] = None) -> List[Task]:
        """Get tasks filtered by type (e.g., 'food', 'medicine')."""
        if pet:
            tasks = pet.get_tasks()
        else:
            tasks = self.owner.get_all_tasks()

        return [t for t in tasks if t.task_type == task_type]

    def complete_task(self, task: Task) -> None:
        """Mark a task as completed."""
        task.mark_complete()

    def print_daily_plan(self, pet: Optional[Pet] = None) -> None:
        """Print a formatted daily plan."""
        daily_tasks = self.get_daily_plan(pet)

        if pet:
            print(f"\n=== Daily Plan for {pet.name} ===")
        else:
            print(f"\n=== Daily Plan for {self.owner.name}'s Pets ===")

        if not daily_tasks:
            print("No tasks scheduled")
            return

        for task in daily_tasks:
            print(f"  {task}")
