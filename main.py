from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import time

if __name__ == "__main__":
    owner = Owner("Chazz")
    pet1 = Pet("Chuck", owner)
    pet2 = Pet("Bun", owner)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)

    # Create and add tasks with all required parameters
    task1 = Task(
        description="Feed pet",
        pet=pet1,
        task_type="food",
        scheduled_time=time(10, 0),  # 10:00 AM
        frequency="daily"
    )
    scheduler.add_task(task1)

    task2 = Task(
        description="Give pet meds",
        pet=pet2,
        task_type="medicine",
        scheduled_time=time(16, 0),  # 4:00 PM
        frequency="daily"
    )
    scheduler.add_task(task2)

    task3 = Task(
        description="Take pet for a walk",
        pet=pet1,
        task_type="play",
        scheduled_time=time(12, 0),  # 12:00 PM
        frequency="daily"
    )
    scheduler.add_task(task3)

    scheduler.print_daily_plan()