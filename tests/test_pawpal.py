import unittest
from datetime import time
from pawpal_system import Owner, Pet, Task


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


if __name__ == "__main__":
    unittest.main()
