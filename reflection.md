# PawPal+ Project Reflection

## 1. System Design
=> Add a pet
=> Feed a pet
=> Schedule a walk 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Initial UML Design — PawPal+

The design uses four classes to separate concerns cleanly:

Pet — a data container for the animal's profile. It holds the pet's name, species, age, and any special needs. Its only responsibility is to store and return pet information.

Task — a data container for a single care activity. It stores the task title, how long it takes (duration), its priority level, and category. It can report whether it's high priority and serialize itself to a dictionary.

Owner — represents the person using the app. It stores the owner's name, how many minutes per day they have available, and any scheduling preferences. It is responsible for exposing the time budget to the rest of the system.

Scheduler — the core logic class. It holds a reference to the Owner and Pet, and manages a list of Tasks. It is responsible for deciding which tasks fit within the owner's time budget, ordering them by priority, and explaining why each task was or wasn't included in the plan.

Relationships: Owner uses Scheduler; Scheduler manages a list of Task objects and references the Pet for context. Owner also owns one Pet.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design changed during the planning and review process.

Change: Added scheduled_plan as a stored attribute on Scheduler

The original design had generate_plan() and explain_plan() as two independent methods. During review, it became clear that explain_plan() had no reliable way to know which tasks were selected unless it recomputed the plan itself — which would be redundant and could produce inconsistent results if the task list changed between calls.

The fix was to add a scheduled_plan: list[Task] attribute to Scheduler. Now generate_plan() stores its result there, and explain_plan() reads from it. This makes the two methods properly coordinated and avoids duplicate computation.

Change: Identified the need to split generate_plan() into helper methods

Originally generate_plan() was designed as a single method responsible for everything — filtering tasks by time budget, sorting by priority, and selecting the final plan. During review it became clear this would create a logic bottleneck: one method doing too much makes it hard to test and debug.

The revised design breaks it into smaller private helpers (_filter_by_time() and _sort_by_priority()), keeping generate_plan() as the coordinator that calls them in sequence. This makes each piece of logic independently testable

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two constraints: **time budget** (the owner's available minutes per day) and **frequency priority** (daily tasks outrank weekly, which outrank monthly). Tasks are first sorted by frequency priority and then by duration (longer tasks first within the same frequency tier), and then trimmed to fit the time budget via a greedy pass.

Time budget was treated as the hard constraint — no task can be included if it would exceed the limit — because missing it would make the plan impossible to execute. Frequency was the soft ranking signal because a daily task (like feeding) is more urgent than a monthly one (like a vet checkup), even if the monthly task takes longer.

**b. Tradeoffs**

The conflict detector only flags tasks that share an **exact** `scheduled_time` string (e.g., both set to `"08:00"`). It does not check whether two tasks *overlap* — for example, a 30-minute task starting at `08:00` and a 20-minute task starting at `08:15` would not be flagged even though they run at the same time.

This tradeoff is reasonable for a starter app because exact-match detection is simple to implement and easy to understand. True overlap detection would require converting `HH:MM` strings to `datetime` objects, computing end times, and checking intervals — significantly more logic for a marginal gain in a demo context where users manually enter clean time values. The tradeoff can be revisited once the core scheduling loop is stable.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used in three distinct roles across the project phases:

1. **Design review** — After drafting the initial UML, AI was used to challenge the design: "Does each class have a single clear responsibility?" This surfaced the `scheduled_plan` attribute issue and the need to split `generate_plan()` into private helpers before any code was written.
2. **Implementation** — AI drafted method bodies (e.g., `sort_by_time`, `detect_conflicts`, the recurring logic in `mark_complete`) based on method signatures and docstrings that were already agreed upon. This kept the AI working within a pre-approved contract rather than designing freely.
3. **Test generation** — AI suggested test cases from method signatures, which were reviewed for coverage gaps (e.g., the untimed-tasks-ignored case for conflict detection was added after reviewing the draft).

The most effective prompts were specific and constrained: "Given this method signature and docstring, implement the body" produced better results than open-ended "build a scheduler" prompts.

**b. Judgment and verification**

When AI drafted `detect_conflicts()`, the initial suggestion used a nested loop (O(n²)) to compare every task pair. That was rejected in favor of the single-pass dictionary approach (`seen: dict[str, str]`) because the O(n) version is easier to read and scales better, even though the dataset is small. The AI suggestion was evaluated by asking: "Is there a simpler data structure that avoids the double loop?" — the answer was a plain dict tracking the first task seen at each time slot. The final version was verified by writing the conflict detection tests, including a case with no conflicts and one with untimed tasks that should be ignored.

---

## 4. Testing and Verification

**a. What you tested**

The test suite covers 15 behaviors across five areas:

| Area | Why it mattered |
|---|---|
| Plan generation (happy path + no tasks) | Core feature — if this breaks, nothing else matters |
| Sort by time (chronological + untimed last) | Ensures the UI display is trustworthy, not misleading |
| Recurring tasks (daily, weekly, monthly, re-queue) | High risk of off-by-one errors with `timedelta`; important to pin the exact date math |
| Conflict detection (flagged, no false positive, untimed ignored) | A false positive would erode owner trust; a missed conflict would cause real scheduling failures |
| Filtering (by status, by pet name) | Powers the "Incomplete only" tab in the UI — wrong results would silently mislead the user |

**b. Confidence**

Confidence: **4 out of 5**. All 15 tests pass and cover both happy paths and meaningful edge cases. The gap is duration-based overlap detection — two tasks at `08:00` and `08:15` where the first runs 30 minutes would overlap, but the current detector misses it. That would require converting `HH:MM` to `datetime`, computing end times, and checking ranges — the next logical test to add.

---

## 5. Reflection

**a. What went well**

The separation between the backend (`pawpal_system.py`) and the UI (`app.py`) worked well. Because the classes had clear, tested interfaces, connecting them to Streamlit was mechanical — each button just called a method and displayed the return value. This made the UI easy to update without touching any scheduling logic, and it meant the logic could be verified in isolation via `pytest` before the UI existed.

**b. What you would improve**

The `Owner` and `Pet` objects are initialized once into `st.session_state` using the default values at page load. If the user changes the owner name or pet name after the first run, those changes are silently ignored because the session-state guard (`if "owner" not in st.session_state`) skips re-initialization. A future iteration would add a "Reset session" button that clears `st.session_state` and rebuilds the objects from the current form values.

**c. Key takeaway**

The most important lesson was that AI is a powerful implementation tool but a poor architect. Every time AI was given an open-ended design question it produced plausible-looking but subtly wrong answers — for example, a `Scheduler` that held a direct reference to a single `Pet` instead of routing through `Owner`, which would have broken multi-pet support. When AI was given a signed contract (method name, parameters, return type, docstring) and asked only to fill in the body, the results were reliable and fast. The human's job is to own the architecture; AI's job is to execute within it.
