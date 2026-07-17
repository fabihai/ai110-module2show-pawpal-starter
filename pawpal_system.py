from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Pet:
    name: str
    owner: 'Owner'
    meds: List[str]

    def getMeds(self) -> List[str]:
        pass


@dataclass
class Task:
    owner: 'Owner'
    pet: Pet
    type: str
    time: datetime


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: List[Pet] = []

    def addPet(self, pet: Pet) -> None:
        pass

    def performAction(self, pet: Pet, action: str) -> None:
        pass

    def addTask(self, scheduler: 'Scheduler', task: Task) -> None:
        pass


class Scheduler:
    def __init__(self, pet: Pet):
        self.pet: Pet = pet
        self.tasks: List[Task] = []

    def addTask(self, task: Task) -> None:
        pass

    def getDailyPlan(self) -> List[Task]:
        pass
