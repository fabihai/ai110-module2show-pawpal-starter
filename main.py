from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import time

if __name__ == "__main__":
    owner = Owner("Chazz")
    pet1 = Pet("Chuck", owner)
    pet2 = Pet("Bun", owner)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)

    # Task 1: Feed Chuck at 10:00 AM
    task1 = Task(
        description="Feed Chuck",
        pet=pet1,
        task_type="food",
        scheduled_time=time(10, 0),
        frequency="daily"
    )
    scheduler.add_task(task1)

    # Task 2: Give Bun meds at 4:00 PM
    task2 = Task(
        description="Give Bun meds",
        pet=pet2,
        task_type="medicine",
        scheduled_time=time(16, 0),
        frequency="daily"
    )
    scheduler.add_task(task2)

    # Task 3: Walk Chuck at 12:00 PM
    task3 = Task(
        description="Take Chuck for a walk",
        pet=pet1,
        task_type="play",
        scheduled_time=time(12, 0),
        frequency="daily"
    )
    scheduler.add_task(task3)

    print("\n" + "="*60)
    print("TESTING CONFLICT DETECTION")
    print("="*60)

    # CONFLICT: Add another task for Chuck at 10:00 AM (same pet, same time)
    task4 = Task(
        description="Give Chuck treats",
        pet=pet1,
        task_type="food",
        scheduled_time=time(10, 0),  # SAME TIME as task1
        frequency="daily"
    )
    print("\n> Attempting to add: 'Give Chuck treats' at 10:00 AM")
    conflicts = scheduler.detect_task_conflicts(task4)
    if conflicts:
        print("  [!] Conflicts detected:")
        for warning in conflicts:
            print(f"    {warning}")
    scheduler.add_task(task4)

    # ALERT: Add a task for Bun at 10:00 AM (different pet, same time as Chuck's task)
    task5 = Task(
        description="Groom Bun",
        pet=pet2,
        task_type="grooming",
        scheduled_time=time(10, 0),  # SAME TIME as task1 (different pet)
        frequency="daily"
    )
    print("\n> Attempting to add: 'Groom Bun' at 10:00 AM")
    conflicts = scheduler.detect_task_conflicts(task5)
    if conflicts:
        print("  [!] Conflicts detected:")
        for warning in conflicts:
            print(f"    {warning}")
    scheduler.add_task(task5)

    print("\n" + "="*60)
    print("FULL SCHEDULE WITH ALL CONFLICTS")
    print("="*60)
    scheduler.print_daily_plan()

    print("\n" + "="*60)
    print("COMPLETE CONFLICT REPORT")
    print("="*60)
    all_conflicts = scheduler.get_all_scheduling_conflicts()
    if all_conflicts:
        print("Conflicts found in schedule:")
        for i, conflict in enumerate(all_conflicts, 1):
            print(f"  {i}. {conflict}")
    else:
        print("✓ No scheduling conflicts detected")