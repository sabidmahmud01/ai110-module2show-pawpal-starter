# PawPal+ (Module 2 Project)

A Streamlit app that helps a busy pet owner build a smart daily care schedule for their pet.

## Features

- **Owner & pet setup** — Enter your name, available time (minutes/day), pet name, and species to personalize the plan.
- **Task management** — Add care tasks with a description, duration, frequency (daily / weekly / monthly), and a start time in `HH:MM` format.
- **Smart scheduling** — The scheduler prioritizes daily tasks first, then fits as many tasks as possible within the owner's time budget.
- **Sort by time** — After generating a plan, tasks are displayed in chronological order by start time using a `lambda` sort key on `HH:MM` strings.
- **Incomplete task filter** — A dedicated tab shows only tasks that haven't been marked complete yet, powered by `Scheduler.filter_tasks()`.
- **Recurring tasks** — Marking a daily or weekly task complete automatically queues a new instance for the next day or next week via Python's `timedelta`.
- **Conflict detection** — If two tasks share the same start time, `Scheduler.detect_conflicts()` surfaces a clear warning message so the owner can adjust — without crashing.

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

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

## Smarter Scheduling

The scheduler includes four algorithmic improvements beyond the basic plan generator:

- **Sort by time** — `Scheduler.sort_by_time()` uses a `lambda` key on the `scheduled_time` field (stored as `"HH:MM"` strings) so tasks are ordered chronologically. Tasks without a start time are appended at the end.
- **Filter tasks** — `Scheduler.filter_tasks(completed, pet_name)` lets callers retrieve only incomplete tasks, only tasks for a specific pet, or any combination of both.
- **Recurring tasks** — `Task.mark_complete()` now returns a new `Task` instance due one day or one week later (via Python's `timedelta`). `Scheduler.mark_task_complete()` calls this and automatically re-queues the next occurrence onto the pet's task list.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans all tasks for duplicate `scheduled_time` values and returns a list of human-readable warning strings instead of crashing.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite contains **15 tests** across `tests/test_pawpal.py` covering:

| Area | Tests |
|---|---|
| Plan generation | Happy path (tasks fit budget), edge case (no tasks) |
| Sorting | Chronological order, untimed tasks sorted last |
| Recurring tasks | Daily → next day, weekly → next week, monthly → no recurrence, re-queue on complete |
| Conflict detection | Duplicate time flagged, no false positives, untimed tasks ignored |
| Filtering | By completion status, by pet name |

**Confidence level: ★★★★☆**
Core scheduling behaviors are fully covered. The one gap is overlap detection (two tasks at different times that still overlap by duration) — exact-match conflict detection is tested but duration-based overlap is not.

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
