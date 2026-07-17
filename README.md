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
- sortng edge cases
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

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `get_daily_plan()` | Sorts tasks by scheduled time using lambda: `key=lambda t: t.scheduled_time` |
| Filtering behavior | `get_tasks_by_completion_status()`, `get_tasks_by_pet_name()`, `get_tasks_by_type()`, `get_pending_tasks()` | Filter by completion status (completed/pending), pet name, task type (food/medicine/play), or only incomplete tasks |
| Conflict detection logic | `detect_task_conflicts()`, `get_all_scheduling_conflicts()` | Lightweight detection returns warning messages for exact time matches; [CONFLICT] for same-pet overlaps, [ALERT] for different-pet overlaps |
| Recurring task logic| `complete_task()` | Marks task complete and auto-creates next occurrence for daily/weekly tasks; one-time tasks do not recur |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
