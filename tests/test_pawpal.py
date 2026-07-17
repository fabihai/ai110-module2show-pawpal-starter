import unittest
from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTaskCompletion(unittest.TestCase):
    """Test task completion functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Test Owner")
        self.pet = Pet("Test Pet", self.owner)
        self.task = Task(
            description="Test task",
            pet=self.pet,
            task_type="food",
            scheduled_time=time(10, 0),
            frequency="daily"
        )

    def test_mark_complete_changes_status(self):
        """Verify that mark_complete() changes is_completed from False to True."""
        # Initially, task should not be completed
        self.assertFalse(self.task.is_completed)

        # Mark task as complete
        self.task.mark_complete()

        # Verify status changed to True
        self.assertTrue(self.task.is_completed)


class TestTaskAddition(unittest.TestCase):
    """Test adding tasks to pets."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Test Owner")
        self.pet = Pet("Test Pet", self.owner)

    def test_adding_task_increases_pet_task_count(self):
        """Verify that adding a task to a pet increases the pet's task count."""
        # Initially, pet should have no tasks
        initial_count = len(self.pet.get_tasks())
        self.assertEqual(initial_count, 0)

        # Create and add a task
        task = Task(
            description="Test task",
            pet=self.pet,
            task_type="food",
            scheduled_time=time(10, 0),
            frequency="daily"
        )
        self.pet.add_task(task)

        # Verify task count increased by 1
        new_count = len(self.pet.get_tasks())
        self.assertEqual(new_count, 1)


class TestSortingCorrectness(unittest.TestCase):
    """Test that tasks are returned in chronological order."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Test Owner")
        self.pet = Pet("Test Pet", self.owner)
        self.scheduler = Scheduler(self.owner)
        self.owner.add_pet(self.pet)

    def test_daily_plan_sorted_by_time(self):
        """Verify tasks are returned in chronological order."""
        # Add tasks in non-chronological order
        task1 = Task("Evening walk", self.pet, "play", time(18, 0), "daily")
        task2 = Task("Morning feed", self.pet, "food", time(8, 0), "daily")
        task3 = Task("Afternoon med", self.pet, "medicine", time(14, 30), "daily")

        self.pet.add_task(task1)
        self.pet.add_task(task2)
        self.pet.add_task(task3)

        # Get daily plan
        daily_plan = self.scheduler.get_daily_plan(self.pet)

        # Verify tasks are sorted chronologically
        self.assertEqual(daily_plan[0].scheduled_time, time(8, 0))
        self.assertEqual(daily_plan[1].scheduled_time, time(14, 30))
        self.assertEqual(daily_plan[2].scheduled_time, time(18, 0))

    def test_sorting_with_same_time_tasks(self):
        """Verify tasks with same scheduled time are all returned."""
        # Add tasks at the same time for the same pet
        task1 = Task("Feed", self.pet, "food", time(10, 0), "daily")
        task2 = Task("Give water", self.pet, "food", time(10, 0), "daily")

        self.pet.add_task(task1)
        self.pet.add_task(task2)

        daily_plan = self.scheduler.get_daily_plan(self.pet)

        # Both tasks should be present at time 10:00
        self.assertEqual(len(daily_plan), 2)
        self.assertTrue(all(t.scheduled_time == time(10, 0) for t in daily_plan))

    def test_sorting_with_multiple_pets(self):
        """Verify all tasks across multiple pets are sorted by time."""
        pet2 = Pet("Another Pet", self.owner)
        self.owner.add_pet(pet2)

        # Add tasks to different pets in random order
        task1 = Task("Dog walk", self.pet, "play", time(17, 0), "daily")
        task2 = Task("Cat feed", pet2, "food", time(9, 0), "daily")
        task3 = Task("Dog feed", self.pet, "food", time(8, 0), "daily")
        task4 = Task("Cat play", pet2, "play", time(15, 0), "daily")

        self.pet.add_task(task1)
        pet2.add_task(task2)
        self.pet.add_task(task3)
        pet2.add_task(task4)

        # Get daily plan for all pets
        daily_plan = self.scheduler.get_daily_plan()

        # Verify tasks are sorted chronologically
        times = [t.scheduled_time for t in daily_plan]
        self.assertEqual(times, sorted(times))

    def test_sorting_with_boundary_times(self):
        """Verify tasks at midnight and end-of-day are sorted correctly."""
        task1 = Task("Midnight task", self.pet, "food", time(0, 0), "daily")
        task2 = Task("Evening task", self.pet, "food", time(23, 59), "daily")
        task3 = Task("Noon task", self.pet, "food", time(12, 0), "daily")

        self.pet.add_task(task1)
        self.pet.add_task(task2)
        self.pet.add_task(task3)

        daily_plan = self.scheduler.get_daily_plan(self.pet)

        self.assertEqual(daily_plan[0].scheduled_time, time(0, 0))
        self.assertEqual(daily_plan[1].scheduled_time, time(12, 0))
        self.assertEqual(daily_plan[2].scheduled_time, time(23, 59))


class TestRecurrenceLogic(unittest.TestCase):
    """Test recurring task creation and management."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Test Owner")
        self.pet = Pet("Test Pet", self.owner)
        self.scheduler = Scheduler(self.owner)
        self.owner.add_pet(self.pet)

    def test_daily_task_creates_next_occurrence(self):
        """Verify completing a daily task creates a new task for the next day."""
        task = Task("Daily feed", self.pet, "food", time(10, 0), "daily", owner=self.owner)
        self.scheduler.add_task(task)

        # Verify initial task count
        self.assertEqual(len(self.pet.get_tasks()), 1)

        # Complete the task
        self.scheduler.complete_task(task)

        # Verify original task is marked complete
        self.assertTrue(task.is_completed)

        # Verify a new task was created
        self.assertEqual(len(self.pet.get_tasks()), 2)

    def test_new_recurring_task_has_same_properties(self):
        """Verify the new recurring task has identical properties."""
        task = Task(
            "Daily medicine",
            self.pet,
            "medicine",
            time(14, 30),
            "daily",
            owner=self.owner
        )
        self.scheduler.add_task(task)

        # Complete the task
        self.scheduler.complete_task(task)

        # Get all tasks
        all_tasks = self.pet.get_tasks()
        new_task = all_tasks[-1]  # Last task is the newly created one

        # Verify properties match
        self.assertEqual(new_task.description, task.description)
        self.assertEqual(new_task.pet, task.pet)
        self.assertEqual(new_task.task_type, task.task_type)
        self.assertEqual(new_task.scheduled_time, task.scheduled_time)
        self.assertEqual(new_task.frequency, task.frequency)
        self.assertFalse(new_task.is_completed)

    def test_weekly_task_creates_next_occurrence(self):
        """Verify completing a weekly task creates a new task."""
        task = Task("Weekly bath", self.pet, "play", time(11, 0), "weekly", owner=self.owner)
        self.scheduler.add_task(task)

        initial_count = len(self.pet.get_tasks())

        # Complete the task
        self.scheduler.complete_task(task)

        # Verify new task was created
        self.assertEqual(len(self.pet.get_tasks()), initial_count + 1)

    def test_once_task_does_not_recur(self):
        """Verify completing a 'once' frequency task does not create a new task."""
        task = Task("One-time vet visit", self.pet, "medicine", time(9, 0), "once", owner=self.owner)
        self.scheduler.add_task(task)

        # Complete the task
        self.scheduler.complete_task(task)

        # Verify no new task was created
        self.assertEqual(len(self.pet.get_tasks()), 1)
        self.assertTrue(self.pet.get_tasks()[0].is_completed)

    def test_pending_tasks_excludes_completed_recurring_tasks(self):
        """Verify completed recurring tasks don't appear in pending tasks."""
        task = Task("Daily play", self.pet, "play", time(16, 0), "daily", owner=self.owner)
        self.scheduler.add_task(task)

        # Complete the task
        self.scheduler.complete_task(task)

        # Get pending tasks
        pending = self.scheduler.get_pending_tasks(self.pet)

        # Only the new uncompleted task should be pending
        self.assertEqual(len(pending), 1)
        self.assertFalse(pending[0].is_completed)
        self.assertEqual(pending[0].description, "Daily play")


class TestConflictDetection(unittest.TestCase):
    """Test task conflict detection functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Test Owner")
        self.pet1 = Pet("Pet One", self.owner)
        self.pet2 = Pet("Pet Two", self.owner)
        self.scheduler = Scheduler(self.owner)
        self.owner.add_pet(self.pet1)
        self.owner.add_pet(self.pet2)

    def test_same_pet_same_time_is_conflict(self):
        """Verify tasks for same pet at same time are flagged as CONFLICT."""
        task1 = Task("Feed", self.pet1, "food", time(10, 0), "daily")
        task2 = Task("Medicine", self.pet1, "medicine", time(10, 0), "daily")

        self.pet1.add_task(task1)
        self.pet1.add_task(task2)

        # Detect conflicts
        conflicts = self.scheduler.detect_task_conflicts(task2)

        # Should have at least one conflict
        self.assertGreater(len(conflicts), 0)
        # Verify it's marked as CONFLICT (not ALERT)
        self.assertTrue(any("[CONFLICT]" in c for c in conflicts))

    def test_different_pets_same_time_is_alert(self):
        """Verify tasks for different pets at same time are flagged as ALERT."""
        task1 = Task("Dog walk", self.pet1, "play", time(15, 0), "daily")
        task2 = Task("Cat play", self.pet2, "play", time(15, 0), "daily")

        self.pet1.add_task(task1)
        self.pet2.add_task(task2)

        # Detect conflicts for the second task
        conflicts = self.scheduler.detect_task_conflicts(task2)

        # Should have at least one alert
        self.assertGreater(len(conflicts), 0)
        # Verify it's marked as ALERT
        self.assertTrue(any("[ALERT]" in c for c in conflicts))

    def test_different_times_no_conflict(self):
        """Verify tasks at different times do not generate conflicts."""
        task1 = Task("Morning feed", self.pet1, "food", time(8, 0), "daily")
        task2 = Task("Evening feed", self.pet1, "food", time(18, 0), "daily")

        self.pet1.add_task(task1)
        self.pet1.add_task(task2)

        # Detect conflicts
        conflicts = self.scheduler.detect_task_conflicts(task2)

        # Should have no conflicts
        self.assertEqual(len(conflicts), 0)

    def test_get_all_scheduling_conflicts(self):
        """Verify get_all_scheduling_conflicts detects all conflicts."""
        # Create multiple conflicts
        task1 = Task("Feed dog", self.pet1, "food", time(10, 0), "daily")
        task2 = Task("Medicine dog", self.pet1, "medicine", time(10, 0), "daily")
        task3 = Task("Play cat", self.pet2, "play", time(10, 0), "daily")
        task4 = Task("Safe task", self.pet1, "play", time(15, 0), "daily")

        self.pet1.add_task(task1)
        self.pet1.add_task(task2)
        self.pet2.add_task(task3)
        self.pet1.add_task(task4)

        # Get all conflicts
        all_conflicts = self.scheduler.get_all_scheduling_conflicts()

        # Should have detected multiple conflicts/alerts
        self.assertGreater(len(all_conflicts), 0)

    def test_no_conflicts_with_empty_schedule(self):
        """Verify empty schedule has no conflicts."""
        conflicts = self.scheduler.get_all_scheduling_conflicts()
        self.assertEqual(len(conflicts), 0)

    def test_single_task_no_conflict(self):
        """Verify a single task has no conflicts."""
        task = Task("Feed", self.pet1, "food", time(10, 0), "daily")
        self.pet1.add_task(task)

        conflicts = self.scheduler.detect_task_conflicts(task)
        self.assertEqual(len(conflicts), 0)


if __name__ == "__main__":
    unittest.main()
