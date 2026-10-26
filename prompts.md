# AI Prompt – Operating Systems Task 2: Process Synchronization

Act as an Operating Systems expert and help me understand, document, and present my OS Task 2 project on **Process Synchronization using Semaphores and Monitors**.

## Project Overview

My project demonstrates two classic Operating Systems synchronization problems using two different synchronization techniques.

### 1. Readers–Writers Problem
- Implementation using Semaphores.
- Implementation using Monitors.

### 2. Dining Philosophers Problem
- Implementation using Semaphores.
- Implementation using Monitors and Condition Variables.

## Project Requirements

For each implementation:

1. Explain the synchronization problem in simple language.
2. Explain the algorithm and its working step by step.
3. Identify the critical section, shared resources, and synchronization mechanisms.
4. Explain how race conditions and deadlocks are prevented or handled.
5. Explain the role of semaphores, mutexes, monitors, and condition variables wherever applicable.
6. Provide accurate Python source code with simple explanations.
7. Create an interactive HTML/CSS/JavaScript visualization showing the processes, resource states, and synchronization events.
8. Display the execution events and final results clearly.
9. Verify that the simulation follows the synchronization rules and does not allow invalid resource access.
10. Provide test cases and explain the expected output.

## Validation Requirements

For the Readers–Writers Problem:
- Multiple readers may read simultaneously.
- Writers must have exclusive access to the shared resource.
- Readers and writers must follow the synchronization rules.
- Explain any reader or writer starvation risks.

For the Dining Philosophers Problem:
- Each philosopher needs two forks to eat.
- A fork cannot be used by two philosophers simultaneously.
- Explain how the implementation prevents deadlock.
- Verify that all philosophers can finish their required rounds.
- Confirm that all forks are released at the end.

## Documentation

Prepare a professional README.md containing:
- Project title and objectives.
- Problem statements.
- Technologies used.
- Project structure.
- Algorithms and synchronization techniques.
- Instructions to run the Python programs and HTML visualizations.
- Sample outputs and test results.
- Screenshots section.
- Conclusion and references.

Also prepare a project report with:
1. Introduction
2. Objectives
3. Problem statements
4. Theory and algorithms
5. System design
6. Implementation details
7. Results and discussion
8. Comparison of semaphores and monitors
9. Conclusion
10. References

## Viva Preparation

Generate simple, accurate viva questions and answers covering:
- Process synchronization.
- Critical sections and race conditions.
- Mutexes and semaphores.
- Binary and counting semaphores.
- Monitors and condition variables.
- Deadlock, starvation, and mutual exclusion.
- Readers–Writers and Dining Philosophers problems.
- Differences between semaphore-based and monitor-based solutions.

## Important Instructions

- Keep explanations suitable for an undergraduate engineering Operating Systems laboratory.
- Use simple English and explain technical terms clearly.
- Do not invent execution results; derive them from the actual code.
- Do not change the existing algorithms or project structure unnecessarily.
- If modifying existing code, preserve working functionality and explain every important change.
- Ensure consistency between the Python code, HTML visualizations, event logs, README, report, and screenshots.
- Clearly distinguish verified results from expected results.
- Help me understand the project well enough to explain it confidently during a viva.

Start by reviewing the existing project files, then identify what is already implemented, what needs improvement, and what documentation or testing is still missing.
