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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
