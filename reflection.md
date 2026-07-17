# PawPal+ Project Reflection

## 1. System Design

User actions:
- Add a pet
- Schedule food and med times
- See a daily plan

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    The classes that I chose are Owner, Pet, Task, and Scheduler. The Owner can add Pets, perform actions on the Pet, and can add tasks to the Scheduler. The Pet can have meds added to their plan and is connected with one owner. Each Task is associated with an Owner and a Pet. The Scheduler must hold a list of Tasks and is associated with a specific Pet. The Scheduler can have Tasks added to it and can have a daily plan retrieved from it.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    My scheduler considers time as a constraint. I decided that timing matters the most so the scheduler will be able to return a chronological list of tasks to do. Oftentimes, priority is decided by how soon it will happen, so I decided that in a way, time will be able to handle both itself and priority.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    One of the tradeoffs that my Scheduler makes is that it only checks for exact time matches instead of overlapping durations when checking for scheduling conflicts. Pet tasks do not take very long so it makes more sense to check for the start time match as opposed to checking a block of time. An owner would be able to do multiple tasks within the same hour.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    I used AI tools to help with debugging and refactoring. The responses were the most helpful when the prompts were very detailed. This helped pinpoint exactly what the AI should help with. I used different chat sessions to help stay organized about the different steps that I was working on (e.g. brainstorming, debugging, testing).

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    Overall the suggestions were very helpful. One case where I did not take the suggestion as is was adding new actions for the user to be able to do. Some of the suggestions were ones that I alreafy planned, and I did not use other ones that I felt were not as large of priorities.
    I evaluated the AI responses by manually working through and reviewing the code to decide if it fit in with the existing code.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

These tests cover a variety of cases across the following categories:
- sorting edge cases
- recurring task logic
- conflict detection
- state & validity
- queries on empty/missing data
These tests were important because they cover the main functions that are emcompassed inside of the pawpal system.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Based on the above test results, the system's reliability is 5 stars.


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I am satisfied with how the classes connect with each other. The UI works well with the backend, and it is able to complete the features that I originally planned.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    I would add an option for the Owner to be able to add their preferences for certain tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    AI will not always get things right on the first try. It is important to iterate and to provide follow up prompts to be able to refine the suggestions that the AI provides.
