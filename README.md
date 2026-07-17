# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
```
=== Daily Plan for Chazz's Pets ===
  ○ Feed pet (food) at 10:00 [daily]
  ○ Take pet for a walk (play) at 12:00 [daily]
  ○ Give pet meds (medicine) at 16:00 [daily]
  ```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest -m pytest

# Run with coverage:
pytest --cov
```

These tests cover a variety of cases across the following categories:
- sorting edge cases
- recurring task logic
- conflict detection
- state & validity
- queries on empty/missing data

Sample test output:

```
# Paste your pytest output here
======================================================= test session starts ========================================================
platform win32 -- Python 3.13.14, pytest-9.0.3, pluggy-1.6.0
rootdir: ############ (project root directory)
plugins: anyio-4.13.0
collected 17 items                                                                                                                  

tests\test_pawpal.py .................                                                                                        [100%]

======================================================== 17 passed in 0.12s ========================================================
```

Based on the above test results, the system's reliability is 5 stars.

## 📐 Smarter Scheduling

### Core Features

| Feature | Method(s) | Algorithm |
|---------|-----------|-----------|
| **Sorting by Time** | `get_daily_plan()` | Sorts tasks chronologically using `key=lambda t: t.scheduled_time`. Handles boundary times (midnight, end-of-day) and multiple tasks at same time. |
| **Task Filtering** | `get_tasks_by_completion_status()`, `get_tasks_by_pet_name()`, `get_tasks_by_type()`, `get_pending_tasks()` | Filter tasks by: completion status (done/pending), pet name, task type (food/medicine/play/grooming), or pending-only. |
| **Conflict Detection** | `detect_task_conflicts()`, `get_all_scheduling_conflicts()` | Lightweight warning system: detects exact time matches. Returns `[CONFLICT]` for same-pet overlaps and `[ALERT]` for different-pet overlaps. |
| **Recurring Tasks** | `complete_task()` | Mark task done → auto-creates next occurrence for daily/weekly tasks. One-time tasks don't recur. Maintains task properties (description, type, time, frequency). |
| **Multi-Pet Aggregation** | `get_all_tasks()`, `get_all_pending_tasks()` | Collects and returns tasks from all owner's pets in a single list. |
| **Task Completion Tracking** | `mark_complete()`, `mark_incomplete()` | Toggle task status with boolean flag. Visual indicators: `[X]` (done) vs `[ ]` (pending). |

### Supported Task Types

- **food** — feeding and nutrition
- **medicine** — medications and supplements
- **play** — exercise and enrichment
- **grooming** — bathing, brushing, nails
- Custom types supported

### Supported Frequencies

- **daily** — repeats every day after completion
- **weekly** — repeats every week after completion
- **once** — one-time task, does not recur

## 📸 Demo Walkthrough

Follow these steps to see PawPal+ in action:

1. **Start the app** — Run `streamlit run app.py` from the project directory. You'll see the PawPal+ welcome screen.

2. **Add a pet** — Under "🐕 Your Pets", enter a pet name (e.g., "Chuck") and select a species (dog/cat/rabbit/other). Click **"Add pet"**. The pet appears in the "Current pets:" list.

3. **Add another pet (optional)** — Repeat step 2 with a different pet name (e.g., "Bun") to demonstrate multi-pet scheduling.

4. **Create your first task** — Under "📋 Tasks", select the pet from the dropdown, enter a task description (e.g., "Feed pet"), select a task type (food/medicine/play/grooming), set a time (hour), and choose a frequency (daily/weekly/once). Click **"Add task"**.

5. **Add more tasks** — Repeat step 4 for different times and pets. For example:
   - Task: "Feed pet" → food @ 10:00 daily (for Chuck)
   - Task: "Give meds" → medicine @ 16:00 daily (for Bun)
   - Task: "Morning walk" → play @ 08:00 daily (for Chuck)

6. **View task list** — See all tasks organized by pet under "Current tasks:". Each task shows its completion status (✓ or ○), description, type, time, and frequency.

7. **Generate daily schedule** — Click **"Generate daily schedule"** to see all tasks sorted chronologically by time, regardless of which pet they belong to. Tasks are displayed with times in HH:MM format.

8. **View summary metrics** — At the bottom, see "Pending tasks summary:" with cards showing:
   - Total pending tasks
   - Number of feeding tasks
   - Number of medicine tasks

9. **Mark tasks complete (optional)** — In a more advanced setup, you could mark tasks as complete and watch daily/weekly tasks auto-generate their next occurrence, while one-time tasks stay completed.

**Sample output:**
```
=== Daily Plan for Pet Owner's Pets ===
  ○ Morning walk (play) at 08:00 [daily]
  ○ Feed pet (food) at 10:00 [daily]
  ○ Give meds (medicine) at 16:00 [daily]
```
